# Short Explanation

This script trys to perform the same task as a human would do when each connection would be checked manual.
Screen, Minicom etc. would present the data as UTF-8 encoded and this function use this property to check for the following criteria:

- "text.encode() == serialData" checks if serial data and UTF-8 encoded text are the same
- "(not text)" returns True for empty text
- "text.isprintable()" returns False for special characters

The core is this little function:

```
def estimateConnectionQuality(text: str, 
                              serialData: bytes):

    if (text.encode() == serialData) == True and (not text) == False and text isprintable() == True:  
            print ('\n########### Connection Properly ok #############\n')
            return True
```

If all the point above are fulfilled the serial properties like baudrate etc. should be correct. 


# Possible Options from pySerial 

It's based on pySerial. pySerial provides the following options:

```  
PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE = 'N', 'E', 'O', 'M', 'S'
 STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO = (1, 1.5, 2)
 FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS = (5, 6, 7, 8)
 PARITY_NAMES = {
     PARITY_NONE: 'None',
     PARITY_EVEN: 'Even',
     PARITY_ODD: 'Odd',
     PARITY_MARK: 'Mark',
     PARITY_SPACE: 'Space',
 }

````
# Assumption for running time

The port timeout at the moment is 10s, which at the moment determines the running time:

- 192 Combinations: 3xParity x 2xStopbit x 2xBitsize * 16 Baudrates * TimeoutPort ==> 32 min --> Should be good for most devices 

- 320 Combinations: 5xParity x 2xStopbit x 2xBitsize * 16 Baudrates * TimeoutPort ==> 50 min

- 960 Combinations: 5xParity x 3xStopbit x 4xBitsize * 16 Baudrates * TimeoutPort ==> 160 min

# Example for the summary

![image](https://user-images.githubusercontent.com/6764544/213922750-f3a0f364-29ab-41d8-aecc-505215173f65.png)

