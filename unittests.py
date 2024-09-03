import BaudSniffer
import unittest
import serial 

class Test_stopbit(unittest.TestCase):
    def test_set_stopbit_1(self):
        stop_bit = "1"
        test = BaudSniffer.set_stopbit(stop_bit)
        self.assertEqual(test, serial.STOPBITS_ONE)
    def test_set_stopbit_2(self):
        stop_bit = "2"
        test = BaudSniffer.set_stopbit(stop_bit)
        self.assertEqual(test, serial.STOPBITS_TWO)
    def test_set_stopbit_wrong(self):
        stop_bit = "3"
        test = BaudSniffer.set_stopbit(stop_bit)
        self.assertEqual(test, None)

class Test_set_bytesize(unittest.TestCase):
    def test_set_bytesize_5(self):
        bytesize = "5"
        test = BaudSniffer.set_bytesize(bytesize)
        self.assertEqual(test, serial.FIVEBITS)
    def test_set_bytesize_6(self):
        bytesize = "6"
        test = BaudSniffer.set_bytesize(bytesize)
        self.assertEqual(test, serial.SIXBITS) 
    def test_set_bytesize_7(self):
        bytesize = "7"
        test = BaudSniffer.set_bytesize(bytesize)
        self.assertEqual(test, serial.SEVENBITS)   
    def test_set_bytesize_8(self):
        bytesize = "8"
        test = BaudSniffer.set_bytesize(bytesize)
        self.assertEqual(test, serial.EIGHTBITS)   
    def test_set_bytesize_wrong(self):
        bytesize = "9"
        test = BaudSniffer.set_bytesize(bytesize)
        self.assertEqual(test, None)

class Test_set_parity(unittest.TestCase):
    def test_set_parity_N(self):
        parity = "N"
        test = BaudSniffer.set_parity(parity)
        self.assertEqual(test, serial.PARITY_NONE)
    def test_set_parity_E(self):
        parity = "E"
        test = BaudSniffer.set_parity(parity)
        self.assertEqual(test, serial.PARITY_EVEN)
    def test_set_parity_O(self):
        parity = "O"
        test = BaudSniffer.set_parity(parity)
        self.assertEqual(test, serial.PARITY_ODD)
    def test_set_parity_M(self):
        parity = "M"
        test = BaudSniffer.set_parity(parity)
        self.assertEqual(test, serial.PARITY_MARK)
    def test_set_parity_S(self):
        parity = "S"
        test = BaudSniffer.set_parity(parity)
        self.assertEqual(test, serial.PARITY_SPACE)
    def test_set_parity_wrong(self):
        parity = "Q"
        test = BaudSniffer.set_parity(parity)
        self.assertEqual(test, None)

if __name__ == '__main__':
    unittest.main()