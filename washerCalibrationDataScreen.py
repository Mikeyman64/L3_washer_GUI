from kivy.app import App
from kivy.uix.screenmanager import Screen
# from washerGlobals import GlobalScreenManager
# from kivymd.app import MDApp
from kivy.clock import Clock
from datetime import *
from wash_profiles import WashProfilesWithNominals
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.factory import Factory
import random
from washerGlobals import GSM, GlobalScreenManager
# from sensor_reader import SensorReader  # Import the new class
import pyodbc
import os


class CalibrationDataPage(Screen):
    def __init__(self, **kwargs):
        super(CalibrationDataPage, self).__init__(**kwargs)
        self.timer = 0
        self.countdown = 30
        self.sensor_reader = None
        self.sensor_updater = None
        
        # conn = pyodbc.connect('calibrate_data.db')
        # cursor = conn.cursor()

        # cursor.execute('''
        #     CREATE TABLE IF NOT EXISTS users (
        #         uNum INTEGER PRIMARY KEY,
        #         empName TEXT,
        #         passcode INTEGER)
        #                ''')
        
        # # for i in range()
        
        # cursor.execute('''
        #     INSERT INTO users (uNum, empName, passcode)
        #     values (?,?,?) 
        # ''', ())

    def on_enter(self):
        self.timer = Clock.schedule_interval(self.update_countdown, 1)
        
        # self.sensor_reader = SensorReader()
        
        #self.sensor_updater = Clock.schedule_interval(self.update_sensor_labels, 0.5)
        
        
    def update_countdown(self, dt):
        if self.countdown > 0:
            self.countdown -= 1
        else: # done:
            '''
            self.timer.cancel()
            self.timer = 0
            self.countdown = 30
            '''
            self.manager.current = "barcode"

    def closeButtonClicked(self):
        '''
        self.timer.cancel()
        self.timer = 0
        self.countdown = 30
        '''
        gsm = GSM()
        gsm.current = "barcode"

    def newCalibButtonClicked(self):
        '''
        self.timer.cancel()
        self.timer = 0
        self.countdown = 30
        '''
        gsm = GSM()
        gsm.current = 'validateCalibUser'
        
        
        # ==========================================================
        # VALIDATE U-NUMBER + 4DIGIT CODE FIRST BEFORE GOING TO THIS PAGE!!!!!!!!

        # 
        #===========================================================
        
        
    
    def on_leave(self):
        if self.timer:
            self.timer.cancel()
            self.timer = 0
            self.countdown = 30
            
            '''
        if self.sensor_updater:
            self.sensor_updater.cancel()
        if self.sensor_reader:
            self.sensor_reader.stop()'''
            
            
    
    def update_sensor_labels(self, dt):
        data = self.sensor_reader.get_data()
        flow = data['flow']
        pressure = data['pressure']

        self.ids.flowrate_value.text = f"{flow:.3f} L/min"
        self.ids.pressure_value.text = f"{pressure:.3f} MPa"
    

    # def flow_press():
        # """
        # Get Pressure
        # This function takes the live data from data input objects and
        # displays them to the LCD object
        # Returns: none
        # """
        # global background_task
        # global count
        # while background_task:
        #     try:
        #         #Get Water Flow Rate
        #         time.sleep(.5) #wait half a seond to accumulate edges in countPulse function (another half below)
        #         """
        #         Flow calc:
        #         Freq = 38*Q +-3% (Q = L/min, aka "flow")
        #         flow = freq/38
        #         freq = count/1sec
        #         may need to update this delay or function if this is pulled out on its own
        #         """
        #         flow = (count / flowCalFac) #use snapshot of pulse count to determine 
        #         flowString = "H2O F: %.3f L/min" % (flow)
        #         lcd.text(flowString,1)
        #         count = 0

        #         #Get Water Pressure
        #         rawADC = chan.value*chipDiff
        #         adcVolt = chan.voltage*0.25
        #         pressOut = rawADC*d2Mpa
        #         pressString = "H2O P: %.3f MPa" % (pressOut)
        #         voltString = "H2O V: %.3f V" % (adcVolt)
        #         lcd.text(pressString,2)
        #         #print('Raw ADC Value: ',chan.value)
        #         #print('ADC Voltage: ' + str(chan.voltage) + 'V')
        #         time.sleep(0.5)
        #     except KeyboardInterrupt:
        #         print('\ncaught keyboard interrupt!, bye')
        #         #GPIO.cleanup()
        #         sys.exit()


class ValidateCalibUser(Screen):
    def __init__(self, **kwargs):
        super(ValidateCalibUser, self).__init__(**kwargs)
        
    def on_enter(self):
        # Clear fields
        self.safe_user_clear(0)
        # self.ids["login_pass_input"].text = ""
        # self.ids["login_user_input"].text = ""
        # self.ids["login_label"].text = "Enter ID and Passcode"
        # self.set_element_focus(self.ids.login_user_input)

    def set_element_focus(self, element):
        # element is a self.ids._____ object.
        element.focus = True

    def safe_user_clear(self, dt):
        self.set_element_focus(self.ids.login_user_input)
        self.ids["login_pass_input"].text = ""
        self.ids["login_user_input"].text = ""
        self.ids["login_label"].text = "Enter U-Number and Code"

    def check_credentials(self):
        user_input = self.ids.login_user_input.text.strip().upper()
        pass_input = self.ids.login_pass_input.text.strip()

        if len(user_input) != 7 or not user_input.startswith('U'):
            self.ids.login_label.text = "Invalid U-number format"
            Clock.schedule_once(self.safe_user_clear, 2)
            return

        if not pass_input.isdigit() or len(pass_input) != 4:
            self.ids.login_label.text = "Passcode must be 4 digits"
            Clock.schedule_once(self.safe_user_clear, 2)
            return

        # Validate against DB!
        user_map = GlobalScreenManager.CALIBRATION_USERS

        # Check existence
        if user_input not in user_map:
            self.ids.login_label.text = "User ID not found"
            print(f"[ERROR] User {user_input} not in CALIBRATION_USERS")
            Clock.schedule_once(self.safe_user_clear, 2)
            return
        
        # Strip whitespace from DB-stored code
        stored_code = user_map[user_input]
        # if stored_code is None:
        #     self.ids.login_label.text = "No code assigned to user"
        #     print(f"[WARN] No code for {user_input}")
        #     Clock.schedule_once(self.safe_user_clear, 2)
        #     return

        stored_code = stored_code.strip()


        if pass_input == stored_code:
            print(f"[OK] Auth success: {user_input}")
            # gsm = GSM()
            # gsm.userID = user_input
            # gsm.empName = "Unknown"  # You could also fetch/display full name if needed
            # gsm.DataDict["User_ID"] = user_input
            # gsm.badID = False

            self.ids.login_label.text = f"Welcome, {user_input}!"
            Clock.schedule_once(lambda dt: self.go_to_passed_page(), 2)
        else:
            print(f"[ERROR] Wrong passcode for {user_input}")
            self.ids.login_label.text = "Incorrect passcode"
            Clock.schedule_once(self.safe_user_clear, 2)


    def go_to_passed_page(self):
        gsm = GSM()
        gsm.current = 'newCalibPage'




# =================================================================================
class NewCalibrationPage(Screen):
    def __init__(self, **kwargs):
        super(NewCalibrationPage, self).__init__(**kwargs)
        self.checklist_items = [
            "Beaker Present?",
            "Turn Valves 1 & 2 to GREEN",
            "Turn Valves 3 & 4 to RED",
        ]
        self.current_index = 0
        self.checkboxes = []

    def on_pre_enter(self):
        # Clear previous checklist state
        self.ids.checklist_container.clear_widgets()

        # set the value of nominal wash based on wash_profile?
        self.ids.nominalValue.text = str(WashProfilesWithNominals["TEST"])
        # ================================================
        # SET TO THE VALUE OF THE EARLIER CONCENTRATION ! 
                # ================================================
        self.current_index = 0
        self.checkboxes = []

        # Hide GO button
        self.ids.go_button.opacity = 0
        self.ids.go_button.disabled = True

        # Start checklist over
        Clock.schedule_once(self.add_next_check, 0.1)

    def add_next_check(self, dt=None):
        if self.current_index >= len(self.checklist_items):
            self.update_go_button()
            return

        label_text = self.checklist_items[self.current_index]
        container = self.ids.checklist_container

        row = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp', spacing=10)
        row.add_widget(Label(text=label_text, font_name="NexaLight", font_size='20pt'))

        checkbox = CheckBox(size=(30,30))
        # checkbox = Factory.StyledCheckBox()
        checkbox.bind(active=self.on_checked)
        self.checkboxes.append(checkbox)
        row.add_widget(checkbox)

        container.add_widget(row)
        self.current_index += 1

    def on_checked(self, checkbox, value):
        if value:
            # If all checkboxes shown so far are checked, show next
            if checkbox == self.checkboxes[-1]:
                Clock.schedule_once(self.add_next_check, 0.1)
        self.update_go_button()

    def update_go_button(self):
        # GO button only visible if all visible checkboxes are checked
        if all(cb.active for cb in self.checkboxes) and len(self.checkboxes) == len(self.checklist_items):
            self.ids.go_button.opacity = 1
            self.ids.go_button.disabled = False
        else:
            self.ids.go_button.opacity = 0
            self.ids.go_button.disabled = True

    def cancelButtonClicked(self):
        gsm = GSM()
        gsm.current = "barcode"

    def newCalibGoClicked(self):
        gsm = GSM()
        gsm.current = 'fillBeakerPage'



# =======================================================================
class FillingBeakerPage(Screen):
    def __init__(self, **kwargs):
        super(FillingBeakerPage, self).__init__(**kwargs)
        self.timer = 0
        self.countdown = 2



    def on_enter(self):
        self.ids.waiting_gif.opacity = 0
        self.ids.waiting_gif.disabled = True
        # Get the list of all files in the sprites directory
        sprites_folder = "assets/calibrate_gifs"
        image_files = [f for f in os.listdir(sprites_folder) if os.path.isfile(os.path.join(sprites_folder, f))]
        
        # Randomly select one of the files
        if image_files:
            rand_source = random.choice(image_files)
            # self.ids.waiting_gif.
            gif_path = os.path.join(sprites_folder, rand_source)
            self.ids.waiting_gif.source = "gif_path"
    
            # Wait one frame before setting the GIF
            Clock.schedule_once(lambda dt: self.show_gif(gif_path), 0)
        else:
            print("No images found in the sprites folder.")

        # self.ids.waiting_gif.source = "sprites/rickroll.gif"

        # start timer
        self.timer = Clock.schedule_interval(self.update_countdown, 1)

        # DISPLAY A RUNNING LCD FEED FOR LIVE FLOW RATE AND LIVE WATER PRESSURE!!!!
    

    def show_gif(self, gif_path):
        self.ids.waiting_gif.opacity = 1
        self.ids.waiting_gif.disabled = False
        self.ids.waiting_gif.source = gif_path
    
    def update_countdown(self, dt):
        if self.countdown > 0:
            self.countdown -= 1
        else: # done:
            self.timer.cancel()
            self.timer = 0
            self.countdown = 2
            gsm = GSM()
            gsm.current = 'testConcPage'

# =====================================================

class TestConcentrationPage(Screen):
    def __init__(self, **kwargs):
        super(TestConcentrationPage, self).__init__(**kwargs)
        self.updating_text = False

    def on_enter(self):
        # Force layout update to fix MDTextField underline issue
        self.ids.inputConcentration.text = ""
        Clock.schedule_once(self.clear_concentration, 0.01)
        Clock.schedule_once(self.refocus_input_field, 0.01) # focus the barcode textfield to avoid having to click into it

    def refocus_input_field(self, dt):
        self.ids.inputConcentration.focus = True

    def clear_concentration(self, dt):
        gsm = GSM()
        gsm.inputConcentration = 0
        self.ids["newConcentration_label"].text = "Current Measured Concentration:"


    def save_concentration(self, *args):

        if not self.ids[args[0]].text.strip():  # Check if the input is empty or contains only whitespace
            self.ids["newConcentration_label"].text = "Concentration cannot be empty!"
            Clock.schedule_once(self.clear_concentration, 2)
            self.refocus_input_field(0.01)
            return
        
        input_val = float(self.ids[args[0]].text) * 0.01

        gsm = GSM()
        gsm.CalibrateDict["inputConcentration"] = input_val
        print(f"Your concentration is {gsm.CalibrateDict["inputConcentration"]}")
        gsm.current = "adjustRatePage"

    def cancelButtonClicked(self):
        gsm = GSM()
        gsm.inputConcentration = 0
        gsm.current = "barcode"

    # def confirmConcClicked(self):
    #     gsm = GSM()
    #     print
        # gsm.current = 'fillBeakerPage'


class AdjustRatePage(Screen):
    def __init__(self, **kwargs):
        super(AdjustRatePage, self).__init__(**kwargs)
        self.timer = 0
        self.countdown = 3

    def on_enter(self):
        gsm = GSM()
        self.ids["desired_conc_label"].text = f"Desired concentration: {gsm.CalibrateDict["inputConcentration"]}"
        self.ids["adjust_valves_label"].text = "Turn valve until flow rate = XX, pressure = YY."
    
    def update_countdown(self, dt):
        if self.countdown > 0:
            self.countdown -= 1
        else: # done:
            self.timer.cancel()
            self.set_all_buttons_disabled(False)
            self.timer = 0
            self.countdown = 3
            self.ids.fill_beaker_button.text = "Fill Beaker (Water)"
            return
        self.ids.fill_beaker_button.text = str(self.countdown)

    def set_all_buttons_disabled(self, disabled):
        for widget in self.walk():
            if isinstance(widget, Button):
                widget.disabled = disabled

    def fillBeakerButton(self):
        print ("Filling BEAKER FOR 10 SECONDS (JUST WATER)")
        self.set_all_buttons_disabled(True) # disable all buttons.
        self.timer = Clock.schedule_interval(self.update_countdown, 1)
        self.ids.fill_beaker_button.text = str(self.countdown)

    # def cancelButtonClicked(self):
    #     gsm = GSM()
    #     gsm.current = "barcode"

'''make a lookup table
fixed flowrate on the pump.
flowrate and pressure of WATER are on LCD.

pump stuff goes to database so we can monitor (+- 20% is something bad and we need to change pump)

real time monitoring is important here!
to get from 13.8 to 15 directly is bad.  need it to be GRADUAL.

[FILL BEAKER BUTTON] here: turn on JUST water for 10 seconds (can be hit multiple times!)
- regulator



last measured concentration: we would know avg flow and pressure (from LCD) at that LAST concentration

next, button to turn on water (on lookup table) to determine how much PRESSURE and WATER
will give us a concentration. until we GET to 15% -> 15.5 -> 16 -> 16.5

need real time way to get to 0.56 (lookup table -> know what pressure and flow rate gives us 0.56)

"TURN VALVE UNTIL FLWO RATE IS X AND PRESSURE IS Y" on lcd screen

- turn water pressure valve CCW = open (to get more water, less concentration)
- CW is closed (MORE concentration)

0.52 -0.58 ===> Look up the pressure and flow rate that SHOULD match that.
= the knobs are turned to get to those specific pressures and flow rates.

Within 5-10 % range, you can alert them that it is done and has reached the concentration


At the end, [CONFIRM NEW FR and PRessure]: off of the LCD screen (visually)

    <2nd Fill beaker> 10 sec with Soap AND Water, will fill beaker with same flow rate and pump and do the concentration again
    this will save to the "desired concentration ACTUAL" -> testing what you just changed
    water pressure (NEW water+soap concentration)
    
    Type it in. If not within 10% of 14.4, go back to the earlier page after [OK] button
    <Current Measured Concentration> =======> redo steps 
    
    After second attempt, (which is really weird and should not happen) have a debug message display, but also have ability to force
    skip forward instead of going back to the earlier page like before, and accept value (goes to home screen) normal state
    
    


If this value is [NOT CORRECT]: 
        ERROR OUT? go to home page. redo again then
        
        
Then new runs will use "measured concentration" on "CALIBRATION DATA PAGE" as 0.54



CALIBRATION DB: 
- 





****** automatic background portion ********


Small white thing (ceramic mug)

sensor at water level- green if water IS at the 10.5 inch depth

from usage or evap the leevl will go down
at 3am thsi wil turn on and do the relay (relay for pump)

5 sec, 30 sec
th esoap and open solenoid for water (calibrated to new stuff)

will fill the tank up until the water sensor is back at th eoriginal level. 

THEN turns off instantly

that data: time of 


DB: pump flow rate, pressure
- ensures nothing went wrong
- if it didn't fill (water level light is on and is fine) 
- but chancse are you'll lose some amount during the day and ahve to refill











'''


#import libgpiod_RPI5_manager as gpio_manager
#import wash_profiles as wp
#from rpi_lcd import LCD
#from datetime import datetime
#from threading import Thread
#import gpiod
#from gpiod.line import Direction, Value, Bias, Edge
#import time, sys, os
##import busio
# import digitalio
# import board
# import adafruit_mcp3xxx.mcp3008 as MCP
# from adafruit_mcp3xxx.analog_in import AnalogIn
# #import pandas as pd
# import pymssql
# import keyboard
 
# #set up SPI comms to MCP Hat (ADC chip for pressure sensor)
# spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
# cs = digitalio.DigitalInOut(board.D5)
# mcp = MCP.MCP3008(spi, cs)
# chan = AnalogIn(mcp, MCP.P0)
 
# #Create object for LCD I2C device
# lcd = LCD()
# chip_path = "/dev/gpiochip0"
 
# #GPIO Pin Variables
# FLOW_SENSOR_H20 = 27
# #FLOW_SENSOR_SOL =  
# PUMP_RELAY = 16
# #VALVE_RELAY = 17
# #DEPTH =
 
# background_task = 1
# count = 0
# flowCalFac = 38 # 
# vdd = 3.3
# size = 4096
# chipDiff = 1024/65536  # lib returns 16b number (65536) and chip returns 1024 number, so result is scaled by 1024/65536
# d2Mpa = 0.101325/620.6061 #calibration for converting ADC output to a pressure value, max pressure over max analog voltge (estimate, needs testing)
 
# raw_config_dict = {
#     #FLOW_SENSOR_H20: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE),
#     PUMP_RELAY: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE),
#     #16: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE),
#     #11: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE),
#     #29: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE),
#     #13: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE),
#     #40: gpiod.LineSettings(direction=Direction.INPUT, bias=Bias.PULL_DOWN),
#     #38: gpiod.LineSettings(direction=Direction.INPUT, bias=Bias.PULL_DOWN) 
#     }
 
# # RPI5_chips inherits the RPI5_GPIO_Manager class
# RPI5_chip = gpio_manager.RPI5_GPIO_Manager(chip_path, raw_config_dict)
 
# #Config.set('graphics', 'width', '1024')
# #Config.set('graphics', 'height', '600')
# #Config.write()
 
# #Function to detect edge and process a counter, to be set to a thread
# def watch_line_falling():
#     global chip_path
#     global FLOW_SENSOR_H20
#     global count
#     #add a while loop that then does a wait_edge_events for 0.1sec as a threaded task so that the while keeps checking instead of the edge check
#     request = gpiod.request_lines(chip_path,consumer="watch-line-falling",config={FLOW_SENSOR_H20: gpiod.LineSettings(edge_detection=Edge.FALLING)})
#     while True:
#         for event in request.read_edge_events():
#             #print("hit # {}:".format(event.line_seqno))
#             count = count + 1
 
# def flow_press():
#     """
#     Get Pressure
#     This function takes the live data from data input objects and
#     displays them to the LCD object
#     Returns: none
#     """
#     global background_task
#     global count
#     while background_task:
#         try:
#             #Get Water Flow Rate
#             time.sleep(.5) #wait half a seond to accumulate edges in countPulse function (another half below)
#             """
#             Flow calc:
#             Freq = 38*Q +-3% (Q = L/min, aka "flow")
#             flow = freq/38
#             freq = count/1sec
#             may need to update this delay or function if this is pulled out on its own
#             """
#             flow = (count / flowCalFac) #use snapshot of pulse count to determine 
#             flowString = "H2O F: %.3f L/min" % (flow)
#             lcd.text(flowString,1)
#             count = 0
 
#             #Get Water Pressure
#             rawADC = chan.value*chipDiff
#             adcVolt = chan.voltage*0.25
#             pressOut = rawADC*d2Mpa
#             pressString = "H2O P: %.3f MPa" % (pressOut)
#             voltString = "H2O V: %.3f V" % (adcVolt)
#             lcd.text(pressString,2)
#             #print('Raw ADC Value: ',chan.value)
#             #print('ADC Voltage: ' + str(chan.voltage) + 'V')
#             time.sleep(0.5)
#         except KeyboardInterrupt:
#             print('\ncaught keyboard interrupt!, bye')
#             #GPIO.cleanup()
#             sys.exit()
 
# def start_threads():
#     #This function creates a thread for the LCD-populating function to
#     #run in parallel to the rest of the system
#     #Returns: none
#     monitor_thread = Thread(target=watch_line_falling)
#     monitor_thread.daemon = True # Allow thread to be killed when the main program exits
#     lcd_thread = Thread(target=flow_press)
#     lcd_thread.daemon = True
#     monitor_thread.start()
#     lcd_thread.start()

