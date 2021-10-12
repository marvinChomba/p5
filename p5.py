import time
import busio
import digitalio
import board
import threading
import RPi.GPIO as GPIO
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
ldr_chan = None
temp_chan = None
sample_btn = 17
sample_rate = 1
timer = 0


def temp_ldr_thread():
    global sample_rate

    """
    Takes the readings and prints afer every [sample_rate]s
    """
    thread = threading.Timer(sample_rate, temp_ldr_thread)
    thread.daemon = True
    thread.start()

    # get the current elapsed time from the timer start
    time_elapsed = (time.time() - timer)

    # get the readings from the components
    tempReading = temp_chan.value
    temp = (temp_chan.voltage - 0.5) * 100
    lightReading = ldr_chan.value

    # to_print = [runtime,"       ",tempReading,"       ",temp,"       ",lightReading]
    # print(*to_print)

       # print the readings in a readable format
       #print(lightReading)
    print("{:<20} {:<20} {:<20} {:<20}".format(str(round(time_elapsed)) + "s",tempReading,str(round(temp,2)) + "C",lightReading))

def btn_press(channel):
    global sample_rate

    # change the sampling rate depending on the previous rate
    if(sample_rate == 1):
        sample_rate = 5
    elif(sample_rate == 5):
        sample_rate = 10
    elif(sample_rate == 10):
        sample_rate = 1
    
    print("Sample rate will change to {}s".format(sample_rate))

def setup():
    global ldr_chan
    global temp_chan
    # create the spi bus
    spi = busio.SPI( clock = board.SCK, MISO = board.MISO, MOSI =
    board.MOSI )
    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)
    # create the mcp object
    mcp = MCP.MCP3008( spi, cs )
    # create analog input channels on pins 0 and 1
    ldr_chan = AnalogIn( mcp, MCP.P0)
    temp_chan = AnalogIn( mcp, MCP.P1)
    # setup sample rate button
    GPIO.setup(sample_btn, GPIO.IN)
    GPIO.setup(sample_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(sample_btn, GPIO.FALLING,
    callback=btn_press_handler, bouncetime=400)



if __name__ == "__main__":
    try:
        setup() 
        timer = time.time()
        #start the timer
        # to_print = ["Runtime"," ","Temp Reading","","Temp"," ","Light Reading"]
        # print(*to_print)
        print("{:<20} {:<20} {:<20} {:<20}".format("Runtime","Temp Reading","Temp","Light Reading"))
        temp_ldr_thread()
        while True:
            pass
        except Exception as e:
            print(e)
        finally:
            GPIO.cleanup()
