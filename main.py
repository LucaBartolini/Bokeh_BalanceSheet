from os.path import dirname, join

import numpy as np
from bokeh.io import curdoc, output_file, show
from bokeh.layouts import column, layout, row, widgetbox
from bokeh.models import (CategoricalColorMapper, ColumnDataSource, CustomJS,
                          Div, Select, Slider, Span, TextInput)
from bokeh.models.tools import HoverTool
from bokeh.models.widgets import Slider
from bokeh.palettes import Spectral6
from bokeh.plotting import figure

import dataframe_gen

#Source Data
df = dataframe_gen.gen_df()
source = ColumnDataSource(df)

# Create plots and widgets
p = figure(plot_height=600, 
            plot_width=700, 
            title="Cumulative Free Cash Flow", 
            tools="crosshair,pan,reset,save,wheel_zoom",
            sizing_mode="scale_both",
            x_axis_type = 'datetime',
            
            )
p.vbar( x="year", 
        top="cum_fcf", 
        source=source, 
        width=0.9, 
        line_color= None,
        fill_color = "cum_fcf_color")

p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
p.xaxis.major_tick_line_color = None  # turn off x-axis major ticks


# Create Input controls
# cogs_mat cogs_lab sga_rate sga_fixed ppt equipm interest_rate loan_size WC sales_evo
cogs_mat = Slider(title="CoGS - material (% Rev.)", value=35, start=10, end=50, step=0.25)
cogs_lab = Slider(title="CoGS - labor (% Rev.)", value=35, start=10, end=50, step=0.25)
sga_rate = Slider(title="SG&A costs (% Rev.)", value=15, start=5, end=30, step=0.25)
sga_fixed = Slider(title="Fixed SG&A costs (k€)", value=8, start=0, end=25, step=0.5)
ppu = Slider(title="Price per Unit (k€)", value=35, start=15, end=55, step=1)
interest = Slider(title="Interest rate (yearly %)", value=8, start=0, end=15, step=0.5)
loan = Slider(title="Loan Amount (k€)", value=35, start=10, end=50, step=5)
WC = Slider(title="Working Capital (% Rev.)", value=5, start=0, end=10, step=0.25)

general, our, cap, forecast = dataframe_gen.get_dicts()

def update():
    general['cogs_mat'] = cogs_mat.value/100
    general['cogs_labor'] = cogs_lab.value/100
    general['sga_rate'] = sga_rate.value/100
    general['sga_fixed'] = sga_fixed.value
    our['ppu'] = ppu.value
    cap['interest_rate'] = interest.value/100
    our['st_loan'] = loan.value
    cap['WC'] = WC.value/100

    source.data.update(
        ColumnDataSource(
            dataframe_gen.gen_df(general=general, our=our, cap=cap, forecast=forecast)).data)


controls = [cogs_mat, cogs_lab, sga_rate, sga_fixed, ppu, interest, loan, WC]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

inputs = column(*controls, width=420, height=800)
inputs.sizing_mode = "fixed"
# l = layout([
#     # [desc],
#     [inputs, p],
# ], 
# sizing_mode="scale_both"
# )

l = row(inputs, p)

update()  # initial load of the data

curdoc().add_root(l)
curdoc().title = "Free Cash Flow"
