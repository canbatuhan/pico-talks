import machine
import utime

class UARTHandler:
    def __init__(self, pin, baudrate):
        self.__uart = machine.UART(pin, baudrate=baudrate)
        
    def __timeout(self, timeout):
        utime.sleep_ms(timeout)
        
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
    
    def __receive_response(self, cmd):
        response = self.__uart.read().decode('utf-8')
        return response[len(cmd):]
    
    def send_receive_data(self, data):
        self.__uart.write(data)
        self.__timeout(2000)
        return self.__receive_response(data)
    
    def send_receive_cmd(self, timeout, cmd, *args):
        self.__send_cmd(cmd, *args)
        self.__timeout(timeout)
        return self.__receive_response(self.__generate_cmd(cmd, *args))
    
    def send_receive_query(self, timeout, cmd, *args):
        self.__send_query(cmd, *args)
        self.__timeout(timeout)
        return self.__receive_response(self.__generate_query(cmd, *args))