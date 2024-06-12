import time
import random
from channels.generic.websocket import WebsocketConsumer

class DataConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        if text_data:
            print("User sent:", text_data) 
            self.send_data(text_data)

    def send_data(self, user_message=None):
        data = ""
        data_set = "Use the import keyword to import the random module(used to generate random integers. Because these are pseudo-random numbers, they are not actually random. This module can be used to generate random numbers, print a random value from a "
        if user_message:
            data = f'You sent: {user_message}\n'
        while len(data) <= 50:
            time.sleep(0.2)
            data += random.choice(data_set)
            self.send(text_data=data)

        

        self.send(text_data="finished")
        self.close()