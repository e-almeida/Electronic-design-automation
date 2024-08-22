# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 15:28:35 2022

@author: Utilizador
"""
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pandas as pd
run=['1.5Leff','3Leff']
for i in run:
#______________transfer curve: data extraction and plotting____________________
    transf=pd.read_csv('P1_transfer_charac_'+ i +'.txt',sep='\t')
    Vgs=np.array(transf['v2'])
    Id=np.array(transf['Id(M1)'])
    
    plt.figure()
    plt.plot(Vgs,Id*1e6,'.',label='LTspice Simulation')
    plt.legend()
    plt.grid()
    plt.xlabel('$V_{GS}$[V]')
    plt.ylabel('$I_{D}$[$\mu \alpha$A]')
#_____________________________Schokley Model___________________________________
    def quad_func(Vgs,k,vt):
        return np.piecewise(Vgs,[Vgs<vt,Vgs>=vt],[0,lambda Vgs:k*(Vgs-vt)**2])
    
    #variáveis modelo Schokley
    var_quad,er_quad=curve_fit(quad_func,Vgs,Id,[1e-4,0.3])
    k_quad=var_quad[0]
    vt_quad=var_quad[1]
    
    print('Quadratic Model',i,': k=',k_quad)
    print('Quadratic Model',i,': vt=',vt_quad)
    
    #gráfico do modelo de Schokley
    Id_Schokley=quad_func(Vgs,k_quad,vt_quad)
    plt.plot(Vgs,Id_Schokley*1e6,label='Schokley Model')
    plt.legend()
    plt.title('Shockley model: Transfer Characteristic (L='+i+')')
#______________________________N Power Mode____________________________________
    def n_func(Vgs,k_n,vt_n,n):
        return np.piecewise(Vgs,[Vgs<vt_n,Vgs>=vt_n],[0,lambda Vgs:k_n*(Vgs-vt_n)**n])
    
    #variáveis modelo n power
    var_n,er_n=curve_fit(n_func,Vgs,Id,[1e-4,0.3,2])
    k_n=var_n[0]
    vt_n=var_n[1]
    n=var_n[2]

    print('N Power Model',i,': k=',k_n)
    print('N Power Model',i,': vt=',vt_n)
    print('N Power Model',i,': n=',n)

    #gráfico modelo n power 
    Id_n=n_func(Vgs,k_n,vt_n,n)
    plt.figure()
    plt.plot(Vgs,Id*1e6,'.',label='LTspice Simulation')
    plt.plot(Vgs,Id_n*1e6,label='N Power Model')
    plt.legend()
    plt.title('N Power model: Transfer Characteristic (L='+i+')')
    plt.xlabel('$V_{GS}$[V]')
    plt.ylabel('$I_{D}$[$\mu \alpha$A]')
    plt.grid()
#_____________________________Relative error___________________________________ 
    #cálculo dos erros relativos para ambos os modelos
    erro_Schokley=((abs(Id-Id_Schokley))/Id)*100
    erro_n=((abs(Id-Id_n))/Id)*100
    
    #gráfico dos erros relativos do modelo de Schokley
    plt.figure()
    plt.plot(Vgs,erro_Schokley,'.')
    #plt.ylim(-2,10)
    #plt.xlim(0.4,1)
    plt.xlabel('$V_{GS}$[V]')
    plt.ylabel('Error %')
    plt.title('Schokley Model: Relative Error (L='+i+')')
    plt.grid()
    
    #gráfico dos erros relativos do modelo n power
    plt.figure()
    plt.plot(Vgs,erro_n,'.')
    #plt.ylim(-2,10)
    #plt.xlim(0.3,1)
    plt.xlabel('$V_{GS}$[V]')
    plt.ylabel('Error %')
    plt.title('N Power Model: Relative Error (L='+i+')')
    plt.grid()