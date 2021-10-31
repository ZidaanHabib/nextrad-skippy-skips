from paho.mqtt import client as mqtt
from configparser import ConfigParser
from misc.ascii_art import STARTUP_MSG
from misc.options import OPTIONS_MENU
import sys


""" MQTT client callbacks:"""
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(" << Connection OK. >>")
    else:
        print("Connection failed with response code " + str(rc))
    client.subscribe("Pi-1/Responses")


def on_log(client, userdata, level, buf):
    print("log:" + buf)


def on_subscribe(client, userdata, mid, granted_qos):
    print("<<Subscription  successful.>>")


def on_message(client, userdata, msg_enc) -> str:
    msg = msg_enc.payload.decode("UTF-8")
    print("Message received: " + msg)
    return msg


def setup():
    global client
    client = mqtt.Client("Command-server", protocol=mqtt.MQTTv31)
    client.on_connect = on_connect
    #client.on_log = on_log
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.loop_start()

    try:
        print("<< Establishing connection to MQTT broker... >> ")
        client.connect(host="localhost", port=1883)
    except Exception as e:
        print(e)
        print("MQTT broker unreachable. Shutting down . . . ")


def control_loop():
    exit = False
    options = OPTIONS_MENU
    while not exit:
        print(options)
        cmd = input("Enter a command: \n")

        if cmd == "1":
            calibrate()
        elif (cmd == "2"):
            slew_to_location()
        elif (cmd == "3"):
            slew_to_az_el()
        elif (cmd == 'q'):
            exit = True
            print("See ya!")
        elif (cmd == "4"):
            slew()
        elif cmd == "5":
            sweep()
        elif cmd == "6":
            stop()
        elif cmd == "7":
            set_slew_rate()
        elif cmd == "8":
            set_az_limits()

def welcome():
    print(STARTUP_MSG)

def calibrate():
    client.publish("Pi-1", "CALIB")

def slew_to_location():
    lat_string = ""
    long_string = ""
    alt_string = ""

    while not(lat_string.isnumeric()): 
        try:
            lat_string = (input("Enter target latitude in degrees [-90, 90] \n"))
            target_lat = float(lat_string)
        except ValueError as e:
            print("Invalid number. ")
    while not(long_string.isnumeric()): 
        try:
            long_string = (input("Enter target longitude in degrees [-180, 180] \n"))
            target_long = float(long_string)
        except ValueError as e:
            print("Invalid number. ")
    while not(alt_string.isnumeric()): 
        try:
            alt_string = (input("Enter altitude in meters\n"))
            target_alt = float(alt_string)
        except ValueError as e:
            print("Invalid number. ")
    print("<<< Slewing to Lat:{}, Long:{}, Alt:{} m >>> \n".format(target_lat, target_long, target_alt))
    client.publish("Pi-1", "GOTO-LOC/{}/{}/{}".format(target_lat, target_long, target_alt))

def slew_to_az_el():
    az_string = ""
    el_string = ""
    while not( az_string.isnumeric() ): 
        try:
            az_string = (input("Enter target azimuth in degrees [-180, 180] \n"))
            target_az = float(az_string)
        except ValueError as e:
            print("Invalid number. ")
    while not ( el_string.isnumeric()):
        try:
            el_string = (input("Enter target elevation in degrees [-180, 180] \n"))
            target_el = float(el_string)
        except ValueError as e:
            print("Invalid number.")
        
    print("<<< Slewing to {}, {} >>> \n".format(target_az, target_el))
    # TODO send az and el to client side
    client.publish("Pi-1", "GOTO-AZEL/{}/{}".format(target_az, target_el))

def slew():
    valid = ["l", "r", "u", "d"]
    cmd = ""
    while cmd not in valid:
        cmd = input("Direction (l,r,d,u):\n")
    axis, dir = "", ""
    if cmd == "l":
        axis, dir = "AZ", "POS"
    elif cmd == "r":
        axis, dir = "AZ", "NEG"
    elif cmd == "u":
        axis, dir = "EL","POS"
    else:
        axis, dir = "EL", "NEG"

def sweep():
    client.publish("Pi-1", "SWEEP")

def stop():
    client.publish("Pi-1", "STOP")

def set_slew_rate():
    rate_str = ""
    rate = 0
    while not rate_str.isnumeric():
        try:
            rate_str = input("Enter slew rate:\n")
        except ValueError as e:
            print("Invalid number.")
    client.publish("Pi-1", "SET-SR/{}".format(rate_str))

def set_az_limits():
    min = ""
    while not min.isnumeric() or float(min) not in range(-180, 180):
        try:
            min = input("Enter min azimuth [-180, 180]:\n")
        except ValueError as e:
            print("Invalid number.")
    max = ""
    while not max.isnumeric() or float(max) not in range(-180, 180):
        try:
            max = input("Enter max azimuth in range [-180, 180]:\n")
        except ValueError as e:
            print("Invalid number.")
    client.publish("Pi-1", "SET-AZ-LIM/{}/{}".format(min, max))

def set_el_limits():
    min = ""
    while not min.isnumeric() or float(min) not in range(-180, 180):
        try:
            min = input("Enter min elevation [-180, 180]:\n")
        except ValueError as e:
            print("Invalid number.")
    max = ""
    while not max.isnumeric() or float(max) not in range(-180, 180):
        try:
            max = input("Enter max elevation in range [-180, 180]:\n")
        except ValueError as e:
            print("Invalid number.")
    client.publish("Pi-1", "SET-EL-LIM/{}/{}".format(min, max))

if __name__ == "__main__":
    global client
    welcome()
    try:
        setup()
        
    except:
        sys.exit(1)

    
    control_loop()
