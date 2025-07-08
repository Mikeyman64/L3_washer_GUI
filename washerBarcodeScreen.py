# from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from washerGlobals import GSM


class BarcodeScreen(Screen):

    def on_enter(self):
        # Force layout update to fix MDTextField underline issue
        Clock.schedule_once(self.safe_user_clear, 0.01)
        Clock.schedule_once(self.update_layout, 0.01) # focus the barcode textfield to avoid having to click into it


    def update_layout(self, dt):
        self.ids.user_id_in.focus = True


    def safe_user_clear(self, dt):
        gsm = GSM()
        gsm.DataDict["User_ID"] = 'null'
        gsm.userID = ''
        gsm.empName = ""
        gsm.badID = True

        self.ids["user_id_in"].text = ""
        self.ids["user_id_label"].text = "Scan Employee ID (U-number)"
        self.ids.user_id_in.focus = True



    def goToWashOptions(self):
        gsm = GSM()
        gsm.current = 'washOptions'

    def user_id_store(self, *args):
        gsm = GSM()

        scanned_text = self.ids[args[1]].text
        gsm.userID = gsm.DataDict[args[0]] = scanned_text

        if len(gsm.userID) < 1:
            gsm.userID = "null"

        # regex to check if the barcode scanned is a U-number

        if gsm.userID[0] == 'U' and len(gsm.userID) == 7:
            found = False
            with open('emp_name.txt', 'r') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if gsm.userID == parts[0]:
                        gsm.badID = False
                        gsm.empName = parts[1]
                        gsm.DataDict["User_ID"] = gsm.userID

                        #if found User based on valid U-Number, move to next screen.
                        print(f"[OK] Found user {gsm.userID}, emp name: {gsm.empName}")
                        self.ids[args[2]].text = f"Welcome, {gsm.empName}!"
                        Clock.schedule_once(lambda dt: self.goToWashOptions(), 1)
                        found = True
                        break

            if not found:
                print(f"[ERROR] User ID {gsm.userID} not found in emp_name.txt")
                self.ids[args[2]].text = "User not found. Try again"
                Clock.schedule_once(self.safe_user_clear, 2)

        else:
            print(f"[ERROR] Invalid format for scanned ID: {gsm.userID}")
            gsm.badID = True
            self.ids[args[2]].text = "Invalid ID. Try again"
            Clock.schedule_once(self.safe_user_clear, 2)

