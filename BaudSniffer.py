import serial
import serial.serialutil
import platform
import os
import time

## Constants 
### For Linux: /dev/ttyS1 etc. ; For Windows: COM1 etc. 
SETTING_SERIAL_PORT = 'COM4' 
TIMEOUT_SERIAL_PORT_SEC = 10 
BYTE_SIZE_TO_READ = 10

connection_list = []

baudrate_list = [
            110,
            300,
            600,
            1200,
            1800,
            2400,
            4800,
            9600,
            38400,
            14400,
            19200,
            38400,
            57600,
            115200,
            128000,
            256000,
    ]
serialport_settings_list =[
            '8N1',
            '8N2',
            '8E1',
            '8E2',
            '8O1',
            '8O2',
            '7N1',
            '7N2',
            '7E1',
            '7E2',
            '7O1',
            '7O2',
        ]

def open_port(baud_set: int, 
             bytesize_set: int, 
             parity_set: str, 
             stopbit_set: int):

    new_bytesize_set = set_bytesize(bytesize_set)
    new_parity_set = set_parity(parity_set)
    new_stopbit_set = set_stopbit(stopbit_set)  

    try:
        # open serial port
        ser = serial.Serial(SETTING_SERIAL_PORT, baud_set, 
                            new_bytesize_set, new_parity_set, 
                            new_stopbit_set, timeout=TIMEOUT_SERIAL_PORT_SEC)  
        data_serial = ser.read(BYTE_SIZE_TO_READ) 
        # close port
        ser.close()             
        return data_serial
    except serial.serialutil.SerialException:
        print ("serial.serialutil.SerialException rised")

def set_stopbit(stop_bit: str):

    if stop_bit == "1": 
        return serial.STOPBITS_ONE
    elif stop_bit == "2":
        return serial.STOPBITS_TWO
    else:
        print ('Unsupported Stopbit (no Option): ', stop_bit)

def set_bytesize(byte_size: str):

    if byte_size == "8":
     return serial.EIGHTBITS
    elif byte_size == "7":
     return serial.SEVENBITS  
    elif byte_size == "6":
     return serial.SIXBITS  
    elif byte_size == "5":
     return serial.FIVEBITS
    else:
     print ('Unspupported Byte Size (no Option): ', byte_size) 

def set_parity (parity: str):

    if parity == "N":
        return   serial.PARITY_NONE
    elif parity == "E":
        return serial.PARITY_EVEN
    elif parity == "O":
        return serial.PARITY_ODD
    elif parity == "M":
        return serial.PARITY_MARK

    elif parity == "S":
        return serial.PARITY_SPACE
    else: 
        print ('Unspupported Parity (no Option):', parity) 

 # serial port parameter = 8N1, 7N1 and so on
def try_baudrate(serialport_parameter:  str):

    new_serialport_parameter = slice_serialport_parameter (serialport_parameter)    
    for baudrate in baudrate_list:
        serialdata = open_port(baudrate, 
                              new_serialport_parameter[0], 
                              new_serialport_parameter[1], 
                              new_serialport_parameter[2])
        bytes_in_text = serialdata.decode(encoding='UTF-8', errors="ignore")
        display_text(baudrate, serialport_parameter, serialdata, bytes_in_text)

        validConnectionOption = estimate_connection_quality(bytes_in_text, 
                                                          serialdata)
        if validConnectionOption == True:
            connection_list.append((serialport_parameter, baudrate))

    

def slice_serialport_parameter (serialport_parameter_string: str):

    if len(serialport_parameter_string) > 3:
        print ('Paramemter to long: ', serialport_parameter_string)

    bytesize:int =  serialport_parameter_string[slice(1)] # ex. 8
    parity:str =    serialport_parameter_string[slice(1,2)] # ex. N
    stopbit:int =   serialport_parameter_string[slice(2,3)] # ex. 1
   
    return (bytesize, parity, stopbit)

##
# This functions trys to perform the same task as a human would do when each 
# connection would be checked manual. Screen, Minicom etc. would present the 
# data as UTF-8 encoded and this function use this property to check for the 
# following criteria:
#
# "text.encode() == serialData" checks if serial data bytes and UTF-8 encoded 
#  text are the same
# "(not text)" returns True for empty text, and needs be False in this 
#  application aka text is not empty
# "text.isprintable()" returns False for special characters
#
# If all the points above are fulfilled the serial properties like 
# baudrate etc. should be correct. 
##
def estimate_connection_quality(text: str, 
                              serialdata: bytes):

    if (text.encode() == serialdata) == True and (not text) == False and text.isprintable() == True:  
            print ('\n########### Connection probably ok #############\n')
            return True

def display_text (actual_baud: str, 
                 actual_serialport_parameter: str, 
                 serial_data: bytes, 
                 text: str): 
    
    print("Parameter: ", actual_serialport_parameter," | Baud:", 
          actual_baud, " bps")
    print("\n")
    print("Text (UTF-8):\t", text)
    print("Serial Data:\t", serial_data)
    print("\n")

def display_best_connection():

    counter_display_connection = 0 
    counter_sorting_baud = 0
    best_baudrate = 0
    best_combination_text = 0

    connection_list.sort()
    print("\n\t Found the following Settings:\n" )
    print("\n\t Serial Settings \t Baudrate\n" )
    while counter_display_connection < len(connection_list):
        print("\t", connection_list[counter_display_connection][0], "\t\t\t\t", 
              connection_list[counter_display_connection][1], "bps")
        counter_display_connection+=1
    
    while counter_sorting_baud < len(connection_list):
        if best_baudrate < connection_list[counter_sorting_baud][1]:
            best_baudrate = connection_list[counter_sorting_baud][1]
            best_combination_text =  str(connection_list[counter_sorting_baud][0]) 
            + " " + str(connection_list[counter_sorting_baud][1] + " bps")
        counter_sorting_baud+=1
    print("\n\n\tBest Connection:", best_combination_text)



def stop_program():

    input("\nPress any key to exit ...\n")
    exit

def return_duration ():

    estimatedTimeInMin = (len(baudrate_list)*len(serialport_settings_list)
                          *TIMEOUT_SERIAL_PORT_SEC) * 0.0166667 # 1s = 0.0166667 min
    return round(estimatedTimeInMin, 2)

##
#
# Checks if a Windows C drive is a avaidable under Linux and 
# rise warning for WSL (Windows-Subsystem for Linux)
#
##
def check_for_wsl():

        if (platform.platform()).__contains__('Linux'):
            test = os.popen('ls /mnt/c').read()
            if test.__contains__('Windows'):
                print("\n\n\n\t\tAttention: \n")
                print("\t\tIf you try to run the tool on WSL (Windows-Subsystem for Linux) please adjust the COM Port Parameter and use Windows.")
                print("\t\tThe script will fail at the moment for this constellation.")
                stop_program()
 
##
#
# Checks for the correct serial port under Windows
#
##
def check_for_windows():

        if (platform.platform()).__contains__('Windows') and SETTING_SERIAL_PORT.__contains__('COM') == False:
            print("\n\n\t\tPlease adjust the COM Port for Windows.")
            stop_program()

##
#
# Checks for the correct serial port under Linux
#
##
def check_for_linux():

        if (platform.platform()).__contains__('Linux') and SETTING_SERIAL_PORT.__contains__('COM') == True:
            print("\n\n\t\tPlease adjust the COM Port for Linux.")
            stop_program()
        
def main():

    srcipt_start_time = time.time()
    check_for_wsl()
    check_for_windows()
    check_for_linux()
    print ("\nUsed Serial Port: \n", SETTING_SERIAL_PORT, "\n")
    print ("Estimated Time: ", return_duration() , "min\n")
    for serial_setting in serialport_settings_list:
        try_baudrate (serial_setting)
    display_best_connection()    
    script_end_time = time.time()
    print("\nRuntime: ", round((script_end_time-srcipt_start_time) * 0.0166667, 2) , " min")  # 1s = 0.0166667 min
    stop_program ()

main()
