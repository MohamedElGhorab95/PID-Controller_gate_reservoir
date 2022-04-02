# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 09:54:36 2022

@author: mel013
"""
import pandas as pd                                 # importing pandas library
Qinp = pd.read_excel('Qinp.xlsx')['Qinp'].tolist()  #reading excel file and storing Qinp in a list 
###################################################################

####################   Defining Constants #########################
sp = 3.5                            #setpoint
A = 10000000                        #area of reservoir
W = 3.0                             #gate width in m
Cc = 0.61                           #coefficient of contraction
dt = 7200                           #timestep
y1 = [3.0]                          #initial water level
ref = 3                             #reference gate opening
#################### Controller parameters #########################
K = 1.25
Ti = 8500000
Td = 25500
###################### Predefining functions #############################

def calc_Qout(Cc,W,y1,y2):
    '''
    Parameters
    ----------
    Cd : discharge coefficient.
    W : gate width.
    y1 : upstream water depth.
    y2 : gate opening.

    Returns
    -------
   output discharge.

    '''
    if y2>=4:
        y2=4
    elif y2<=2:
        y2=2
    if y1<y2:
        return (1/0.015)*(W*y1)*((W*y1)/(W+2*y1))**(2/3)*(0.001)**0.5 #manning equation
    else:
        Cd = Cc/(1+Cc*y2/y1)**0.5
        return y2*W*Cd*(2*9.81*y1)**0.5                #gate equation

def calc_level(y,Qin,Qout,dt,A):
    '''
    Parameters
    ----------
    y : water level.
    Qin : input discharge.
    Qout : output discharge.
    dt : time step.
    A : area.

    Returns
    -------
    water level for the next timestep.

    '''
    return y+dt/A*(Qin-Qout)                            #Mass balance equation

def PID(e,ae,de,k,dt,Ti,Td):
    '''
    Parameters
    ----------
    e : error at current timestep.
    ae : accumulated error at current timestep.
    de : delta error.
    dt : timestep.
    k : proportional gain.
    Ti : integral action.
    Td : differential action.

    Returns
    -------
    control output based on PID basics.

    '''
    return k*(e + 1/Ti*ae*dt + Td*de/dt)

def graphs(Qinp,Qout,sp,y1,y2):
    
    import matplotlib.pyplot as plt
    import numpy as np
    Qi = np.array(Qinp)
    Qo = np.array(Qout)
    WL = np.array(y1)
    GL = np.array(y2)
    SP = np.array([sp for i in range(len(Qinp))])
    FL = np.array([4.5 for i in range(len(Qinp))])
    DL = np.array([3.2 for i in range(len(Qinp))])
    t = np.array([i for i in range(len(Qinp))])
    plt.figure('Discharge')
    plt.plot(t,Qi,Qo)
    plt.legend(['Inflow Discharge','Outflow Discharge'])
    plt.xlabel('timestep') 
    plt.ylabel('Discharge')
    plt.xlim([0,172])
    plt.grid()
    plt.figure('levels')
    plt.plot(t,FL,'r',DL,'y')
    plt.plot(t,SP,'--')
    plt.plot(t,WL,'b')
    plt.legend(['Flood level','Drought Level','Setpoint','Water Level'])
    plt.xlabel('timestep') 
    plt.ylabel('level')
    plt.xlim([0,172])
    plt.grid()
    plt.figure('Gate')
    plt.plot(t,WL,'r-',GL, 'k')
    plt.xlabel('timestep') 
    plt.ylabel('level')
    plt.xlim([0,172])
    plt.legend(['water level','gate opening'])
    plt.grid()
    return plt.show(['Discharge','levels','Gate'])

def gate_op(sp,A,W,Cc,dt,y1,ref,K,Ti,Td):
    '''
    engine for running the PID controller operation

    Parameters
    ----------
    sp : setpoint.
    A : Area.
    W : gate width.
    Cc : coefficient of contraction.
    dt : timestep.
    y1 : water level.
    ref : reference opening of the gate.
    K : proportional gain.
    Ti : integral coefficient.
    Td : differential coefficient.

    Returns
    -------
    input discharge, output discharge, setpoint, water level, gate level

    '''
################### initializing first timestep ##########################

    error= [y1[0]-sp]                           #error calculation (water level - setpoint)
    accerror = [error[0]]                       #array for accumulated error
    u=[K*(error[0])]                            #first control output
    y2 = [ref]                             #first gate response
    Qout = [calc_Qout(Cc, W, y1[0], y2[0])]     #calculating output discharge
    
    ################## looping on the second to final timestep ###############
    
    for i in range(1,len(Qinp)):
        y1.append(calc_level(y1[i-1], Qinp[i-1], Qout[i-1], dt, A))     #appending calculated waterlevel
        error.append(y1[i] - sp)                                        #appending calculated error
        accerror.append(error[i] + accerror[i-1])                       #appending calculated accumulated error
        de = error[i]-error[i-1]                                        #calculating error difference
        u.append(PID(error[i],accerror[i],de,K,dt,Ti,Td))               #appending calculated controller output
        ######### Checking on gate level ########
        if u[i] + ref >= 4:
            y2.append(4.0)
        elif u[i] + ref <= 2:
            y2.append(2.0)
        else:
            y2.append(u[i] + ref)
        Qout.append(calc_Qout(Cc, W, y1[i], y2[i]))                     #appending calculated output discharge
    return Qinp, Qout, sp, y1, y2

def fixed_gate(sp,A,W,Cc,dt,y1,ref):
    '''
    water level calculation engine with a fixed gate.
    '''
    ################### initializing first timestep ##########################

    error= [y1[0]-sp]                           #error calculation (water level - setpoint)
    accerror = [error[0]]                       #array for accumulated error
    y2 = [ref]                             #first gate response
    Qout = [calc_Qout(Cc, W, y1[0], y2[0])]     #calculating output discharge

    ################## looping on the second to final timestep ###############

    for i in range(1,len(Qinp)):
        y1.append(calc_level(y1[i-1], Qinp[i-1], Qout[i-1], dt, A))     #appending calculated waterlevel
        error.append(y1[i] - sp)                                        #appending calculated error
        accerror.append(error[i] + accerror[i-1])                       #appending calculated accumulated error
        Qout.append(calc_Qout(Cc, W, y1[i], y2[0]))                     #appending calculated output discharge
    y2 = [ref for i in range(len(Qinp))]
    return Qinp, Qout, sp, y1, y2        
######################################################################

[Qinp,Qout,sq,y1,y2] = gate_op(sp,A,W,Cc,dt,y1,ref,K,Ti,Td)         #initiate the model (with control)
# [Qinp,Qout,sq,y1,y2] = fixed_gate(sp,A,W,Cc,dt,y1,ref)              #initiate the model (fixed gate)
##############  Plotting results #####################################

graphs(Qinp, Qout, sp, y1, y2)                                      #Displaying results
print('maximum water level = ',round(max(y1),2),'m')
print('maximum output discharge = ',round(max(Qout),2), 'm3/s')


