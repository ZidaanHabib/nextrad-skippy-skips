from paho.mqtt import client as mqtt
from configparser import ConfigParser
from misc.ascii_art import STARTUP_MSG


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

    try:
        print("<< Establishing connection to MQTT broker... >> ")
        client.connect(host="mosquitto_broker", port=1883)
    except Exception as e:
        print(e)
        print("MQTT broker unreachable. Shutting down . . . ")


def control_loop():
    exit = False
    options = """ 1) Slew to GPS location \n 2) Adjust slew speed \n q) Quit. """
    while not exit:
        print(options)
        cmd = input("Enter a command: \n")

        if (cmd == 'q'):
            exit = True

def welcome():
    print(STARTUP_MSG)

if __name__ == "__main__":
    global client
    welcome()
    try:
        setup()
        client.loop_start()
    except:
        exit()

    
    control_loop()
