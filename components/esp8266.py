import utime

from components.uart_handler import UARTHandler
from components.settings import *

class ESP8266:
    def __init__(self, pin, baudrate):
        self.__uart_handler = UARTHandler(pin, baudrate)
    
    """ HELPERS """
    def __get_timestamp(self):
        y, m, md, h, m, s, wd, yd = utime.localtime()
        return "{}/{}/{} {}:{}:{}".format(y, m, md, h, m, s)
        
    def __log(self, msg):
        print("[ESP8266] {}\t- {}".format(
            self.__get_timestamp(), msg))
    
    """
        BASIC COMMANDS
    """
    def start(self):
        response = self.__uart_handler.send_receive_cmd(STARTUP)
        if "OK" in response: self.__log("Started")
        else: self.restart()

    def restart(self):
        response = self.__uart_handler.send_receive_cmd(RESTART, timeout=5000)
        if "OK" in response: self.__log("Restarted")
        else: self.__log("Failed to restart")
    
    """
        WI-FI COMMANDS
    """
    def get_mode(self):
        response = self.__uart_handler.send_receive_query(WIFI_MODE)
        mode = -1
        if "OK" in response:
            mode = response.split("\n")[0].split(":")[1]
            self.__log("Works in {} mode".format(
                WIFI_MODES.get(int(mode))))
        else:
            self.__log("Failed to query WiFi mode")
        return WIFI_MODES.get(int(mode))
    
    def set_mode(self, mode):
        response = self.__uart_handler.send_receive_cmd(WIFI_MODE, mode, timeout=2000)
        if "OK" in response: self.__log("WiFi mode is set to {}".format(WIFI_MODES.get(mode)))
        else: self.__log("Failed to set the Wifi mode to {}".format(WIFI_MODES.get(mode)))
            
    def list_access_points(self):
        response = self.__uart_handler.send_receive_cmd(LIST_APS, timeout=10000)
        for access_point in response.split("\n"):
            ap_entires = access_point.split(",")
            if len(ap_entires) > 1:
                ap_name = ap_entires[1]
                self.__log("Access Point {} is in range.".format(ap_name))
                utime.sleep_ms(250)
        
    def join_access_point(self, ssid, pwd):
        ssid, pwd = "\"{}\"".format(ssid), "\"{}\"".format(pwd)
        response = self.__uart_handler.send_receive_cmd(
            WIFI_CONNECTION, ssid, pwd, timeout=5000)
        if "OK" in response: self.__log("Joined to {}".format(ssid))
        else: self.__log("Failed to join to {}".format(ssid))
        
    def get_access_point(self):
        response = self.__uart_handler.send_receive_query(WIFI_CONNECTION)
        
    def quit_access_point(self):
        response = self.__uart_handler.send_receive_cmd(WIFI_DISCONNECT)
        if "OK" in response: self.__log("Quit from access point")
        else: self.__log("Failed to quit from access point")
    
    def get_static_ip(self):
        response = self.__uart_handler.send_receive_query(GET_SET_IP)
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
        return addrs.get("ip")
    
    def set_static_ip(self, ip):
        ip = "\"{}\"".format(ip)
        response = self.__uart_handler.send_receive_cmd(GET_SET_IP, ip, timeout=2000)
        if "OK" in response: self.__log("IP Address is set to {}".format(ip))
        else: self.__log("Failed to set the IP Address to {}".format(ip))
    
    """
        TCP COMMANDS
    """
    def get_status(self):
        response = self.__uart_handler.send_receive_cmd(CONN_STATUS)
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
        response = self.__uart_handler.send_receive_cmd(
            CONN_START, conn_type, remote_ip, str(remote_port), timeout=2000)
        if "OK" in response:
            self.__log("Connected to {} at port {}.".format(
                remote_ip, remote_port))
        else:
            self.__log("Failed to create a connection with {} at port {}.".format(
                remote_ip, remote_port))
            
    def close_connection(self):
        response = self.__uart_handler.send_receive_cmd(CONN_CLOSE)
        if "OK" in response: self.__log("Disconnected")
        else: self.__log("Failed to disconnect")
    
    def get_connection_mode(self):
        response = self.__uart_handler.send_receive_query(CONN_MODE),
        mode = -1
        if "OK" in response:  
            mode = response.split("\n")[0].split(":")[1]
            self.__log("Connection mode is {}.".format(
                CONNECTION_MODES.get(int(mode))))
        else:
            self.__log("Failed to query the connection mode.")
        return CONNECTION_MODES.get(int(mode))
    
    def set_connection_mode(self, mode):
        response = self.__uart_handler.send_receive_cmd(TCP_MODE, mode, timeout=2000)
        if "OK" in response: self.__log("Connection mode is set to {}".format(
            CONNECTION_MODES.get(mode)))
        else: self.__log("Failed to set the connection mode to {}".format(
            CONNECTION_MODES.get(mode)))
    
    def send_receive_data(self, data):
        response = self.__uart_handler.send_receive_cmd(SEND, len(data), timeout=2000)
        if "OK" in response:
            response = self.__uart_handler.send_receive_data(data)
            print(response)
            self.__log("Data is sent and response received")
        else:
            self.__log("Failed to send data and receive response")
