from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.screenmanager import Screen
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
from kivy.clock import Clock
from kivy.properties import *
from kivy.core.window import Window
from kivymd.uix.textfield import MDTextField

from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDButton, MDButtonText


from washerGlobals import GSM
# from kivymd.app import MDApp
from kivy.clock import Clock


class AddBoardsScreen(Screen):
    def __init__(self, **kwargs):
        super(AddBoardsScreen, self).__init__(**kwargs)
        self.entry_count = 0
        

    def on_enter(self):
        gsm = GSM()
        print("Entered AddBoards Screen") #, userID: " + gsm.userID)
        self.ids.wash_type_board.text = gsm.washType # Save the type of wash type previously selected to the text next to heading

    def add_item(self, pn, sn):
        self.entry_count += 1
        new_entry = CCAEntry(
            index=self.entry_count,
            pn=pn,
            sn=sn,
            remove_callback=self.remove_item
        )
        self.ids.list_layout.add_widget(new_entry)
        self.store_entry(self.entry_count, pn, sn)
        Clock.schedule_once(self.set_focus, 0.1)  # Schedule focus after layout update

    def set_focus(self, dt):
        self.ids.item_input.focus = True

    def remove_item(self, index):
        self.entry_count -= 1
        for entry in self.ids.list_layout.children:
            if entry.index == index:
                self.ids.list_layout.remove_widget(entry)
                break
        self.clear_entry(index)
        self.ids.item_input.focus = True

    def store_entry(self, index, pn, sn):
        gsm = GSM()
        if len(gsm.PN_BackingList) < index:
            gsm.PN_BackingList.append(pn)
            gsm.SN_BackingList.append(sn)
        else:
            gsm.PN_BackingList[index - 1] = pn
            gsm.SN_BackingList[index - 1] = sn

    def clear_entry(self, index):
        gsm = GSM()
        

        if len(gsm.PN_BackingList) >= index:
            del gsm.PN_BackingList[index - 1]
            del gsm.SN_BackingList[index - 1]
        for i, entry in enumerate(self.ids.list_layout.children):
            entry.index = len(self.ids.list_layout.children) - i

    def parse_and_add_item(self, text):
        if len(text) != 19 or text[6] != '-':
            self.ids.item_input.text = ""
            self.ids.item_input.hint_text = "Invalid Barcode"
            Clock.schedule_once(self.reset_hint_text, 2)
        else:
            pn, rev, sn = text.split("/")
            self.add_item(pn, sn)
            self.ids.item_input.text = ""

    def reset_hint_text(self, dt):
        self.ids.item_input.hint_text = "Enter CCA Full Number"
        Clock.schedule_once(self.set_focus, 0.1)

    def backButtonClicked(self):
        gsm = GSM()
        self.clearAllButton() # Call functionality of clearing all board-related information.
        print("Back button clicked, clear all called.")
        gsm.current = "washOptions"

    def clearAllButton(self):
        gsm = GSM()
        print("Clear All Boards Called")
        self.ids.list_layout.clear_widgets()
        gsm.PN_BackingList.clear()
        gsm.SN_BackingList.clear()
        gsm.DataDict["PN_SN_String"] = "" # just in case this is still populated, clear it.
        self.entry_count = 0
        gsm.DataDict["CCA_Count"] = 0
        self.ids.item_input.focus = True

    def printArrays(self):
        gsm = GSM()
        print("PNs: " + str(gsm.PN_BackingList))
        print("SNs: " + str(gsm.SN_BackingList))
        print("total entries: " + str(self.entry_count))
        self.ids.item_input.focus = True

    def confirmButtonClicked(self):
        gsm = GSM()
        gsm.DataDict["CCA_Count"] = self.entry_count
        gsm.boardCount = self.entry_count

        print("NUMBER OF BOARDS: " + str(gsm.DataDict["CCA_Count"]))
        gsm.current = "confirmWashPage"


class CCAEntry(BoxLayout):
    def __init__(self, index, pn, sn, remove_callback, **kwargs):
        super(CCAEntry, self).__init__(**kwargs)
        self.index = index  # Store the index in the arrays
        self.orientation = 'horizontal'
        self.spacing = 10
        self.size_hint_y = None
        self.height = '40dp'



        self.pn_input = MDTextField(
            text=pn,
            theme_font_name = "Custom",
            font_name = "C:/Users/U313773/Documents/WasherGUI/washer-venv/fonts/Nexa-Heavy.ttf",
            hint_text="CCA PN",
            readonly=True,
            height = 40,
            mode="outlined",  # gives rounded edges
            font_size=15
        )

            # Rounded TextInput
        self.sn_input = MDTextField(
            text=sn,
            theme_font_name = "Custom",
            font_name = "C:/Users/U313773/Documents/WasherGUI/washer-venv/fonts/Nexa-Heavy.ttf",
            hint_text="CCA SN",
            mode="outlined",  # 'filled' is another option
            # radius=[10, 10, 10, 10],
            height = 40,
            readonly=True,
            font_size=15
        )

        # Rounded Button (formerly MDRaisedButton)
        self.remove_button = MDButton(
            style="elevated",
            radius=[10, 10, 10, 10],
            height="40dp",
            width="40dp",
            size_hint=(None, None),
            theme_bg_color = "Custom",
            md_bg_color = [172/255,88/255,89/255,1]
        )
        self.remove_button_text = MDButtonText(text="X", theme_text_color="Custom",text_color = "white")
        self.remove_button.add_widget(self.remove_button_text)
        self.remove_button.bind(on_release=self.remove_entry)

        self.add_widget(self.pn_input)
        self.add_widget(self.sn_input)
        self.add_widget(self.remove_button)

        self.remove_callback = remove_callback

    def remove_entry(self, instance):
        self.remove_callback(self.index)