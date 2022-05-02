#####################################################
# Title: sensors.py				    #
# Description: Reads two sensors from the gpio's    #
# of the Raspberry Pi and send the values through   #
# MQTT and to InfluxDB				    #
# 						    #
# Author: David M.				    #
#####################################################

# ----- INCLUSIONS -----
import os
import time

# GPIO - SENSORS
from gpiozero import LightSensor, DistanceSensor

# MQTT
import paho.mqtt.client as mqtt
import ssl

# InfluxDB
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


# ----- CONSTANTS -----
PERIOD = 10  	# Every 5 seconds reads sensors and sents information

# GPIO
PIN_LIGHT_SENSOR = 17
PIN_DISTANCE_SENSOR_ECHO = 27
PIN_DISTANCE_SENSOR_TRIGGER = 22
MAX_DISTANCE = 2.0     # max distance in meters

# MQTT
MQTT_HOST = "node02.myqtthub.com"
MQTT_PORT = 8883
MQTT_CLEAN_SESSION = True
MQTT_CLIENT_ID = os.environ.get("MQTT_CLIENT_ID")
MQTT_USER_NAME = os.environ.get("MQTT_USER_NAME")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD")
MQTT_TOPIC = "mqtt/sensors"
MQTT_TOPIC_LIGHT = "mqtt/sensors/light"
MQTT_TOPIC_DISTANCE = "mqtt/sensors/distance"

# InfluxDB
INFLUX_TOKEN = os.environ.get("INFLUXDB_TOKEN")
INFLUX_ORG = "david_org"
INFLUX_BUCKET = "mqtt"
INFLUX_URL = "https://europe-west1-1.gcp.cloud2.influxdata.com"


# ----- FUNCTIONS -----
# MQTT
def on_connect(client, userdata, flags, rc):
    """ Callback called when connection/reconnection is detected """
    print("Connect %s result is: %s" % (MQTT_HOST, rc))

    if rc == 0:
        client.connected_flag = True
        print("connected OK")
        return

    print("Failed to connect to %s, error was, rc=%s" % (MQTT_HOST, rc))


# ----- MAIN FUNCTION -----
def main():
    # Initialization the sensors
    ldr = LightSensor(PIN_LIGHT_SENSOR)
    sensor = DistanceSensor(echo=PIN_DISTANCE_SENSOR_ECHO, trigger=PIN_DISTANCE_SENSOR_TRIGGER)

    # mqtt
    mqtt_client = mqtt.Client(client_id=MQTT_CLIENT_ID, clean_session=MQTT_CLEAN_SESSION)
    mqtt_client.username_pw_set(MQTT_USER_NAME, MQTT_PASSWORD)

    mqtt_client.on_connect = on_connect

    # configure TLS connection
    mqtt_client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)
    mqtt_client.tls_insecure_set(False)

    # connect using standard unsecure MQTT with keepalive to 60
    mqtt_client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    mqtt_client.connected_flag = False
    while not mqtt_client.connected_flag:  # wait in loop
    	mqtt_client.loop()
    	time.sleep(1)

    mqtt_client.loop_start()

    # InfluxDB
    influx_client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
    write_api = influx_client.write_api(write_options=SYNCHRONOUS)

    while True:
        if not mqtt_client.is_connected():
            print("Reconnect mqtt client")
            mqtt_client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
            mqtt_client.loop_start()

        # Read sensors
        light = ldr.value
        distance = sensor.distance * 100 * MAX_DISTANCE

        # Accommodate data to MQTT
        msg = """{"light": %s, "distance": %s}""" % (light, distance)
        print("Publishing %s -> %s" % (MQTT_TOPIC, msg))

        # Accommodate data to InfluxDB
        influx_data = [
            Point("sensors").field("light", light),
            Point("sensors").field("dist", distance)]

        # Sent MQTT
        mqtt_client.publish(MQTT_TOPIC, msg)

        # Sent InfluxDB
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=influx_data, write_precision=WritePrecision.S)

        time.sleep(PERIOD)

    client.loop_stop()


if __name__ == '__main__':
    main()
