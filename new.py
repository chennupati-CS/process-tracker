import subprocess
import time
import collections
import datetime


process_dict = {}


class AppRecord:
    def __init__(self, start_time = None, end_time = None):
        self.start_time = start_time
        self.end_time = end_time


while True:
    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in proc.stdout:
        # os.system('clear')
        if not line.decode()[0].isspace() \
                and not (line.decode().rstrip() == 'Description' or '--' in line.decode().rstrip()):
            app_name = line.decode().rstrip()
            start_time_local = None
            if app_name not in process_dict:
                start_time_local = datetime.datetime.now()
                process_dict[app_name] = AppRecord(start_time_local)
            end = process_dict[app_name][1] if process_dict[app_name][1] else datetime.datetime.now()
            print(app_name, ' : ', end - process_dict[app_name].start_time)
            ## how to determine end time end time
            ## how to reset start time For re-opened apps
            ## update the usage_time variable within the tuple
    time.sleep(3)
    print('\n\n\n\n\n\n')

    # time.sleep(300)