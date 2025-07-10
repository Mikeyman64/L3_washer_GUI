from kivy.app import App
from kivy.uix.screenmanager import Screen
# from washerGlobals import GlobalScreenManager
# from kivymd.app import MDApp
from kivy.clock import Clock
from datetime import *
from washerGlobals import GSM


class ConfirmWashPage(Screen):
    
    def on_enter(self):
        self.assignDataToText()
        # self.update_layout()
        
    def assignDataToText(self):
        # set SessionID:

        
        gsm = GSM()
        self.ids.sessionID_label.text = "Session ID: " + str(self.new_sess())
        # set userID:
        self.ids.userID_label.text = "User ID: " + str(gsm.userID)
        # set profileWashType:
        self.ids.profile_label.text = "Chosen Profile: " + str(gsm.washType)
        # set CCACount:
        self.ids.CCACount_label.text = "CCA Count: " + str(gsm.boardCount)


    def new_sess(self): #create new session
        gsm = GSM()
        newSessID = gsm.userID + datetime.now().strftime("%H%M%m%d%Y")
        gsm.DataDict["Session_ID"] = newSessID
        return newSessID
    
    # def create_session_id(self):
    #     gsm = GSM()
    #     gsm.DataDict["Session_ID"] = gsm.DataDict["User_ID"] + datetime.now().strftime("%m%d%Y%H%M")
    








    def backButtonClicked(self):
        gsm = GSM()
        gsm.current = "boards_list"

    def washButtonClicked(self):
        gsm = GSM()
        #start timer here
        # self.create_session_id()
        # self.new_sess()

        #debug: print all info:
        # for elem in gsm.DataDict.keys():
        #     print(str(elem) + ": " + str(gsm.DataDict[elem]))


        # print(" WASH TYPE SAVED: ===================" + gsm.washType)
        gsm.current = 'washerScreenCountdown'

