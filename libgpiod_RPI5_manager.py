import gpiod
from gpiod.line import Direction, Value, Bias



class RPI5_GPIO_Manager():
    def __init__(self,chip_device_path,raw_gpio_config_dict):
        
        # Dictionary Mapping Physical RPI5 pins to GPIO Functional Names "/dev/gpiochip0"
        self.RPI5_pin_to_gpiofunction_dict = {
            "3": "GPIO02",
            "5": "GPIO03",
            "7": "GPIO04",
            "8": "GPIO14",
            "10": "GPIO15",
            "11": "GPIO17",
            "12": "GPIO18",
            "13": "GPIO27",
            "15": "GPIO22",
            "16": "GPIO23",
            "18": "GPIO24",
            "19": "GPIO10",
            "21": "GPIO09",
            "22": "GPIO25",
            "23": "GPIO11",
            "24": "GPIO08",
            "26": "GPIO07",
            "29": "GPIO05",
            "31": "GPIO06",
            "32": "GPIO12",
            "33": "GPIO13",
            "35": "GPIO19",
            "36": "GPIO16",
            "37": "GPIO26",
            "38": "GPIO20",
            "40": "GPIO21"
            }
        
        # Dictionary Mapping GPIO Functional Names to Assigned GPIO Line Levels "/dev/gpiochip0"
        self.RPI5_gpiofunction_to_linelevel_dict = {
            "GPIO02": "2",
            "GPIO03": "3",
            "GPIO04": "4",
            "GPIO05": "5",
            "GPIO06": "6",
            "GPIO07": "7",
            "GPIO08": "8",
            "GPIO09": "9",
            "GPIO10": "10",
            "GPIO11": "11",
            "GPIO12": "12",
            "GPIO13": "13",
            "GPIO14": "14",
            "GPIO15": "15",
            "GPIO16": "16",
            "GPIO17": "17",
            "GPIO18": "18",
            "GPIO19": "19",
            "GPIO20": "20",
            "GPIO21": "21",
            "GPIO22": "22",
            "GPIO23": "23",
            "GPIO24": "24",
            "GPIO25": "25",
            "GPIO26": "26",
            "GPIO27": "27"
                    }
        
        # Chip device path
        self.chip_path = chip_device_path
        
        # Raw gpio configuration dictionary (i.e. - uses physical pin numbers instead of gpiod line levels)
        self.raw_gpio_config_dict = raw_gpio_config_dict
        
        # Converts RPI5 physical pin numbers into corresponding gpiod line levels
        self.line_settings_config_dict = self.create_gpiod_line_config_dict(self.raw_gpio_config_dict)
        
        self.request = gpiod.request_lines(self.chip_path, consumer="Initial_class_setup", config=self.line_settings_config_dict,)
        
    # Creates a new gpiod config dictionary containing the gpio pin numbers converted to line levels    
    def create_gpiod_line_config_dict(self,raw_config_dict):
        # Create empty dictionary
        gpiod_line_config_dict = {}
        
        #Loop through raw_config_dictionary and convert physical gpio pin numbers to line levels
        for key, value in raw_config_dict.items():
            # GPIO Pin Number Conversion to Line Levels
            gpio_to_line_level_conversion = int(self.RPI5_gpiofunction_to_linelevel_dict[self.RPI5_pin_to_gpiofunction_dict[str(key)]])
            # Add converted line level with its associated GPIOd linesettings to the gpiod_line_config_dict dictionary
            gpiod_line_config_dict.setdefault(gpio_to_line_level_conversion,value)
        
        # Output the completed gpiod_line_config_dictionary
        return gpiod_line_config_dict
        
        
    def set_gpio_output_value(self, physical_gpio_pin, pin_output_value):
        value_str = {"LOW": Value.INACTIVE, "HIGH": Value.ACTIVE}
        
        # GPIO Pin Number Conversion to Line Levels
        gpio_to_line_level_conversion = int(self.RPI5_gpiofunction_to_linelevel_dict[self.RPI5_pin_to_gpiofunction_dict[str(physical_gpio_pin)]])
        
        self.request.set_value(gpio_to_line_level_conversion,value_str[pin_output_value])
