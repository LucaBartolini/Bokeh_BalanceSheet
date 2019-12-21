import pandas as pd
import numpy as np

# General
general = dict(
    wage = {
        'mgmt'   : 70,
        'rd' : 50,
        'sales'  : 40,
        'finance' : 50,
        'production' : 35,
        'office' : 35,
    },
    cogs_mat = 0.3, #as fraction of sales 
    cogs_labor = 0.35,
    sga_rate = 0.25, # Sales, General, Administrative Costs
    sga_fixed = 7,
)

# Regarding OUR COMPANY
our = dict(
    ppu = 35, # Product Price Tag, in k€
    equipment = 70, # equipment at beginning
    st_loan = 100, # 100k in short term loan, at 8% interest rate
 
)

# CAPITAL COSTS
cap = dict(
    interest_rate = 0.08,
    tax_rate = 0.25,
    depr = 0.2, # rate of yearly depreciation: 20%
    WC = 0.05, # assumption that account payable and receivable even out, and inventory is 5% of rev
    # account_payable = 
    # account receivable = 
)


# Forecasts
N_years = 5
forecast = dict(
    sales = [2, 4, 7, 13, 20],
    cap_exp = [0, 0, 0, 0, 0],
    hr = {
        'mgmt'   :      [0.5, 1,   1, 1, 1],
        'rd' :          [1.5, 1.5, 1, 1, 1],
        'sales' :       [0.5, 1,   2, 2, 4],
        'finance' :     [0,   0,   0, 0, 0.5],
        'production' :  [1,   2, 2.5, 3, 5],
        'office' :      [0,   0,   0, 0, 0.5],
    },
)

def get_dicts():
    return general, our, cap, forecast

## GENERATION
def gen_df(general = general, our = our, cap = cap, forecast = forecast, start = 2020):
    fcf = pd.DataFrame()
    fcf['year'] = [int(start+x) for x in range(N_years)]
    fcf['revenue'] = [pcs*our['ppu']*1.0 for pcs in forecast['sales']]
    fcf['cogs_mat'] = fcf.revenue * general['cogs_mat']
    fcf['cogs_labor'] = fcf.revenue * general['cogs_labor']
    fcf['cogs'] = fcf.cogs_mat + fcf.cogs_labor
    fcf['gp'] = fcf.revenue - fcf.cogs # gross profit 
    fcf['sga'] = fcf.revenue * general['sga_rate'] + general['sga_fixed'] # we assumed SG&A costs are a fixed pc of sales
    fcf['equipment'] = [our['equipment']*((1-cap['depr'])**x) for x in range(N_years)]
    fcf['depr'] = fcf.equipment*cap['depr']
    fcf['EBIT'] = fcf.gp - fcf.sga - fcf.depr #earnings b4 interest%taxes
    fcf['interest'] = our['st_loan']*cap['interest_rate']
    fcf['EBT'] = fcf.EBIT - fcf.interest
    fcf['taxes'] = [ebt*cap['tax_rate'] if ebt>0 else 0 for ebt in fcf.EBT] # taxe
    fcf['NOPAT'] = fcf.EBIT - fcf.taxes # not sure that this is correct. Are taxes calc'd on the EBIT or on the EBT?
    ## QUESTION: If EBIT>0 but there are high interests, so that EBT<0, are taxes 0 or not??\
    fcf['gross_cf'] = fcf.NOPAT + fcf.depr
    fcf['delta_wc'] = fcf.revenue * cap['WC'] # working capital
    fcf['cap_exp'] = forecast['cap_exp'] # capital expenditures 
    fcf['fcf'] = fcf.gross_cf - fcf.delta_wc - fcf.cap_exp
    fcf['cum_fcf'] = [sum(fcf.fcf[:i+1]) for i in range(N_years)]
    
    fcf['cum_fcf_color'] = ["forestgreen" if el>0 else "firebrick" for el in fcf.cum_fcf]
    
    #formatting
    fcf.round(3)
    fcf.year.astype(int)

    return fcf

if __name__ == '__main__':
    print('Can compile')