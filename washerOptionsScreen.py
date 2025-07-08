from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivymd.uix.button import *
from kivy.properties import *

from washerGlobals import GSM
import wash_profiles as wp


class WashOptionsScreen(Screen):
    def __init__(self, **kwargs):
        super(WashOptionsScreen, self).__init__(**kwargs)
        self.wt_button_build()

    
    def on_enter(self):
        gsm = GSM()
        print("Entering WashOptionsScreen") # , userID: " + gsm.userID)

        self.ids.chosenOptn.text = "Choose A Profile"
        gsm.DataDict["Wash_Type"] = ""
        gsm.washType = ""


    def radio_click(self, *args):
        gsm = GSM()
        print("Before setting washType, userID: " + gsm.userID)

        newTypeText = args[0].text
        if newTypeText != gsm.DataDict['Wash_Type']:
            self.ids.chosenOptn.text = newTypeText
            gsm.DataDict["Wash_Type"] = newTypeText
            gsm.washType = newTypeText

            print("After setting washType, userID: " + gsm.userID)

            # go to boards list upon clicking one of the washType options.
            gsm.current = 'boards_list'
            # if navigating to the boards list for the first time, ALL information regarding boards should be CLEARED:
            gsm.PN_BackingList = []
            gsm.SN_BackingList = []
            gsm.DataDict["PN_SN_String"] = ""
            # access the add_boards screen and clear the widgets before entering it.
            temporary_boards_list = gsm.get_screen("boards_list")
            temporary_boards_list.clearAllButton() # call my local function
        else:
            self.ids.chosenOptn.text = "Choose A Profile"
            gsm.DataDict["Wash_Type"] = ""
            gsm.washType = ""


    def wt_button_build(self):
        # to be called on Screen init, not just screen enter (too late)
        for key in wp.WashProfiles:
            new_button = Button(
                text=key,
                font_size=12,
                font_name="NexaHeavy",
                background_color=(0.5, 0.5, 0.5, 1),
                border=(20, 20, 20, 20),
                on_release=self.radio_click
            )
            self.ids.wt_buttons.add_widget(new_button)

    def washOptionsclickBackButton(self):
        # going back to barcode screen nulifies my userID.
        gsm = GSM()
        gsm.DataDict["User_ID"] = 'null'
        gsm.userID = ''
        gsm.current = 'barcode'
