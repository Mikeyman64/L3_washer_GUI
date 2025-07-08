from kivy.app import App
from kivy.uix.screenmanager import Screen
# from washerGlobals import GlobalScreenManager
# from kivymd.app import MDApp
from kivy.clock import Clock
from datetime import *
from washerGlobals import GSM


class CalibrationDataPage(Screen):
    def __init__(self, **kwargs):
        super(CalibrationDataPage, self).__init__(**kwargs)
        self.timer = 0
        self.countdown = 30

    def on_enter(self):
        self.timer = Clock.schedule_interval(self.update_countdown, 1)

    def update_countdown(self, dt):
        if self.countdown > 0:
            self.countdown -= 1
        else: # done:
            self.timer.cancel()
            self.timer = 0
            self.countdown = 30
            self.manager.current = "barcode"

    def closeButtonClicked(self):
        gsm = GSM()
        gsm.current = "barcode"

    def newCalibButtonClicked(self):
        gsm = GSM()
        gsm.current = 'newCalibPage'

# =================================================================================
class NewCalibrationPage(Screen):
    def __init__(self, **kwargs):
        super(NewCalibrationPage, self).__init__(**kwargs)



    def closeButtonClicked(self):
        gsm = GSM()
        gsm.current = "barcode"






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
'''
