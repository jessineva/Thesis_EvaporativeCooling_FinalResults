import pandas as pd
import matplotlib.pyplot as plt
from iertools.read import read_sql
from dateutil.parser import parse
import numpy as np
import matplotlib.dates as mdates

def import_csv(file, inicio, final):
    df = pd.read_csv(file)
    fecha = pd.DataFrame(pd.date_range(inicio, final, freq="1min"))
    df["date"] = fecha
    df.set_index(df.date, inplace=True)

    extras = ["Date/Time", "ESTE:Surface Outside Face Outdoor Air Wind Speed [m/s](TimeStep)", "ESTE:Surface Outside Face Outdoor Air Wind Direction [deg](TimeStep)",
             "OESTE:Surface Outside Face Outdoor Air Wind Speed [m/s](TimeStep)","OESTE:Surface Outside Face Outdoor Air Wind Direction [deg](TimeStep)"]
    df.drop(extras, axis=1, inplace=True)
    nombres = {'Environment:Site Outdoor Air Drybulb Temperature [C](TimeStep)':"t_out",
           'Environment:Site Outdoor Air Relative Humidity [%](TimeStep)':"rh_out",
           'Environment:Site Outdoor Air Barometric Pressure [Pa](TimeStep)':"p_atm",
           'Environment:Site Wind Speed [m/s](TimeStep)': "ws_out",
           'Environment:Site Wind Direction [deg](TimeStep)':"wd_out",
           'VENTANA_ESTE:Surface Outside Face Outdoor Air Wind Speed [m/s](TimeStep)':"ws_SOFO_este",
           'VENTANA_ESTE:Surface Outside Face Outdoor Air Wind Direction [deg](TimeStep)':"wd_SOFO_este",
           'VENTANA_OESTE:Surface Outside Face Outdoor Air Wind Speed [m/s](TimeStep)':"ws_SOFO_oeste",
           'VENTANA_OESTE:Surface Outside Face Outdoor Air Wind Direction [deg](TimeStep)':"wd_SOFO_oeste",
           'THERMAL ZONE 1:Zone Mean Air Temperature [C](TimeStep)':"t_zone",
           'THERMAL ZONE 1:Zone Mean Air Humidity Ratio [kgWater/kgDryAir](TimeStep)':"wi_zone",
           'VENTANA_OESTE:AFN Linkage Node 1 to Node 2 Volume Flow Rate [m3/s](TimeStep)':"OESTE_air_out",
           'VENTANA_OESTE:AFN Linkage Node 2 to Node 1 Volume Flow Rate [m3/s](TimeStep)':"OESTE_air_in",
           'VENTANA_OESTE:AFN Linkage Node 1 to Node 2 Pressure Difference [Pa](TimeStep)':"OESTE_PresDiference",
           'VENTANA_ESTE:AFN Linkage Node 1 to Node 2 Volume Flow Rate [m3/s](TimeStep)':"ESTE_air_out",
           'VENTANA_ESTE:AFN Linkage Node 2 to Node 1 Volume Flow Rate [m3/s](TimeStep)':"ESTE_air_in",
           'VENTANA_ESTE:AFN Linkage Node 1 to Node 2 Pressure Difference [Pa](TimeStep)':"ESTE_PresDiference",
           'THERMAL ZONE 1:AFN Zone Infiltration Volume [m3](TimeStep)':"infiltration_vol",
           'THERMAL ZONE 1:AFN Zone Ventilation Volume [m3](TimeStep)':"ventilation_vol",
           'THERMAL ZONE 1:Zone Air Relative Humidity [%](TimeStep)':"rh_zone",
           'MODEL OUTDOOR AIR NODE:System Node Current Density [kg/m3](TimeStep)': "Dens_out",
            "Environment:Site Outdoor Air Humidity Ratio [kgWater/kgDryAir](TimeStep)":"w_out",
            "VENTANA_OESTE:AFN Linkage Node 2 to Node 1 Mass Flow Rate [kg/s](TimeStep)":"Este_mass_in",
            "THERMAL ZONE 1:AFN Zone Ventilation Mass [kg](TimeStep)":"ventilation_mass",
            "Environment:Site Outdoor Air Enthalpy [J/kg](TimeStep)": "h_out",                                             
           "ESTE:Surface Inside Face Temperature [C](TimeStep)" : "ESTE_Ti",                                                     
           "ESTE:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)" : "ESTE_hi",                            
           "OESTE:Surface Inside Face Temperature [C](TimeStep)" : "OESTE_Ti",                                                    
           "OESTE:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)" : "OESTE_hi",                     
           "SURFACE 3:Surface Inside Face Temperature [C](TimeStep)" : "S3_Ti",                                                
           "SURFACE 3:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)" : "S3_hi",                  
           "SURFACE 5:Surface Inside Face Temperature [C](TimeStep)" : "S5_Ti",                                                
           "SURFACE 5:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)" : "S5_hi",                  
           "SURFACE 1:Surface Inside Face Temperature [C](TimeStep)" : "S1_Ti",                                                
           "SURFACE 1:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)" : "S1_hi",                  
           "SURFACE 6:Surface Inside Face Temperature [C](TimeStep)" : "S6_Ti",                                                
           "SURFACE 6:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)" : "S6_hi",                  
           "VENTANA_ESTE:Surface Inside Face Temperature [C](TimeStep)" : "VENTANA_ESTE_Ti",                                             
           "VENTANA_ESTE:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)" : "VENTANA_ESTE_hi",               
           "VENTANA_OESTE:Surface Inside Face Temperature [C](TimeStep)" : "VENTANA_OESTE_Ti",                                            
           "VENTANA_OESTE:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)" : "VENTANA_OESTE_hi",
           "ESTE:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)":         "Este_Qrate_conv",   
           "OESTE:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)":        "Oeste_Qrate_conv",          
           "SURFACE 3:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)":    "S3_Qrate_conv",
           "SURFACE 5:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)":    "S5_Qrate_conv",              
           "SURFACE 1:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)":    "S1_Qrate_conv",      
           "SURFACE 6:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)":    "S6_Qrate_conv",    
           "VENTANA_ESTE:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)": "VentEste_Qrate_conv",             
           "VENTANA_OESTE:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)":"VentOeste_Qrate_conv",
            "THERMAL ZONE 1:Zone Air Heat Balance Surface Convection Rate [W](TimeStep)": "Q_conv"
               
                        }
    df.rename(columns = nombres, inplace=True)
    return df



def graph_general(fecha1,timedelta,data, ylim, area = None, mode = "EffectArea"):
    fecha1 = parse(fecha1)
    fecha2 = fecha1 + pd.Timedelta(timedelta)

    def formato(ax, titulo):
        ax.set_title(titulo)
        ax.legend()
        ax.set_xlim(fecha1,fecha2)
        
    if mode=="EffectArea":
        vol_in = data.infiltration_vol
    if mode=="DetOpen":
        vol_in = data.ventilation_vol

    if area == None:
        sale1       = data["ESTE_air_out"]
        entra1      = data["ESTE_air_in"]
        sale2       = data["OESTE_air_out"]
        entra2      = data["OESTE_air_in"]
        label_entra = "West window [m3/s]"
        label_sale  = "East window [m3/s]"

    else:
        sale1  = data["ESTE_air_out"] /area
        entra1 = data["ESTE_air_in"]  /area
        sale2  = data["OESTE_air_out"]/area
        entra2 = data["OESTE_air_in"] /area
        label_entra = "West window [m/s]"
        label_sale  = "East window [m/s]"



    fig, ax = plt.subplots(4,2, figsize=(15,9), sharex=True)

    ax[0][0].plot(data.t_out, "b.", label="Outdoors")
    ax[0][0].plot(data.t_zone, "r", label="Zone")
    formato(ax[0][0], "Temperature [°C]")
    if ylim[0] != None:
        ax[0][0].set_ylim(ylim[0][0], ylim[0][1])

    ax[0][1].plot(data.rh_out, "b.", label="outdoors")
    ax[0][1].plot(data.rh_zone, "r", label="Zone")
    formato(ax[0][1], "Humidity [%]")
    if ylim[1] != None:
        ax[0][1].set_ylim(ylim[1][0], ylim[1][1])

    ax[1][0].plot(data.ws_out,"b.", label="outdoors")
    ax[1][0].plot(data.ws_SOFO_oeste, "r", label="Zone")
    formato(ax[1][0], "Wind speed [m/s]")
    if ylim[2] != None:
        ax[1][0].set_ylim(ylim[2][0], ylim[2][1])

    ax[1][1].plot(data.wd_out,"b.", label="outdoors")
    ax[1][1].plot(data.wd_SOFO_oeste,"r", label="Zone")
    formato(ax[1][1], "Wind direction [°]")
    if ylim[3] != None:
        ax[1][1].set_ylim(ylim[3][0], ylim[3][1])

    ax[2][0].plot(sale2,"r.", label="out")
    ax[2][0].plot(entra2, label="in")
    formato(ax[2][0], label_entra)
    if ylim[4] != None:
        ax[2][0].set_ylim(ylim[4][0], ylim[4][1])

    ax[2][1].plot(sale1,"r.", label="out")
    ax[2][1].plot(entra1, label="in")
    formato(ax[2][1], label_sale)
    if ylim[5] != None:
        ax[2][1].set_ylim(ylim[5][0], ylim[5][1])
        
    ax[3][0].plot(vol_in)
    ax[3][0].set_title("Inlet air volume [m3]")
    ax[3][0].set_xlim(fecha1,fecha2)
    if ylim[6] != None:
        ax[3][0].set_ylim(ylim[6][0], ylim[6][1])
        
    ax[3][1].plot(data.wi_zone)
    ax[3][1].set_title("Humidity Ratio [kgWater/kgDryAir]")
    ax[3][1].set_xlim(fecha1,fecha2)
    if ylim[7] != None:
        ax[3][1].set_ylim(ylim[7][0], ylim[7][1])
        


        
def graph_EPyNum(df, fecha1, timedelta, ylim):
    
    def formato(ax, titulo):
        ax.set_title(titulo)
        ax.legend()
        ax.set_xlim(fecha1,fecha2)
        
    fecha1 = parse(fecha1)
    fecha2 = fecha1 + pd.Timedelta(timedelta)

    fig, (ax,ax1) = plt.subplots(1,2,figsize=(15,3))
    
    ax.plot(df.t_zone_valid,"r.", label="Numeric")
    ax.plot(df.t_zone, label="EP")
    formato(ax,"Ti [°C]" )
    if ylim[0] != None:
        ax.set_ylim(ylim[0][0], ylim[0][1])

    ax1.plot(df.rh_zone_valid,"r.",label="Numeric")
    ax1.plot(df.rh_zone, label="EP")
    formato(ax1,"Rhi [%]")
    if ylim[0] != None:
        ax1.set_ylim(ylim[1][0], ylim[1][1])