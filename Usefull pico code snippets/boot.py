from machine import Pin
# Turn on the onboard LED to signal startup completed
led_onboard = Pin(25, Pin.OUT).high()