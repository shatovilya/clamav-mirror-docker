# from ast import While
# from ctypes.wintypes import PINT
# from readline import append_history_file
# from turtle import home
import threading
import logging
import os
import time
import http.server
import socketserver
import json

# Updating ClamAV databases once EVERY_N_HOURS hours.
EVERY_N_HOURS = 1

def git_clone():

    command_clone="curl -LSOs https://github.com/ladar/clamav-data/raw/main/main.cvd.[01-10] -LSOs https://github.com/ladar/clamav-data/raw/main/main.cvd.sha256 -LSOs https://github.com/ladar/clamav-data/raw/main/daily.cvd.[01-10] -LSOs https://github.com/ladar/clamav-data/raw/main/daily.cvd.sha256 -LSOs https://github.com/ladar/clamav-data/raw/main/bytecode.cvd -LSOs https://github.com/ladar/clamav-data/raw/main/bytecode.cvd.sha256"
    os.system(command_clone)

    print("Download completed")
    command_generate_main="cat main.cvd.01 main.cvd.02 main.cvd.03 main.cvd.04 main.cvd.05 main.cvd.06 main.cvd.07 main.cvd.08 main.cvd.09 main.cvd.10 > main.cvd"
    os.system(command_generate_main)
    print("generate_main")
    
    command_generate_daily="cat daily.cvd.01 daily.cvd.02 daily.cvd.03 daily.cvd.04 daily.cvd.05 daily.cvd.06 daily.cvd.07 daily.cvd.08 daily.cvd.09 daily.cvd.10 > daily.cvd"
    os.system(command_generate_daily)
    print("generate_daily")

    command_generate_full="sha256sum -c main.cvd.sha256 daily.cvd.sha256 bytecode.cvd.sha256 && rm -f main.cvd.sha256 daily.cvd.sha256 bytecode.cvd.sha256 main.cvd.* daily.cvd.*"
    os.system(command_generate_full)
    print("generate_full")

    print("Update completed")
    os.system("cp bytecode.cvd /home/app-user/clamav-data && cp main.cvd /home/app-user/clamav-data && cp daily.cvd /home/app-user/clamav-data")



def keep_updating():
    '''Updating ClamAV databases cyclically'''
    while True:
        print("Performing update!")
        git_clone()
        print("Update completed")
        time.sleep(60 * 60 * EVERY_N_HOURS)

if __name__ == "__main__":
    print("Performing initial update")
    t = threading.Thread(target=git_clone)
    t.start()

    print("Starting web server")
    try:
        time.sleep(60)
        os.chdir('/home/app-user/clamav-data')
        with socketserver.TCPServer(("", 80), http.server.SimpleHTTPRequestHandler) as httpd:
            print("Now serving at port TCP 80")
            httpd.serve_forever()
    except Exception as e:
        logging.error("Failed bringing up the web server. %s" % e)
