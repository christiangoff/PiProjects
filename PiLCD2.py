import RPi.GPIO as GPIO
import time

E_PULSE = 0.0005
E_DELAY = 0.0005

LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0

class newLCD:
    def __init__(self, width, height, LCD_E, LCD_RS, LCD_D4, LCD_D5, LCD_D6, LCD_D7):
        self.width = width
        self.height = height
        self.E = LCD_E
        self.RS = LCD_RS
        self.D4 = LCD_D4
        self.D5 = LCD_D5
        self.D6 = LCD_D6
        self.D7 = LCD_D7
   
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
        GPIO.setup(LCD_E , GPIO.OUT)  
        GPIO.setup(LCD_RS, GPIO.OUT) 
        GPIO.setup(LCD_D4, GPIO.OUT) 
        GPIO.setup(LCD_D5, GPIO.OUT) 
        GPIO.setup(LCD_D6, GPIO.OUT) 
        GPIO.setup(LCD_D7, GPIO.OUT) 

        self.lcd_init()
        
    def test(self):
        print(self.E)
        print(E_PULSE)
        
    def lcd_init(self):
        self.lcd_byte(0x33,LCD_CMD) # 110011 Initialise
        self.lcd_byte(0x32,LCD_CMD) # 110010 Initialise
        self.lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
        self.lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
        self.lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
        self.lcd_byte(0x01,LCD_CMD) # 000001 Clear display
        time.sleep(E_DELAY)
         
    def lcd_byte(self,bits, mode):
        # Send byte to data pins
        # bits = data
        # mode = True  for character
        #        False for command

        GPIO.output(self.RS, mode) # RS

        # High bits
        GPIO.output(self.D4, False)
        GPIO.output(self.D5, False)
        GPIO.output(self.D6, False)
        GPIO.output(self.D7, False)
        if bits&0x10==0x10:
            GPIO.output(self.D4, True)
        if bits&0x20==0x20:
            GPIO.output(self.D5, True)
        if bits&0x40==0x40:
            GPIO.output(self.D6, True)
        if bits&0x80==0x80:
            GPIO.output(self.D7, True)

        # Toggle 'Enable' pin
        self.lcd_toggle_enable()

        # Low bits
        GPIO.output(self.D4, False)
        GPIO.output(self.D5, False)
        GPIO.output(self.D6, False)
        GPIO.output(self.D7, False)
        if bits&0x01==0x01:
            GPIO.output(self.D4, True)
        if bits&0x02==0x02:
            GPIO.output(self.D5, True)
        if bits&0x04==0x04:
            GPIO.output(self.D6, True)
        if bits&0x08==0x08:
            GPIO.output(self.D7, True)

          # Toggle 'Enable' pin
        self.lcd_toggle_enable()

    def lcd_toggle_enable(self):
          # Toggle enable
        time.sleep(E_DELAY)
        GPIO.output(self.E, True)
        time.sleep(E_PULSE)
        GPIO.output(self.E, False)
        time.sleep(E_DELAY)

    def lcd_string(self,message,line):
      # Send string to display

        message = message.ljust(self.width," ")

        self.lcd_byte(line, LCD_CMD)

        for i in range(self.width):
            self.lcd_byte(ord(message[i]),LCD_CHR)

    def writeFullLine(self,message,line):
        if line == 0:
            self.lcd_string(message, LCD_LINE_1)
        elif line == 1:
            self.lcd_string(message, LCD_LINE_2)
        else:
            pass
        
    def setCursor(self, col, row):
        self.rowOffsets = [0x00, 0x40]
        if row > self.height:
            row = self.height - 1
        self.lcd_byte(0x80 | (col + self.rowOffsets[row]),LCD_CMD)

    def write(self,message, row, col):
        for i in range(0,len(message)):
            self.setCursor(col, row)
            self.lcd_byte(ord(message[i]), True)
            col+=1

    def clear(self):
        self.lcd_byte(0x01,LCD_CMD)
            
    def scrollMessage(self,message, row, seconds):
        if row <= self.height:
            for i in range(0,len(message)+1):
                self.writeFullLine(message[i:(i+16)],row)
                time.sleep(seconds)
            self.writeFullLine(message)
        

    

            
