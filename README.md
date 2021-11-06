# nextrad-skippy-skips
Auhtor: Zidaan Habib

Command server application that contains MQTT broker for nextrad-linky-links, as well as control app.

## Installation:
1. Clone the repository
2. run pip3 install -r requirements.txt

## Running the application:
1. For first time use, start the MQTT broker by running *docker-compose up* in the root of the project
2. run *python3 main.py* to run the application from the project directory

Alternatively, once the docker image has been built, you can start the broker container from anywhere using *docker-compose up nextrad-skippy-skips_mosquitto_broker_1*
