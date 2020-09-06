import neopixel
import time
import machine
import network
import utime
import ntptime
import wifi

utc_shift = 3 #задать дельту временной зоны
startTime = time.ticks_ms()
wifissid2 = 'Tensor'
wifipassword2 = '87654321'
wifissid1 = 'Tomato24'
wifipassword1 = '77777777'
rtc = machine.RTC()
tcounter = 0
main_timer1 = machine.Timer(2)
uart = machine.UART(1, 9600)
uart.init(9600, bits=8, parity=None, stop=1)

COLOR = (0, 0, 0)
np = neopixel.NeoPixel(machine.Pin(2), 8)

class ZeroDivisionError(Exception):
    def init(self, message):
        super().init(message)
class NameError(Exception):
    def init(self, message):
        super().init(message)
class PasswordError(Exception):
    def init(self, message):
        super().init(message)

def for_range():
    for i in range (8):
        np[i] = COLOR
        np.write()
        i += 1
        time.sleep(0.1)
for_range()
def nice_wait():
    x = 0
    y = 5
    z = 9
    COLOR2 = (0, 0, 0)
    while True:
        for i in range (8):
            np[i] = COLOR2
            time.sleep_ms(100)
            COLOR2 = (x, y, z)
            x += 1
            y += 0
            z += 0
            uart.write("x")   # write the 3 characters
            if x > 20:
                x = 0
            if y > 20:
                y = 0
            if z > 20:
                z = 0
            np.write()
nice_wait()
def disconnect():
    station = network.WLAN(network.STA_IF)
    if station.active():
        station.disconnect()
        station.active(False)
        oled.text('disconnected!', 0, 30)
        time.sleep(1)
        oled.fill(0)
        time.sleep(1)
def log(logs):
    oled.fill(0)
    oled.text(logs, 0, 50)
    oled.show()
    time.sleep(1)
def connect(ssid, password):
    station = network.WLAN(network.STA_IF) 
    if not station.active():
        station.active(True) 
    if station.isconnected():
        tuple1 = station.ifconfig()
        ipold = tuple1[0]
        return ipold
    try:
        station.connect(ssid, password)
        time.sleep(3)
        while station.isconnected() == False:
            if time.ticks_diff(time.ticks_ms(), startTime) > 15000:
                raise PasswordError('Неверный пароль')
            #log(str(time.ticks_diff(time.ticks_ms(), startTime)))
            log('try wifi #1...')
        tuple1 = station.ifconfig()
        ipnew = tuple1[0]
        return ipnew
    except PasswordError:
        time.sleep_ms(1000)
        log("wrong pass")
        log("try wifi #2...")
        iperr = '127.0.0.1' 
        return iperr
def sync_time():        #пробуем синхронизировать время
    try:
        ntptime.settime()
        #oled.fill(0)
        #oled.show()
        #oled.text('sync is succesful', 0, 10)
        #oled.show()
        time.sleep(1)
    except Exception as ex:
        #oled.fill(0)
        #oled.show()
        #oled.text('something went wrong', 0, 10)
        #oled.show()
        time.sleep(15)
    else:
        #oled.fill(0)
        #oled.text('OK', 0, 10)
        oled.show()
        time.sleep(1)
    finally:
        #oled.fill(0)
        #oled.text('OK!', 0, 10)
        oled.show()
        time.sleep(1)
    
    tm = utime.localtime(utime.mktime(utime.localtime()) + utc_shift*3600)
    tm = tm[0:3] + (0,) + tm[3:6] + (0,)
    rtc.datetime(tm)
def tcb(timer):         #функция, выполняющаяся по коллбэку таймера
    update_oled()
    global tcounter
    if tcounter & 1:
        p1.value(0)
    else:
        p1.value(1)
    tcounter += 1
    if (tcounter % 10000) == 0:
        print("[tcb] timer: {} counter: {}".format(timer.timernum(), tcounter))
'''
try:
    ip = str(connect(wifissid1, wifipassword1))
    if ip == '127.0.0.1':
        ip = str(connect(wifissid2, wifipassword2))
except Exception as e:
    print('could not connect to wifi {}{}'.format(type(e).__name__, e))
    sys.exit()
'''

