
#####################################################
# Title: influxdb_to_csv.py			    #
# Description: Reads the values from InfluxDB and   #
# saves the data to a csv                           #
# 						    #
# Author: David M.				    #
#####################################################

# ----- INCLUSIONS -----
import csv
import sys, getopt, os.path
import time
from datetime import datetime
from influxdb_client import InfluxDBClient


# ----- CONSTANTS -----
# The default time range is from an hour ago to now
DEFAULT_TIME_RANGE = 3600    # 1 h = 3600 s
DEFAULT_END_TIME = int(time.time())
DEFAULT_START_TIME = DEFAULT_END_TIME - DEFAULT_TIME_RANGE
DEFAULT_FOLDER = 'csv_files/'
DT_FORMAT = "%Y_%m_%d-%H_%M_%S"

# InfluxDB
INFLUX_TOKEN = os.environ.get("INFLUXDB_TOKEN")
INFLUX_ORG = "david_org"
INFLUX_BUCKET = "mqtt"
INFLUX_URL = "https://europe-west1-1.gcp.cloud2.influxdata.com"
INFLUX_MEASUREMENT = 'sensors'


def get_data_range(start_time, end_time, time_range):
    start_t = DEFAULT_START_TIME
    end_t = DEFAULT_END_TIME
    t_range = DEFAULT_TIME_RANGE
    if start_time != DEFAULT_START_TIME:
        if end_time != DEFAULT_END_TIME:
            if time_range != DEFAULT_TIME_RANGE:
                print("Error! Incompatible time selected")
                sys.exit()
            else:
                start_t = start_time
                end_t = end_time
        else:
            if time_range != DEFAULT_TIME_RANGE:
                start_t = start_time
                end_t = start_time + time_range
            else:
                start_t = start_time
                end_t = DEFAULT_END_TIME
    else:
        if end_time != DEFAULT_END_TIME:
            if time_range != DEFAULT_TIME_RANGE:
                start_t = end_time - time_range
                end_t = end_time
            else:
                start_t = DEFAULT_START_TIME
                end_t = end_time
        else:
            if time_range != DEFAULT_TIME_RANGE:
                start_t = DEFAULT_END_TIME - time_range
                end_t = DEFAULT_END_TIME
            else:
                start_t = DEFAULT_START_TIME
                end_t = DEFAULT_END_TIME
    if start_t > end_t:
        print("Error. Start time grater than end time")
        sys.exit()
    return int(start_t), int(end_t)


def get_filename(start_time, end_time, destination_folder):
    filename = destination_folder
    if filename[-1] != "/":
        filename += '/'

    # Datetime in UTC for the start and end time
    dt1 = datetime.utcfromtimestamp(start_time)
    dt2 = datetime.utcfromtimestamp(end_time)

    # Uncomment the next two lines if you want the filename get the time in your local time instead of UTC
    # dt1 = datetime.fromtimestamp(start_time)
    # dt2 = datetime.fromtimestamp(end_time)

    # Convert the datetime to string
    st1 = dt1.strftime(DT_FORMAT)
    st2 = dt2.strftime(DT_FORMAT)

    filename += st1 + "_" + st2
    return filename


def influxdb_to_csv(start_time=DEFAULT_START_TIME, end_time=DEFAULT_END_TIME, time_range=DEFAULT_TIME_RANGE, destination_folder=DEFAULT_FOLDER, verbose=False):
    # Get the actual start and end time
    start_time, end_time = get_data_range(int(start_time), int(end_time), int(time_range))
    if verbose:
        print("Start time = ", start_time, "\t-\t End time = ", end_time)

    # Gerenataes a filename based on the start time, end time and the destination folder
    filename = get_filename(start_time, end_time, destination_folder)
    if verbose:
        print("destination file ", filename)

    # Initialization of the InfluxDB client
    influx_client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
    query_api = influx_client.query_api()

    # Query
    query = """from(bucket: "%s")
     |> range(start: %s, stop: %s)
     |> filter(fn: (r) => r._measurement == "%s")""" % (INFLUX_BUCKET, str(int(start_time)), str(int(end_time)), INFLUX_MEASUREMENT)

    # Saves the results of the query to a csv file
    csv_results = query_api.query_csv(query=query, org=INFLUX_ORG)
    f = open(filename, 'w')
    writer = csv.writer(f)
    for row in csv_results:
        writer.writerow(row)
    f.close()


def check_arguments(argv):
    try:
        opts, args = getopt.getopt(argv, "hvs:e:r:f:", ["help", "verbose", "start_time", "end_time", "time_range", "destination_folder"])
    except getopt.GetoptError:
        print("bad arguments \n")
        print_help()
        sys.exit(2)
    k = []
    v = []
    for i in opts:
        k.append(i[0])
        v.append(i[1])

    if '-h' in k or '--help' in k:
        print_help()
        sys.exit()
    else:
        d = get_arguments(opts)
    return d


def get_arguments(opts):
    d = dict()
    for opt, arg in opts:
        if opt in ('-v', '--verbose'):
            d['verbose'] = True
        if opt in ('-s', '--start_time'):
            d['start_time'] = arg
        if opt in ('-e', '--end_time'):
            d['end_time'] = arg
        if opt in ('-r', '--range_time'):
            d['time_range'] = arg
        if opt in ('-f', '--destination_folder'):
            d['destination_folder'] = arg

    return d


def print_help():
    print("Help:")
    print("python3 influxdb_to_csv.py [options]")
    print("Options:")
    print(" -h / --help \t\t\t\t\t\t Print this help")
    print(" -v / --verbose \t\t\t\t\t Increase the verbosity")
    print(" -s / --start_time \t\t<EPOCH_TIME[s]>\t\t Start time in EPOCH format (seconds)")
    print(" -e / --end_time \t\t<EPOCH_TIME[s]>\t\t End time in EPOCH format (seconds)")
    print(" -r / --range_time \t\t<RANGE_TIME[s]>\t\t Seconds between start and end times")
    print(" -f / --destination_folder \t<PATH>\t\t\t Folder where the csv output file will be saved")
    sys.exit()


if __name__ == '__main__':
    args = check_arguments(sys.argv[1:])
    influxdb_to_csv(**args)
