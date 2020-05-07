# -*- coding: utf-8 -*-
"""
Created on Sat May  2 14:30:48 2020

@author: yushi
"""

# %reset -f # clears variable space
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from line_profiler import LineProfiler

# example testing from notes
S_T = np.array([[100,	92.8,	108.8,	121.1],
                [100,   100.1,	 94.2,	92.1],
                [100	,  98.87,	93.11,	97.8],
                [100, 96.34, 93.11, 90.36],
                [100, 102.1, 100.1, 96.43],
                [100, 98.3, 110.2, 99.2],
                [100, 102.9, 120.1, 128.4],
                [100, 110.2, 98.2, 94.5],
                [100, 89.87, 93.8, 90],
                [100, 86.12, 90.21, 98.34]])
dt = 1
T = 3
n = 10
k = 3
S_0 = 100
K = 97.5
r = 0.05
sigma = 0.35

 
def hermite(X,Y,k):
    # L_i(x)
    def Lfun(X, k):
        if k == 1: return(np.array([1 if x > 0 else 0 for x in X]))
        elif k == 2: return(2*X)
        elif k == 3: return(4*X**2 - 2)
        elif k == 4: return(8*X**3 - 12*X)
    
    A = np.zeros(k*k).reshape(k,k)
    b = np.zeros(k)
  
    for i in range(k):
        for j in range(k):
            A[i,j] = sum(Lfun(X, i+1) * Lfun(X, j+1))
        b[i] = Y @ Lfun(X, i+1)

    #A = np.maximum( A, A.transpose() )
    chol_A = np.linalg.cholesky(A)
    A_inv = np.dot(np.transpose(np.linalg.inv(chol_A)), np.linalg.inv(chol_A))
    a = np.dot(A_inv, b)
    
    if k == 2: return(a[0] + a[1] *2*X)
    elif k == 3: return(a[0] + a[1] *2*X + a[2]*(4* np.square(X) -2))
    elif k == 4: return(a[0] + a[1] *2*X + a[2]*(4* np.square(X) -2) +
                        a[3]* (8*X**3 -12*X))
    

def laguerre(X,Y,k):
    # L_i(x)
    def Lfun(X_filtered, k):
        if k == 1: return(np.exp(-X_filtered/2))
        elif k == 2: return(np.exp(-X_filtered/2)*(1-X_filtered))
        elif k == 3: return(np.exp(-X_filtered/2)*(1-2*X_filtered + X_filtered**2/2))
        elif k == 4: return(np.exp(-X_filtered/2)*(1-3*X_filtered + 3*X_filtered**2/2 - X_filtered**3/6))
    
    indicatorFN = np.array([1 if x > 0 else 0 for x in X])
    #result_X = np.copy(X)
    #result_Y = np.copy(Y)
    indicators = np.argwhere(X>0)
    
    X_filtered = X[indicators]
    Y_filtered = Y[indicators]
    
    A = np.zeros(k*k).reshape(k,k)
    b = np.zeros(k)
    
    Lfun_all = [0]
    for i in range(1,k+1):
        Lfun_all.append(Lfun(X_filtered,i))
        
    for i in range(k):
        for j in range(k):
            A[i,j] = sum(Lfun_all[i+1] * Lfun_all[j+1])
        b[i] = sum(Y_filtered * Lfun(X_filtered, i+1))
    
    chol_A = np.linalg.cholesky(A)
    A_inv = np.dot(np.transpose(np.linalg.inv(chol_A)), np.linalg.inv(chol_A))
    # A_inv = np.linalg.inv(A)
    a = np.dot(A_inv, b)
    
    if k == 2: return((a[0] + a[1] *np.exp(-X/2)*(1-X)))
    elif k == 3: return(a[0] + a[1] *np.exp(-X/2)*(1-X) + a[2]*np.exp(-X/2)*(1-2*X + X**2/2))
    elif k == 4: return(a[0] + a[1] *np.exp(-X/2)*(1-X) + a[2]*np.exp(-X/2)*(1-2*X + X**2/2) +
                        a[3]* np.exp(-X/2)*(1-3*X + 3*X**2/2 - X**3/6))
    
    
    # if k == 2: return((a[0] + a[1] *np.exp(-X/2)*(1-X)) * indicatorFN)
    # elif k == 3: return(a[0] + a[1] *np.exp(-X/2)*(1-X) + a[2]*np.exp(-X/2)*(1-2*X + X**2/2) * indicatorFN)
    # elif k == 4: return(a[0] + a[1] *np.exp(-X/2)*(1-X) + a[2]*np.exp(-X/2)*(1-2*X + X**2/2) +
    #                     a[3]* np.exp(-X/2)*(1-3*X + 3*X**2/2 - X**3/6) * indicatorFN)


def monomial(X,Y,k):
    # L_i(x)
    def Lfun(X, k):
        if k == 1: return(np.array([1 if x > 0 else 0 for x in X]))
        elif k == 2: return(X)
        elif k == 3: return(X**2)
        elif k == 4: return(X**3)
    
    A = np.zeros(k*k).reshape(k,k)
    b = np.zeros(k)
  
    Lfun_all = [0]
    for i in range(1,k+1):
        Lfun_all.append(Lfun(X,i))
        
    for i in range(k):
        for j in range(k):
            A[i,j] = Lfun_all[i+1] @ Lfun_all[j+1]
        b[i] = Y @ Lfun(X, i+1)
    
    #A = np.maximum( A, A.transpose() )
    chol_A = np.linalg.cholesky(A)
    A_inv = np.dot(np.transpose(np.linalg.inv(chol_A)), np.linalg.inv(chol_A))
    #A_inv = np.linalg.inv(A)
    a = np.dot(A_inv, b)
    
    if k == 2: return(a[0] + a[1] *X)
    elif k == 3: return(a[0] + a[1] *X + a[2]*X**2)
    elif k == 4: return(a[0] + a[1] *X + a[2]*X**2 + a[3]* X**3)


def stock_price(n, T, S_0 = 40, sigma = 0.20, r = 0.06):
    dt = T/np.sqrt(n)
    column = int(T/dt+1)
    S_T = np.zeros(n*column).reshape(n,column)
    Z = np.random.normal(size = int(n/2 * column)).reshape(int(n/2), column) 
    Z = np.insert(Z,0,np.repeat(0,int(n/2)), axis = 1)
    Z = np.concatenate([Z,-Z]) # antithetic variance reduction

    S_T[:,0] = S_0
    #start = datetime.now()
    for j in range(1,column):           
        S_T[:,j] = S_T[:,(j-1)] + S_T[:,(j-1)] * r *dt + S_T[:,(j-1)]*np.sqrt(dt)*sigma*Z[:,j]
    #end = datetime.now()
    #end - start
    return(S_T)


def LSMC(k, method, S_T, S_0 = 40, K = 40, r = 0.06, T = 3, n = 1000, sigma = 0.20):
    dt = T/np.sqrt(n)
    # generating stock prices
    column = int(T/dt+1)
    exercise = np.zeros(n*column).reshape(n,column)
    itm = np.copy(exercise)
    exercise_value = np.copy(exercise)
    exercise_value_PV = np.copy(exercise)
    
    payoff = np.maximum(K - S_T, 0)
    exercise[:,-1] = [1 if x > 0 else 0 for x in payoff[:,-1]] # assign to final payoff
    # np.where(payoff > 0, 1 , 0) # indicator
    itm = np.asarray(S_T < K, dtype = int) # in the money or not
    
    exercise_value[:,-1] = np.maximum(K - S_T[:,-1], 0)
    #EV_test = np.copy(exercise)
    #EV_test[:,-1] = np.maximum(K - S_T[:,-1], 0)
    for j in range(column-2,0,-1): # iterate through time (columns) 
        tempX = itm[:,j] * S_T[:,j]
        indicatorX = np.argwhere(tempX>0)
        
        # bringing exercise value to time t
        option_time_t = exercise_value[indicatorX,range(j+1,column)]
        opt_pv_value = np.copy(option_time_t)
        for d in range(option_time_t.shape[1]):
            opt_pv_value[:,d] = np.exp(-r*d*dt) * option_time_t[:,d]
        Y = np.sum(opt_pv_value, axis = 1) # summing along the row
        Y = Y.reshape(len(Y),1)
        X = tempX[indicatorX]
      
        
        # Y = itm[:,j] * np.exp(-r*dt)*exercise_value[:,(j+1)]
   
        # ECV = laguerre(X,Y,k) * itm[:,j]
        ECV = method(X,Y,k) * itm[:,j]
        
        for i in range(n):
            if payoff[i,j] > ECV[i]: 
                exercise[i,j] = 1
                exercise[i,(j+1):int(column/dt)] = 0
                exercise_value[i,j] = payoff[i,j]
                exercise_value[i,(j+1):int(column/dt)] = 0
                #EV_test[i,j] = np.exp(-r*dt)*payoff[i,j]
                #EV_test[i,(j+1):int(column/dt)] = 0
                #EV_test method is WRONG!!!
                
        
        # 1 if payoff[:,j] > ECV else 
# =============================================================================
#         for i in range(n):
#             if EV[i] > ECV[i]: 
#                 exercise[i,j] = 1
#                 exercise[i,(j+1):int(column/dt)] = 0
# =============================================================================

    for z in range(payoff.shape[1]):
        exercise_value_PV[:,z] = np.exp(-r*z*dt) * exercise_value[:,z]
    # EV_test is equivalent to exercise_value_PV
    american_put = np.sum(exercise_value_PV)/n
    return american_put


hermite_method = pd.DataFrame(np.zeros((3,3)), columns = ["k=2","k=3","k=4"])
laguerre_method = pd.DataFrame(np.zeros((3,3)), columns = ["k=2","k=3","k=4"])
monomial_method = pd.DataFrame(np.zeros((3,3)), columns = ["k=2","k=3","k=4"])
time_periods = [0.5, 1, 2]
k = [2, 3, 4]
iterations = 

start = datetime.now()
stocksim = []
for i in range(3):
    stocksim.append(stock_price(n = iterations, T = time_periods[i], S_0 = 40, sigma = 0.20, r = 0.06))
datetime.now() - start

start = datetime.now()
for i in range(3):
    for j in range(3):
        laguerre_method.iloc[i,j] = LSMC(S_T = stocksim[i], T=time_periods[i], k=k[j], n=iterations, method = laguerre)
        monomial_method.iloc[i,j] = LSMC(S_T = stocksim[i], T=time_periods[i], k=k[j], n=iterations, method = monomial)
        hermite_method.iloc[i,j] = LSMC(S_T = stocksim[i], T=time_periods[i], k=k[j], n=iterations, method = hermite)
datetime.now() - start


it = 500
S_Test = stock_price(n = it, T = 1, S_0 = 40, sigma = 0.20, r = 0.06)
test = LSMC(S_T = S_Test, T=1, k=3, n=it, method = laguerre)
test 

# profiling performance
# lp = LineProfiler()
# lp_wrapper = lp(LSMC)
# lp_wrapper(S_T = stocksim[0], T=time_periods[0], k=3, n=iterations, method = monomial)
# lp.print_stats()

# lp = LineProfiler()
# lp_wrapper = lp(laguerre)
# lp_wrapper(X = X, Y = Y, k = 3)
# lp.print_stats()

