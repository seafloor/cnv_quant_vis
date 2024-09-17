from statsmodels.nonparametric.kde import KDEUnivariate
from bokeh.models import LegendItem, ColumnDataSource, Legend, Range1d
from bokeh.plotting import figure
from bokeh.models.glyphs import VArea
from transforms import rescale_data, transform_variable

import numpy as np
import pandas as pd


def get_kde(cnv_name, test_name, data, n_points=1000):
    dist1 = data.loc[data[cnv_name]==0, test_name].dropna().values
    dist2 = data.loc[data[cnv_name]==1, test_name].dropna().values

    d_min = np.min(np.hstack((dist1, dist2)))
    d_max = np.max(np.hstack((dist1, dist2)))
    kde1 = KDEUnivariate(dist1)
    kde1.fit(kernel='gau', bw='scott', fft=True, gridsize=100, cut=3)
    kde2 = KDEUnivariate(dist2)
    kde2.fit(kernel='gau', bw='scott', fft=True, gridsize=100, cut=3)

    x1, y1 = kde1.support, kde1.density
    x2, y2 = kde2.support, kde2.density
    y01 = np.zeros(y1.shape[0])
    y02 = np.zeros(y2.shape[0])

    # Make sure the densities are nonnegative
    y1 = np.amax(np.c_[np.zeros_like(y1), y1], axis=1)
    y2 = np.amax(np.c_[np.zeros_like(y2), y2], axis=1)
    
    return y01, y02, x1, y1, x2, y2, d_min, d_max


def get_rug(cnv, test, data):
    dist = data.loc[:, [cnv, test]].dropna()
    unique_0 = np.unique(dist[dist[cnv]==0][test].values)
    unique_1 = np.unique(dist[dist[cnv]==1][test].values)
    unique_dist = pd.DataFrame({
        'cnv': np.hstack((np.repeat(0, unique_0.shape[0]),
                        np.repeat(1, unique_1.shape[0]))),
        'test': np.hstack((unique_0, unique_1)),
        'col': np.hstack((np.repeat('LightCoral', unique_0.shape[0]),
                          np.repeat('LightBlue', unique_1.shape[0])))})
    
    return unique_dist


def make_plot(cnv_name, test_name, data, d_min, d_max):
    plot = figure(
        title=test_name, width=700, height=500,
        min_border=0)

    glyph1 = VArea(x="x1", y1="y01", y2="y1", fill_color="LightCoral",
                   fill_alpha=0.6)
    glyph2 = VArea(x="x2", y1="y02", y2="y2", fill_color="LightBlue",
                   fill_alpha=0.6)
    plot.add_glyph(data, glyph1)
    plot.add_glyph(data, glyph2)

    li1 = LegendItem(label='0 (Absent)', renderers=[plot.renderers[0]])
    li2 = LegendItem(label='1 (Present)', renderers=[plot.renderers[1]])
    legend1 = Legend(items=[li1, li2], location='top_right')
    plot.add_layout(legend1)
    plot.legend.title = cnv_name

    return plot


def make_rug(raw_data, cnv, test):
    rug = figure(width=700, height=110,
                 min_border=0)
    rug.toolbar_location = None
    rug.yaxis[0].ticker.desired_num_ticks = 2
    rug.y_range = Range1d(-0.5, 1.5)
    rug.dash('test', 'cnv', size=15, angle=90, angle_units='deg',
             source=raw_data, fill_alpha=0.35, color='col')
    rug.yaxis.major_label_overrides = {0: 'Absent', 1: 'Present'}

    return rug


def get_data(file_name, cnv, test, clip_range, z_transform, sex_choice,
             transform_choice, scale_timing):
     data = pd.read_parquet(file_name, columns=[cnv, 'Sex', test]).dropna()
     if scale_timing in [0, 2]:
         data = rescale_data(data, clip_range, test, z_transform)
     if sex_choice != 0:
         data = data.loc[data.Sex == sex_choice, :]
     if transform_choice != 0:
         data.loc[:, test] = transform_variable(data.loc[:, test].values, transform_choice)
     if scale_timing in [1, 2]:
         data = rescale_data(data, clip_range, test, z_transform)

     y01, y02, x1, y1, x2, y2, d_min, d_max = get_kde(cnv, test, data)
     kdedata = ColumnDataSource(dict(x1=x1, x2=x2, y01=y01, y02=y02, y1=y1, y2=y2))
     rawdata = ColumnDataSource(get_rug(cnv, test, data))

     return kdedata, rawdata, d_min, d_max
