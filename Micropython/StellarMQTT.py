# Asynchronous mqtt client with clean session (C) Copyright Peter Hinch 2017-2019.
# Released under the MIT licence.

# Public brokers https://github.com/mqtt/mqtt.github.io/wiki/public_brokers

# The use of clean_session means that after a connection failure subscriptions
# must be renewed (MQTT spec 3.1.2.4). This is done by the connect handler.
# Note that publications issued during the outage will be missed. If this is
# an issue see unclean.py.

# red LED: ON == WiFi fail
# blue LED heartbeat: demonstrates scheduler is running.



#Import libraries - config.py sets up wifi and mqtt
import time
from stellar import StellarUnicorn
from picographics import PicoGraphics, DISPLAY_STELLAR_UNICORN as DISPLAY

from mqtt_as import MQTTClient, config
from config import wifi_led, blue_led  # Local definitions
import uasyncio as asyncio
import machine
from machine import Pin, PWM
from time import sleep



# constants for controlling scrolling text
PADDING = 5
MESSAGE_COLOUR = (255, 255, 255)
OUTLINE_COLOUR = (0, 0, 0)
MESSAGE = ""
BACKGROUND_COLOUR = (0, 0, 0)
HOLD_TIME = 2.0
STEP_TIME = 0.045



# create Cosmic object and graphics surface for drawing
su = StellarUnicorn()
graphics = PicoGraphics(DISPLAY)
su.set_brightness(0.1)


width = StellarUnicorn.WIDTH -5
height = StellarUnicorn.HEIGHT
# state constants
STATE_PRE_SCROLL = 0
STATE_SCROLLING = 1
STATE_POST_SCROLL = 2

shift = 0
state = STATE_PRE_SCROLL

# set the font
graphics.set_font("bitmap8")

# calsulate the message width so scrolling can happen
msg_width = graphics.measure_text(MESSAGE, 1)

last_time = time.ticks_ms()


def yellowbox():
    graphics.set_pen(graphics.create_pen(255,255,0))

    graphics.rectangle(0, 0, 32, 32)
    graphics.set_pen(graphics.create_pen(255,255,255))


def redbox():
    graphics.set_pen(graphics.create_pen(255,0,0))
    graphics.rectangle(0, 0, 32, 32)
    
    
def bluebox():
    graphics.set_pen(graphics.create_pen(0,255,255))
    graphics.rectangle(0, 0, 32, 32)
    
def outline_text(text, x, y):
        graphics.set_pen(graphics.create_pen(int(OUTLINE_COLOUR[0]), int(OUTLINE_COLOUR[1]), int(OUTLINE_COLOUR[2])))
        graphics.text(text, x - 1, y - 1, -1, 1)
        graphics.text(text, x, y - 1, -1, 1)
        graphics.text(text, x + 1, y - 1, -1, 1)
        graphics.text(text, x - 1, y, -1, 1)
        graphics.text(text, x + 1, y, -1, 1)
        graphics.text(text, x - 1, y + 1, -1, 1)
        graphics.text(text, x, y + 1, -1, 1)
        graphics.text(text, x + 1, y + 1, -1, 1)

        graphics.set_pen(graphics.create_pen(int(MESSAGE_COLOUR[0]), int(MESSAGE_COLOUR[1]), int(MESSAGE_COLOUR[2])))
        graphics.text(text, x, y, -1, 1)
        

# MQTT Message Subscription and Display

def sub_cb(topic, msg, retained):
    print(f'Topic: "{topic.decode()}" Message: "{msg.decode()}" Retained: {retained}')
    
      
    # state constants
    su.set_brightness(0.5)
    STATE_PRE_SCROLL = 0
    STATE_SCROLLING = 1
    STATE_POST_SCROLL = 2

    shift = 0
    state = STATE_PRE_SCROLL
          
    DATA = (msg.decode('utf-8'))
    MESSAGE = str("          " + DATA + "          ")
  
    msg_width = graphics.measure_text(MESSAGE, 1)

    last_time = time.ticks_ms()
          

    print (MESSAGE)
    
    while True:
      
        time_ms = time.ticks_ms()


        if state == STATE_PRE_SCROLL and time_ms - last_time > HOLD_TIME * 1000:
            if msg_width + PADDING * 2 >= width:
                state = STATE_SCROLLING
            last_time = time_ms

        if state == STATE_SCROLLING and time_ms - last_time > STEP_TIME * 1000:
            shift += 1
            if shift >= (msg_width + PADDING * 2) - width - 1:
                state = STATE_POST_SCROLL
                brightness = 0
                su.set_brightness(brightness)
                su.update(graphics)
                break
            last_time = time_ms

        if state == STATE_POST_SCROLL and time_ms - last_time > HOLD_TIME * 1000:
            state = STATE_PRE_SCROLL
            shift = 0
            last_time = time_ms

        graphics.set_pen(graphics.create_pen(int(BACKGROUND_COLOUR[0]), int(BACKGROUND_COLOUR[1]), int(BACKGROUND_COLOUR[2])))
        graphics.clear()
        
      
        if "Time" in MESSAGE:
            yellowbox()
            outline_text(MESSAGE, x=PADDING - shift, y=4)
            
        elif "News" in MESSAGE:
            redbox()
            outline_text(MESSAGE, x=PADDING - shift, y=4)
            
        elif "Weather" in MESSAGE:
            
            bluebox()
            outline_text(MESSAGE, x=PADDING - shift, y=4)
            
        else:
            bluebox()
            outline_text(MESSAGE, x=PADDING - shift, y=4)
            

        # update the display
        su.update(graphics)

        # pause for a moment (important or the USB serial device will fail)
        time.sleep(0.001)
        
# Demonstrate scheduler is operational.
async def heartbeat():
    s = True
    while True:
        await asyncio.sleep_ms(500)
        blue_led(s)
        s = not s

async def wifi_han(state):
    wifi_led(not state)
    print('Wifi is ', 'up' if state else 'down')
   # sweep()
    await asyncio.sleep(1)

# If you connect with clean_session True, must re-subscribe (MQTT spec 3.1.2.4)
async def conn_han(client):
    
# MQTT Subscirbe Topic   
    await client.subscribe('personal/ucfnaps/led/#', 1)

async def main(client):
    try:
        await client.connect()
    except OSError:
        print('Connection failed.')
        machine.reset()
        return
    n = 0
    while True:
        await asyncio.sleep(5)
       # print('publish', n)
        # If WiFi is down the following will pause for the duration.
        #await client.publish('result', '{} {}'.format(n, client.REPUB_COUNT), qos = 1)
        n += 1

# Define confisuration
config['subs_cb'] = sub_cb
config['wifi_coro'] = wifi_han
config['connect_coro'] = conn_han
config['clean'] = True

# Set up client
MQTTClient.DEBUG = True  # Optional
client = MQTTClient(config)

asyncio.create_task(heartbeat())


try:
    asyncio.run(main(client))
    

finally:
    client.close()  # Prevent LmacRxBlk:1 errors
    asyncio.new_event_loop()