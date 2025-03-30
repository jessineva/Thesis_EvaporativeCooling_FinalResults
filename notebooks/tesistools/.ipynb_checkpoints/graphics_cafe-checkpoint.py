import pandas as pd
import matplotlib.pyplot as plt
from iertools.read import read_sql
from dateutil.parser import parse
import numpy as np
import matplotlib.dates as mdates
from matplotlib.ticker import StrMethodFormatter

def import_csv(file, inicio, final):
    df = pd.read_csv(file)
    fecha = pd.DataFrame(pd.date_range(inicio, final, freq="1min"))
    df["date"] = fecha
    df.set_index(df.date, inplace=True)

    extras = ["Date/Time"]
    df.drop(extras, axis=1, inplace=True)
    nombres = {'Environment:Site Outdoor Air Drybulb Temperature [C](TimeStep)':                                       "t_out",
           'Environment:Site Outdoor Air Humidity Ratio [kgWater/kgDryAir](TimeStep)':                                 "w_out",
           'Environment:Site Outdoor Air Relative Humidity [%](TimeStep)':                                             "rh_out",
           'Environment:Site Outdoor Air Enthalpy [J/kg](TimeStep)':                                                   "h_out",
           'Environment:Site Outdoor Air Barometric Pressure [Pa](TimeStep)':                                          "p_atm",
           'Environment:Site Wind Speed [m/s](TimeStep)':                                                              "ws_out",
           'Environment:Site Wind Direction [deg](TimeStep)':                                                          "wd_out",
       'NCAFETERIA-DIVISIONCAFETERIA:Surface Inside Face Temperature [C](TimeStep)' :                                  "DivCafe_Ti",
       'NCAFETERIA-DIVISIONCAFETERIA:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':     "DivCafe_hi",
       'NCAFETERIA-DIVISIONCAFETERIA:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                     "DivCafe_Qrate_conv",
       'NCAFETERIA-DIVISIONCAFETERIA_OESTE:Surface Inside Face Temperature [C](TimeStep)':                             "DivCafeOeste_Ti",
       'NCAFETERIA-DIVISIONCAFETERIA_OESTE:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)': "DivCafeOeste_hi",
       'NCAFETERIA-DIVISIONCAFETERIA_OESTE:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':          "DivCafeOeste_Qrate_conv",
       'NCAFETERIA-MUROEVAP:Surface Inside Face Temperature [C](TimeStep)' :                                      "MuroEvap_Ti",
       'NCAFETERIA-MUROEVAP:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':         "MuroEvap_hi",
       'NCAFETERIA-MUROEVAP:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                         "MuroEvap_Qrate_conv",
       'NCAFETERIA-MUROEVAP:Surface Outside Face Outdoor Air Wind Speed [m/s](TimeStep)':                         "MuroEvap_ws",
       'NCAFETERIA-MUROEVAP:Surface Outside Face Outdoor Air Wind Direction [deg](TimeStep)':                     "MuroEvap_wd",
       'NCAFETERIA-MUROOESTEEVAP:Surface Inside Face Temperature [C](TimeStep)':                                  "MuroEvapEste_Ti",
       'NCAFETERIA-MUROOESTEEVAP:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':    "MuroEvapEste_hi",
       'NCAFETERIA-MUROOESTEEVAP:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                    "MuroEvapEste_Qrate_conv",
       'NCAFETERIA-MUROOESTEEVAP:Surface Outside Face Outdoor Air Wind Speed [m/s](TimeStep)':                    "MuroEvapEste_ws",
       'NCAFETERIA-MUROOESTEEVAP:Surface Outside Face Outdoor Air Wind Direction [deg](TimeStep)':                "MuroEvapEste_wd",
       'NCAFETERIA-MUROSUR 1:Surface Inside Face Temperature [C](TimeStep)':                                      "MuroSur_Ti",
       'NCAFETERIA-MUROSUR 1:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':        "MuroSur_hi",
       'NCAFETERIA-MUROSUR 1:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)' :                       "MuroSur_Qrate_conv",
       'NCAFETERIA-MUROSUR 1:Surface Outside Face Outdoor Air Wind Speed [m/s](TimeStep)':                        "MuroSur_ws",
       'NCAFETERIA-MUROSUR 1:Surface Outside Face Outdoor Air Wind Direction [deg](TimeStep)':                    "MuroSur_wd",
       'SURFACE 31:Surface Inside Face Temperature [C](TimeStep)':                                                "S31_Ti",
       'SURFACE 31:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':                  "S31_hi",
       'SURFACE 31:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                                  "S31_Qrate_conv",
       'SURFACE 31:Surface Outside Face Outdoor Air Wind Speed [m/s](TimeStep)':                                  "S31_ws",
       'SURFACE 31:Surface Outside Face Outdoor Air Wind Direction [deg](TimeStep)':                              "S31_wd",
       'NCAFETERIA-PISO 1:Surface Inside Face Temperature [C](TimeStep)':                                           "Piso_Ti",
       'NCAFETERIA-PISO 1:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':             "Piso_hi",
       'NCAFETERIA-PISO 1:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                             "Piso_Qrate_conv",
       'NCAFETERIA-TECHO 1:Surface Inside Face Temperature [C](TimeStep)':                                          "Techo_Ti",
       'NCAFETERIA-TECHO 1:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':            "Techo_hi",
       'NCAFETERIA-TECHO 1:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                            "Techo_Qrate_conv",
       'NCAFETERIA_ENTRADA:Surface Inside Face Temperature [C](TimeStep)':                                        "VentEnt_Ti",
       'NCAFETERIA_ENTRADA:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':          "VentEnt_hi",
       'NCAFETERIA_ENTRADA:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                          "VentEnt_Qrate_conv",
       'NCAFETERIA_ENTRADA:Surface Outside Face Outdoor Air Wind Speed [m/s](TimeStep)':                          "VentEnt_ws",
       'NCAFETERIA_ENTRADA:Surface Outside Face Outdoor Air Wind Direction [deg](TimeStep)':                      "VentEnt_wd",
       'NCAFETERIA_VENTANAOESTE:Surface Inside Face Temperature [C](TimeStep)':                                   "VentOeste_Ti",
       'NCAFETERIA_VENTANAOESTE:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':     "VentOeste_hi",
       'NCAFETERIA_VENTANAOESTE:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                     "VentOeste_Qrate_conv",
       'NCAFETERIA_VENTANAOESTE:Surface Outside Face Outdoor Air Wind Speed [m/s](TimeStep)':                     "VentOeste_ws",
       'NCAFETERIA_VENTANAOESTE:Surface Outside Face Outdoor Air Wind Direction [deg](TimeStep)':                 "VentOeste_wd",
       'SUB SURFACE 1:Surface Inside Face Temperature [C](TimeStep)':                                             "VentS1_Ti",
       'SUB SURFACE 1:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':               "VentS1_hi",
       'SUB SURFACE 1:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                               "VentS1_Qrate_conv",
       'SUB SURFACE 1:Surface Outside Face Outdoor Air Wind Speed [m/s](TimeStep)':                               "VentS1_ws",
       'SUB SURFACE 1:Surface Outside Face Outdoor Air Wind Direction [deg](TimeStep)':                           "VentS1_wd",
       'SUB SURFACE 2:Surface Inside Face Temperature [C](TimeStep)':                                             "VentS2_Ti",
       'SUB SURFACE 2:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':               "VentS2_hi",
       'SUB SURFACE 2:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                               "VentS2_Qrate_conv",
       'SUB SURFACE 2:Surface Outside Face Outdoor Air Wind Speed [m/s](TimeStep)':                               "VentS2_ws",
       'SUB SURFACE 2:Surface Outside Face Outdoor Air Wind Direction [deg](TimeStep)':                           "VentS2_wd",
       'NCAFETERIA:Zone Mean Air Temperature [C](TimeStep)':                                                      "t_zone",    
       'NCAFETERIA:Zone Mean Air Humidity Ratio [kgWater/kgDryAir](TimeStep)':                                    "wi_zone",
       'NCAFETERIA_ENTRADA:AFN Linkage Node 1 to Node 2 Mass Flow Rate [kg/s](TimeStep)':                         "VentEnt_mass_out",     
       'NCAFETERIA_ENTRADA:AFN Linkage Node 2 to Node 1 Mass Flow Rate [kg/s](TimeStep)':                         "VentEnt_mass_in", 
       'NCAFETERIA_ENTRADA:AFN Linkage Node 1 to Node 2 Volume Flow Rate [m3/s](TimeStep)':                       "VentEnt_vol_out", 
       'NCAFETERIA_ENTRADA:AFN Linkage Node 2 to Node 1 Volume Flow Rate [m3/s](TimeStep)':                       "VentEnt_vol_in",
       'NCAFETERIA_ENTRADA:AFN Linkage Node 1 to Node 2 Pressure Difference [Pa](TimeStep)':                      "VentEnt_PresDif",
       'NCAFETERIA_VENTANAOESTE:AFN Linkage Node 1 to Node 2 Mass Flow Rate [kg/s](TimeStep)':                    "VentOeste_mass_out",   
       'NCAFETERIA_VENTANAOESTE:AFN Linkage Node 2 to Node 1 Mass Flow Rate [kg/s](TimeStep)':                    "VentOeste_mass_in", 
       'NCAFETERIA_VENTANAOESTE:AFN Linkage Node 1 to Node 2 Volume Flow Rate [m3/s](TimeStep)':                  "VentOeste_vol_out", 
       'NCAFETERIA_VENTANAOESTE:AFN Linkage Node 2 to Node 1 Volume Flow Rate [m3/s](TimeStep)':                  "VentOeste_vol_in",
       'NCAFETERIA_VENTANAOESTE:AFN Linkage Node 1 to Node 2 Pressure Difference [Pa](TimeStep)':                 "VentOeste_PresDif",
       'NCAFETERIA:AFN Zone Infiltration Volume [m3](TimeStep)':                                                  "Infil_vol", 
       'NCAFETERIA:AFN Zone Infiltration Mass [kg](TimeStep)':                                                    "Infil_mass",
       'NCAFETERIA:AFN Zone Ventilation Volume [m3](TimeStep)':                                                   "Venti_vol",
       'NCAFETERIA:AFN Zone Ventilation Mass [kg](TimeStep)':                                                     "ventilation_mass",
       'NCAFETERIA:Zone Air Relative Humidity [%](TimeStep)':                                                     "rh_zone",
       'MODEL OUTDOOR AIR NODE:System Node Relative Humidity [%](TimeStep)':           "Node_rh",
       'MODEL OUTDOOR AIR NODE:System Node Current Density [kg/m3](TimeStep)':        "Dens_out",
       'MODEL OUTDOOR AIR NODE:System Node Specific Heat [J/kg-K](TimeStep)':          "Node_Cp",
       'MODEL OUTDOOR AIR NODE:System Node Enthalpy [J/kg](TimeStep)':                 "Node_enthalpy",
       'MODEL OUTDOOR AIR NODE:System Node Wind Speed [m/s](TimeStep) ':               "Node_ws"
                        }
    
    df.rename(columns = nombres, inplace=True)
    return df


def graph_general(fecha1,timedelta,data, ylim, area = None):
    fecha1 = parse(fecha1)
    fecha2 = fecha1 + pd.Timedelta(timedelta)

    def formato(ax, titulo):
        ax.set_title(titulo)
        ax.legend()
        ax.set_xlim(fecha1,fecha2)

        

    fig, ax = plt.subplots(3,2, figsize=(15,9), sharex=True)

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

    ax[1][0].plot(data.ws_out, label="outdoors")
    formato(ax[1][0], "Wind speed [m/s]")
    if ylim[2] != None:
        ax[1][0].set_ylim(ylim[2][0], ylim[2][1])

    ax[1][1].plot(data.wd_out, label="outdoors")
    formato(ax[1][1], "Wind direction [°]")
    if ylim[3] != None:
        ax[1][1].set_ylim(ylim[3][0], ylim[3][1])

        
    ax[2][0].plot(data.Venti_vol)
    ax[2][0].set_title("Inlet air volume [m3]")
    ax[2][0].set_xlim(fecha1,fecha2)
    if ylim[4] != None:
        ax[2][0].set_ylim(ylim[4][0], ylim[4][1])
        
    ax[2][1].plot(data.wi_zone)
    ax[2][1].set_title("Humidity Ratio [kgWater/kgDryAir]")
    ax[2][1].set_xlim(fecha1,fecha2)
    if ylim[5] != None:
        ax[2][1].set_ylim(ylim[5][0], ylim[5][1])
        

def graph_EPyNum(df, fecha1, timedelta, ylim):
    
    def formato(ax):
        ax.legend()
        ax.set_xlim(fecha1,fecha2)
        
    fecha1 = parse(fecha1)
    fecha2 = fecha1 + pd.Timedelta(timedelta)

    fig, (ax,ax1) = plt.subplots(1,2,figsize=(15,3))
    
    ax.plot(df.t_zone_valid,"r.", label="Function")
    ax.plot(df.t_zone, label="EnergyPlus")
    ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.1f}'))
    ax.set_ylabel("Tdb [°C]")
    ax.set_xlabel("Time [dd HH:mm]")
    ax.grid()
    formato(ax)
    if ylim[0] != None:
        ax.set_ylim(ylim[0][0], ylim[0][1])

    ax1.plot(df.rh_zone_valid,"r.",label="Function")
    ax1.plot(df.rh_zone, label="EnergyPlus")
    ax1.yaxis.set_major_formatter(StrMethodFormatter('{x:,.1f}'))
    ax1.set_ylabel("RH [%]")
    ax1.set_xlabel("Time [dd HH:mm]")
    ax1.grid()
    formato(ax1)
    if ylim[0] != None:
        ax1.set_ylim(ylim[1][0], ylim[1][1])