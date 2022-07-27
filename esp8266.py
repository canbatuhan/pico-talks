import machine
import utime

from uart_handler import UARTHandler
from settings import *

class ESP8266:
    def __init__(self, pin, baudrate):
        self.__uart_handler = UARTHandler(pin, baudrate)
        
    def __get_timestamp(self):
        y, m, md, h, m, s, wd, yd = utime.localtime()
        return "{}/{}/{} {}:{}:{}".format(y, m, md, h, m, s)
        
    def __log(self, msg):
        print("[ESP8266] {}\t- {}".format(
            self.__get_timestamp(), msg))
        
    def start(self):
        response = self.__uart_handler.send_receive_cmd(2000, STARTUP)
        if "OK" in response: self.__log("Started")
        else: msg = self.__log("Failed to start")
            
    """def restart(self):
        response = self.__uart_handler.send_receive_cmd(RESTART)
        msg = None
        if "OK" in response:
            msg = "Restarted sucessfully"
            self.__log(msg)
        else:
            msg = "Could not be restarted"
            self.__log(msg)"""
    
    def get_mode(self):
        response = self.__uart_handler.send_receive_query(2000, WIFI_MODE)
        mode = -1
        if "OK" in response:
            mode = response.split("\n")[0].split(":")[1]
            self.__log("Works in {} mode".format(
                WIFI_MODES.get(int(mode))))
        else:
            self.__log("Failed to query WiFi mode")
        return WIFI_MODES.get(int(mode))
    
    def set_mode(self, mode):
        response = self.__uart_handler.send_receive_cmd(2000, WIFI_MODE, mode)
        if "OK" in response: self.__log("WiFi mode is set to {}".format(WIFI_MODES.get(mode)))
        else: self.__log("Failed to set the Wifi mode to {}".format(WIFI_MODES.get(mode)))
            
    def list_access_points(self):
        response = self.__uart_handler.send_receive_cmd(10000, LIST_APS)
        for access_point in response.split("\n"):
            ap_entires = access_point.split(",")
            if len(ap_entires) > 1:
                ap_name = ap_entires[1]
                self.__log("Access Point {} is in range.".format(ap_name))
                utime.sleep_ms(250)
        
    def join_access_point(self, ssid, pwd):
        ssid, pwd = "\"{}\"".format(ssid), "\"{}\"".format(pwd)
        response = self.__uart_handler.send_receive_cmd(5000, WIFI_CONNECT, ssid, pwd)
        if "OK" in response: self.__log("Joined to {}".format(ssid))
        else: self.__log("Failed to join to {}".format(ssid))
        
    def quit_access_point(self):
        response = self.__uart_handler.send_receive_cmd(2000, WIFI_DISCONNECT)
        if "OK" in response: self.__log("Quit from access point")
        else: self.__log("Failed to quit from access point")
    
    def get_static_addrs(self):
        response = self.__uart_handler.send_receive_query(2000, GET_SET_IP)
        addrs = dict()
        if "OK" in response:
            for entry in response.split("\n")[0:-2]:
                entry_parts = entry.split(":")
                if len(entry_parts) > 1:
                    name = entry.split(":")[1]
                    value = entry.split(":")[2]
                    addrs[name] = value
                    self.__log("{}: {}".format(name.upper(), value))
                    utime.sleep_ms(250)
        else:
            self.__log("Failed to get static addresses")
        return addrs.get("ip"), addrs.get("gateway"), addrs.get("netmask")
    
    def set_static_ip(self, ip):
        ip = "\"{}\"".format(ip)
        response = self.__uart_handler.send_receive_cmd(2000, GET_SET_IP, ip)
        if "OK" in response: self.__log("IP Address is set to {}".format(ip))
        else: self.__log("Failed to set the IP Address to {}".format(ip))
        
    """def configure_access_point(self, ssid, pwd, chl, ecn):
        ssid, pwd, chl = "\"{}\"".format(ssid), "\"{}\"".format(pwd), "\"{}\"".format(chl)
        self.__log("Configuring Access Point {}...".format(ssid))
        response = self.__uart_handler.send_receive_cmd(5000, WIFI_CONFIG_AP, ssid, pwd, chl, ecn)
        if "OK" in response:
            self.__log("Configured Access Point {} successfully.".format(ssid))
            self.__log("SSID/AP: {}".format(ssid))
            self.__log("PWD: {}".format(pwd))
            self.__log("CHANNEL ID: {}".format(chl))
            self.__log("ENCRYPTION METHOD: {}".format(enc))
        else:
            self.__log("Could not configured Access Point {}.".format(ssid))"""
            
    """def list_connected_stations(self):
        response = self.__uart_handler.send_receive_cmd(5000, LIST_IPS)
        print(response)"""
    
    def get_status(self):
        response = self.__uart_handler.send_receive_cmd(2000, CONN_STATUS)
        status = -1
        if "OK" in response:
            status = response.split("\n")[0]
            status = status.split(":")[1]
            self.__log(CONNECTION_STATUS.get(int(status)))
        else:
            self.__log("Failed to get connection status.")
        return CONNECTION_STATUS.get(int(status))
    
    def start_connection(self, conn_type, remote_ip, remote_port):
        conn_type, remote_ip = "\"{}\"".format(conn_type), "\"{}\"".format(remote_ip)
        response = self.__uart_handler.send_receive_cmd(2000, CONN_START, conn_type, remote_ip, str(remote_port))
        if "OK" in response:
            self.__log("Connected to {} at port {}.".format(
                remote_ip, remote_port))
        else:
            self.__log("Failed to create a connection with {} at port {}.".format(
                remote_ip, remote_port))
            
    """def get_addrs(self):
        response = self.__uart_handler.send_receive_cmd(1000, OBTAIN_IP)
        print(response)"""
    
    def get_connection_mode(self):
        response = self.__uart_handler.send_receive_query(2000, CONN_MODE)
        mode = -1
        if "OK" in response:  
            mode = response.split("\n")[0].split(":")[1]
            self.__log("Connection mode is {}.".format(
                CONNECTION_MODES.get(int(mode))))
        else:
            self.__log("Failed to query the connection mode.")
        return CONNECTION_MODES.get(int(mode))
    
    def set_connection_mode(self, mode):
        response = self.__uart_handler.send_receive_cmd(2000, TCP_MODE, mode)
        if "OK" in response: self.__log("Connection mode is set to {}".format(
            CONNECTION_MODES.get(mode)))
        else: self.__log("Failed to set the connection mode to {}".format(
            CONNECTION_MODES.get(mode)))
        
    """def delete_server(self, port):
        response = self.__uart_handler.send_receive_cmd(5000, SET_CLR_SERVER, 0, port)
        if "OK" in response: self.__log("Server is deleted at port {}".format(port))
        else: self.__log("Failed to deleted a server at port {}".format(port))"""
        
    """def create_server(self, port):
        response = self.__uart_handler.send_receive_cmd(5000, SET_CLR_SERVER, 0, port)
        if "OK" in response: self.__log("Server is created at port {}".format(port))
        else: self.__log("Failed to crate a server at port {}".format(port))"""
    
    def send_data(self, data):
        response = self.__uart_handler.send_receive_cmd(2000, SEND, len(data))
        if "OK" in response:
            response = self.__uart_handler.send_receive_data(data)
            print(response)
            self.__log("Data is sent and response received")
        else:
            self.__log("Failed to send data and receive response")
        
    def test(self):
        self.start()
        self.get_mode()
        self.join_access_point("Lenovo K6 NOTE", "sekizkarakter")
        self.start_connection("TCP", "192.168.43.100", 1773)
        for i in range(10):
            self.send_data("Hello World")
        self.quit_access_point()

if __name__ == "__main__":
    wifi_module = ESP8266(0, 115200)
    wifi_module.test()
