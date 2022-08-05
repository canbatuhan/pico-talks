import machine

ANALOG_MAX = 2**16
ANALOG_MIN = 0

class SoilMoistureSensor:
    def __init__(self, sensor_id, analog_pin):
        self.__id = sensor_id
        self.__analog_pin = machine.ADC(analog_pin)
        self.__soil_moisture = 0.0
    
    def __normalize(self, analog_value):
        return (analog_value-ANALOG_MIN)/(ANALOG_MAX-ANALOG_MIN)
        
    def __generate_data(self):
        analog_value = self.__analog_pin.read_u16()
        self.__soil_moisture =  -100 * self.__normalize(analog_value) + 100
    
    def generate_package(self):
        self.__generate_data()
        return {"sensor_id": self.__id,
                "soil_moisture": self.__soil_moisture}

