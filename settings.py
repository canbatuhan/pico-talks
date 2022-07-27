# Basic Commands
STARTUP = "AT"
RESTART = "AT+RST"
VERSION = "AT+GMR"

# WiFi Commands
WIFI_MODE       = "AT+CWMODE" # <mode>(1=STA,2=AP,3=STA+AP)
LIST_APS        = "AT+CWLAP"
WIFI_CONNECT    = "AT+CWJAP" # <ssid>,<pwd>
WIFI_DISCONNECT = "AT+CWQAP"
GET_SET_IP      = "AT+CIPSTA" # <ip>
WIFI_CONFIG_AP  = "AT+CWSAP" # <ssid>,<pwd>,<chl>,<ecn>
LIST_IPS        = "AT+CWLIF"

# TCP/IP Commands
CONN_STATUS    = "AT+CIPSTATUS"
CONN_START     = "AT+CIPSTART" # <type>(TCP,UDP,SSL),<remoteIP>,<remoteport>
OBTAIN_IP      = "AT+CIFSR"
CONN_MODE      = "AT+CIPMUX" # <mode>(0=single,1=multiple)
SET_CLR_SERVER = "AT+CIPSERVER" # <mode>(0=delete,1=create)
SEND           = "AT+CIPSEND"

# WiFi Modes
WIFI_MODES = {
    1: "Station",
    2: "Access Point", 
    3: "Station / Access Point"
}

# Connection Status
CONNECTION_STATUS = {
    2: "Connected to an AP and its IP is obtained.",
    3: "Created a TCP or UDP transmission.",
    4: "Disconnected.",
    5: "Does NOT Connect."
}

# Connection Modes
CONNECTION_MODES = {
    0: "Single",
    1: "Multiple"
}