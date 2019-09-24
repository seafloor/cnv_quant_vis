from bokeh.models.widgets import CheckboxGroup, RadioButtonGroup, Div
from bokeh.models.widgets import RadioGroup, Button
from bokeh.layouts import row, column
from bokeh.core.properties import AngleSpec
from bokeh.models import LinearAxis, Grid, Plot
from bokeh.models import Select
from bokeh.transform import factor_cmap
from bokeh.io import curdoc, show
import pandas as pd
import numpy as np
from plotting import get_kde, get_rug, make_plot, make_rug
from plotting import get_data


def update_plot(attr, old, new):
    cnv_name = cnv_select.value
    test_name = test_select.value
    clip_range = range_radio.active
    z_transform = znorm_checkbox.active
    sex_choice = sex_radiobutton.active
    transform_choice = transform_radio.active
    scale_timing = scale_time_radio.active

    df, raw_df, d_min, d_max = get_data(file_name, cnv_name, test_name,
                                        clip_range, z_transform, sex_choice,
                                        transform_choice, scale_timing)

    data.data.update(df.data)
    raw_data.data.update(raw_df.data)
    plot.title.text = test_name
    plot.legend.title = cnv_name


def reset_data():
    df, raw_df, d_min, d_max = get_data(file_name, cnv_name, test_name, 0, [], 2, 0, 1)

    data.data.update(df.data)
    raw_data.data.update(raw_df.data)
    plot.title.text = test_name
    plot.legend.title = cnv_name

    range_radio.active = 0
    znorm_checkbox.active = []
    sex_radiobutton.active = 0
    transform_radio.active = 0
    scale_time_radio.active = 1


file_name = 'data/biobank2.parquet'
cnv_name = 'TAR deletion'
test_name = 'HDL cholesterol'
data, raw_data, x_min, x_max = get_data(file_name, cnv_name, test_name, 0, [],
                                        0, 0, 1)
plot = make_plot(cnv_name, test_name, data, x_min, x_max)
rug = make_rug(raw_data, cnv_name, test_name)
rug.x_range = plot.x_range

####################### Subsetting #######################
test_select = Select(
    options=['Birthweight', 'Weight', 'Height', 'BMI',
             'Hand grip strength left', 'Hand grip strength right',
             'Waist circumference', 'Hip circumference', 'waist to hip ratio',
             'Leg fat percentage right', 'Leg fat percentage left',
             'Arm fat percentage right', 'Trunk fat percentage',
             'Pulse rate mean', 'BP systolic', 'BP diastolic',
             'Peak expiratory flow', 'Acceleration average',
             'Heel bone mineral density', 'Ventricular rate', 'QT interval',
             'QTc', 'ALT', 'Albumin', 'ALP', 'APOA1', 'APOB', 'AST', 'CRP',
             'Calcium', 'Cholesterol', 'Creatinine', 'CysC', 'Bilirubin direct',
             'GGT', 'Glucose', 'HbA1c', 'HDL cholesterol', 'IGF 1',
             'LDL cholesterol', 'LipoA', 'Phosphate', 'SHBG', 'Testosterone',
             'Bilirubin total', 'Protein total', 'Triglycerides', 'Uric acid',
             'Urea', 'Vitamin D', 'WBC', 'RBC', 'Haemoglobin', 'Haematocrit',
             'MCV', 'MCH', 'MCHC', 'Platelets', 'Lymphocyte', 'Monocyte', 'Neutrophill',
             'Eosinophill', 'Basophill', 'NRBC', 'Lymphocyte percent',
             'Monocyte percent', 'Neutrophill percent', 'Eusinophill percent',
             'Basophill percent', 'NRBC percent', 'Reticulocyte percent',
             'Reticulocte', 'MRV'],
    value='HDL cholesterol',
    title='Biochemical Test'
)

test_select.on_change('value', update_plot)

cnv_select = Select(
    options=['TAR deletion', 'TAR duplication', '1q21.1 deletion', '1q21.1 duplication',
             'NRXN1 deletion', '2q11.2 deletion', '2q11.2 duplication', '2q13 deletion',
             '2q13 duplication', '2q13 deletion (NPHP1)', '2q13 duplication (NPHP1)',
             '2q21.1 deletion', '2q21.1 duplication', '3q29 deletion', '3q29 duplication',
             'WBS duplication', '7q11.23 duplication (distal)', '8p23.1 duplication',
             '10q11.21q11.23 deletion', '10q11.21q11.23 duplication', '10q23 duplication',
             '13q12.12 deletion', '13q12.12 duplication', '13q12 deletion (CRYL1)',
             '13q12 duplication (CRYL1)', '15q11.2 deletion', '15q11.2 duplication',
             'PWS duplication', '15q11q13 deletion (BP3-BP4)', '15q11q13 duplication (BP3-BP4)',
             '15q11q13 duplication (BP3-BP5)', '15q13.3 deletion', '15q13.3 duplication',
             '15q13.3 deletion (CHRNA7)', '15q13.3 duplication (CHRNA7)', '15q24 duplication',
             '16p11.2 deletion', '16p11.2 duplication', '16p11.2 distal deletion',
             '16p11.2 distal duplication', '16p12.1 deletion', '16p12.1 duplication',
             '16p13.11 deletion', '16p13.11 duplication', '17p12 deletion (HNPP)',
             '17p12 duplication (CMT1A)', 'Potocki-Lupski', '17q11.2 deletion (NF1)',
             '17q12 deletion', '17q12 duplication', '22q11.2 deletion', '22q11.2 duplication',
             '22q11.2 distal deletion', '22q11.2 distal duplication'],
    value='TAR deletion',
    title='CNV'
)

cnv_select.on_change('value', update_plot)

sex_radiobutton = RadioButtonGroup(labels=['Both', 'Male', 'Female'], active=0)
sex_radiobutton.on_change('active', update_plot)

####################### Rescaling ####################### 
range_radio = RadioGroup(labels=["None",
                                 "Remove values +/- 5 s.d. from the mean",
                                 "Remove values with med/mad*"], active=0)
range_radio.on_change('active', update_plot)

znorm_checkbox = CheckboxGroup(labels=["Standardise"], active=[])
znorm_checkbox.on_change('active', update_plot)
scale_time_radio = RadioButtonGroup(labels=['Before', 'After', 'Both'],
                                    active=1)
scale_time_radio.on_change('active', update_plot)

####################### Transforms ####################### 
transform_radio = RadioGroup(labels=['None', 'Log (ln)**',
                                     'Square root***', 'Yeo-Johnson'],
                             active=0)
transform_radio.on_change('active', update_plot)

reset_button = Button(label='Reset Clean / Scale / Transform',
                      button_type='success')
reset_button.on_click(reset_data)

########################## Text ##########################
# Section titles, dividers, button subtitles
# Possible overall header
labname = Div(text="<b>CARDIFF UNIVERSITY</b>", width=800, height=20,
              style={'color': '#6a6a6a'})
header = Div(text="""
             <b>Visualiser for the Effects of CNVs on Quantitative Traits</b>
             """, width=800, height=30,
             style={'color': '#373737', 'font-size': '200%'})
authors = Div(text="""
              <i>Authors List</i>
              """, width=700, height=5, style={'color': '#373737',
                                                 'font-size': '90%'})
subheader = Div(text="""
                <p>
                This page gives interactive Seaborn-style KDE plots for the
                effects of pathogenic CNVs on quantitative traits in UK
                Biobank. The results have been collated from two papers: one preprint from
                <a href="https://www.biorxiv.org/content/10.1101/723270v1">
                Bracher-Smith et al.</a>
                on biochemical markers, and another by
                <a href="https://bmcgenomics.biomedcentral.com/articles/10.1186/s12864-018-5292-7">
                Owen et al.</a> on anthropometric traits.
                </p>
                """,
                width=700, height=80, style={'color': '#373737'})
sex_header = Div(text="Sex", width=100, height=10)
outlier_header = Div(text="Outlier removal", width=250, height=10)
scale_radio_header = Div(text="Clean/scale before or after transformation?",
                         width=300, height=10)
section_subset = Div(text="<b>Subset Selection</b><hr>", width=150, height=40,
                     style={'color': '#373737', 'font-size': '110%'})
section_rescale = Div(text="<b>Cleaning and Rescaling</b><hr>", width=250,
                      height=40,
                      style={'color': '#373737', 'font-size': '110%'})
section_transform = Div(text="<b>Transformations</b><hr>", width=100, height=40,
                        style={'color': '#373737', 'font-size': '110%'})
log_note = Div(text="""
               *med/mad is a robust outlier identification rule, outlined
               <a href="https://stats.stackexchange.com/a/121075">here</a>. In
               practice it's slightly more stringent than using the 5 s.d.
               option<br>
               **a ln(n + x) transform is used if any(x <= 0), where
               n is abs(min(x))+1<br>
               ***the square-root is also taken as sqrt(n + x) where n is
               abs(min(x)) when any(x < 0), zeroing-out negatives""",
               width=700, height=10, style={'color': '#373737', 'font-size':
                                            '80%'})


########################## Show ##########################
plots = column(plot, rug, log_note)
controls = column(section_subset, test_select, cnv_select, sex_header,
                  sex_radiobutton, section_rescale, znorm_checkbox,
                  outlier_header, range_radio, scale_radio_header,
                  scale_time_radio, section_transform, transform_radio,
                  reset_button)
page = column(labname, header, subheader, row(plots, controls))
curdoc().add_root(page)
