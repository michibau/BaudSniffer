import serial
import serial.serialutil
import platform
import os

# TODO: Standalone Tool with Options as a next step
# TODO: Database with tested devices

## Global Var
globalSerialport = 'COM4' # For Linux: /dev/ttyS1 etc. ; For Windows: COM1 etc. 
globaelTimeout = 10 #dont change! - Timeout for searial port
globalByteSizetoRead = 10

connectionList = []

baudRateList = [
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
serialportSettingsList =[
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
#############

def openPort(baudSet: int, 
             bytesizeSet: int, 
             paritySet: str, 
             stopbitSet: int):

    newBytesizeSet = setBytsize(bytesizeSet)
    newParitySet = setParity(paritySet)
    newStopbitSet = setStopbit(stopbitSet)  

    try:
        ser = serial.Serial(globalSerialport, baudSet, newBytesizeSet, newParitySet, newStopbitSet, timeout=globaelTimeout)  # open serial port
        dataSerial = ser.read(globalByteSizetoRead) 
        ser.close()             # close port
        return dataSerial
    except serial.serialutil.SerialException:
        print ("serial.serialutil.SerialException rised")

def setStopbit(stopBit: str):

    if stopBit == "1":
        return serial.STOPBITS_ONE
    elif stopBit == "2":
        return serial.STOPBITS_TWO
    else:
        print ('Unsupported Stopbit (no Option): ', stopBit)

def setBytsize(byteSize: str):

    if byteSize == "8":
     return serial.EIGHTBITS
    elif byteSize == "7":
     return serial.SEVENBITS  
    elif byteSize == "6":
     return serial.SIXBITS  
    elif byteSize == "5":
     return serial.FIVEBITS
    else:
     print ('Unspupported Byte Size (no Option): ', byteSize) 

def setParity (parity: str):

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

def tryBaudrate(serialportParameter = str): # serial port parameter = 8N1, 7N1 and so on

    newSerialportParameter = sliceSerialportParameter (serialportParameter)    
    for baudrate in baudRateList:
        serialData = openPort(baudrate, newSerialportParameter[0], newSerialportParameter[1], newSerialportParameter[2])
        bytesInText = serialData.decode(encoding='UTF-8', errors="ignore")
        displayText(baudrate, serialportParameter, serialData, bytesInText)

        validConnectionOption = estimateConnectionQuality(bytesInText, serialData)
        if validConnectionOption == True:
            strBaudrate = str(baudrate)
            connectionList.append(strBaudrate + ' bps \t' + serialportParameter)

    

def sliceSerialportParameter (serialportParameterString: str):

    if len(serialportParameterString) > 3:
        print ('Wrong Serialport Paramemter (to long): ', serialportParameterString)

    bytesize:int =  serialportParameterString[slice(1)] # ex. 8
    parity:str =    serialportParameterString[slice(1,2)] # ex. N
    stopbit:int =   serialportParameterString[slice(2,3)] # ex. 1
   
    return (bytesize, parity, stopbit)

##
# This functions trys to perform the same task as a human would do when each connection would be checked manual.
# Screen, Minicom etc. would present the data as UTF-8 encoded and this function use this property to check for the following criteria:
#
# "text.encode() == serialData" checks if serial data and UTF-8 encoded text are the same
# "(not text)" returns True for empty text
# "text.isprintable()" returns False for special characters
#
# If all the point above are fulfilled the serial properties like baudrate etc. should be correct. 
##
def estimateConnectionQuality(text: str, 
                              serialData: bytes):

    if (text.encode() == serialData) == True and (not text) == False and text.isprintable() == True:  
            print ('\n########### Connection Properly ok #############\n')
            return True

def displayText (actualBaud: str, 
                 actualSerialportParameter: str, 
                 serialData: bytes, 
                 text: str): 
    
    print("Parameter: ", actualSerialportParameter," | Baud:", actualBaud, " bps")
    print("\n")
    print("Text (UTF-8):\t", text)
    print("Serial Data:\t", serialData)
    print("\n")

def displayBestConnection():
    # TODO: Improve List sorting. 
    connectionList.sort(reverse=True)
    print('Result List: (higher bps = better)\n\nBaud\t\tSerial Connection Propertys\n')
    for eachConnetion in connectionList:
        print (eachConnetion)

def pause():

    input("\nPress the <ENTER> key to exit or continue...\n")

def returnDuration ():
    estiamtedTimeInMin = (len(baudRateList)*len(serialportSettingsList)*globaelTimeout) * 0.0166667 # 1s = 0.0166667 min
    return round(estiamtedTimeInMin, 2)

##
#
# Checks if a Windows C drive is a avaidable under Linux and rise warning
#
##
def checkforWSL():
        if (platform.platform()).__contains__('Linux'):
            test = os.popen('ls /mnt/c').read()
            if test.__contains__('Windows'):
                print("\n\n\n\t\tAttention: \n")
                print("\t\tIf you try to run the tool on WSL (Windows-Subsystem for Linux) please adjust the COM Port Parameter and use Windows.")
                print("\t\tThe script will fail at the moment for this constellation.")
                pause()
 
##
#
# Checks for the correct COM port under Windows
#
##
def checkForWindows():
        if (platform.platform()).__contains__('Windows') and globalSerialport.__contains__('COM') == False:
            print("\n\n\t\tPlease adjust the COM Port for Windows.")
            pause()

##
#
# Checks for the correct COM port under Linux
#
##
def checkForLinux():
        if (platform.platform()).__contains__('Linux') and globalSerialport.__contains__('COM') == True:
            print("\n\n\t\tPlease adjust the COM Port for Linux.")
            pause()
        
def main():
    checkforWSL()
    checkForWindows()
    checkForLinux()
    print ("\nUsed Serial Port: \n", globalSerialport, "\n", flush=True)
    print ("Estimated Time: ", returnDuration() , "min\n")
    for serialSetting in serialportSettingsList:
        tryBaudrate (serialSetting)
    displayBestConnection()    
    pause ()
main()