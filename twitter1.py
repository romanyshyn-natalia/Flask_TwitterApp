import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl


def get_url(user_acc):
    '''
    str -> str
    Function for creating GET request
    '''
    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': user_acc, 'count': '10'})
    return url


def get_data(url):
    '''
    str -> str
    Function for getting user data from url.
    '''
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()
    return data


def write_data(file, data):
    '''
    str, str -> ()
    Function for writing data to json file.
    '''
    with open(file, "w") as file:
        d = file.write(data)
    return d


def get_dict(file):
    '''
    str -> dict
    Function for retrieving data from json to dict. 
    '''
    with open(file, 'r', encoding='utf-8') as f:
        decoded_data = json.load(f)
    return decoded_data


def main(name):
    '''
    str -> dict
    Function for getting other functions all together.
    '''
    user_acc = name
    data = get_data(get_url(user_acc))
    file = 'data.json'
    write_data(file, data)
    dict_json = get_dict(file)
    return dict_json
