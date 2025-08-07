# Washer GUI Application

A touchscreen-based GUI built using [Kivy](https://kivy.org/) and [KivyMD](https://kivymd.readthedocs.io/) to control and select modes for the board washer, as well as other utilities.

-Nathan L


---

## Features

- User authentication and calibration pages
- Multiple wash option modes
- Error handling and mis-input handling
- SQL data logging (See Ben Barger for more specifics / extending existing features)
- LCD display and GPIO integration (ONGOING!)

---

## Venvs

- (washVenv) is the main virtual environment used to run just the GUI, with working SQL functionality.
- Hardware integration with the raspberry pi, and anything related to reading values for the Calibration, may require extra playing around
with packages like gpiod, rpi_lcd, etc. In other words, functionality reading from washer hardware is not automatically guaranteed inside of
washVenv.
- (washVenv2) is an experimental one that might also work. However, I would still recommend just sticking with washVenv.

### Requirements

- Python 3.8+
- everything inside of requirements.txt

### Raspberry Pi Integration

- As of 7/25, hardware integration has been started on a makeshift washer harness, with an LCD screen and a couple of flow rate meters.
- NOT complete, and additional work will need to be done to integrate what was on the very first iteration of the GUI that DID have hardware into this iteration.
- see "sensor_reader.py" for all the helper functions that the old GUI utilized to pass in hardware values and read from those sensors.
- "sensor_reader.py" is currently NOT being used at all, but the functions in there are all pertinent and can later be integrated into the calibration data logic.


## Project Structure 

### Screens:

- Any .py file with "washer" appended to the front - ex: washerOptionsScreen, washerScreenCountdown, etc - represents an individual screen that the user can land on, with the exception of washerCalibrationDataScreen, which houses classes for every single screen related to the calibration data logic (settings button on barcode screen where you first scan U-number).
- Typically, the name of the class inside the .py file corresponds to the actual screen, which can be referenced in the .kv file.  Essentially, every washer_.py file contains just one class, corresponding to a Screen object, with the exception of the calibration file, which contains multiple classes and thus multiple screens.

### run_washer_main.py

This is the main runner file that instantiates the full kivy build.

In build():
- set GlobalScreenManager (where we set global variables that persist across screens, and hold pulled data from SQL)
- set kivy themes and import fonts
- load the kivy file 
- add all kivy screens to GlobalScreenManager instance
- pull users from SQL database to locally stored CALIBRATION_USERS dictionary for faster load

In order to add a NEW PAGE or SCREEN:
Add a new kivy screen on the washerGUI.kv: start it with brackets, like <NewPageHere>, with a ```name``` attribute you can also remember.
Example:
```
<BarcodeScreen>:
    name: "barcode"
```
In either a new python file (or an existing one) add a class with the same name as the one in brackets:


```
class BarcodeScreen(Screen):
    def on_enter(self):
        # Custom behaviors here
        Clock.schedule_once(self.safe_user_clear, 0.01)
    
    def more_functions(self): ...
```



These must match in order for kivy to link the .kv to the Python functionality.

Finally, in the build() function within run_washer_main.py, import that class and add it to the globalSM() object as a widget:


```
    globalSM.add_widget(BarcodeScreen(name='barcode'))
```

Now, you can switch to this screen at any point (works especially well when binding button click event to navigation to that page),
by referencing that page via the gsm() object. 

Example:
```
    def goToWashOptions(self):
        gsm = GSM()
        gsm.current = 'washOptions'
```


## washerGlobals.py

### GlobalScreenManager()
Contains any and all global variables of interest, which can be referenced across different kivy screens.
Usage: within any function that you want to set or access a global variable, instantiate a gsm object:

<code>gsm = GSM()</code>

Then, you can access any variable by calling it directly, such as: <code>gsm.CALIBRATION_USERS</code> or <code>gsm.CalibrateDict["key"]</code>

The Kiosk GUI utilizes this too, but has a slightly different mechanic for calling global variables within the screen manager.

## wash_profiles.py

Contains dictionary with mapping of wash profile to wash time (selecting a wash option changes how long the wash runs).

## credentials.env

If this does NOT exist yet, make one with the following content:



``
    SERVER=USW-SQL30003.rootforest.com
    DATABASE=Oven_Bake_Log
    UID=OvenBakedUsr
    PWD=???????
``


Consult Ben Barger for the password.

## concentration_lookup.csv

For the calibration data, we temporarily use a lookup table to 
determine at what concentration we are to set the pressure and flow to achieve it.

# CalibrationDataScreen.py

Most of the TODO is here.  After the first Measured Concentration page,
some lookup table or algorithm is needed to determine the exact FLOW RATE and pressure
to set the valves to in order for the concentration to move in the right direction
(0.13 requires a slight nudge in the upwards direction, if desired concentration is 0.15).

Also, hardware integration is still INCOMPLETE.  The flow rate meter, pressure sensor, do not yet
read their values into the live calibration info page that you first land on.

If it helps, any relevant concentration, flow rate, or pressure values can be saved in various CalibrateDict
variables. As seen above, you can reference these by doing:

```
    gsm = GSM()
    gsm.CalibrateDict["solutionTankConcentration"] = 0.14
```

However, be aware that in order for these values to be USEFUL, you might want to then uploaded
those values to the SQL database at the end of setting them locally to GSM.

Additionally, you might want to consider setting permissions for whichever 