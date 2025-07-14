#11-21-24: have pressure sensor working with GUI, but can't get GUI to close properly, need to add exception in while loop
#04/24/2025: Starting project back up. First action is to switch from RPI.GPIO to gpiod.
#04/30/2025: got gpiod working, starting to integrate that test code into this release
#05/15/2025: removed individual classes for each screen, was confusing and made variable sharing extremely cumbersome
# now all screens are made within a single class with arg ScreenManager
#5/28/2025: fixed a lot of little things to be more smooth and professional
import libgpiod_RPI5_manager as gpio_manager
import kivy
kivy.require('2.3.0')
from kivy.app import App
from kivy.core.window import Window
from kivy.config import Config
#from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.properties import *
import wash_profiles as wp
from rpi_lcd import LCD
from datetime import datetime
from threading import Thread
import gpiod
from gpiod.line import Direction, Value, Bias, Edge
import time, sys, os
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
#import pandas as pd
import pymssql
import keyboard

#set up SPI comms to MCP Hat (ADC chip for pressure sensor)
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
chan = AnalogIn(mcp, MCP.P0)

#Create object for LCD I2C device
lcd = LCD()

#Variables
chip_path = "/dev/gpiochip0"

#GPIO Pin Variables
FLOW_SENSOR_H20 = 27
#FLOW_SENSOR_SOL =  
PUMP_RELAY = 16
#VALVE_RELAY = 17
#DEPTH = 

background_task = 1
count = 0
flowCalFac = 38 # 
vdd = 3.3
size = 4096
chipDiff = 1024/65536  # lib returns 16b number (65536) and chip returns 1024 number, so result is scaled by 1024/65536
d2Mpa = 0.101325/620.6061 #calibration for converting ADC output to a pressure value, max pressure over max analog voltge (estimate, needs testing)

raw_config_dict = {
    #FLOW_SENSOR_H20: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE),
    PUMP_RELAY: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE),
    #16: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE),
    #11: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE),
    #29: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE),
    #13: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE),
    #40: gpiod.LineSettings(direction=Direction.INPUT, bias=Bias.PULL_DOWN),
    #38: gpiod.LineSettings(direction=Direction.INPUT, bias=Bias.PULL_DOWN) 
    }

# RPI5_chips inherits the RPI5_GPIO_Manager class
RPI5_chip = gpio_manager.RPI5_GPIO_Manager(chip_path, raw_config_dict)

#Config.set('graphics', 'width', '1024')
#Config.set('graphics', 'height', '600')
#Config.write()

#Function to detect edge and process a counter, to be set to a thread
def watch_line_falling():
    global chip_path
    global FLOW_SENSOR_H20
    global count
    #add a while loop that then does a wait_edge_events for 0.1sec as a threaded task so that the while keeps checking instead of the edge check
    request = gpiod.request_lines(chip_path,consumer="watch-line-falling",config={FLOW_SENSOR_H20: gpiod.LineSettings(edge_detection=Edge.FALLING)})
    while True:
        for event in request.read_edge_events():
            #print("hit # {}:".format(event.line_seqno))
            count = count + 1

def flow_press():
    """
    Get Pressure
    This function takes the live data from data input objects and
    displays them to the LCD object
    Returns: none
    """
    global background_task
    global count
    while background_task:
        try:
            #Get Water Flow Rate
            time.sleep(.5) #wait half a seond to accumulate edges in countPulse function (another half below)
            """
            Flow calc:
            Freq = 38*Q +-3% (Q = L/min, aka "flow")
            flow = freq/38
            freq = count/1sec
            may need to update this delay or function if this is pulled out on its own
            """
            flow = (count / flowCalFac) #use snapshot of pulse count to determine 
            flowString = "H2O F: %.3f L/min" % (flow)
            lcd.text(flowString,1)
            count = 0

            #Get Water Pressure
            rawADC = chan.value*chipDiff
            adcVolt = chan.voltage*0.25
            pressOut = rawADC*d2Mpa
            pressString = "H2O P: %.3f MPa" % (pressOut)
            voltString = "H2O V: %.3f V" % (adcVolt)
            lcd.text(pressString,2)
            #print('Raw ADC Value: ',chan.value)
            #print('ADC Voltage: ' + str(chan.voltage) + 'V')
            time.sleep(0.5)
        except KeyboardInterrupt:
            print('\ncaught keyboard interrupt!, bye')
            #GPIO.cleanup()
            sys.exit()

def start_threads():
    #This function creates a thread for the LCD-populating function to
    #run in parallel to the rest of the system
    #Returns: none
    monitor_thread = Thread(target=watch_line_falling)
    monitor_thread.daemon = True # Allow thread to be killed when the main program exits
    
    lcd_thread = Thread(target=flow_press)
    lcd_thread.daemon = True
    
    monitor_thread.start()
    lcd_thread.start()

def return_profile(self):
    chosen_profile = self.root.get_screen('UseWasher').ids.profile_btn.text
    return chosen_profile

class WasherMenu(ScreenManager):
    sn_msg = StringProperty("CCA SN")
    pn_msg = StringProperty("CCA PN")
    #sess = ObjectProperty(None)
    sessID = StringProperty("")
    userID = StringProperty("")
    badID = BooleanProperty(True)
    washType = StringProperty("")
    boardCount = NumericProperty(0)
    boardScrnList = ListProperty([
        "pn1_in",
        "pn2_in",
        "pn3_in",
        "pn4_in",
        "pn5_in",
        "pn6_in",
        "pn7_in",
        "pn8_in",
        "pn9_in",
        "pn10_in",
        "sn1_in",
        "sn2_in",
        "sn3_in",
        "sn4_in",
        "sn5_in",
        "sn6_in",
        "sn7_in",
        "sn8_in",
        "sn9_in",
        "sn10_in"])
    DataDict = DictProperty({
        "Washer_ID":"WSH1001",
        "Session_ID":0,
        "User_ID":"null",
        "Wash_Type":"null",
        "CCA_Count":0,
        "PN1":"null",
        "PN2":"null",
        "PN3":"null",
        "PN4":"null",
        "PN5":"null",
        "PN6":"null",
        "PN7":"null",
        "PN8":"null",
        "PN9":"null",
        "PN10":"null",
        "SN1":"null",
        "SN2":"null",
        "SN3":"null",
        "SN4":"null",
        "SN5":"null",
        "SN6":"null",
        "SN7":"null",
        "SN8":"null",
        "SN9":"null",
        "SN10":"null",
        "Start_Time":'12:00:00',
        "End_Time":'12:00:00',
        "Aborted":'false',
        "Date":datetime.now().strftime("01-01-2000")
        })
        
    def __init__(self, **kwargs):
        super(WasherMenu, self).__init__(**kwargs)
        Window.bind(on_request_close=self.end_func)
        for key in wp.WashProfiles:
            new_button = ToggleButton(
                text = key,
                group='branch',
                on_press=self.radio_click)
            self.ids.wt_buttons.add_widget(new_button)
        #for i in range(10):    #create 10 rows
        #    self.create_cca_row(i) #create the first row in the board input screen
    def end_func(self, *args):
        global background_task
        background_task = 0
        if Thread(target = flow_press).is_alive():
            Thread(target = flow_press).join()
        if Thread(target=watch_line_falling).is_alive():
            Thread(target=watch_line_falling).join()
        App.stop
        Window.close() 
                
    button_font = 22
    sw_seconds = 0
    sw_started = False
    global PUMP_RELAY
    def new_sess(self): #create new session
        newSessID = self.userID + datetime.now().strftime("%H%M%m%d%Y")
        self.DataDict["Session_ID"] = newSessID
        return newSessID

    def test_pump(self):
        #turn on pump
        RPI5_chip.set_gpio_output_value(PUMP_RELAY,"HIGH")
        for i in range(5):
            print(i+1)
            time.sleep(1)
        print("Test Done")
        RPI5_chip.set_gpio_output_value(PUMP_RELAY,"LOW")
        #turn off pump
        
    def user_id_store(self, *args):
        self.userID = self.DataDict[args[0]] = self.ids[args[1]].text
        if len(self.userID) < 1:
            self.userID = "null" #allows indexing if name cleared (no indext for len = 0)
        if self.userID[0] == 'U' and len(self.userID) == 7:
            with open('emp_name.txt','r') as f:
                for line in f:
                    if self.userID in line.strip('\n').split(',')[0:1]: #if input id matches current line of file
                        self.badID = False
                        self.empName = line.strip('\n').split(',')[1]
                        #python to move to wash screen
                        self.current = 'washOptions'
                        break
                    else:
                        self.ids["user_id_in"].text = ""
                        #self.ids["user_id_in"].focus = True
                        self.ids[args[2]].text = "User not found. Try again"
        else:
            self.badID = True
            self.ids["user_id_in"].text = ""
            self.ids["user_id_in"].focus = True
            self.ids[args[2]].text = "Invalid ID. Try again."
    
    def user_clear(self):
        self.DataDict["User_ID_In"] = 'null'
        self.ids["user_id_in"].text = ""
        self.userID = ''
        self.ids["user_id_label"].text = "Scan Employee ID (U-number)"
    
    def pn_store(self):
        self.partNum = self.DataDict["Part_Number"] = self.ids["pn_in"].text

    def sn_row_store(self, *args):
        listnumstr = str(args[0].listnum)
        combinedString = self.ids["pn"+ listnumstr +"_in"].text
        #code to verify the pn/sn data
        if len(combinedString) != 19 and combinedString[6] != '-':
            #popup with "Invalid Barcode" that last for 3 seconds then disappears, clears the text and resets the focus
            pass
        else:
            pn = combinedString.split("/")[0]
            rev = combinedString.split("/")[1] #may never use
            sn = combinedString.split("/")[2]
            self.ids["pn"+ listnumstr +"_in"].text = self.DataDict["PN" + listnumstr] = pn
            self.ids["sn"+ listnumstr +"_in"].text = self.DataDict["SN" + listnumstr] = sn
        
        
    def sn_row_clear(self, *args):
        listnumstr = str(args[0].listnum)
        self.DataDict["SN" + listnumstr] = 'null'
        self.ids["sn"+ listnumstr +"_in"].text = ""
        self.DataDict["PN" + listnumstr] = 'null'
        self.ids["pn"+ listnumstr +"_in"].text = ""
        
    def board_all_clear(self):
        for i in range(1,11):
            self.DataDict["SN" + str(i)] = 'null'
            self.ids["sn"+ str(i) +"_in"].text = ""
            self.DataDict["PN" + str(i)] = 'null'
            self.ids["pn"+ str(i) +"_in"].text = ""
    
    def create_session_id(self):
        self.DataDict["Session_ID"] = self.DataDict["User_ID"] + datetime.now().strftime("%m%d%Y%H%M")
    
    def update_cca_count(self):
        self.DataDict["CCA_Count"] = 0
        for key, value in self.DataDict.items():
            if str(key)[:2] == "SN" and str(value) !="null":
                self.DataDict["CCA_Count"] += 1
        self.boardCount = self.DataDict["CCA_Count"]
        #print(self.boardCount)
            
    def sn_list_store(self):
        #Improve: Check for file size and create new file (move old?) when too big
        file = open("Washer_Log_SNs.txt", "a")
        file.write(','.join(map(str,self.DataDict.values()))+"\n")
        file.close()
    
    def set_focus(self,textId):
        if len(self.ids[textId].text) == 0:
            self.ids[textId].focus = True
        else:
            for i in range(len(self.boardScrnList)):
                if len(self.ids[self.boardScrnList[i]].text) == 0:
                    self.ids[self.boardScrnList[i]].focus = True
                    break
    
    def radio_click(self, *args):
        newTypeText = args[0].text
        if newTypeText != self.DataDict['Wash_Type']:            
            self.ids.chosenOptn.text = newTypeText
            self.DataDict["Wash_Type"] = newTypeText
            self.washType = self.DataDict["Wash_Type"]
            self.current = 'boardInput'
        else:
            self.ids.chosenOptn.text = "Choose A Profile"
            self.DataDict["Wash_Type"] = ""
            self.washType = "" 
         
    def wt_button_build(self):
        for key in wp.WashProfiles:
            new_button = ToggleButton(
                text = key,
                group='branch',
                on_press=self.radio_click)
            self.ids.wt_buttons.add_widget(new_button)
            
    def start_timer(self):
        self.timeLimit = wp.WashProfiles[self.DataDict['Wash_Type']] + 1
        self.DataDict["Start_Time"] = datetime.now().strftime("%H"+":%M"+":%S")
        self.timer = Clock.schedule_interval(self.update_time, 1)
    
    def update_time(self, *args):
        if self.timeLimit > 0:
            self.timeLimit -= 1
        else:
            self.timer.cancel()
            self.current = 'completeScreen'
            #go to finish screen
            
        minutes, seconds = divmod(self.timeLimit,60)
        self.ids.washTime.text = "{:02d}:{:02d}".format(int(minutes), int(seconds))
    
    def full_reset(self):
        self.sessID = ""
        self.userID = ""
        self.badID = True
        self.washType = ""
        self.partNum = ""
        self.boardCount = 0
        self.DataDict ={
            "Washer_ID":"WSH1001",
            "Session_ID":0,
            "User_ID":"null",
            "Wash_Type":"null",
            "CCA_Count":0,
            "PN1":"null",
            "PN2":"null",
            "PN3":"null",
            "PN4":"null",
            "PN5":"null",
            "PN6":"null",
            "PN7":"null",
            "PN8":"null",
            "PN9":"null",
            "PN10":"null",
            "SN1":"null",
            "SN2":"null",
            "SN3":"null",
            "SN4":"null",
            "SN5":"null",
            "SN6":"null",
            "SN7":"null",
            "SN8":"null",
            "SN9":"null",
            "SN10":"null",
            "Start_Time":'12:00:00',
            "End_Time":'12:00:00',
            "Aborted":"false",
            "Date":datetime.now().strftime("01-01-2000")
            }
    def data_log(self,Data):
        file = open("Washer_Log.txt", "w")
        file.write(','.join(map(str,Data.values())))
        file.close()
        
        data = []
        
        #is this used?
        with open('Washer_Log.txt' ,'r') as file:
            for line in file:
                data.append(line.strip().split(','))
                
        conn = pymssql.connect(server='USW-SQL30003.rootforest.com',
                               user='OvenBakedUsr',
                               password='aztmvcjfrizkcpdcehky',
                               database='Oven_Bake_Log',
                               )
        cursor = conn.cursor()
        
        #Date/Time is wrong on the IOT network
        self.DataDict["Date"] = datetime.now().strftime("%m"+"-%d"+"-%Y")
        self.DataDict["End_Time"] = datetime.now().strftime("%H"+":%M"+":%S")
        
        executeStr = "'" +"','".join(map(str,self.DataDict.values())) + "'"
        cursor.execute("INSERT INTO Wash_Log VALUES (" + executeStr + ")")
        conn.commit()
        cursor.close()
        conn.close()
        
    pass
    
#Class to build GUI App
class Main(App):
    title = 'Washer Log'
    def build(self):
        #Window.fullscreen = True
        Builder.load_file('washer_gui.kv')
        return WasherMenu()

if __name__ == '__main__':
    start_threads()
    Main().run()
