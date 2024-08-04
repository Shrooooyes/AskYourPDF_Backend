import time
import random
from channels.generic.websocket import WebsocketConsumer

import json
from bson import json_util

class DataConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        if text_data:
            data = json.loads(text_data)
            print("User sent:", len(data['selectedStudents'])) 
            # body_unicode = text_data.decode('utf-8')
            students = data['selectedStudents']
            std_data = ""
            for student in students:
                roll_nos = student['institute']['roll_no']
                std_data = std_data + student['external']['name'] + " : " +  str(next(iter(roll_nos.values()))) + "\n"
            
            if len(std_data) != 0:
                std_data = "Selected Students: \n" + f"{std_data}"
            else:
                std_data = "Selected Students: None \n"
            
            
            self.send_data(std_data)

    def send_data(self, user_message=None):
        data = ""
        data_set = "Use the import keyword to import the random module(used to generate random integers. Because these are pseudo-random numbers, they are not actually random. This module can be used to generate random numbers, print a random value from a "
        while len(data) <= 10:
            time.sleep(0.2)
            data += random.choice(data_set)
            self.send(text_data=data)
            
        if user_message:
            data += f'\n{user_message}'
            self.send(text_data=data)
            
        self.send(text_data="finished")
        self.close()