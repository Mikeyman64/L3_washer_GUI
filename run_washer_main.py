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
from washerCalibrationDataScreen import CalibrationDataPage, NewCalibrationPage
from washerGlobals import GlobalScreenManager
from kivy.uix.screenmanager import NoTransition 



from datetime import datetime
from threading import Thread
#import gpiod
#from gpiod.line import Direction, Value, Bias, Edge
import time, sys, os

        

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
        # Window.size = (1024, 500)

        Builder.load_file('washerGUI.kv')

        # return sm
        globalSM = GlobalScreenManager()
        # these SHOULD be in the order you want them to appear!!!
        globalSM.add_widget(BarcodeScreen(name='barcode'))
        globalSM.add_widget(CalibrationDataPage(name='calibrationDataPage'))
        globalSM.add_widget(NewCalibrationPage(name='newCalibPage'))
        globalSM.add_widget(WashOptionsScreen(name='washOptions'))
        globalSM.add_widget(AddBoardsScreen(name='boards_list'))
        globalSM.add_widget(ConfirmWashPage(name='confirmWashPage'))
        globalSM.add_widget(WasherScreenCountdown(name='washerScreenCountdown'))
        globalSM.add_widget(WasherAbortScreen(name="washerAbortScreen"))
        globalSM.add_widget(WasherCompleteScreen(name="washerCompleteScreen"))



        globalSM.transition = NoTransition()

        return globalSM

    def on_start(self):
        self.root.current = 'barcode'

if __name__ == "__main__":
    import traceback
    try:
        Runner().run()
    except Exception as e:
        traceback.print_exc()
    # Runner().run()
