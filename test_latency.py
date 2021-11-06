from paho.mqtt import client as mqtt
import time

""" MQTT client callbacks:"""
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(" << Connection OK. >>")

    else:
        print("Connection failed with response code " + str(rc))


def on_log(client, userdata, level, buf):
    print("log:" + buf)




def on_message(client, userdata, msg_enc) -> str:
    msg = msg_enc.payload.decode("UTF-8")
    print("Message received: " + msg)
    return msg

def main():
    global client
    client = mqtt.Client("Command-server", protocol=mqtt.MQTTv31)
    client.on_connect = on_connect
    #client.on_log = on_log
    client.on_message = on_message
    client.loop_start()

    try:
        print("<< Establishing connection to MQTT broker... >> ")
        client.connect(host="localhost", port=1883)
    except Exception as e:
        print(e)
        print("MQTT broker unreachable. Shutting down . . . ")

if __name__ == "__main__":
    global client
    main()
    time.sleep(3)

    for i in range(50):
        time_rec = time.time()
        time_str = str(time_rec)
        client.publish("Pi-1", "TIMING-TEST/{}".format(time_str))
        time.sleep(0.2)
    """try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Exiting")"""
    """time_rec = time.time()
    time_str = str(time_rec)
    print("Sending timestamp...")
    client.publish("Pi-1", "TIMING-TEST/{}".format(time_str))
    print("Sent")
    time.sleep(0.1)"""
