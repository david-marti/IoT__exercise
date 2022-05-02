# InfluxDB
Python program wich reads data from InfluDB (query) and saves the data to a csv file. The program let us select some parameter of the query, such as the start time, end time, time between start and end time and the destination folder where the csv file will be saved.

You can use the next line to print help for the program. 

```
$ python3 influxdb_to_csv.py --help
Help:
python3 influxdb_to_csv.py [options]
Options:
 -h / --help 						 Print this help
 -v / --verbose 					 Increase the verbosity
 -s / --start_time 		<EPOCH_TIME[s]>		 Start time in EPOCH format (seconds)
 -e / --end_time 		<EPOCH_TIME[s]>		 End time in EPOCH format (seconds)
 -r / --range_time 		<RANGE_TIME[s]>		 Seconds between start and end times
 -f / --destination_folder 	<PATH>			 Folder where the csv output file will be saved
```

For exemple, to get the data from Monday, 2 May 2022 16:00:00 (GMT) (Epoch = 1651507200) to Monday, 2 May 2022 18:00:00 (GMT) (Epoch = 1651514400) and save the csv file to the existing folder *./my_csv_folder*, we can use:
```
$ python3 influxdb_to_csv.py -s 1651507200 -e 1651514400 -f './my_csv_folder'
```
The command will generate the file *my_csv_folder/2022_05_02-16_00_00_2022_05_02-18_00_00*

Note: You may need to install the python package influxdb-client
