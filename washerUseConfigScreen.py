from kivy.app import App
from kivy.uix.screenmanager import Screen
# from washerGlobals import GlobalScreenManager
# from kivymd.app import MDApp
from kivy.clock import Clock
from datetime import *
import wash_profiles as wp 
from washerGlobals import GSM

class WasherUseConfigScreen(Screen):
    #on_enter: root.data_log(DataDict) #add data dict with start time and other info
    def __init__(self, **kwargs):
        super(WasherUseConfigScreen, self).__init__(**kwargs)
        self.timeLimit = 0 ##
        self.timer = 0


    # def test_pump(self):
    #     #turn on pump
    #     RPI5_chip.set_gpio_output_value(PUMP_RELAY,"HIGH")
    #     for i in range(5):
    #         print(i+1)
    #         time.sleep(1)
    #     print("Test Done")
    #     RPI5_chip.set_gpio_output_value(PUMP_RELAY,"LOW")
    #     #turn off pump
        
    # def configMenuButton(self):
    #     gsm = GSM()
    #     gsm.current = "barcode"





    # <UseConfigScreen>:
    # name: "useConfig"
    # Button:
    #     text: "Test Pump"
    #     font_size: '20pt'
    #     background_color: [1,0,0,1]
    #     size_hint: (0.5, 0.1)
    #     pos_hint: {'center_x':0.5, 'center_y':0.5}
    #     on_release: 
    #         root.test_pump()
    # Button:
    #     text: "Back"
    #     font_size: '20pt'
    #     background_color: [1,0,0,1]
    #     size_hint: (1.5, 0.1)
    #     pos_hint: {'center_x':0.5, 'top':1.0}
    #     on_release: 
    #         app.root.current = 'main'
    #         #root.manager.transition.direction = "down"