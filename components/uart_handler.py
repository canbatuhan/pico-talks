import machine
import utime

from components.settings import *

class UARTHandler:
    def __init__(self, pin, baudrate):
        self.__uart = machine.UART(pin, baudrate=baudrate)
        
    def __timeout(self, timeout):
        utime.sleep_ms(timeout)
        
    def __wait_until_available(self):
        while True:
            response = self.__uart.read()
            if response is not None:
                try:
                    response = response.decode('utf-8')
                    if BUSY_MSG not in response: break
                except: pass
            self.__timeout(1000)
        return response
        
    def __generate_cmd(self, cmd, *args):
        if len(args) != 0:
            cmd += "="
            for idx, each in enumerate(args):
                cmd += str(each)
                if idx != len(args)-1:
                    cmd += ","
        cmd += "\r\n"
        return cmd
    
    def __generate_query(self, cmd, *args):
        cmd += "?"
        cmd += "\r\n"
        return cmd

    def __send_cmd(self, cmd, *args):
        sent_cmd = self.__generate_cmd(cmd, *args)
        self.__uart.write(sent_cmd)

    def __send_query(self, cmd, *args):
        sent_query = self.__generate_query(cmd, *args)
        self.__uart.write(sent_query)
    
    def __receive_response(self):
        response = self.__uart.read()
        try:
            response = response.decode('utf-8')
            if BUSY_MSG in response:
                response = self.__wait_until_available()
        except: pass
        return response
    
    def send_receive_data(self, data, timeout=1000):
        self.__uart.write(data)
        self.__timeout(timeout)
        return self.__receive_response()
    
    def send_receive_cmd(self, cmd, *args, timeout=1000):
        self.__send_cmd(cmd, *args)
        self.__timeout(timeout)
        return self.__receive_response()
    
    def send_receive_query(self, cmd, *args, timeout=1000):
        self.__send_query(cmd, *args)
        self.__timeout(timeout)
        return self.__receive_response()
