import subprocess
import time
import collections
import datetime


from collections import defaultdict
process_dict = defaultdict(list)


class AppRecord:
    def __init__(self, start_time = None, end_time = None):
        self.start_time = start_time
        self.end_time = end_time
        self.interval = datetime.timedelta(seconds=0)

    def calculate_interval(self):
        self.interval = self.end_time - self.start_time

    # def __add__(self, other):
    #     print(self.interval, other.interval)
    #     return self.interval + other.interval


def sum(l):
    s = datetime.timedelta(seconds=0)
    for i in l:
        # print('i interval' , i.interval)
        s+=i.interval
    return s

active_dict = {}
while True:
    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    prev_check = []
    for line in proc.stdout:
        flag = not line.decode()[0].isspace() and not (line.decode().rstrip() == 'Description' or '--' in line.decode().rstrip())

        if flag:
            app_name = line.decode().rstrip()
            start_time_local = None
            if app_name not in process_dict or process_dict[app_name][-1].end_time is not None:
                start_time_local = datetime.datetime.now()
                app = AppRecord(start_time_local)
                process_dict[app_name].append(app)
                active_dict[app_name] = app
            end = process_dict[app_name][-1].end_time if process_dict[app_name][-1].end_time else datetime.datetime.now()
            curr_interval = end - process_dict[app_name][-1].start_time
            print(app_name,"'s current session", ' : ', curr_interval)
            if len(process_dict[app_name]) > 1:
                # print('len ', len(process_dict[app_name]))
                print(f"{app_name}'s total usage: {sum(process_dict[app_name])+curr_interval}")
            prev_check.append(app_name)
        delete = []

        for active_app in active_dict:
            # print(active_app not in prev_check)
            # print(1,1)
            if active_app not in prev_check:
                print(active_app, prev_check, active_app not in prev_check, 'in end_time loop')
                active_dict[active_app].end_time = datetime.datetime.now()
                active_dict[active_app].calculate_interval()
                delete.append(active_app)
        for app_name in delete:
            print(f'deleting {app_name}')
            del active_dict[app_name]




            ## how to determine end time
            ## how to reset start time For re-opened apps
            ## update the usage_time variable within the tuple
    time.sleep(3)
    print('\n\n\n\n\n\n')

    # time.sleep(300)