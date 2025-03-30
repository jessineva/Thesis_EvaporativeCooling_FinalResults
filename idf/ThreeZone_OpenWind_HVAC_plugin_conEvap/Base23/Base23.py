from pyenergyplus.plugin import EnergyPlusPlugin
from io import open

class EvapMistCooling(EnergyPlusPlugin):
    def __init__(self):
        """
        Creates a new instance asking for get handles.
        """
        super().__init__()
        try:
            self.file = open("Base23.csv", 'r')
            self.file.readline()
            self.mode = True
        except Exception:
            self.mode = False
        self.need_to_get_handles = True
       
    def evap_eff(self, flow, threshold=0.5, amp=0.5, min_eff=(0.01), max_eff = 0.2):
        """
        Modifies evaporative effectiveness based on flow

        Parameters
        ----------
        flow -- Airflow (m^3/s)
        threshold -- Maximum value where evaporation is 100% effective (m^3/s)
        amp -- Range of decay of effectiveness (m^3/s) 
        min_eff -- Adimensional minimum effectiveness

        Returns
        -------
        eff -- Adimensional evaporative effectiveness

        """
        if (abs(flow) < threshold):
            eff = max_eff
        elif (abs(flow) > threshold + amp):
            eff = min_eff
        else :
            eff = max_eff - (max_eff - min_eff) / amp * (abs(flow) - threshold)
        return eff

    def get_result_temperature(self, state, Tbs, Tbh, pa, Qin, eff_ev, nozzles):
        """
        Calculates the result temperature based on 100% evaporation of water in the fictional evaporative zone.
        
        Parameters
        ----------
        state -- state object required to pass into EnergyPlus Runtime API function calls
        Tbs -- drybulb temperature of inlet airstream (°C)
        Tbh -- wetbulb temperature of inlet airstream (°C)
        pa -- atmospheric pressure of environment (Pa)
        Qin -- inlet airflow (m^3/s)
        nozzles -- quantity of nozzles of the evaporative system
        
        Returns
        -------
        Tee -- result evaporative temperature of outlet airstream (°C)
        """
        psychro = self.api.functional.psychrometrics(state)
        #SpFlow =  0.500e-6 #m3/s
        #SpFlow = 3.33e-6 #m3/s
        SpFlow  = 1.135e-6 #m3/s
        w   = psychro.humidity_ratio_d(state, Tbs, Tbh, pa)
        m_a = abs(Qin) / psychro.specific_volume(state, Tbs, w, pa)
        m_w = w * m_a
        m_w += eff_ev * 1000. * nozzles * SpFlow
        #20210530 eapuertoc - Se crea una curva de ajuste recta: si m_a = -2.0, ya no es efectivo el evaporativo
        if (m_a <= 1.2):
             return Tbs-(Tbs-Tbh)/4
        
        #    if (m_a < -2.0):
        #        Tbh_eq = Tbh
        #    else:
        #        Tbh_eq = Tbs + 0.5 * m_a * (Tbs - Tbh)
        #    hum = psychro.humidity_ratio_d(state, Tbs, Tbh_eq, pa)
        #else:
        #    hum = m_w / m_a
        
        hum = m_w/m_a
        Tee = (psychro.enthalpy(state, Tbs, w) / 1000. - 2501. * hum) / (1.006 + 1.86 * hum)
        
        if (Tee < Tbh):
            Tee = Tbh
        return Tee
        
    def get_effectiveness(self, Tbs, Tbh, Tee):
        """
        Calculates evaporative effectiveness system.
        
        Parameters
        ----------
        Tbs -- drybulb temperature of inlet airstream (°C)
        Tbh -- wetbulb temperature of inlet airstream (°C)
        Tee -- result evaporative temperature of outlet airstream (°C)    

        Returns:
        --------
        Adimensional value of effectiveness        
        """
        
        if abs(Tbs - Tbh) < 0.001:
            return 0
        return (Tbs - Tee) / (Tbs - Tbh)

    def get_rel_hum(self, state, Tbs, Tbh, Pb):
        """
        Uses psychrometric functions of EnergyPlus to calculate relative humidity.
        
        Parameters
        ----------
        Tbs -- drybulb temperature of inlet airstream (°C)
        Tbh -- wetbulb temperature of inlet airstream (°C)
        Pb -- barometric pressure of environment (Pa)  

        Returns:
        --------
        Relative humidity as a fraction value [0, 1]  
        """
        psychro = self.api.functional.psychrometrics(state)
        return psychro.relative_humidity_b(state, Tbs, psychro.humidity_ratio_d(state, Tbs, Tbh, Pb), Pb)

    def get_handles(self, state):
        """
        Obtains the handles required for the simulation.
        
        Parameters
        ----------
        state -- state object required to pass into EnergyPlus Runtime API function calls
        """
        
        mtnQ21 = u"AFN LINKAGE NODE 2 TO NODE 1 VOLUME FLOW RATE"
        mtnQ12 = u"AFN LINKAGE NODE 1 TO NODE 2 VOLUME FLOW RATE"
        keyENV = u"ENVIRONMENT"
        compSchCompact = u"SCHEDULE:COMPACT"
        ctrlSch = u"SCHEDULE VALUE"
        # Sensors
        #  - Enviroment variable handles
        self.senTbs = self.api.exchange.get_variable_handle(state, u"SITE OUTDOOR AIR DRYBULB TEMPERATURE", keyENV)
        self.senTbh = self.api.exchange.get_variable_handle(state, u"SITE OUTDOOR AIR WETBULB TEMPERATURE", keyENV)
        self.senRH = self.api.exchange.get_variable_handle(state, u"SITE OUTDOOR AIR RELATIVE HUMIDITY", keyENV)
        self.senPb = self.api.exchange.get_variable_handle(state, u"SITE OUTDOOR AIR BAROMETRIC PRESSURE", keyENV)
        
        #  - Airflow AFN variable handles
        self.senPBCafe1_Q12 = self.api.exchange.get_variable_handle(state, mtnQ12, u"EVAPZONE_WE")
        self.senPBCafe1_Q21 = self.api.exchange.get_variable_handle(state, mtnQ21, u"EVAPZONE_WE")
        self.senPBCafe2_Q12 = self.api.exchange.get_variable_handle(state, mtnQ12, u"EVAPZONE2_WOESTE")
        self.senPBCafe2_Q21 = self.api.exchange.get_variable_handle(state, mtnQ21, u"EVAPZONE2_WOESTE")
        
        # Global Variables
        self.PBCafe1_effev = self.api.exchange.get_global_handle(state, u"PBCafe1_eff_evp")
        self.PBCafe1_eff = self.api.exchange.get_global_handle(state, u"PBCafe1_eff_sys")
        self.PBCafe1_Tee = self.api.exchange.get_global_handle(state, u"PBCafe1_Tee")
        self.PBCafe2_effev = self.api.exchange.get_global_handle(state, u"PBCafe2_eff_evp")
        self.PBCafe2_eff = self.api.exchange.get_global_handle(state, u"PBCafe2_eff_sys")
        self.PBCafe2_Tee = self.api.exchange.get_global_handle(state, u"PBCafe2_Tee")
        self.PBCafe1_RHee = self.api.exchange.get_global_handle(state, u"PBCafe1_RHee")
        self.PBCafe2_RHee = self.api.exchange.get_global_handle(state, u"PBCafe2_RHee") 
        self.gvPBCafe1_Qin = self.api.exchange.get_global_handle(state, u"PBCafe1_Qin")
        self.gvPBCafe2_Qin = self.api.exchange.get_global_handle(state, u"PBCafe2_Qin")
      
        # Actuators
        self.actPBCafe1_Tee = self.api.exchange.get_actuator_handle(state, compSchCompact, ctrlSch, u"PBCAFE1_TSP")
        self.actPBCafe1_RHee = self.api.exchange.get_actuator_handle(state, compSchCompact, ctrlSch, u"PBCAFE1_HSP") 
        self.actPBCafe2_Tee = self.api.exchange.get_actuator_handle(state, compSchCompact, ctrlSch, u"PBCAFE2_TSP")
        self.actPBCafe2_RHee = self.api.exchange.get_actuator_handle(state, compSchCompact, ctrlSch, u"PBCAFE2_HSP")
        
        self.need_to_get_handles = False
        
    def on_begin_timestep_before_predictor(self, state) -> int:
        #Manage handles
        if self.need_to_get_handles:
            if self.api.exchange.api_data_fully_ready(state):
                self.get_handles(state)
            else:
                return 0
        
        #Get sensor values
        Tbs = self.api.exchange.get_variable_value(state, self.senTbs)
        Tbh = self.api.exchange.get_variable_value(state, self.senTbh)
        RH  = self.api.exchange.get_variable_value(state, self.senTbs)
        Pb  = self.api.exchange.get_variable_value(state, self.senPb)
        
        #If is the first run, mode is FALSE, it will be the first run and the program shall use the sensor value, otherwise
        #the program shall use the previous output variable report to extract the values to use.
        if (self.mode):
            midata = self.file.readline().split(',')
            PBCafe1_Qin = float(midata[18]) - float(midata[17])
            PBCafe2_Qin = float(midata[20]) - float(midata[19])
        else:
            PBCafe1_Qin = self.api.exchange.get_variable_value(state, self.senPBCafe1_Q21)\
                    - self.api.exchange.get_variable_value(state, self.senPBCafe1_Q12)
            PBCafe2_Qin = self.api.exchange.get_variable_value(state, self.senPBCafe2_Q12)\
                    - self.api.exchange.get_variable_value(state, self.senPBCafe2_Q21)

        #Calculates the evaporative effectiveness 
#         effev1 = self.evap_eff(PBCafe1_Qin, min_eff=(2/14), max_eff= 0.2)
#         effev2 = self.evap_eff(PBCafe2_Qin, min_eff=(2/14), max_eff= 0.3)
        effev1 = 1
        effev2 = 1
        
        #This lines are to compare results in notebook, it doesn't affect the results 
        self.api.exchange.set_global_value(state, self.gvPBCafe1_Qin, PBCafe1_Qin)
        self.api.exchange.set_global_value(state, self.gvPBCafe2_Qin, PBCafe2_Qin)

        #Calculate misting evaporative system conditionns in PBCafe1
#         effev1 = 1
        self.api.exchange.set_global_value(state, self.PBCafe1_effev, effev1)
        self.api.exchange.set_global_value(state, self.PBCafe1_Tee, self.get_result_temperature(state, Tbs, Tbh, Pb, PBCafe1_Qin, effev1, 14))
        self.api.exchange.set_global_value(state, self.PBCafe1_eff, self.get_effectiveness(Tbs, Tbh, self.api.exchange.get_global_value(state, self.PBCafe1_Tee)))
        self.api.exchange.set_global_value(state, self.PBCafe1_RHee, self.get_rel_hum(state, self.api.exchange.get_global_value(state, self.PBCafe1_Tee), Tbh, Pb))
        
        #Calculate misting evaporative system conditionns in PBCafe2
#         effev2 = 1
        self.api.exchange.set_global_value(state, self.PBCafe2_effev, effev2)
        self.api.exchange.set_global_value(state, self.PBCafe2_Tee, self.get_result_temperature(state, Tbs, Tbh, Pb, PBCafe2_Qin, effev2, 13))
        self.api.exchange.set_global_value(state, self.PBCafe2_eff, self.get_effectiveness(Tbs, Tbh, self.api.exchange.get_global_value(state, self.PBCafe2_Tee)))
        self.api.exchange.set_global_value(state, self.PBCafe2_RHee, self.get_rel_hum(state, self.api.exchange.get_global_value(state, self.PBCafe1_Tee), Tbh, Pb))
                
        #Set actuator values
        self.api.exchange.set_actuator_value(state, self.actPBCafe1_Tee, self.api.exchange.get_global_value(state, self.PBCafe1_Tee))
        self.api.exchange.set_actuator_value(state, self.actPBCafe1_RHee, self.PBCafe1_RHee)
        self.api.exchange.set_actuator_value(state, self.actPBCafe2_Tee, self.api.exchange.get_global_value(state, self.PBCafe2_Tee))
        self.api.exchange.set_actuator_value(state, self.actPBCafe2_RHee, self.PBCafe2_RHee)
              
        return 0
