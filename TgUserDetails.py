import argparse
import colorama
import datetime
import getpass
import json
import urllib.parse

from telethon import TelegramClient, sync
from telethon.errors.rpcerrorlist import SessionPasswordNeededError
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.contacts import ImportContactsRequest, DeleteContactsRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import InputPhoneContact, InputUser
from telethon.tl.types import PeerUser, PeerChat, PeerChannel

from telethon.tl.types import UserStatusEmpty, UserStatusOnline, UserStatusOffline, UserStatusRecently, UserStatusLastWeek, UserStatusLastMonth

from urllib.parse import urljoin, urlparse

colorama.init()

parser = argparse.ArgumentParser(description='Get information about a Telegram user (or a public channel or group) by their username, ID, phone number, or the URL of a message they sent.')
parser.add_argument('-u', '--username', type=str, help='The username of the user, group or channel (with or without the @ symbol)')
parser.add_argument('-i', '--id', type=int, help='The ID of the user, public group or channel (a numerical value)')
parser.add_argument('-p', '--phone', type=str, help='The phone number of the user (with the country code)')
parser.add_argument('-l', '--url', type=str, help='The URL of a message sent by the user in a public channel or group')
args = parser.parse_args()

api_id = ******** 
api_hash = "-----------------------------" 
phone = "+00000000000"
client = TelegramClient('session_name', api_id, api_hash)

client.connect()

if not client.is_user_authorized():
    client.send_code_request(phone)
    code = input('Enter the Telegram code: ')
    try:
        client.sign_in(phone, code)
    except SessionPasswordNeededError:
        password = getpass.getpass('Enter the password for the Telegram session ')
        client.sign_in(password=password)

def main():
    entity = None 
    alias = '' 

    if args.username is not None:
        alias = args.username
        try:
            entity = client.get_entity(alias)
            entity_type = entity.__class__.__name__
            if entity_type == 'User':            
                user_id = entity.id
                name = entity.first_name
                username = entity.username
                full = client(GetFullUserRequest(entity))
                bio = full.full_user.about
                print(f'The ID of the user with username {colorama.Fore.RED}@{alias}{colorama.Style.RESET_ALL} is {colorama.Fore.RED}{user_id}{colorama.Style.RESET_ALL}')
                print(f'The first name of the user with username {colorama.Fore.RED}@{alias}{colorama.Style.RESET_ALL} is {colorama.Fore.RED}{name}{colorama.Style.RESET_ALL}')
                last_name = entity.last_name 
                print(f'The last name of the user with username {colorama.Fore.RED}@{alias}{colorama.Style.RESET_ALL} is {colorama.Fore.RED}{last_name}{colorama.Style.RESET_ALL}')
                status = entity.status 
                last_seen = get_user_status(status) 

                print(f'The user was last seen online on {colorama.Fore.RED}{last_seen}{colorama.Style.RESET_ALL}')
                if username is not None:
                    print(f'The username of the user with username {colorama.Fore.RED}@{alias}{colorama.Style.RESET_ALL} is {colorama.Fore.RED}@{username}{colorama.Style.RESET_ALL}')
                else:
                    print(f'The user with username {colorama.Fore.RED}@{alias}{colorama.Style.RESET_ALL} does not have a username')

                print(f'Biography of the user with username {colorama.Fore.RED}@{alias}{colorama.Style.RESET_ALL}: {colorama.Fore.RED}{bio}{colorama.Style.RESET_ALL}')            
                client.download_profile_photo(entity, file=f'{user_id}.jpg')
                print(f'The profile picture of the user with username {colorama.Fore.RED}@{alias}{colorama.Style.RESET_ALL} has been downloaded in the file {colorama.Fore.RED}{user_id}.jpg{colorama.Style.RESET_ALL}')

                for photo in client.iter_profile_photos(entity): 
                    date = photo.date 
                    date_str = date.strftime('%Y%m%d_%H%M%S') 
                    client.download_media(photo, file=f'{date_str}.jpg') 
                    print(f'A profile picture of the user with username {colorama.Fore.RED}@{alias}{colorama.Style.RESET_ALL} has been downloaded in the file {colorama.Fore.RED}{date_str}.jpg{colorama.Style.RESET_ALL}')

            elif entity_type == 'Channel':
                if entity.megagroup: 
                    get_chat_info(entity)
                else: 
                    get_channel_info(entity)

        except (ValueError) as e: 
            print(f"Could not find the user with username {colorama.Fore.RED}@{alias}{colorama.Style.RESET_ALL}")
            print(f"Please check that the username is correct and that the user exists")

    elif args.id is not None:
        user_id = args.id
        try:
            entity = client.get_entity(user_id)
            entity_type = entity.__class__.__name__
            if entity_type == 'User':            
                name = entity.first_name
                username = entity.username
                print(f'The first name of the user with ID {colorama.Fore.RED}{user_id}{colorama.Style.RESET_ALL} is {colorama.Fore.RED}{name}{colorama.Style.RESET_ALL}')
                last_name = entity.last_name 
                print(f'The last name of the user with ID {colorama.Fore.RED}{user_id}{colorama.Style.RESET_ALL} is {colorama.Fore.RED}{last_name}{colorama.Style.RESET_ALL}')        
                full = client(GetFullUserRequest(entity))
                bio = full.full_user.about        
                print(f'Biography of the user with ID {colorama.Fore.RED}{user_id}{colorama.Style.RESET_ALL}: {colorama.Fore.RED}{bio}{colorama.Style.RESET_ALL}')  
                status = entity.status 
                last_seen = get_user_status(status) 

                print(f'The user was last seen online on {colorama.Fore.RED}{last_seen}{colorama.Style.RESET_ALL}')

                if username is not None:
                    print(f'The username of the user with ID {colorama.Fore.RED}{user_id}{colorama.Style.RESET_ALL} is {colorama.Fore.RED}@{username}{colorama.Style.RESET_ALL}')
                    client.download_profile_photo(entity, file=f'{user_id}.jpg')
                    print(f'The profile picture of the user with ID {colorama.Fore.RED}{user_id}{colorama.Style.RESET_ALL} has been downloaded in the file {colorama.Fore.RED}{user_id}.jpg{colorama.Style.RESET_ALL}')

                    for photo in client.iter_profile_photos(entity): 
                        date = photo.date 
                        date_str = date.strftime('%Y%m%d_%H%M%S') 
                        client.download_media(photo, file=f'{date_str}.jpg') 
                        print(f'A profile picture of the user with ID {colorama.Fore.RED}{user_id}{colorama.Style.RESET_ALL} has been downloaded in the file {colorama.Fore.RED}{date_str}.jpg{colorama.Style.RESET_ALL}')

                else:
                    print(f'The user with ID {colorama.Fore.RED}{user_id}{colorama.Style.RESET_ALL} does not have a username')

            elif entity_type == 'Channel':
                get_channel_info(entity)
            elif entity_type == 'Chat':
                get_chat_info(entity)

        except ValueError as e: 
            print(f"Could not find the user with ID {colorama.Fore.RED}{user_id}{colorama.Style.RESET_ALL}")
            print(f"Please use the parameter -i only with users that are in your contacts list")

    elif args.phone is not None:
        phone_number = args.phone
        contact = InputPhoneContact(client_id=0, phone=phone_number, first_name='Contacto', last_name='Temporal')
        result = client(ImportContactsRequest([contact]))

        if result.users:
            user = result.users[0]
            user_id = user.id
            name = user.first_name
            username = user.username
            last_name = user.last_name             
            full = client(GetFullUserRequest(user))
            bio = full.full_user.about            
            print(f'The ID of the user with phone number {colorama.Fore.RED}{phone_number}{colorama.Style.RESET_ALL} is {colorama.Fore.RED}{user_id}{colorama.Style.RESET_ALL}')
            user_full = client(GetFullUserRequest(user))
            user_id = result.users[0].id 
            entity = client.get_entity(user_id)
            status = entity.status 
            last_seen = get_user_status(status) 

            print(f'The user was last seen online on {colorama.Fore.RED}{last_seen}{colorama.Style.RESET_ALL}')

            if username is not None:
                print(f'The username of the user with phone number {colorama.Fore.RED}{phone_number}{colorama.Style.RESET_ALL} is {colorama.Fore.RED}@{username}{colorama.Style.RESET_ALL}')
            else:
                print(f'The user with phone number {colorama.Fore.RED}{phone_number}{colorama.Style.RESET_ALL} does not have a username')

            print(f'Biography of the user with phone number {colorama.Fore.RED}{phone_number}{colorama.Style.RESET_ALL}: {colorama.Fore.RED}{bio}{colorama.Style.RESET_ALL}')                 
            client.download_profile_photo(user, file=f'{user_id}.jpg')
            print(f'The profile picture of the user with phone number {colorama.Fore.RED}{phone_number}{colorama.Style.RESET_ALL} has been downloaded in the file {colorama.Fore.RED}{user_id}.jpg{colorama.Style.RESET_ALL}')

            for photo in client.iter_profile_photos(user): 
                date = photo.date 
                date_str = date.strftime('%Y%m%d_%H%M%S') 
                client.download_media(photo, file=f'{date_str}.jpg') 
                print(f'A profile picture of the user with phone number {colorama.Fore.RED}{phone_number}{colorama.Style.RESET_ALL} has been downloaded in the file {colorama.Fore.RED}{date_str}.jpg{colorama.Style.RESET_ALL}')

            client(DeleteContactsRequest(id=[InputUser(user_id=user.id, access_hash=user.access_hash)]))
            user_full = client(GetFullUserRequest(user))
            user_id = result.users[0].id 
            entity = client.get_entity(user_id)

            name_after_delete = entity.first_name
            lastname_after_delete = entity.last_name            
            print(f'The current first name of the user with phone number {colorama.Fore.RED}{phone_number}{colorama.Style.RESET_ALL} is {colorama.Fore.RED}{name_after_delete}{colorama.Style.RESET_ALL}')
            print(f'The current last name of the user with phone number {colorama.Fore.RED}{phone_number}{colorama.Style.RESET_ALL} is {colorama.Fore.RED}{lastname_after_delete}{colorama.Style.RESET_ALL}')
                
        else:
            print(f'No user was found with the phone number {colorama.Fore.RED}{phone_number}{colorama.Style.RESET_ALL}')

    elif args.url is not None:
        url = args.url 
        result = urlparse(url) 
        path = result.path 
        parts = path.split('/') 
        channel_name = parts[1] 
        message_id = int(parts[2]) 
        message = client.get_messages(entity=channel_name, ids=message_id, limit=1) 
        message_json = json.dumps(message.to_dict(), indent=2, default=bytes_to_str) 
        print(message_json) 
    else:
        print('You must pass an argument -u, -i or -p to obtain information about a Telegram user')

def get_channel_info(channel):
    channel_id = channel.id
    title = channel.title
    username = channel.username
    ch = client.get_entity(channel_id)
    ch_full = client(GetFullChannelRequest(channel=ch))
    ch_full.full_chat.about
    photo = channel.photo
    date = channel.date
    print(f'The channel ID is {colorama.Fore.RED}{channel_id}{colorama.Style.RESET_ALL}')
    print(f'The channel title is {colorama.Fore.RED}{title}{colorama.Style.RESET_ALL}')
    if username is not None:
        print(f'The username of the channel is {colorama.Fore.RED}@{username}{colorama.Style.RESET_ALL}')
    else:
        print(f'The channel does not have a user name')
    print(f'The channel description is: {colorama.Fore.RED}{ch_full.full_chat.about}{colorama.Style.RESET_ALL}')
    print(f'The channel creation date is: {colorama.Fore.RED}{date.strftime("%Y-%m-%d %H%M%S (UTC)")}{colorama.Style.RESET_ALL}')
    client.download_profile_photo(channel, file=f'{channel_id}.jpg')
    print(f'The profile picture of the channel has been downloaded to the file {colorama.Fore.RED}{channel_id}.jpg{colorama.Style.RESET_ALL}')

    for photo in client.iter_profile_photos(channel_id): 
        date = photo.date 
        date_str = date.strftime('%Y%m%d_%H%M%S') 
        client.download_media(photo, file=f'{date_str}.jpg') 
        print(f'A profile picture of the user with username {colorama.Fore.RED}@{username}{colorama.Style.RESET_ALL} has been downloaded in the file {colorama.Fore.RED}{date_str}.jpg{colorama.Style.RESET_ALL}')

def get_chat_info(chat):
    chat_id = chat.id
    title = chat.title
    photo = chat.photo
    date = chat.date
    print(f'The group ID is {colorama.Fore.RED}{chat_id}{colorama.Style.RESET_ALL}')
    print(f'The group title is {colorama.Fore.RED}{title}{colorama.Style.RESET_ALL}')
    participants = client.get_participants(chat)    
    participants_count = len(participants) 
    print(f'The number of administrators in the group is: {colorama.Fore.RED}{participants_count}{colorama.Style.RESET_ALL}')
    print(f'The group creation date is: {colorama.Fore.RED}{date.strftime("%Y-%m-%d %H%M%S (UTC)")}{colorama.Style.RESET_ALL}')
    client.download_media(photo, file=f'{chat_id}.jpg')
    print(f'The group profile picture has been downloaded in the file {colorama.Fore.RED}{chat_id}.jpg{colorama.Style.RESET_ALL}')

    for photo in client.iter_profile_photos(chat_id): 
        date = photo.date 
        date_str = date.strftime('%Y%m%d_%H%M%S') 
        client.download_media(photo, file=f'{date_str}.jpg') 
        print(f'A profile picture of the user with username {colorama.Fore.RED}@{chat_id}{colorama.Style.RESET_ALL} has been downloaded in the file {colorama.Fore.RED}{date_str}.jpg{colorama.Style.RESET_ALL}')

def get_user_status(status):
    if isinstance(status, UserStatusEmpty): 
        return "never" 
    elif isinstance(status, UserStatusOnline): 
        return "now" 
    elif isinstance(status, UserStatusOffline): 
        return status.was_online.isoformat() 
    elif isinstance(status, UserStatusRecently): 
        return "recently" 
    elif isinstance(status, UserStatusLastWeek): 
        return "last week" 
    elif isinstance(status, UserStatusLastMonth): 
        return "last month" 

def bytes_to_str(b):
    if isinstance(b, bytes): 
        return b.hex() 
    elif isinstance(b, datetime.datetime): 
        return b.strftime('%Y-%m-%d %H%M%S (UTC)') 
    else: 
        return str(b) 

if __name__ == '__main__':
    main()
