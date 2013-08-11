#!/usr/bin/python

# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from time import sleep
import os
import datetime

class HD44780:

    def __init__(self, pin_rs=26, pin_e=24, pins_db=[22, 18, 16, 12]):					   #RS = 26, E = 24, Data = 22, 18, 16, 12 (I used 4-bit mode) Refer to LMB162ABC datasheet for LCD pins.
        sleep(0.1)
        GPIO.setwarnings(False)
        self.pin_rs=pin_rs
        self.pin_e=pin_e
        self.pins_db=pins_db

        GPIO.setmode(GPIO.BOARD)														   #Use board GPIO numbering
        GPIO.setup(self.pin_e, GPIO.OUT)
        GPIO.setup(self.pin_rs, GPIO.OUT)
        for pin in self.pins_db:
            GPIO.setup(pin, GPIO.OUT)

        self.clear()

    def clear(self):
        """ Blank / Reset LCD """

        self.cmd(0x33) 																		#$33 8-bit mode
        self.cmd(0x32) 																		#$32 8-bit mode
        self.cmd(0x28) 																		#$28 8-bit mode
        self.cmd(0x0C) 																		#$0C 8-bit mode
        self.cmd(0x06) 																		#$06 8-bit mode
        self.cmd(0x01) 																		#$01 8-bit mode

    def cmd(self, bits, char_mode=False):
        """ Send command to LCD """

        
        bits=bin(bits)[2:].zfill(8)

        GPIO.output(self.pin_rs, char_mode)

        for pin in self.pins_db:
            GPIO.output(pin, False)

        for i in range(4):
            if bits[i] == "1":
                GPIO.output(self.pins_db[::-1][i], True)

        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)

        for pin in self.pins_db:
            GPIO.output(pin, False)

        for i in range(4,8):
            if bits[i] == "1":
                GPIO.output(self.pins_db[::-1][i-4], True)


        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)

        sleep(0.0015)

    def message(self, text):																#Send string to LCD.
        for char in text:
            if char == '\n':
                self.cmd(0xC0) # next line
            else:
                self.cmd(ord(char),True)

if __name__ == '__main__':

    def getCPUTemp():
        res = os.popen('vcgencmd measure_temp').readline()
        return(res.replace("temp=","").replace("'C\n",""))


    lcd = HD44780()
    
    def display_CPU_Temp():																	#Display Raspberry Pi CPU temperature in an endless loop. (Example: CPU Temperature '\n' 34.7 'degree symbol' C)
        while True:
            lcd.message("CPU Temperature:\n")
            lcd.message(getCPUTemp())
            lcd.message(" ")
            lcd.message(chr(223))
            lcd.message("C")
            sleep(0.5)																		#Update temperature every 0.5 seconds.
            lcd.clear()

    def display_Date_Time():																#Display date and time in an endless loop. (Example: 11/08/2013 '\n' 10:44:38 Sunday '\n' 11 August 2013)
        b = True
        while True:
            if b == True:
                for s in range(0, 20):
                    lcd.message(datetime.datetime.now().strftime('%d/%m/%Y'))
                    lcd.message("\n")
                    lcd.message(datetime.datetime.now().strftime('%H:%M:%S'))
                    sleep(0.25)																#Update time every 0.25 seconds.
                    lcd.clear()
                b = False
            elif b == False:
                lcd.message(datetime.datetime.now().strftime('%A'))
                lcd.message("\n")
                lcd.message(datetime.datetime.now().strftime('%d %B %Y'))
                sleep(5)
                lcd.clear()
                b = True
                 
            
	#Example usage (Uncomment to test, one function at a time for best results)
	
    #display_CPU_Temp()
	#display_Date_Time()

