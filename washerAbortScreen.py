from kivy.app import App
from kivy.uix.screenmanager import Screen
from washerGlobals import GlobalScreenManager
# from kivymd.app import MDApp
from kivy.clock import Clock
from datetime import *
import wash_profiles as wp 
from washerGlobals import GSM
# import pymssql # OUTDATED
import pyodbc

class WasherAbortScreen(Screen):
    #on_enter: root.data_log(DataDict) #add data dict with start time and other info
    def __init__(self, **kwargs):
        super(WasherAbortScreen, self).__init__(**kwargs)
        self.timeLimit = 0 ##
        self.timer = 0
        self.countdown = 5

    def on_enter(self):
        # self.data_log(gsm.DataDict)
        Clock.schedule_once(self.data_log, 1)
        self.timer = Clock.schedule_interval(self.update_countdown, 1)
        self.ids.returnToMenuTimer.text = str(self.countdown)

    def update_countdown(self, dt):
        if self.countdown > 0:
            self.countdown -= 1
        else: # done:
            self.timer.cancel()
            self.timer = 0
            self.countdown = 5
            self.manager.current = "barcode"
        self.ids.returnToMenuTimer.text = str(self.countdown)

    def compact_PN_SN_string(self, pn_array, sn_array): # return a STRING that combines the  PN and SN's into one string: "1234-4,1234-5,1234-6/SN2001,SN2002,SN2003"
        pn_part = ",".join(pn_array)
        sn_part = ",".join(sn_array)
        return f"{pn_part}/{sn_part}"
    

    def data_log(self,dt=None):
        gsm = GSM()


        file = open("Washer_Log.txt", "w")
        file.write(','.join(map(str,gsm.DataDict.values())))
        file.close()
        
        # combine all PN and SN values into one single string:
        compact_string = self.compact_PN_SN_string(
            gsm.PN_BackingList,
            gsm.SN_BackingList
        )
        gsm.DataDict["PN_SN_String"] = compact_string # assign string to empty DataDict value.

        # Convert values to tuple
        values = tuple(gsm.DataDict.values())

        # Create parameter placeholders matching the number of columns
        placeholders = ','.join(['?'] * len(values))
        


        conn = None
        cursor = None

        try:
            conn = pyodbc.connect(
                'DrsoRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=USW-SQL30003.rootforest.com;'
                'DATABASE=Oven_Bake_Log;'
                'UID=OvenBakedUsr;'
                'PWD=aztmvcjfrizkcpdcehky;'
                'TrustServerCertificate=yes;'
            )
            cursor = conn.cur()

            query = f"INSERT INTO Wash_Log VALUES ({placeholders})"


            print("\nVALUES BEING SENT TO SQL:\n")
            for i, val in enumerate(values):
                print(f"  [{i+1}] {val} ({type(val)})")


            cursor.execute(query, values)
            conn.commit()

        except pyodbc.Error as e:
            print("Database Error:", e)

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


        # clean up everything, after SQL database has been written to.
        self.board_all_clear()

        # DONE, 5 sec delay should take the user back to "barcode"


    def board_all_clear(self):
        gsm = GSM()
        gsm.DataDict["User_ID"] = 'null'
        gsm.userID = ''
        gsm.PN_BackingList = []
        gsm.SN_BackingList = []
        gsm.DataDict["PN_SN_String"] = ""
        gsm.DataDict["CCA_Count"] = 0
