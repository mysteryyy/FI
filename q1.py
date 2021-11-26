import pandas as pd
import yfinance as yf
import numpy as np
k = pd.read_csv('stockdata_fi.csv')
for i in k.columns[1:]:
    logcolname = f"ln_ret_{i[10:]}"
    ord_ret = f"%ret_{i[10:]}" # Column anme for percentage returns
    k[logcolname] = np.log(k[i]/k[i].shift(1))
    k[ord_ret] = np.exp(k[logcolname])-1
print(k)
k['portfolio_returns_percentage'] = k[[i for i in k.columns if "%ret" in i]].mean(axis=1)
k['portfolio_log_returns'] = k[[i for i in k.columns if "ln_ret" in i]].mean(axis=1)
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
return_info['portfolio_annual_mean_returns'] = [k.portfolio_log_returns.mean()*250]
return_info['portfolio_std_returns'] = [k.portfolio_log_returns.std()*250**.5]
print(return_info)
