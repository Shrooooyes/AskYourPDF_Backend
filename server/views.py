from django.http import StreamingHttpResponse

import time
import datetime
import random


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from bson import json_util

import pymongo
import sys

password = '430mCNBIXAhaVGE6'
uri = f"mongodb+srv://shreyashsawant37:{password}@cluster0.ojuq0lp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

uri = "mongodb://0.0.0.0:27017/"

client = pymongo.MongoClient(uri)
db = client.USERS
my_collection = db["Users"]

@csrf_exempt
def addUser(request):
    if request.method == 'POST': 
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        print(data)
        
        chat = []
        data = {
            'user' : data,
            'chat' : chat
        }
        
        user_documents = [data]
        my_doc = my_collection.find_one({"user.email": data['user']["email"]})


        if my_doc is not None:
            print("Already user exists cant add new user")
            return JsonResponse({'error': 'User with this email already exists'}, status=200)
        try: 
            result = my_collection.insert_many(user_documents)

        except pymongo.errors.OperationFailure:
            print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
        else:
            inserted_count = len(result.inserted_ids)
            print("I inserted %x documents." %(inserted_count))

        print("\n")

        data = json.loads(json_util.dumps(data))
        return JsonResponse(data, status=200)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        print(data)
        
        my_doc = None
        if data['email'] == '':
            my_doc = my_collection.find_one({"user.email": data["email"]})
        if my_doc is None:
            print("No such user exists\n")
            return JsonResponse({'error': 'No such user exists'}, status=400)
        
        if(my_doc['user']['password']==data['password']):
            my_doc = json.loads(json_util.dumps(my_doc))
            print(my_doc)
            return JsonResponse(my_doc, status=200)
        else:
            return JsonResponse({'error': 'Incorrect Password'}, status=400)
        
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    

@csrf_exempt
def updateChat(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        
        is_user = None    
        if data['email'] != '':
            is_user = my_collection.find_one({"user.email": data["email"]})
        if is_user:
            user_chats = is_user['chat']
            print(f"user_chats: {len(user_chats)}, myChats: {len(data['chat'])}")
            
            if (len(user_chats)-1) >= data['id']:
                user_chats[int(data['id'])] = data['chat']
            else :
                user_chats.append(data['chat'])

            query = {"user.email": data["email"]}
            new_chat = {"$set" : {"chat" : user_chats}}
            my_collection.update_one(query, new_chat)
            # found = my_collection.find_one(query)
            print("updated")        
        
        return JsonResponse({'error' : "NULL"}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


#!Can be used
@csrf_exempt
def getUser(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        print(data)
        my_doc = my_collection.find_one({"email": data["email"]})
        
        my_doc = json.loads(json_util.dumps(my_doc))
        print(my_doc)
        return JsonResponse(my_doc, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
@csrf_exempt
def pdfUpload(request):
    if request.method == 'POST':
        data = request.FILES['file'] 
        print(data)
        return JsonResponse({'error': False}, status=200)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def testSEE(request):
    def event_stream():
        data = ""
        while True:
            finished = len(data) > 30
            data_set = "Use the import keyword to import the random module(used to generate random integers. Because these are pseudo-random numbers, they are not actually random. This module can be used to generate random numbers, print a random value from a "
            time.sleep(0.2)
            data = data + random.choice(data_set)
            if not finished :
                yield 'data: %s\n\n' % data
            else:
                yield 'data: finished\n\n'
            
    return StreamingHttpResponse(event_stream(),content_type = 'text/event-stream')
