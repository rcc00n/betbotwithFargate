#                                      ***  ATTENTION  ***


#                 UNDER NO CIRCUMSTANCE THIS FILE CAN BE RUN WITHOUT KILLING ALL PYTHON PROCESSES:


#                                           pkill python3

#                                               OR           
                                 
#                                           pkill python
 
#                                                            RUN IN TERMINAL


import os
import sys
import subprocess
import logging
import signal
import time

pid_file = 'bot.pid'

def check_pid(pid):
    try:
        os.kill(pid, signal.SIG_DFL)  # Check if the process exists without sending a signal
        return True
    except OSError:
        return False

def create_pid_file():
    pid = str(os.getpid())
    with open(pid_file, 'w') as file:
        file.write(pid)

def run_script(script):
    if os.path.isfile(pid_file):
        with open(pid_file, 'r') as file:
            old_pid = int(file.read())
        if check_pid(old_pid):
            logging.info("Script is already running.")
            sys.exit()
        else:
            logging.info("PID file exists but the process is not active. Starting script.")
            os.remove(pid_file)

    create_pid_file()
    logging.info(f"Starting script: {script}")
    process = subprocess.Popen([sys.executable, script])
    return process

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(name)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='discord_bot.log')
    processes = []
    processes.append(run_script("discord/discord_main.py"))

    try:
        # Wait for all processes to complete
        for process in processes:
            process.wait()
    except KeyboardInterrupt:
        logging.info("Script interrupted by user.")
    finally:
        if os.path.isfile(pid_file):
            os.remove(pid_file)
