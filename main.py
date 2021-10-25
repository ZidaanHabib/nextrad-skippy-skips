from paho.mqtt import client as mqtt
from configparser import ConfigParser
from misc.ascii_art import STARTUP_MSG
import sys


""" MQTT client callbacks:"""
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(" << Connection OK. >>")
    else:
        print("Connection failed with response code " + str(rc))
    client.subscribe("test")


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
        client.connect(host="mosquitto_broker", port=1883)
    except Exception as e:
        print(e)
        print("MQTT broker unreachable. Shutting down . . . ")


def control_loop():
    exit = False
    options = """ 1) Slew to GPS location \n 2) Slew to azimuth, elevation \n 3) Adjust slew speed \n q) Quit. """
    while not exit:
        print(options)
        cmd = input("Enter a command: \n")

        if (cmd == "1"):
            slew_to_location()
        
        elif (cmd == "2"):
            slew_to_az_el()

        elif (cmd == 'q'):
            exit = True
            print("See ya!")

def welcome():
    print(STARTUP_MSG)

def slew_to_location():
    target_lat = eval(input("Enter target latitude in degrees. Valid range[-90,90] (eg. -77.342 ) \n"))
    target_long = eval(input("Enter target longitude in degrees (eg. -65.342 ) \n"))
    # TODO send lat and long to client side

def slew_to_az_el():
    az_string = ""
    el_string = ""
    while not( az_string.isnumeric() ): 
        try:
            az_string = (input("Enter target azimuth in degrees [-180, 180] \n"))
            target_az = float(az_string)
        except:
            print("Invalid number. ")
    while not ( el_string.isnumeric()):
        try:
            el_string = (input("Enter target elevation in degrees [-180, 180] \n"))
            target_el = float(el_string)
        except:
            print("Invalid number. ")
        
    print("<<< Slewing to {}, {} >>> \n".format(target_az, target_el))
    # TODO send az and el to client side

if __name__ == "__main__":
    global client
    welcome()
    try:
        setup()
        
    except:
        sys.exit(1)

    
    control_loop()
