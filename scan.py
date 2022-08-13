import queue
import socket
from colorama import init, Fore
import sys
import time
import threading
red=Fore.RED
green=Fore.GREEN
yellow=Fore.YELLOW
reset=Fore.RESET
def banner():

    print(f"""{green}
             --------- |------- |-----| ||    |      |-----| |-----| |----| -------- |---------
             |         |        |     | | |   |      |     | |     | |    |    |     |
             |-------| |        |-----| |  |  |      |-----| |     | |----|    |     |--------|
                     | |        |     | |   | |      |       |     | ||        |              |
             --------| |------- |     | |    ||      |       |-----| | |       |     ---------|
             @Developed by - Mayank Pal                                 |
                           """)
banner()
target=input("[+]Enter hostname or ip adress of the target")
start_time=time.time()
try:
    target=socket.gethostbyname(target)
except Exception as e:
    print(f"[+]{red}The target you entered is invalid")
start_port=int(input(f"[+]{green}Enter the port from where you want to begin scanning"))
end_port=int(input(f"[+]{green}Enter the port till when you want to scan"))
threads=int(input(f"[+]{green}Enter on how many threads you wnat to run the scan"))
def portscan(TH):
    while not q.empty():
        ports = q.get()
        try:
            sockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as e:
            print(f"[-]{red}We were not able to create socket")
        sockets.settimeout(1)
        result = sockets.connect_ex((target, ports))
        if result == 0:
            print(f"{red}[+]{ports} port is open")
        sockets.close()
        q.task_done()
q=queue.Queue()
for ports in range(start_port,end_port+1):
    q.put(ports)
for i in range(threads):
    t=threading.Thread(target=portscan, args=(i,))
    t.start()
t.join()
end_time=time.time()
print(f"{green}It took {end_time-start_time} seconds to run the scan")
