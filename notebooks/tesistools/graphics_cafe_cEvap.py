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

    extras = ["Date/Time"]
    df.drop(extras, axis=1, inplace=True)
    nombres = {'Environment:Site Outdoor Air Drybulb Temperature [C](TimeStep)':                             "t_out",
 'Environment:Site Outdoor Air Wetbulb Temperature [C](TimeStep)':                                           "twb_out",
 'Environment:Site Outdoor Air Humidity Ratio [kgWater/kgDryAir](TimeStep)':                                 "w_out",
 'Environment:Site Outdoor Air Relative Humidity [%](TimeStep)':                                             "rh_out",
 'Environment:Site Outdoor Air Barometric Pressure [Pa](TimeStep)':                                          "p_atm",
 'Environment:Site Wind Speed [m/s](TimeStep)':                                                              "ws_out",
 'Environment:Site Wind Direction [deg](TimeStep)':                                                          "wd_out",
 'Environment:Site Outdoor Air Enthalpy [J/kg](TimeStep)' :                                                  "h_out",
 'EVAPZONE_MUROESTE:Surface Inside Face Temperature [C](TimeStep)':                                    "EvZone_MuroEste_Ti",
 'EVAPZONE_MUROESTE:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':      "EvZone_MuroEste_hi",
 'EVAPZONE_MUROESTE:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                      "EvZone_MuroEste_Qrate_conv",
 'EVAPZONE_MURONORTE:Surface Inside Face Temperature [C](TimeStep)':                                   "EvZone_MuroNorte_Ti",
 'EVAPZONE_MURONORTE:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':     "EvZone_MuroNorte_hi",
 'EVAPZONE_MURONORTE:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                     "EvZone_MuroNorte_Qrate_conv",
 'EVAPZONE_MUROOESTE:Surface Inside Face Temperature [C](TimeStep)':                                   "EvZone_MuroOeste_Ti",
 'EVAPZONE_MUROOESTE:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':     "EvZone_MuroOeste_hi",
 'EVAPZONE_MUROOESTE:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                     "EvZone_MuroOeste_Qrate_conv",
 'EVAPZONE_MUROSUR:Surface Inside Face Temperature [C](TimeStep)':                                     "EvZone_MuroSur_Ti",
 'EVAPZONE_MUROSUR:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':       "EvZone_MuroSur_hi",
 'EVAPZONE_MUROSUR:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                       "EvZone_MuroSur_Qrate_conv",
 'EVAPZONE_PISO:Surface Inside Face Temperature [C](TimeStep)':                                        "EvZone_Piso_Ti",
 'EVAPZONE_PISO:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':          "EvZone_Piso_hi",
 'EVAPZONE_PISO:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                          "EvZone_Piso_Qrate_conv",
 'EVAPZONE_TECHO:Surface Inside Face Temperature [C](TimeStep)':                                       "EvZone_Techo_Ti",
 'EVAPZONE_TECHO:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':         "EvZone_Techo_hi",
 'EVAPZONE_TECHO:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                         "EvZone_Techo_Qrate_conv",
 'EVAPZONE_WE:Surface Inside Face Temperature [C](TimeStep)':                                          "EvZone_WE_Ti",
 'EVAPZONE_WE:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':            "EvZone_WE_hi",
 'EVAPZONE_WE:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                            "EvZone_WE_Qrate_conv",
 'EVAPZONE_WN:Surface Inside Face Temperature [C](TimeStep)':                                          "EvZone_WN_Ti",
 'EVAPZONE_WN:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':            "EvZone_WN_hi",
 'EVAPZONE_WN:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                            "EvZone_WN_Qrate_conv",
 'EVAPZONE_WO:Surface Inside Face Temperature [C](TimeStep)':                                          "EvZone_WO_Ti",
 'EVAPZONE_WO:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':            "EvZone_WO_hi",
 'EVAPZONE_WO:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                            "EvZone_WO_Qrate_conv",
 'EVAPZONE_WS:Surface Inside Face Temperature [C](TimeStep)':                                          "EvZone_WS_Ti",
 'EVAPZONE_WS:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':            "EvZone_WS_hi",
 'EVAPZONE_WS:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                            "EvZone_WS_Qrate_conv",
 'EVAPZONE2_MUROESTE:Surface Inside Face Temperature [C](TimeStep)':                                   "EvZone2_MuroEste_Ti",
 'EVAPZONE2_MUROESTE:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':     "EvZone2_MuroEste_hi",
 'EVAPZONE2_MUROESTE:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                     "EvZone2_MuroEste_Qrate_conv",
 'EVAPZONE2_MURONORTE:Surface Inside Face Temperature [C](TimeStep)':                                  "EvZone2_MuroNorte_Ti",
 'EVAPZONE2_MURONORTE:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':    "EvZone2_MuroNorte_hi",
 'EVAPZONE2_MURONORTE:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                    "EvZone2_MuroNorte_Qrate_conv",
 'EVAPZONE2_MUROOESTE:Surface Inside Face Temperature [C](TimeStep)':                                  "EvZone2_MuroOeste_Ti",
 'EVAPZONE2_MUROOESTE:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':    "EvZone2_MuroOeste_hi",
 'EVAPZONE2_MUROOESTE:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                    "EvZone2_MuroOeste_Qrate_conv",
 'EVAPZONE2_MUROSUR:Surface Inside Face Temperature [C](TimeStep)':                                    "EvZone2_MuroSur_Ti",
 'EVAPZONE2_MUROSUR:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':      "EvZone2_MuroSur_hi",
 'EVAPZONE2_MUROSUR:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                      "EvZone2_MuroSur_Qrate_conv",
 'EVAPZONE2_PISO:Surface Inside Face Temperature [C](TimeStep)':                                       "EvZone2_MuroPiso_Ti",
 'EVAPZONE2_PISO:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':         "EvZone2_MuroPiso_hi",
 'EVAPZONE2_PISO:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                         "EvZone2_MuroPiso_Qrate_conv",
 'EVAPZONE2_TECHO:Surface Inside Face Temperature [C](TimeStep)':                                      "EvZone2_MuroTecho_Ti",
 'EVAPZONE2_TECHO:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':        "EvZone2_MuroTecho_hi",
 'EVAPZONE2_TECHO:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                        "EvZone2_MuroTecho_Qrate_conv",
 'EVAPZONE2_WESTE:Surface Inside Face Temperature [C](TimeStep)':                                      "EvZone2_WE_Ti",
 'EVAPZONE2_WESTE:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':        "EvZone2_WE_hi",
 'EVAPZONE2_WESTE:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                        "EvZone2_WE_Qrate_conv",
 'EVAPZONE2_WOESTE:Surface Inside Face Temperature [C](TimeStep)':                                     "EvZone2_WO_Ti",
 'EVAPZONE2_WOESTE:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':       "EvZone2_WO_hi",
 'EVAPZONE2_WOESTE:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                       "EvZone2_WO_Qrate_conv",
 'NCAFETERIA-DIVISIONCAFETERIA:Surface Inside Face Temperature [C](TimeStep)':                                   "Cafe_DivCafe_Ti",
 'NCAFETERIA-DIVISIONCAFETERIA:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':     "Cafe_DivCafe_hi",
 'NCAFETERIA-DIVISIONCAFETERIA:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                     "Cafe_DivCafe_Qrate_conv",
 'NCAFETERIA-DIVISIONCAFETERIA_OESTE:Surface Inside Face Temperature [C](TimeStep)':                             "Cafe_DivCafeOeste_Ti",
 'NCAFETERIA-DIVISIONCAFETERIA_OESTE:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':"Cafe_DivCafeOeste_hi",
 'NCAFETERIA-DIVISIONCAFETERIA_OESTE:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':        "Cafe_DivCafeOeste_Qrate_conv",
 'NCAFETERIA-MUROEVAP:Surface Inside Face Temperature [C](TimeStep)':                                           "Cafe_MuroEvap_Ti",
 'NCAFETERIA-MUROEVAP:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':             "Cafe_MuroEvap_hi",
 'NCAFETERIA-MUROEVAP:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                             "Cafe_MuroEvap_Qrate_conv",
 'NCAFETERIA-MUROOESTEEVAP:Surface Inside Face Temperature [C](TimeStep)':                                 "Cafe_MuroEvapOeste_Ti",
 'NCAFETERIA-MUROOESTEEVAP:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':   "Cafe_MuroEvapOeste_hi",
 'NCAFETERIA-MUROOESTEEVAP:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                   "Cafe_MuroEvapOeste_Qrate_conv",
 'NCAFETERIA-MUROSUR 1:Surface Inside Face Temperature [C](TimeStep)':                                     "Cafe_MuroSur_Ti",
 'NCAFETERIA-MUROSUR 1:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':       "Cafe_MuroSur_hi",
 'NCAFETERIA-MUROSUR 1:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                       "Cafe_MuroSur_Qrate_conv",
 'SURFACE 31:Surface Inside Face Temperature [C](TimeStep)':                                               "Cafe_S31_Ti",
 'SURFACE 31:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':                 "Cafe_S31_hi",
 'SURFACE 31:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                                 "Cafe_S31_Qrate_conv",
 'NCAFETERIA-PISO 1:Surface Inside Face Temperature [C](TimeStep)':                                        "Cafe_Piso_Ti",
 'NCAFETERIA-PISO 1:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':          "Cafe_Piso_hi",
 'NCAFETERIA-PISO 1:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                          "Cafe_Piso_Qrate_conv",
 'NCAFETERIA-TECHO 1:Surface Inside Face Temperature [C](TimeStep)':                                       "Cafe_Techo_Ti",
 'NCAFETERIA-TECHO 1:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':         "Cafe_Techo_hi",
 'NCAFETERIA-TECHO 1:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                         "Cafe_Techo_Qrate_conv",
 'NCAFETERIA_ENTRADA:Surface Inside Face Temperature [C](TimeStep)':                                       "Cafe_VentEnt_Ti",
 'NCAFETERIA_ENTRADA:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':         "Cafe_VentEnt_hi",
 'NCAFETERIA_ENTRADA:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                         "Cafe_VentEnt_Qrate_conv",
 'NCAFETERIA_VENTANAOESTE:Surface Inside Face Temperature [C](TimeStep)':                                  "Cafe_VentOeste_Ti",
 'NCAFETERIA_VENTANAOESTE:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':    "Cafe_VentOeste_hi",
 'NCAFETERIA_VENTANAOESTE:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                    "Cafe_VentOeste_Qrate_conv",
 'SUB SURFACE 1:Surface Inside Face Temperature [C](TimeStep)':                                            "Cafe_VentS1_Ti",
 'SUB SURFACE 1:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':              "Cafe_VentS1_hi",
 'SUB SURFACE 1:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                              "Cafe_VentS1_Qrate_conv",
 'SUB SURFACE 2:Surface Inside Face Temperature [C](TimeStep)':                                            "Cafe_VentS2_Ti",
 'SUB SURFACE 2:Surface Inside Face Convection Heat Transfer Coefficient [W/m2-K](TimeStep)':              "Cafe_VentS2_hi",
 'SUB SURFACE 2:Surface Inside Face Convection Heat Gain Rate [W](TimeStep)':                              "Cafe_VentS2_Qrate_conv",
 'EVAPZONE:Zone Mean Air Temperature [C](TimeStep)':                                                       "EvZone_t_zone",
 'EVAPZONE:Zone Mean Air Humidity Ratio [kgWater/kgDryAir](TimeStep)':                                     "EvZone_w_zone",
 'EVAPZONE2:Zone Mean Air Temperature [C](TimeStep)':                                                      "EvZone2_t_zone",
 'EVAPZONE2:Zone Mean Air Humidity Ratio [kgWater/kgDryAir](TimeStep)':                                    "EvZone2_w_zone",
 'NCAFETERIA:Zone Mean Air Temperature [C](TimeStep)':                                                     "Cafe_t_zone",
 'NCAFETERIA:Zone Mean Air Humidity Ratio [kgWater/kgDryAir](TimeStep)':                                   "Cafe_w_zone",
 'EVAPZONE_WE:AFN Linkage Node 1 to Node 2 Mass Flow Rate [kg/s](TimeStep)':                               "EvZone_WE_link_mass_out",
 'EVAPZONE_WE:AFN Linkage Node 2 to Node 1 Mass Flow Rate [kg/s](TimeStep)':                               "EvZone_WE_link_mass_in",
 'EVAPZONE_WN:AFN Linkage Node 1 to Node 2 Mass Flow Rate [kg/s](TimeStep)':                               "EvZone_WN_link_mass_out",
 'EVAPZONE_WN:AFN Linkage Node 2 to Node 1 Mass Flow Rate [kg/s](TimeStep)':                               "EvZone_WN_link_mass_in",
 'EVAPZONE_WO:AFN Linkage Node 1 to Node 2 Mass Flow Rate [kg/s](TimeStep)':                               "EvZone_WO_link_mass_out",
 'EVAPZONE_WO:AFN Linkage Node 2 to Node 1 Mass Flow Rate [kg/s](TimeStep)':                               "EvZone_WO_link_mass_in",
 'EVAPZONE_WS:AFN Linkage Node 1 to Node 2 Mass Flow Rate [kg/s](TimeStep)':                               "EvZone_WS_link_mass_out",
 'EVAPZONE_WS:AFN Linkage Node 2 to Node 1 Mass Flow Rate [kg/s](TimeStep)':                               "EvZone_WS_link_mass_in",
 'EVAPZONE2_WESTE:AFN Linkage Node 1 to Node 2 Mass Flow Rate [kg/s](TimeStep)':                           "EvZone2_WE_link_mass_out",
 'EVAPZONE2_WESTE:AFN Linkage Node 2 to Node 1 Mass Flow Rate [kg/s](TimeStep)':                           "EvZone2_WE_link_mass_in",
 'EVAPZONE2_WOESTE:AFN Linkage Node 1 to Node 2 Mass Flow Rate [kg/s](TimeStep)':                          "EvZone2_WO_link_mass_out",
 'EVAPZONE2_WOESTE:AFN Linkage Node 2 to Node 1 Mass Flow Rate [kg/s](TimeStep)':                          "EvZone2_WO_link_mass_in",
 'NCAFETERIA_ENTRADA:AFN Linkage Node 1 to Node 2 Mass Flow Rate [kg/s](TimeStep)':                        "Cafe_VentEnt_mass_out", 
 'NCAFETERIA_ENTRADA:AFN Linkage Node 2 to Node 1 Mass Flow Rate [kg/s](TimeStep)':                        "Cafe_VentEnt_mass_in", 
 'NCAFETERIA_VENTANAOESTE:AFN Linkage Node 1 to Node 2 Mass Flow Rate [kg/s](TimeStep)':                   "Cafe_VentOeste_mass_out", 
 'NCAFETERIA_VENTANAOESTE:AFN Linkage Node 2 to Node 1 Mass Flow Rate [kg/s](TimeStep)':                   "Cafe_VentOeste_mass_in", 
 'SUB SURFACE 1:AFN Linkage Node 1 to Node 2 Mass Flow Rate [kg/s](TimeStep)':                             "Cafe_VentS1_mass_out",  
 'SUB SURFACE 1:AFN Linkage Node 2 to Node 1 Mass Flow Rate [kg/s](TimeStep)':                             "Cafe_VentS1_mass_in", 
 'SUB SURFACE 2:AFN Linkage Node 1 to Node 2 Mass Flow Rate [kg/s](TimeStep)':                             "Cafe_VentS2_mass_out", 
 'SUB SURFACE 2:AFN Linkage Node 2 to Node 1 Mass Flow Rate [kg/s](TimeStep)':                             "Cafe_VentS2_mass_in", 
   'EVAPZONE_WE:AFN Linkage Node 1 to Node 2 Volume Flow Rate [m3/s](TimeStep)':                           "EvZone_WE_link_vol_out",
   'EVAPZONE_WE:AFN Linkage Node 2 to Node 1 Volume Flow Rate [m3/s](TimeStep)':                           "EvZone_WE_link_vol_in",
   'EVAPZONE2_WOESTE:AFN Linkage Node 1 to Node 2 Volume Flow Rate [m3/s](TimeStep)':                      "EvZone2_WO_link_vol_out",
   'EVAPZONE2_WOESTE:AFN Linkage Node 2 to Node 1 Volume Flow Rate [m3/s](TimeStep)':                      "EvZone2_WO_link_vol_in",
   'NCAFETERIA_ENTRADA:AFN Linkage Node 1 to Node 2 Volume Flow Rate [m3/s](TimeStep)':                    "Cafe_VentEnt_vol_out", 
   'NCAFETERIA_ENTRADA:AFN Linkage Node 2 to Node 1 Volume Flow Rate [m3/s](TimeStep)':                    "Cafe_VentEnt_vol_in", 
   'NCAFETERIA_VENTANAOESTE:AFN Linkage Node 1 to Node 2 Volume Flow Rate [m3/s](TimeStep)':               "Cafe_VentOeste_vol_out", 
   'NCAFETERIA_VENTANAOESTE:AFN Linkage Node 2 to Node 1 Volume Flow Rate [m3/s](TimeStep)' :              "Cafe_VentOeste_vol_in", 
 'EVAPZONE:AFN Zone Infiltration Mass [kg](TimeStep)':                                                     "EvZone_InfMass",
 'EVAPZONE:AFN Zone Ventilation Mass [kg](TimeStep)':                                                      "EvZone_VentiMass",
 'EVAPZONE2:AFN Zone Infiltration Mass [kg](TimeStep)':                                                    "EvZone2_InfMass",
 'EVAPZONE2:AFN Zone Ventilation Mass [kg](TimeStep)':                                                     "EvZone2_VentiMass",
 'NCAFETERIA:AFN Zone Infiltration Mass [kg](TimeStep)':                                                   "Cafe_InfMass",
 'NCAFETERIA:AFN Zone Ventilation Mass [kg](TimeStep)':                                                    "Cafe_VentiMass",
 'EVAPZONE:Zone Air Relative Humidity [%](TimeStep)':                                                      "EvZone_rh_zone",
 'EVAPZONE2:Zone Air Relative Humidity [%](TimeStep)':                                                     "EvZone2_rh_zone",
 'NCAFETERIA:Zone Air Relative Humidity [%](TimeStep)':                                                    "Cafe_rh_zone",
 'MODEL OUTDOOR AIR NODE:System Node Current Density [kg/m3](TimeStep) ':                                  "Dens_out",
 'EVAPZONE:Zone Air Heat Balance Interzone Air Transfer Rate [W](TimeStep)':                               "EvZone_Q_zones",
 'EVAPZONE2:Zone Air Heat Balance Interzone Air Transfer Rate [W](TimeStep)':                              "EvZone2_Q_zones",
 'NCAFETERIA:Zone Air Heat Balance Interzone Air Transfer Rate [W](TimeStep)':                             "Cafe_Q_zones",
       'PBCAFE1_NODE:System Node Current Density [kg/m3](TimeStep)':                                       "PBCAFE1_NODE_dens",
       'PBCAFE1_SUPP:System Node Current Density [kg/m3](TimeStep)':                                       "PBCAFE1_SUPP_dens",
       'PBCAFE1_RETN:System Node Current Density [kg/m3](TimeStep)':                                       "PBCAFE1_RETN_dens",
       'PBCAFE2_NODE:System Node Current Density [kg/m3](TimeStep)':                                       "PBCAFE2_NODE_dens",
       'PBCAFE2_SUPP:System Node Current Density [kg/m3](TimeStep)':                                       "PBCAFE2_SUPP_dens",
       'PBCAFE2_RETN:System Node Current Density [kg/m3](TimeStep)':                                       "PBCAFE2_RETN_dens",
       'PBCafe1 Evaporative Effectiveness:PythonPlugin:OutputVariable [](TimeStep)':                       "PBCafe1_eff",           
       'PBCafe1 Result HR:PythonPlugin:OutputVariable [%](TimeStep)':                                      "PBCafe1_RH",
       'PBCafe1 Result Temperature:PythonPlugin:OutputVariable [C](TimeStep)':                             "PBCafe1_T",     
       'PBCafe1 System Effectiveness:PythonPlugin:OutputVariable [](TimeStep)':                            "PBCafe1_Syseff",      
       'PBCafe1 input airflow:PythonPlugin:OutputVariable [m^3/s](TimeStep)':                              "PBCafe1_Qin",    
       'PBCafe2 Evaporative Effectiveness:PythonPlugin:OutputVariable [](TimeStep)':                       "PBCafe2_eff",              
       'PBCafe2 Result HR:PythonPlugin:OutputVariable [%](TimeStep)':                                      "PBCafe2_RH",
       'PBCafe2 Result Temperature:PythonPlugin:OutputVariable [C](TimeStep)':                             "PBCafe2_T",          
       'PBCafe2 System Effectiveness:PythonPlugin:OutputVariable [](TimeStep)':                            "PBCafe2_Syseff",      
       'PBCafe2 input airflow:PythonPlugin:OutputVariable [m^3/s](TimeStep) ':                             "PBCafe2_Qin",        
    
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
    ax[0][0].plot(data.Cafe_t_zone, "r", label="Zone")
    formato(ax[0][0], "Temperature [°C]")
    if ylim[0] != None:
        ax[0][0].set_ylim(ylim[0][0], ylim[0][1])

    ax[0][1].plot(data.rh_out, "b.", label="outdoors")
    ax[0][1].plot(data.Cafe_rh_zone, "r", label="Zone")
    formato(ax[0][1], "Humidity [%]")
    if ylim[1] != None:
        ax[0][1].set_ylim(ylim[1][0], ylim[1][1])

    ax[1][0].plot(data.ws_out,"b.", label="outdoors")
    formato(ax[1][0], "Wind speed [m/s]")
    if ylim[2] != None:
        ax[1][0].set_ylim(ylim[2][0], ylim[2][1])

    ax[1][1].plot(data.wd_out,"b.", label="outdoors")
    formato(ax[1][1], "Wind direction [°]")
    if ylim[3] != None:
        ax[1][1].set_ylim(ylim[3][0], ylim[3][1])

        
    ax[2][0].plot(data.Cafe_VentiMass)
    ax[2][0].set_title("Inlet air mass [kg]")
    ax[2][0].set_xlim(fecha1,fecha2)
    if ylim[4] != None:
        ax[2][0].set_ylim(ylim[4][0], ylim[4][1])
        
    ax[2][1].plot(data.Cafe_w_zone)
    ax[2][1].set_title("Humidity Ratio [kgWater/kgDryAir]")
    ax[2][1].set_xlim(fecha1,fecha2)
    if ylim[5] != None:
        ax[2][1].set_ylim(ylim[5][0], ylim[5][1])
        

def graph_EPyNum(df, fecha1, timedelta, ylim):
    
    def formato(ax, titulo):
        ax.set_title(titulo)
        ax.legend()
        ax.set_xlim(fecha1,fecha2)
        
    fecha1 = parse(fecha1)
    fecha2 = fecha1 + pd.Timedelta(timedelta)

    fig, (ax,ax1) = plt.subplots(1,2,figsize=(15,3))
    
    ax.plot(df.t_zone_valid,"r.", label="Numeric")
    ax.plot(df.Cafe_t_zone, label="EP")
    formato(ax,"Ti [°C]" )
    if ylim[0] != None:
        ax.set_ylim(ylim[0][0], ylim[0][1])

    ax1.plot(df.rh_zone_valid,"r.",label="Numeric")
    ax1.plot(df.Cafe_rh_zone, label="EP")
    formato(ax1,"Rhi [%]")
    if ylim[0] != None:
        ax1.set_ylim(ylim[1][0], ylim[1][1])