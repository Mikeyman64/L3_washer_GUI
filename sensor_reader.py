# sensor_reader.py
import time
from threading import Thread
import board
import busio
import digitalio
from adafruit_mcp3xxx.mcp3008 import MCP3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import libgpiod_RPI5_manager as gpio_manager

from rpi_lcd import LCD
import gpiod
from gpiod.line import Direction, Value, Edge, Bias

class SensorReader:
    def __init__(self, lcd_enabled=True):
        # ADC (Pressure sensor)
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        cs = digitalio.DigitalInOut(board.D5)
        self.mcp = MCP(spi, cs)
        self.chan = AnalogIn(self.mcp, 0)

        # LCD
        #self.lcd = LCD() if lcd_enabled else None
        #self.lcd_lock = threading.Lock()

        # Flow sensor setup
        self.chip_path = "/dev/gpiochip0"
        self.FLOW_SENSOR_H20 = 27
        self.PUMP_RELAY = 16

        self.flowCalFac = 38
        self.chipDiff = 1024 / 65536
        self.d2Mpa = 0.101325 / 620.6061

        self.count = 0
        self.running = False

        # Configure GPIO
        raw_config_dict = {
            self.PUMP_RELAY: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE),
        }
        RPI5_chip = gpio_manager.RPI5_GPIO_Manager(self.chip_path, raw_config_dict)


        # Threads
        self.flow_thread = None
        self.watch_thread = None

        # Optional UI hooks (Kivy)
        self.flow_callback = None
        self.pressure_callback = None

    def start(self):
        """Start background threads for monitoring flow and pressure."""
        self.running = True
        self.watch_thread = threading.Thread(target=self._watch_line_falling, daemon=True)
        self.flow_thread = threading.Thread(target=self._flow_press_monitor, daemon=True)

        self.watch_thread.start()
        self.flow_thread.start()

    def stop(self):
        """Stop background tasks gracefully."""
        self.running = False

    def _watch_line_falling(self):
        request = gpiod.request_lines(
            self.chip_path,
            consumer="watch-line-falling",
            config={self.FLOW_SENSOR_H20: gpiod.LineSettings(edge_detection=Edge.FALLING)}
        )
        while self.running:
            for event in request.read_edge_events(timeout=0.1):  # 100ms poll
                self.count += 1

    def _flow_press_monitor(self):
        while self.running:
            try:
                time.sleep(0.5)

                # Flow rate
                flow = self.count / self.flowCalFac
                self.count = 0
                flow_string = f"H2O F: {flow:.3f} L/min"

                # Pressure
                raw_adc = self.chan.value * self.chipDiff
                adc_volt = self.chan.voltage * 0.25
                press_out = raw_adc * self.d2Mpa
                press_string = f"H2O P: {press_out:.3f} MPa"

                # Update LCD
                if self.lcd:
                    with self.lcd_lock:
                        self.lcd.text(flow_string, 1)
                        self.lcd.text(press_string, 2)

                # Update Kivy UI (if callbacks are set)
                if self.flow_callback:
                    self.flow_callback(flow)
                if self.pressure_callback:
                    self.pressure_callback(press_out)
                    
                # ✅ Store values for get_data()
                self.flow = flow
                self.pressure = press_out

                time.sleep(0.5)
            except Exception as e:
                print(f"[SensorReader] Exception: {e}")
                sys.exit(1)
                
    def get_data(self):
        return {
            "flow": self.flow,
            "pressure": self.pressure
        }
        
        
        
    '''
    def __init__(self):
        # SPI setup for pressure sensor (ADC)
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        cs = digitalio.DigitalInOut(board.D5)
        self.mcp = MCP(spi, cs)
        self.chan = AnalogIn(self.mcp, 0)
        #Create object for LCD I2C device
        lcd = LCD()
        
        # GPIO for flow sensor
        self.chip_path = "/dev/gpiochip0"
        self.FLOW_SENSOR_H20 = 27
        self.flowCalFac = 38
        self.d2Mpa = 0.101325 / 620.6061
        self.chipDiff = 1024 / 65536

        self.count = 0
        self.running = True
        self.flow = 0
        self.pressure = 0

        self._start_threads()

    def _watch_flow(self):
        request = gpiod.request_lines(
            self.chip_path,
            consumer="watch-line-falling",
            config={self.FLOW_SENSOR_H20: gpiod.LineSettings(edge_detection=Edge.FALLING)}
        )
        while self.running:
            for event in request.read_edge_events(timeout=0.1):
                self.count += 1

    def _update_readings(self):
        while self.running:
            time.sleep(0.5)
            self.flow = self.count / self.flowCalFac
            self.count = 0
            rawADC = self.chan.value * self.chipDiff
            self.pressure = rawADC * self.d2Mpa
            # === Add LCD updates here ===
            self.lcd.text(f"H2O F: {self.flow:.3f} L/min", 1)
            self.lcd.text(f"H2O P: {self.pressure:.3f} MPa", 2)
            
            

    def _start_threads(self):
        Thread(target=self._watch_flow, daemon=True).start()
        Thread(target=self._update_readings, daemon=True).start()



    def stop(self):
        self.running = False
        '''
