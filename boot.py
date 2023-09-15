# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import wifi
wifi.do_connect()
import webrepl
# webrepl.start()
webrepl.start(password='1234')
# import webpage