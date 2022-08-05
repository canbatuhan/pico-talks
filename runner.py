from components.esp8266 import ESP8266
from components.sensor import SoilMoistureSensor

UART_PIN = 0
BAUDRATE = 115200
SOIL_MOISTURE_PIN = 26

STATION_MODE = 1
AP_NAME = "Lenovo K6 NOTE"
AP_PWD = "sekizkarakter"

SERVER_HOST = "192.168.43.1"
SERVER_PORT = 1773

class EndDevice:
    def __init__(self, sensor_id):
        self.__wifi_module = ESP8266(UART_PIN, BAUDRATE)
        self.__sm_sensor = SoilMoistureSensor(sensor_id, SOIL_MOISTURE_PIN)
        
    def init(self):
        self.__wifi_module.start()
        self.__wifi_module.set_mode(STATION_MODE)
        self.__wifi_module.join_access_point(AP_NAME, AP_PWD)
        
    def run(self):
        while True:
            if self.__wifi_module.start_connection(
                "TCP", SERVER_HOST, SERVER_PORT):
                while True:
                    received_data = self.__wifi_module.send_receive_data(
                        str(self.__sm_sensor.generate_package()))
                self.__wifi_module.close_connection()
                

if __name__ == "__main__":
    pico = EndDevice("SM-0")
    pico.init()
    while True:
        pico.run()
        
