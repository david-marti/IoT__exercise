# Raspberry Pi
A python script to be run on the Raspberry Pi, which performs a basic example of an IoT device.
 - Read two sensors (in this case, a LDR and a distance sensor)
 - Sent the values through MQTT (Free online broker)
 - Sent the values to InfluxDB (InfluxDB Cloud)

Run this script executing the next command and let it running.

```$ python3 sensors.py```


Note: You may need to install the python packages: python-gpiozero, paho-mqtt, influxdb-client
 
