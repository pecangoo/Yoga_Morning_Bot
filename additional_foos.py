import json_file
import settings
from datetime import datetime



def checking_new_user(dict_users:dict, id:int):
    if str(id) in dict_users.keys():
        print("User have found\n")
        return 0
    else:
        print("User don't found\n")
        return 1

def reg_new_user(dict_users:dict, message):
    timestamp = int(datetime.today().timestamp())
    dict_users[str(message.chat.id)] = [message.chat.first_name, 0, 0, timestamp]   # Add to user to dict
    json_file.save_json(dict_users)  # Update json_file
    return dict_users   # Return updated dict



def get_video_id(num_video:int):
    #print ("load enter\n")
    num_video = int(num_video[0])
    with open(settings.path_video_db) as f:
        #print ("file open\n")
        print(type(num_video))  # typeof(num))
        for i in f.readlines():
            key, val = i.strip().split(':')
            key = int(key)
            #print(type(key))# typeof(num))
            if key == num_video:
                print("Video found")
                return val
        print("Error: get_video_id: Can't find video")
    return -1

def add_video_to_db(video:str):

    file_line = ""
    with open(settings.path_video_db) as f:
        for i in f.readlines():
            key, val = i.strip().split(':')
            count = int(key)
            file_line = file_line + f"{key}:{val}\n"
    count = count+1

    file_line = file_line + f"{count}:{video}"
    print(file_line)
    with open(settings.path_video_db, 'w') as file:
        file.write(file_line)




def MinusDay_PlusNumClass_UpdateJson(id_chat:int, dict_users:dict):
    dict_users[str(id_chat)][1] -= 1
    dict_users[str(id_chat)][2] += 1
    json_file.save_json(dict_users)  # Update json_file
    return dict_users
    #return dict_users  # Return updated dict

async def last_msg_time_more(time_user:int):
    timestamp = int(datetime.today().timestamp())
    time_last = timestamp - time_user
    if time_last > settings.two_weeks_time_sec:
        return True
    else:
        return  False
