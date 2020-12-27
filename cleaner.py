import datetime
from termcolor import colored
import os
import time
import math
path="/home/bottino/notiziae/bin/"
new_path="/home/bottino/notiziae/new/"
log_path="/home/bottino/notiziae/cleaner.txt"
gap=40
checker=None

def log(file, rotted):
    with open(log_path,"a") as f:
        report=f"{datetime.datetime.now()} - - {file} deleted after {rotted} days.\n"
        f.write(report)
        f.close()

def bin():
    if not os.path.exists(path):
        print(f"Error with {path}, path does not exists")
        quit()
    for file in os.listdir(path):
        space="".join([" " for i in range(gap-len(file))])
        date=os.stat(path+file).st_mtime
        passed_dd_ts=time.time()-date
        passed_dd=math.ceil(passed_dd_ts/(3600*24))
        if passed_dd>=4:
            log(file,passed_dd)
            os.remove(path+file)

print(colored("CLEANER ONLINE","cyan"))
while True:
    bin()
    time.sleep(3600)
