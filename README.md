# IoT exercise

The exercise consists of 3 parts:
 1. A python script running on a Raspberry Pi which reads two sensors and send the data to a MQTT broker and to a database (InfluxDB).
 2. A flow on Node-red wichs reads the data send by the Raspberry Pi through MQTT and plot some charts.
 3. A python program which reads the data from InfluxDB and saves it to a csv file.

To test the entire exercise:
 1. Run the python script on a terminal of the Raspberry Pi with the command `$ python3 Raspberry_Pi/sensors.py` and let it running.
 2. Open Node-red. In my case I run it in local `$ node-red-pi --max-old-space-size=256`. Import the project from the node_red folder and visualize the charts on the Node-red dashboard.
 3. Run the python program to read the database and store the data to a csv and check the file. The program have some options to select the time range of the data and the folder where the csv file will be stored, but you can run the programm with the default parameter with the command `$ python3 InfluxDB/influxdb_to_csv.py`.

Here we can see some **screenshots** done during the exercise.

Node-red flow
![2022-05-02-1651528255_screenshot_1920x1080](https://user-images.githubusercontent.com/90136459/166333474-e7bc03df-c702-4fed-a5dd-a881e1c389b9.jpg)

Node-red charts
![2022-05-02-1651515879_screenshot_1920x1080](https://user-images.githubusercontent.com/90136459/166333477-4024cb63-ddac-487d-9b06-84d7fa51c7d5.jpg)

InfluxDB sample of light sensors values
![2022-05-02-1651528003_screenshot_1920x1080](https://user-images.githubusercontent.com/90136459/166333479-abc886eb-c1ab-4374-a0b6-a24074926b42.jpg)

InfluxDB sample of distance sensors values
![2022-05-02-1651528014_screenshot_1920x1080](https://user-images.githubusercontent.com/90136459/166333481-8d92e504-5ee7-412b-a4d5-2aab9870690d.jpg)
