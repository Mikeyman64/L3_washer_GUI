from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ListProperty, DictProperty
from datetime import datetime

class GlobalScreenManager(ScreenManager):

    #Define global properties
    PUMP_RELAY = 0
    background_task = 1
    count = 0
    flowCalFac = 38 # 
    vdd = 3.3
    global_size = 4096
    chipDiff = 1024/65536  # lib returns 16b number (65536) and chip returns 1024 number, so result is scaled by 1024/65536
    d2Mpa = 0.101325/620.6061 #calibration for converting ADC output to a pressure value, max pressure over max analog voltge (estimate, needs testing)




    sn_msg = StringProperty("CCA SN")
    pn_msg = StringProperty("CCA PN")
    sessID = StringProperty("")
    userID = StringProperty("")
    badID = BooleanProperty(True)
    washType = StringProperty("")
    boardCount = NumericProperty(0)
    boardScrnList = ListProperty([])
    PN_BackingList = ListProperty([])
    SN_BackingList = ListProperty([])
    DataDict = DictProperty({
        "Washer_ID": "WSH1001",
        "Session_ID": 0,
        "User_ID": "null",
        "Wash_Type": "null",
        "CCA_Count": 0,
        # "PN_Array": [],
        # "SN_Array": [],
        "PN_SN_String": "",
        "Start_Time": '12:00:00',
        "End_Time": '12:00:00',
        "Aborted": 'false',
        "Date": datetime.now().strftime("01-01-2000")
    })
    
    CalibrateDict = {
        "inputConcentration": 0,
        "oldConcentration": 0,
        "flowRate": None,
        "pressure": None,

    }
    CALIBRATION_USERS = {}

    inputConcentration = NumericProperty(None)




def GSM():
    """Returns the GlobalScreenManager instance from the running app. USE FOR ALL GLOBAL VARIABLES!"""
    return App.get_running_app().root
