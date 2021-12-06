import pandas as pd
import os
import statsmodels.api as sm
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
k = yf.download('SPY DBE JPM MA NFLX WMT',start='2016-12-31',end='2021-09-30')
k=k[[i for i in k.columns if 'Adj Close' in i]]
k=k.set_axis(k.columns.map('_'.join), axis=1, inplace=False)

for i in k.columns:
    logcolname = f"ln_ret_{i[10:]}"
    ord_ret = f"%ret_{i[10:]}" # Column anme for percentage returns
    k[logcolname] = np.log(k[i]/k[i].shift(1))
    k[ord_ret] = np.exp(k[logcolname])-1
print(k)
per_ret=[i for i in k.columns if "%ret" in i and 'SPY' not in i]
log_ret=[i for i in k.columns if "ln_ret" in i and 'SPY' not in i]
k['portfolio_returns_percentage'] = k[per_ret].mean(axis=1)
k['portfolio_log_returns'] = k[log_ret].mean(axis=1)
plt.scatter(k.portfolio_returns_percentage,k['%ret_SPY'])
plt.xlabel("SPY % Returns")
plt.ylabel("Portfolio % Returns")
os.system("rm ScatterPLot.jpg")
plt.savefig("ScatterPlot.jpg")
cov_mat_cols =[i for i in k.columns if 'ln_ret' in i or 'log_returns' in i]#Extracting Columns for covariance matrix
cov_mat = k[cov_mat_cols].cov() # covariance matrix of markets and portfolio
info = pd.DataFrame()
for i in cov_mat.columns[:-2]:
    
    info[f"{i[7:]}_beta"]=[cov_mat.loc['ln_ret_SPY',i]/cov_mat.loc['ln_ret_SPY','ln_ret_SPY']]
# Computing beta for portfolio returns
info[f"portfolio_returns_beta"]=[
        cov_mat.loc['ln_ret_SPY','portfolio_log_returns']/cov_mat.loc['ln_ret_SPY','ln_ret_SPY']] 
print(info)
return_info = pd.DataFrame()
return_info1 = pd.DataFrame() # For calculating Mean of all series
for i in cov_mat_cols:
    return_info1[f"{i}_mean"] = [k[i].mean()]

return_info['portfolio_annual_mean_returns'] = [k.portfolio_log_returns.mean()*250]
return_info['portfolio_std_returns'] = [k.portfolio_log_returns.std()*250**.5]
per_ret1 = per_ret + ['portfolio_returns_percentage']
latexdict = dict()

for i in per_ret1:
    y = k[i].dropna()
    x = k['%ret_SPY'].dropna()
    x = sm.add_constant(x) #Add constant for intercept
    model = sm.OLS(y,x)
    res = model.fit()
    print(res.summary())
    lat = pd.read_html(res.summary().tables[1].as_html())[0].to_latex(caption=f"{i[5:]} Beta details")
    latexdict[i] = lat

print(return_info)
