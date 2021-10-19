from paho.mqtt import client as mqtt
from configparser import ConfigParser
from misc.ascii_art import STARTUP_MSG

def main():
    print("hello world")

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
    welcome()
    control_loop()