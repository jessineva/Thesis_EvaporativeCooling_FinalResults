import pandas as pd
import matplotlib.pyplot as plt
from dateutil.parser import parse
import numpy as np
import psychrolib as ps #DOI  10.5281/zendi.2537945
ps.SetUnitSystem(ps.SI)

def interpolation(y0, y1, x0, x1, x):
    y = y0 + (y1-y0)/(x1-x0)*(x-x0)
    return y

def adiabatic_mix(T_in, rh_in, T_out, rh_out, V_out, area_window, Patm, ts=60, Volumen=8.65*10*3.5):
    
    """adiabatic_mix(T_in, rh_in, T_out, rh_out, vel_out, area_window, masl=0, ts=10, Volumen=5)
    
    Compute and return the final dry bulb temperature, relative humidity, specific volumen, humidity ratio
    and enthalpy of an adiabatic mix between the air inside an space and the incoming air to the space.
    
    Inputs:
    -T_in:        dry buld temperature (°C) of the air inside the space.
    -rh_in:       relative humidity fraction (0-1) of the air inside the space.
    -T_out:       dry buld temperature (°C) of the incoming air.
    -rh_out:      relative humidity fraction (0-1) of the incoming air.
    -vel_out:     velocity at whitch air is getting in to the space.
    -area_window: area of the window where the aire is getting in.
    -masl:        altitud of the geographical (MASL) place where this effect is taking place.
    -ts:          timestep (s).
    -Volumen:     total volumen (m^3) of the space.
    
    Outputs:
    
    *string with the amount of condensated water.
    
    *(T_final, rh_final, w_final, h_final)
       -T_final:    final temperature of the mix [°C].
       -rh_final:   final relative humidity of the mix [%].
       -w_final:    final humidity ratio of the mix[g/kg air].
       -h_final:    final enthalpy of the mix [kj/kg].
       """
            

    w_in , _ , _ , Psteam_in , h_in , v_in , *_  =  ps.CalcPsychrometricsFromRelHum(T_in, rh_in, Patm)
    w_out, _ , _ , Psteam_out, h_out, v_out, *_  =  ps.CalcPsychrometricsFromRelHum(T_out,rh_out, Patm)
    
    V_in    =  Volumen - V_out
    
    if area_window <=0:
        if area_window < 0:
            print("WARNING: Window area must be a positive value")
        if area_window == 0 or V_out == 0:
            h_final      =  h_in 
            w_final      =  w_in 
            Psteam_final =  Psteam_in
            T_final      =  T_in
            rh_final     =  rh_in
            v_final      =  v_in
            mwater = 0
            print(f"Se condensaron {mwater} kg de agua por la mezcla de aire")
            return T_final, rh_final, w_final*1000, h_final/1000
            
    else:
        if  V_out        > Volumen:
            Volumen      =  V_out
            h_final      =  h_out 
            w_final      =  w_out 
            Psteam_final =  Psteam_out
            T_final      =  T_out
            rh_final     =  rh_out
            v_final      =  v_out
            
                
            mdryair_in   =  0
            mdryair_out  =  Volumen / v_final
            
            mwater = 0
#             print(f"Se condensaron {mwater} kg de agua por la mezcla de aire")
            return T_final, rh_final, w_final*1000, h_final/1000
                
        else:
            mdryair_in    =  V_in / v_in
            mdryair_out   =  V_out / v_out
            mdryair_final =  mdryair_in + mdryair_out
            
            h_final       =  (mdryair_in * h_in + mdryair_out * h_out) / (mdryair_in + mdryair_out)
            w_final       =  (mdryair_in * w_in + mdryair_out * w_out) / (mdryair_in + mdryair_out)
            Psteam_final  =  ps.GetVapPresFromHumRatio(w_final, Patm)
            T_final       =  ps.GetTDryBulbFromEnthalpyAndHumRatio(h_final, w_final)
            rh_final      =  ps.GetRelHumFromVapPres(T_final, Psteam_final) 
            v_final       =  ps.GetMoistAirVolume(T_final, w_final, Patm)
            
                
            if  rh_final   >  1: #Se condensa el agua
                rh_final   = 1
                w_extra    = w_final
                    
                lista = np.array([[0,0]])
                for t in np.arange(-10, 50, 0.1):
                    h          =  ps.GetSatAirEnthalpy(t, Patm)   
                    if  h      >  h_final:
                        lista2 =  np.array([[t,h]])
                        lista  =  np.concatenate((lista, lista2), axis=0)
                        break
                            
                    lista2     =  np.array([[t,h]])
                    lista      =  np.concatenate((lista, lista2), axis=0)
                        
                #interpolación
                y0      =   lista[-2][0]
                y1      =   lista[-1][0]
                x0      =   lista[-2][1]
                x1      =   lista[-1][1]
                x       =   h_final
                T_final =   interpolation(y0, y1, x0, x1, x)
        
                w_final , _ , _ , Psteam_final , h_final , v_final ,*_ = ps.CalcPsychrometricsFromRelHum(T_final, 1, Patm)
                    
                mwater = format(mdryair_final * (w_extra - w_final), ".3E")
#                 print(f"Se condensaron {mwater} kg de agua")
                return T_final, rh_final, w_final*1000, h_final/1000
                    
            else:
                mwater = 0
#                 print(f"Se condensaron {mwater} kg de agua por la mezcla de aire")
                return T_final, rh_final, w_final*1000, h_final/1000


def adiabatic_mix_sdesplazar(T_in, rh_in, T_out, rh_out, V_out, area_window, Patm, ts=10, Volumen=5):
    
    """adiabatic_mix(T_in, rh_in, T_out, rh_out, vel_out, area_window, masl=0, ts=10, Volumen=5)
    
    Compute and return the final dry bulb temperature, relative humidity, specific volumen, humidity ratio
    and enthalpy of an adiabatic mix between the air inside an space and the incoming air to the space.
    
    Inputs:
    -T_in:        dry buld temperature (°C) of the air inside the space.
    -rh_in:       relative humidity fraction (0-1) of the air inside the space.
    -T_out:       dry buld temperature (°C) of the incoming air.
    -rh_out:      relative humidity fraction (0-1) of the incoming air.
    -vel_out:     velocity at whitch air is getting in to the space.
    -area_window: area of the window where the aire is getting in.
    -masl:        altitud of the geographical (MASL) place where this effect is taking place.
    -ts:          timestep (s).
    -Volumen:     total volumen (m^3) of the space.
    
    Outputs:
    
    *string with the amount of condensated water.
    
    *(T_final, rh_final, w_final, h_final)
       -T_final:    final temperature of the mix [°C].
       -rh_final:   final relative humidity of the mix [%].
       -w_final:    final humidity ratio of the mix[g/kg air].
       -h_final:    final enthalpy of the mix [kj/kg].
       """
            
    w_in , _ , _ , Psteam_in , h_in , v_in , *_  =  ps.CalcPsychrometricsFromRelHum(T_in, rh_in, Patm)
    w_out, _ , _ , Psteam_out, h_out, v_out, *_  =  ps.CalcPsychrometricsFromRelHum(T_out,rh_out, Patm)
     
    V_in    =  Volumen
    
    if area_window <=0:
        if area_window < 0:
            print("WARNING: Window area must be a positive value")
        if area_window == 0:
            h_final      =  h_in 
            w_final      =  w_in 
            Psteam_final =  Psteam_in
            T_final      =  T_in
            rh_final     =  rh_in
            v_final      =  v_in
            mwater = 0
#             print(f"Se condensaron {mwater} kg de agua por la mezcla de aire")
            return T_final, rh_final, w_final*1000, h_final/1000
            
    else:
        if  V_out        > Volumen:
            Volumen      =  V_out
            h_final      =  h_out 
            w_final      =  w_out 
            Psteam_final =  Psteam_out
            T_final      =  T_out
            rh_final     =  rh_out
            v_final      =  v_out
            
                
            mdryair_in   =  0
            mdryair_out  =  Volumen / v_final
            
            mwater = 0
#             print(f"Se condensaron {mwater} kg de agua por la mezcla de aire")
            return T_final, rh_final, w_final*1000, h_final/1000
                
        else:
            mdryair_in    =  V_in / v_in
            mdryair_out   =  V_out / v_out
            mdryair_final =  mdryair_in + mdryair_out
            
            h_final       =  (mdryair_in * h_in + mdryair_out * h_out) / (mdryair_in + mdryair_out)
            w_final       =  (mdryair_in * w_in + mdryair_out * w_out) / (mdryair_in + mdryair_out)
            Psteam_final  =  ps.GetVapPresFromHumRatio(w_final, Patm)
            T_final       =  ps.GetTDryBulbFromEnthalpyAndHumRatio(h_final, w_final)
            rh_final      =  ps.GetRelHumFromVapPres(T_final, Psteam_final) 
            v_final       =  ps.GetMoistAirVolume(T_final, w_final, Patm)
            
                
            if  rh_final   >  1: #Se condensa el agua
                rh_final   = 1
                w_extra    = w_final
                    
                lista = np.array([[0,0]])
                for t in np.arange(-10, 50, 0.1):
                    h          =  ps.GetSatAirEnthalpy(t, Patm)   
                    if  h      >  h_final:
                        lista2 =  np.array([[t,h]])
                        lista  =  np.concatenate((lista, lista2), axis=0)
                        break
                            
                    lista2     =  np.array([[t,h]])
                    lista      =  np.concatenate((lista, lista2), axis=0)
                        
                #interpolación
                y0      =   lista[-2][0]
                y1      =   lista[-1][0]
                x0      =   lista[-2][1]
                x1      =   lista[-1][1]
                x       =   h_final
                T_final =   interpolation(y0, y1, x0, x1, x)
        
                w_final , _ , _ , Psteam_final , h_final , v_final ,*_ = ps.CalcPsychrometricsFromRelHum(T_final, 1, Patm)
                    
                mwater = format(mdryair_final * (w_extra - w_final), ".3E")
#                 print(f"Se condensaron {mwater} kg de agua")
                return T_final, rh_final, w_final*1000, h_final/1000
                    
            else:
                mwater = 0
#                 print(f"Se condensaron {mwater} kg de agua por la mezcla de aire")
                return T_final, rh_final, w_final*1000, h_final/1000
        



def EPYNum(data, mode = "EffectArea", area_vent = 4, ts = 60, volume = 8.65*10*3.5):

    t_in       = data.t_zone[0]
    rh_in      = data.rh_zone[0]/100

    inicio = str(data.index[0])
    final  = str(data.index[-1])
    freq   = "1min"
    fechas = pd.date_range(inicio, final, freq=freq)
    
    temp = []
    RH   = []


    for i in np.arange(0,len(fechas)):
        fecha = data.iloc[i]
        
        if mode=="EffectArea":
            vol_in = fecha.infiltration_vol
        if mode=="DetOpen":
            vol_in = fecha.ventilation_vol
 
        T, rh, w, h =  adiabatic_mix(t_in, rh_in, fecha.t_out, fecha.rh_out/100, vol_in, area_vent, fecha.p_atm, ts, volume)
        temp.append(T)
        RH.append(rh*100)
        t_in  = T
        rh_in = rh
    data["t_zone_valid"]  = temp
    data["rh_zone_valid"] = RH
    
    return data


def EPYNum_sdesplazar(data, mode = "EffectArea", area_vent = 4, ts = 60, volume = 8.65*10*3.5):

    t_in       = data.t_zone[0]
    rh_in      = data.rh_zone[0]/100

    inicio = str(data.index[0])
    final  = str(data.index[-1])
    freq   = "1min"
    fechas = pd.date_range(inicio, final, freq=freq)
    
    temp = []
    RH   = []


    for i in np.arange(0,len(fechas)):
        fecha = data.iloc[i]
        
        if mode=="EffectArea":
            vol_in = fecha.infiltration_vol
        if mode=="DetOpen":
            vol_in = fecha.ventilation_vol
 
        T, rh, w, h =  adiabatic_mix_sdesplazar(t_in, rh_in, fecha.t_out, fecha.rh_out/100, vol_in, area_vent, fecha.p_atm, ts, volume)
        temp.append(T)
        RH.append(rh*100)
        t_in  = T
        rh_in = rh
    data["t_zone_valid"]  = temp
    data["rh_zone_valid"] = RH
    
    return data