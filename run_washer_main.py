from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton, MDFabButton
from kivy.clock import Clock
from kivy.properties import *
from kivy.core.window import Window
from kivymd.theming import ThemeManager
from kivymd.font_definitions import theme_font_styles


#These imports are NECESSARY.
from washerBarcodeScreen import BarcodeScreen
from washerOptionsScreen import WashOptionsScreen
from washerAddBoardsScreen import AddBoardsScreen
from washerConfirmationScreen import ConfirmWashPage
from washerScreenCountdown import WasherScreenCountdown
from washerAbortScreen import WasherAbortScreen
from washerCompleteScreen import WasherCompleteScreen
from washerCalibrationDataScreen import * # CalibrationDataPage, NewCalibrationPage, FillingBeakerPage#, start_threads
from washerGlobals import GlobalScreenManager
from kivy.uix.screenmanager import NoTransition 

from datetime import datetime
from threading import Thread
#import gpiod
#from gpiod.line import Direction, Value, Bias, Edge
import pymssql 
import time, sys, os
from dotenv import load_dotenv

        

class Runner(MDApp):

    # ALL GLOBALS INITIALIZED HERE
    # sn_msg = StringProperty("CCA SN")
    # pn_msg = StringProperty("CCA PN")
    # sessID = StringProperty("")
    # userID = StringProperty("")
    # badID = BooleanProperty(True)
    # washType = StringProperty("")
    # boardCount = NumericProperty(0)
    # boardScrnList = ListProperty([])
    # DataDict = DictProperty({
    #     "Washer_ID": "WSH1001",
    #     "Session_ID": 0,
    #     "User_ID": "null",
    #     "Wash_Type": "null",
    #     "CCA_Count": 0,
    #     "Start_Time": '12:00:00',
    #     "End_Time": '12:00:00',
    #     "Aborted": 'false',
    #     "Date": datetime.now().strftime("01-01-2000")
    # })



    def build(self):
        globalSM = GlobalScreenManager()
        Window.size = (1024, 600)
#        LabelBase.register(name='NexaHeavy', fn_regular='C:/Users/U313773/Documents/WasherGUI/washer-venv/fonts/Nexa-Heavy.ttf')
#        LabelBase.register(name='NexaLight', fn_regular='C:/Users/U313773/Documents/WasherGUI/washer-venv/fonts/Nexa-ExtraLight.ttf')
#        LabelBase.register(name='MC_Alt', fn_regular='C:/Users/U313773/Documents/WasherGUI/washer-venv/fonts/MinecrafterAlt.ttf')
#        LabelBase.register(name='MC_Reg', fn_regular='C:/Users/U313773/Documents/WasherGUI/washer-venv/fonts/MinecrafterReg.ttf')

        LabelBase.register(name='NexaHeavy', fn_regular='./fonts/Nexa-Heavy.ttf')
        LabelBase.register(name='NexaLight', fn_regular='./fonts/Nexa-ExtraLight.ttf')
        LabelBase.register(name='MC_Alt', fn_regular='./fonts/MinecrafterAlt.ttf')
        LabelBase.register(name='MC_Reg', fn_regular='./fonts/MinecrafterReg.ttf')

        self.theme_cls.font_styles.update({
            "NexaHeavy": ["NexaHeavy", 16, False, 0.15],
        })

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
         # Set colors explicitly (optional but helpful)
        # self.theme_cls.text_color = [1, 1, 1, 1]  # white
        # self.theme_cls.disabled_hint_text_color = [1, 1, 1, 0.6]


        Builder.load_file('washerGUI.kv')

        # return sm
        globalSM.add_widget(BarcodeScreen(name='barcode'))
        globalSM.add_widget(SetTimeDeltaPage(name='setTimeDeltaPage'))
        globalSM.add_widget(CalibrationDataPage(name='calibrationDataPage'))
        globalSM.add_widget(ValidateCalibUser(name='validateCalibUser'))
        globalSM.add_widget(InputSolutionTankConcentration(name="inputSolutionTankConcentration"))
        globalSM.add_widget(NewCalibrationPage(name='newCalibPage'))
        globalSM.add_widget(FillingBeakerPage(name='fillBeakerPage'))
        globalSM.add_widget(TestConcentrationPage(name='testConcPage'))
        globalSM.add_widget(AdjustRatePage(name='adjustRatePage'))
        globalSM.add_widget(WashOptionsScreen(name='washOptions'))
        globalSM.add_widget(AddBoardsScreen(name='boards_list'))
        globalSM.add_widget(ConfirmWashPage(name='confirmWashPage'))
        globalSM.add_widget(WasherScreenCountdown(name='washerScreenCountdown'))
        globalSM.add_widget(WasherAbortScreen(name="washerAbortScreen"))
        globalSM.add_widget(WasherCompleteScreen(name="washerCompleteScreen"))
        # ...
        # ...
        # When adding more pages, you MUST add it by Python classname and also reference it with the name attribute from the .kv file.

        self.populateUsersList()


        globalSM.transition = NoTransition()

        return globalSM
    

    def populateUsersList(self):
        load_dotenv("credentials.env")  # or just load_dotenv() if it's named `.env` in same dir

        driver = os.getenv('DRIVER')
        server = os.getenv('SERVER')
        user = os.getenv('UID')
        password = os.getenv('PWD')
        database = os.getenv('DATABASE')

        # Connect to the database using pyodbc
        # conn = pyodbc.connect(
        #     f'DRIVER={driver};'
        #     f'SERVER={server};'
        #     f'DATABASE={database};'
        #     f'UID={user};'
        #     f'PWD={password};'
        #     'TrustServerCertificate=yes;'
        # )
        conn = pymssql.connect(
            server=server,
            user=user,
            password=password,
            database=database
        )

        cursor = conn.cursor()
        cursor.execute('SELECT * FROM User_Table')
 
        data = cursor.fetchall()
 
        print("REMOTE_DB =====================================")
        for row in data:
            # print(row)
            GlobalScreenManager.CALIBRATION_USERS[row[0]] = row[1:]
            # if row[2] == True: # Basic Access
            #     GlobalScreenManager.USERS.append(row[0])
            # if row[3] == True: # Rework Access
            #     GlobalScreenManager.REWORK_USERS.append(row[0])
            # if row[4] == True: # BGA Access
            #     GlobalScreenManager.BGA_USERS.append(row[0])
            # if row[5] == True: # Admin Access
            #     GlobalScreenManager.ADMIN_USERS.append(row[0])
            # if row[6] == True: # Admin Access
            #     GlobalScreenManager.QA_USERS.append(row[0])


        # PRINTS ALL THE USERS PULLED FROM SQL INTO CALIBRATION_USERS.
        print(GlobalScreenManager.CALIBRATION_USERS)\
        
        # Close the connection
        conn.close()
 
        # print("Users:        ",GlobalScreenManager.USERS)
        # print("Rework Users: ",GlobalScreenManager.REWORK_USERS)
        # print("BGA Users:    ",GlobalScreenManager.BGA_USERS)
        # print("Admin Users:  ",GlobalScreenManager.ADMIN_USERS)
        # print("QA Users:     ",GlobalScreenManager.QA_USERS)
 


    def on_start(self):
        self.root.current = 'barcode'

if __name__ == "__main__":
    import traceback
    try:
        Runner().run()

    except Exception as e:
        traceback.print_exc()
    # Runner().run()
