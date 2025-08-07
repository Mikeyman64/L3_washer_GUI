OPERATOR INSTRUCTIONS:

MAIN SCREEN:

Scan <Barcode>
- Use the barcode to scan in to a new wash session, OR type the U-number directly.
- This saves the U-number to the washer session.

    Also contains 2 settings buttons:
    <Calibration>
    <Set_Time>



<Choose Washer Profile>
- 16 Options exist here (Test and Test2 can be removed or replaced)
- Choose whichever wash type you need to complete.

<Scan Board Data>
- Using attached barcode scanner, scan the long product barcode identifier on the MO sheet for each board being washed.
- It automatically selects the text field after every scan, so you can continue scanning as many boards as you want in one continuous motion without clicking the screen.
- Press <Next> to confirm.


<Confirmation Screen>
- On this screen, you will verify your ID, the wash profile you have selected, and the number of boards you are about to wash.
- Click <Wash!> to confirm.


<Complete or Abort Screen>
- Once the wash either ABORTS or COMPLETES, you will land on the respective page for 5 seconds, during which time the wash session and all related details are uploaded to the SQL database.
- Then, it returns to the initial <Scan Barcode> screen.







SETTINGS BUTTONS:

<CALIBRATION> - Gear Cog Icon

Click this to set up new calibration for the tank.

This will contain information about the CURRENT flow rate and pressure measured (TODO: link the hardware to the measured data metrics, ensure it's "live").

Click <New Calibration> to enter a new calibration.
- U-number
- Calibration Passcode: Set to "1234" for some users, can be set in the SQL.

- Consult Ben Barger if your account isn't yet setup for Calibration on the washer database (If you don't have permission you'll need to set the last column in the to whatever 4-digit numerical password you'd like).


<Enter Tank Solution Concentration>
Enter, as a float, the concentration of the tank solution.  Press <ENTER> to continue.


<Add New Calibration Screen>
Contains information about the current soap water concentration last stored / measured.
You must then set up the washer to set a new calibration by completing the checklist items.

<Input Beaker Concentration>
The external beaker will give you a concentration, which you must measure MANUALLY and add that value to the text input (something like 0.145). Hit <GO> to confirm.

<Measured Concentration Page>
STILL A WORK IN PROGRESS. Ideally, there will be some algorithm or lookup table that should be able to determine at what flow rate and pressure the washer valves need to be set to in order to guarantee our concentration gets us closer to our desired concentration (0.15 at the moment).

There should be a second round of filling the beaker with the solution (both water and soap), but details of what go on these final screens should be left up to Brian Lewis.





DELTA TIME SETTINGS BUTTON:

This is a way for a registered WASHER ADMIN user to change the frequency at which we run calibrations.  Only those with knowledge of the Delta Time password (right now time123) will be able to modify this value.

The two fields are:
- <Delta>The number of days to set the frequency: default is 7, but type 10 if you wish to change it to 10, for instance.
- <Password> to set the delta_time variable. Will only apply the change if this password is CORRECT.