"""
NATIONAL AUTONOMOUS UNIVERSITY OF MEXICO (UNAM)
RENEWABLE ENERGY INSTITUTE (IER)
ENERGY IN BUILDINGS GROUP (GEE)
AUTHOR: M.Eng. Efrain Alonso Puerto Castellanos 
DESCRIPTION: Collection of functions to use ESOLMET csv file as EnergyPlus EPW Input File using Ladybug Tools
NOTE: Before use this class, install the following packages:
 - pip install lbt-ladybug
 - pip install pandas
 - pip install psychrolib
"""

import pandas as pd
import datetime
from ladybug.epw import EPW
from ladybug.epw import EPWFields
from ladybug.analysisperiod import AnalysisPeriod
from ladybug.datacollection import HourlyContinuousCollection
from ladybug.datacollection import MonthlyCollection
from ladybug.location import Location
from ladybug.futil import write_to_file

def __epw_from_dict(data:dict) -> EPW:
    """ Create EPW from a dictionary.

    Parameters:
    -----------
        data: A python dictionary in the following format
    .. code-block:: python
            {
            "location": {} ,  # ladybug location schema
            "data_collections": [],  # list of hourly annual hourly data collection
                # schemas for each of the 35 fields within the EPW file.
            "metadata": {},  # dict of metadata assigned to all data collections
            "heating_dict": {},  # dict containing heating design conditions
            "cooling_dict": {},  # dict containing cooling design conditions
            "extremes_dict": {},  # dict containing extreme design conditions
            "extreme_hot_weeks": {},  # dict with values of week-long ladybug
                # analysis period schemas signifying extreme hot weeks.
            "extreme_cold_weeks": {},  # dict with values of week-long ladybug
                # analysis period schemas signifying extreme cold weeks.
            "typical_weeks": {},  # dict with values of week-long ladybug
                # analysis period schemas signifying typical weeks.
            "monthly_ground_temps": {},  # dict with keys as floats signifying
                # depths in meters below ground and values of monthly
                # collection schema
            "is_ip": False  # Boolean // denote whether the data is in IP units
            "is_leap_year": False  # Boolean, denote whether data is for
                                   # a leap year
            "daylight_savings_start": 0,  # signify when daylight savings starts
                                          # or 0 for no daylight savings
            "daylight_savings_end" 0,  # signify when daylight savings ends
                                       # or 0 for no daylight savings
            "comments_1": ""  # String, epw comments
            "comments_2": ""  # String, epw comments
            }
    """
    # Initialize the class with all data missing
    epw_obj = EPW(None)
    epw_obj._is_header_loaded = True
    epw_obj._is_data_loaded = True
    # Check required and optional keys
    required_keys = ('location', 'data_collections')
    option_keys_dict = ('metadata', 'heating_dict', 'cooling_dict',
                        'extremes_dict', 'extreme_hot_weeks', 'extreme_cold_weeks',
                        'typical_weeks', 'monthly_ground_temps')
    for key in required_keys:
        assert key in data, 'Required key "{}" is missing!'.format(key)
    assert len(data['data_collections']) == epw_obj._num_of_fields, \
        'The number of data_collections must be {}. Got {}.'.format(
            epw_obj._num_of_fields, len(data['data_collections']))
    for key in option_keys_dict:
        if key not in data:
            data[key] = {}
    # Set the required properties of the EPW object.
    epw_obj._location = Location.from_dict(data['location'])
    epw_obj._data = [HourlyContinuousCollection.from_dict(dc)
                     for dc in data['data_collections']]
    if 'is_leap_year' in data:
        epw_obj._is_leap_year = data['is_leap_year']
    if 'is_ip' in data:
        epw_obj._is_ip = data['is_ip']
    epw_obj._metadata = data['metadata']
    epw_obj.heating_design_condition_dictionary = data['heating_dict']
    epw_obj.cooling_design_condition_dictionary = data['cooling_dict']
    epw_obj.extreme_design_condition_dictionary = data['extremes_dict']
    def _dedict(parent_dict, obj):
        new_dict = {}
        for key, val in parent_dict.items():
            new_dict[key] = obj.from_dict(val)
        return new_dict
    epw_obj.extreme_hot_weeks = _dedict(data['extreme_hot_weeks'], AnalysisPeriod)
    epw_obj.extreme_cold_weeks = _dedict(data['extreme_cold_weeks'], AnalysisPeriod)
    epw_obj.typical_weeks = _dedict(data['typical_weeks'], AnalysisPeriod)
    epw_obj.monthly_ground_temperature = _dedict(
        data['monthly_ground_temps'], MonthlyCollection)
    if 'daylight_savings_start' in data:
        epw_obj.daylight_savings_start = data['daylight_savings_start']
    if 'daylight_savings_end' in data:
        epw_obj.daylight_savings_end = data['daylight_savings_end']
    if 'comments_1' in data:
        epw_obj.comments_1 = data['comments_1']
    if 'comments_2' in data:
        epw_obj.comments_2 = data['comments_2']
    return epw_obj

def __fill_epw_with_df(epw_dict:dict, data:pd.DataFrame, cols:dict):
    """
    Based on a dictionary, this function fills defined EPW Fields in EPW dictionary with an specified DataFrame column
    Use the function create_field_dictionary to know the valid EPW Fields.

    Parameters:
    -----------
    epw_dict -- dictionary using LadyBug EPW format
    data -- pandas dataframe with ESOLMET data
    cols -- dictionary with EPWFields to modify in Keys and dataframe column names in Values

    Returns:
    --------
    This function affects the epw_dict in place
    """
    epw_dict["data_collections"][0]["values"] = list(data.index.year)
    epw_dict["data_collections"][1]["values"] = list(data.index.month)
    epw_dict["data_collections"][2]["values"] = list(data.index.day)
    epw_dict["data_collections"][3]["values"] = list(data.index.hour)
    epw_dict["data_collections"][4]["values"] = list(data.index.minute)
    for i in range(34):
        field_name = epw_dict["data_collections"][i]["header"]["data_type"]["name"]
        if field_name in cols.keys():
            epw_dict["data_collections"][i]["values"] = list(data[cols[field_name]])

def __getDataPeriodLine(a_period:AnalysisPeriod, year:int):
    """
    Create the string line with DATA PERIOD of the EPW File

    Parameters:
    -----------
    a_period -- LadyBug Analysis Period
    year -- year of EPW

    Returns:
    string line with DATAPERIOD of the EPW File
    """
    startDate = a_period.datetimes[0].replace(year=year)
    endDate = a_period.datetimes[-1].replace(year=year)
    startDate.strftime("%A")
    endDate.strftime("%A")
    line = ["DATA PERIODS,1"]
    line.append(str(a_period.timestep) + ",Data")
    line.append(startDate.strftime("%A"))
    line.append(str(startDate.month) + "/" + str(startDate.day))
    line.append(str(endDate.month) + "/" + str(endDate.day))
    return ",".join(line) + '\n'

def create_field_dict() -> dict:
    """
    Create a dictionary with all EPW Fields allowed as keys and preset values to modify with dataframe column names

    Returns:
    --------
    Dictionary with all EPW Fields
    """
    field_dict = {}
    for i in range(5,35):
        key_name = str(EPWFields.field_by_number(i).name)
        field_dict[key_name] = "Data " + str(EPWFields.field_by_number(i).name) + " Name"
    return field_dict

def epw_from_dataframe(data:pd.DataFrame, a_period:AnalysisPeriod, location:Location, cols:dict) -> EPW:
    """
    Create a LadyBug EPW instance using a pandas DataFrame
    
    Parameters:
    -----------
    data -- Pandas DataFrame with data to use to fill epw
    a_period -- LadyBug Analysis Period with DATA PERIOD info of epw
    location -- LadyBug Location instance with the data of the EPW location
    cols -- dictionary with EPW Field names as keys and dataframe column names to use to fill as values

    Returns:
    --------
    LadyBug EPW instance with data adquired from DataFrame
    """
    year = data.index[0].year
    startdate = datetime.datetime(year=year, month=a_period.st_month, day=a_period.st_day, hour=a_period.st_hour, minute=0)
    enddate = datetime.datetime(year=year, month=a_period.end_month, day=a_period.end_day, hour=a_period.end_hour, minute=59)
    epw_dict = EPW.from_missing_values().to_dict()
    epw_dict["location"] = location.to_dict()
    epwdata = data[startdate:enddate]
    for i in range(len(epw_dict["data_collections"]) - 1):
        epw_dict["data_collections"][i]["header"]["analysis_period"] = a_period.to_dict()
        epw_dict["data_collections"][i]["values"] = epw_dict["data_collections"][i]["values"][:len(epwdata)]
    __fill_epw_with_df(epw_dict, epwdata, cols)
    return __epw_from_dict(epw_dict)

def read_esolmet_file(filepath:str, timestep:int = 60) -> pd.DataFrame:
    """
    Create a dataframe with an ESOLMET CSV file
    
    Parameters:
    -----------
    filepath -- path with filename of the ESOLMET file
    timestep -- value with a validated timestep to stablish timestamps, use AnalysisPeriod.VALIDTIMESTEPS Keys,
                it will use 60 in case of incorrect input

    Returns:
    --------
    Dataframe with ESOLMET data
    """
    try:
        tstp = AnalysisPeriod.VALIDTIMESTEPS[timestep]
    except KeyError:
        tstp = AnalysisPeriod.VALIDTIMESTEPS[60]
        print("The timestep is not valid, adjusted to 60 mins (1 hour)")
    df = pd.read_csv(filepath, delimiter='\t', skiprows=[0,2,3], encoding="ISO-8859-1", na_values="NAN")
    df["Timestamp"] = pd.to_datetime(df["TIMESTAMP"],format="%d/%m/%Y\t%H:%M")
    df.set_index("Timestamp", inplace = True)
    df.dropna(inplace = True)
    a_period = AnalysisPeriod(st_month=df.index[0].month,
                              st_day=df.index[0].day,
                              st_hour=df.index[0].hour,
                              end_month=df.index[-1].month,
                              end_day=df.index[-1].day,
                              end_hour=df.index[-1].hour,
                              timestep=timestep)
    rs = df.resample("{}Min".format(tstp)).mean()
    return rs.interpolate(), a_period


def save_epw(epw:EPW, filepath:str, a_period:AnalysisPeriod):
    """Get a text string for the entirety of the EPW file contents.
    
    Parameters:
    -----------
    epw -- LadyBug EPW instance to save
    filepath -- path with filename of the epw file
    a_period -- LadyBug Analysis Period instance to calculate DATA PERIOD line
    """
    # load data if it's  not loaded convert to SI if it is in IP
    if not epw.is_data_loaded:
        epw._import_data()
    originally_ip = False
    if epw.is_ip:
        epw.convert_to_si()
        originally_ip = True
    # write the file
    lines = epw.header
    lines[-1] = __getDataPeriodLine(a_period, epw._data[0]._values[0])
    try:
        for timestamp in range(0, len(a_period.datetimes)):
            line = []
            for field in range(0, epw._num_of_fields):
                line.append(str(epw._data[field]._values[timestamp]))
            lines.append(",".join(line) + "\n")
    except IndexError:
        length_error_msg = 'Data length has not the analysis period length and cannot be ' + \
            'saved as an EPW file.'
        raise ValueError(length_error_msg)
    finally:  # move last item to start position for fields on the hour
        for field in range(0, epw._num_of_fields):
            point_in_time = epw._data[field].header.data_type.point_in_time
            if point_in_time:
                last_hour = epw._data[field]._values.pop()
                epw._data[field]._values.insert(0, last_hour)
    if originally_ip:  # put back the object as it was
        epw.convert_to_ip()
    with open(filepath, "w") as outf:
        for line in lines:
            outf.write(line)