import pyautogui, sys, pynput
from time import sleep
import math
print('Press ESC to quit.')


config = {
    "mouse_at": [],
    "frequency": 0,
    "wait_time": 0,
    "running": True,
    "max_taps": 0,
    "current_taps": 0,
    "coin_per_click": 0,
    "additional_clicks": 0,
    "pointed": False,
}

max_amount, current_taps, coin_per_click, frequency = map(float, input("[MAX AMOUNT] [CURRENT TAPS] [COINS PER TAP] [FREQUENCY]:\n\te.g: |4000 3250 5 0.08|  ~> ").split(" "))

def calculate(max_amount, current_taps, coin_per_click, frequency):
    config["max_taps"] = max_amount
    config["current_taps"] = int(current_taps)
    config["coin_per_click"] = coin_per_click
    config["frequency"] = frequency
    config["wait_time"] = math.ceil(config["max_taps"]/3)
    config["additional_clicks"] = math.ceil(current_taps / coin_per_click*frequency*3) + round(current_taps*15/100)
calculate(max_amount=max_amount, current_taps=current_taps, coin_per_click=coin_per_click, frequency=frequency) 

state = 100
def moving():
    global state
    state *= -1
    changed = config["mouse_at"][0] + state
    pyautogui.moveTo(x=changed, y=config["mouse_at"][1])

def point(key):
    if key == pynput.keyboard.Key.ctrl_l:
        print("Pointed!")
        x, y = pyautogui.position()
        
        config["mouse_at"] = [x, y]
        config["pointed"] = True
        put_point.stop()

def start():
    wait_for_point()
    count = 0
    amount = config["current_taps"]+config["additional_clicks"]
    while config["running"]:
        if count >= amount:
            sleep(config["wait_time"])
            count = 0
        pyautogui.click(button="left", interval=config["frequency"])
        moving()
        count += config["coin_per_click"]
    
def cancel_loop(key):
    
    if key == pynput.keyboard.Key.shift_l:
        config["running"] = False;
        print("Terminated by user!")
        sys.exit(1)

def wait_for_point():
    while config["pointed"] != True:
        pass

wait_calcelling = pynput.keyboard.Listener(on_release=cancel_loop) #, on_press=click)
put_point = pynput.keyboard.Listener(on_release=point)

# run listener in background so that the while loop gets executed
put_point.start()
wait_calcelling.start()

start()


wait_calcelling.stop()