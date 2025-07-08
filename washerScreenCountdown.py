from kivy.app import App
from kivy.uix.screenmanager import Screen
# from washerGlobals import GlobalScreenManager
# from kivymd.app import MDApp
from kivy.clock import Clock
from datetime import *
import wash_profiles as wp 
from washerGlobals import GSM

class WasherScreenCountdown(Screen):
    #on_enter: root.data_log(DataDict) #add data dict with start time and other info
    def __init__(self, **kwargs):
        super(WasherScreenCountdown, self).__init__(**kwargs)
        self.timeLimit = 0 ##
        self.timer = 0

        




    def on_enter(self, *args):
        gsm = GSM()
        gsm.DataDict['Aborted'] = 'False'

        # IMMEDIATELY UPON ENTERING THE COUNTDOWN SCREEN WE START THE TIMER!
        self.ids.washTypeLabel.text = "Chosen Profile: " + str(gsm.washType)
        self.timeLimit = wp.WashProfiles[gsm.DataDict['Wash_Type']] # + 1
        # gsm.DataDict["Start_Time"] = datetime.now()

        # self.update_time()
        self.timer = Clock.schedule_interval(self.update_time, 1)
        
        #immediately show the "highest" number in the countdown.
        minutes, seconds = divmod(self.timeLimit,60)
        self.ids.washTime.text = "{:02d}:{:02d}".format(int(minutes), int(seconds))

        # save the DataDict's start time to NOW. Also save the date if you haven't already.
        gsm.DataDict["Start_Time"] = datetime.now().strftime("%H"+":%M"+":%S")
        gsm.DataDict["Date"] = datetime.now().strftime("%m-%d-%Y")


    def update_time(self, *args):
        gsm = GSM()
        if self.timeLimit > 0:
            self.timeLimit -= 1
        else:
            gsm.DataDict["End_Time"] = datetime.now().strftime("%H"+":%M"+":%S") # ////////////////////////////////////////////////
            self.timer.cancel()
            self.timer = 0
            gsm.current = 'washerCompleteScreen'
            print("DONE")
            #go to finish screen
            
        minutes, seconds = divmod(self.timeLimit,60)
        self.ids.washTime.text = "{:02d}:{:02d}".format(int(minutes), int(seconds))



    def on_leave(self, *args):
        self.ids.washTime.text = " "
        # return super().on_leave(*args)

    def abortPressed(self):
        print("ABORT PRESSED!")
        gsm = GSM()

        # KILL THE TIMER WHEN ABORTED
        if hasattr(self, 'timer') and self.timer:
            self.timer.cancel()
            self.timer = 0

        gsm.DataDict['Aborted'] = 'True'
        gsm.DataDict["End_Time"] = datetime.now().strftime("%H"+":%M"+":%S")
        gsm.current = "washerAbortScreen"


    # name: "washerScreenCountdown"
    # on_enter: 
    #     root.start_timer()
    # BoxLayout:
    #     orientation: 'vertical'
    #     Label:
    #         text: "Chosen Profile: " + root.washType
    #         font_size: '20pt'
    #         background_color: [1,0,0,1]
    #         pos_hint: {'center_x':0.5, 'center_y':0.5}
            
    #     #Timer showing wash type and time remaining as per profile
    #     Label:
    #         id: washTime
    #         font_size: 40
    #         markup: True
    #         text: '00:00'
    #     Button:
    #         text: "Start Timer"
    #         font_size: '20pt'
    #         background_color: [1,0,0,1]
    #         size_hint: (1.0, 0.1)
    #         #pos_hint: {'center_x':0.5, 'bottom':0.0}
    #         on_release: 
    #             root.start_timer()
    #     Button:
    #         text: "Abort"
    #         font_size: '20pt'
    #         background_color: [1,0,0,1]
    #         size_hint: (1.0, 0.1)
    #         pos_hint: {'center_x':0.5, 'bottom':0.0}
    #         on_release: 
    #             root.DataDict['Aborted'] = 'true'
    #             app.root.current = 'abortScreen'
    #             #root.manager.transition.direction = "right"
    
    # def on_enter(self):
        # Force layout update to fix MDTextField underline issue
        # self.start_timer()
        # self.update_layout()
        

