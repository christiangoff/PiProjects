# PiProjects
A Collection of Raspberry Pi projects

#PiLCD2 

PiLCD2 is a library for driving a 16x9 LCD on a Raspberry Pi
required libraries are time and RPi.GPIO

There is no set pin usage so you are free to connect any pins from your Pi to the LCD Screen.
Pin declaration is done during the initial Object creation.

There will be future updates for driving larger LCD screens but right now this is set up for 16X2 only

###
Functions
###

newLCD(self, width, height, LCD_E, LCD_RS, LCD_D4, LCD_D5, LCD_D6, LCD_D7)
creates an instance of the LCD Screen and initializzes it.

ex: myLCD = PiLCD2.newLCD(16, 2, 25, 24, 19, 20, 21, 22)
    this creates a new LCD Object using the following pin configuration on the LCD
    Enable (E)           -> Pi Pin 25
    Register Select (RS) -> Pi Pin 24
    Data 4               -> Pi Pin 19
    Data 5               -> Pi Pin 20
    Data 6               -> Pi Pin 21
    Data 7               -> Pi Pin 22
    
This setup can be changed to meet you Pi Setup but make sure you put the right pin numbers in the init method.
Data regarding the LCD pinout is easily available.

writeFullLine(message, line)
this will take any string, and fill the line(row) with training " " to fill it out.  
Any characters past the first 16 will not show up. Remember rows are either 0 or 1.

write(message, row, col)
will write your string (message) to the point on the LCD identified by (row,col)

scrollMessage(message, row, seconds)
if you have a string that is too long for the LCD screen, use this function to scroll your message on the screen on the identified row.
the 'seconds' parameter determines the delay between scroll ticks.
