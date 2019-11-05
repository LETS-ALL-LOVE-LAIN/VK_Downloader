import vk as vk
import numpy as np
import urllib
import os.path 
import os

def init(token):
    session = vk.Session(access_token=token)
    vk_api = vk.API(session)
    return vk_api

def id_from_shortcut(short):

    return vk_api.groups.getById(group_id = short, v = '5.103')[0]['id']
def txt_read(path):
    groups = []

    txt = open(path,'r')
    token = txt.readline().split('"')[1]

    global vk_api
    vk_api = init(token)

    [groups.append(-id_from_shortcut(group)) for group in txt.readline().split('"')[1].split(",")]
    albums_n = [[]] * len(groups)
    albums = (txt.readline().split('"')[1].split(";"))
    for i in range(len(albums)):
        albums[i] = albums[i].split(',')
        
    path = txt.readline().split('"')
    
    amounts = (txt.readline().split('"')[1].split(";"))
    amounts_new = []
    for i in range(len(amounts)):
        amounts[i] = amounts[i].split(',')
        amounts_new.append([int(item) for item in amounts[i]])
        
    reverse = (txt.readline().split('"')[1].split(";"))
    reverse_new = []
    for i in range(len(reverse)):
        reverse[i] = reverse[i].split(',')
        reverse_new.append([int(item) for item in reverse[i]])
        
    return token, groups, albums[0], path[1], amounts_new[0][0], reverse_new

def parse(u_id,alb_id, amount = 0, reverse = 0): #reverse 0 or 1 #number - custom number of photos
    response = vk_api.photos.get(owner_id = u_id, album_id = alb_id, count = 1, v = '5.103')
    response['items'][0] = 0
    response['items'].remove(0)

    if response['count'] < amount:
        print("Custom amount too large")
        return
    elif amount == 0:
        if response['count'] > 1000:
            for i in range((response['count']//1000)):
                response["items"].extend(vk_api.photos.get(owner_id = u_id, album_id = alb_id, count = 1000,offset = 1000*(i), rev = reverse, v = '5.103')['items'])
    else:
        for i in range((amount//100)):
            response["items"].extend(vk_api.photos.get(owner_id = u_id, album_id = alb_id, count = 100,offset = 100*(i), rev = reverse, v = '5.103')['items'])
    return response
def download(directory,content,quality = 6): #quality 1 to 7
    i=0
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)
    for item in content['items']:
        urllib.request.urlretrieve(item['sizes'][quality]['url'],str(directory)  + str(i) + ".jpg")
        i = i +  1
def clear(content,quality = 6):
    for item in content['items']:
        if len(item['sizes']) <  quality:
            print(item['sizes'])
            content['items'].remove(item)
def input_params():
    print("Token:")
    token = str(input())

    global vk_api
    vk_api = init(token)
    print("Say if you want to download user's album? Type y/n")
    if input() == 'y':
        print("User Id:") 
        groups = id_from_shortcut(input())
    else:
        print("Group Id:") 
        groups = -id_from_shortcut(input())
        
    print("Album Id:")
    albums = input()
    if albums == 'wall':
        pass
    else:
        albums = int(albums)
    print("Path to download photos:")
    path = input()
    print("Amount of photos:")
    amounts = int(input())
    print("New photos first? Type y/n")
    if input() == 'y':
        reverse = 1
    else:
        reverse = 0
    return token, groups, albums, path, amounts, reverse

if __name__ == "__main__":
    if os.path.isfile("Settings.txt") == True:
        token, groups, albums, path, amounts, reverse = txt_read("Settings.txt")
        content = parse(groups, albums, amounts, reverse)
        clear(content)
        download(path, content)

    else:
        token, groups, albums, path, amounts, reverse = input_params()
        
        content = parse(groups, albums, amounts, reverse)
        clear(content)
        download(path, content)

