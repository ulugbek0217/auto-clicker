import pyautogui, sys, pynput
from time import sleep
import math
print('Press ESC to quit.')


config = {
    "mouse_at": [],
    "frequency": 0.2,
    "wait_time": 0,
    "running": True,
    "tap_limit": 0,
    "coin_per_click": 0,
    "clicks_count": 0,
    "pointed": False,
}

tap_limit, coin_per_click = map(int, input("Enter the tap limit and coin per click separated by a space:\n\te.g: |4000 5|  ~> ").split(" "))

def calculate(tap_limit, coin_per_click):
    config["tap_limit"] = tap_limit
    config["coin_per_click"] = coin_per_click
    config["wait_time"] = math.ceil(tap_limit/3)
calculate(tap_limit=tap_limit, coin_per_click=coin_per_click) 


def point(key):
    if key == pynput.keyboard.Key.ctrl:
        print("Pointed!")
        x, y = pyautogui.position()
        config["mouse_at"] = [x, y]
        config["pointed"] = True

def start():
    wait_for_point()
    count = 0
    while config["running"]:
        if count >= config["tap_limit"]:
            sleep(config["wait_time"])
        pyautogui.click(x=config["mouse_at"][0], y=config["mouse_at"][1], button="left", interval=config["frequency"])
        count += config["coin_per_click"]
    
def cancel_loop(key):
    
    if key == pynput.keyboard.Key.esc:
        config["running"] = False;
        print("Terminated by user!")

def wait_for_point():
    while config["pointed"] != True:
        # print("waiting pointing")
        pass

wait_calcelling = pynput.keyboard.Listener(on_release=cancel_loop) #, on_press=click)
put_point = pynput.keyboard.Listener(on_release=point)
put_point.start()

# run listener in background so that the while loop gets executed
wait_calcelling.start()

start()

put_point.stop()
wait_calcelling.stop()


