import requests
import json
from Crypto.Cipher import AES
import base64
import csv
import sys

headers = {
    'Host':'music.163.com',
    'Cookie': 'appver=1.5.0.75771;',
    'Referer': 'http://music.163.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}

param1 = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}'
param2 = "010001"
param3 = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
param4 = "0CoJUm6Qyw8W8jud"

def get_params():
    iv = "0102030405060708"
    key1 = param4
    key2 = 16 * 'F'
    h_encText = AES_encrypt(param1, key1, iv)
    h_encText = AES_encrypt(h_encText, key2, iv)
    return h_encText

def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text.decode()

def get_encSecKey():
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey

def get_json(url, params, encSecKey):
    data = {
        "params": params,
        "encSecKey": encSecKey
    }
    response = requests.post(url, headers=headers, data=data)
    return response.content

def start(songID,page):
    url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_"+str(songID)+"/?csrf_token="
    global param1
    param1 = '{rid:"", offset:"'+str(page)+'", total:"true", limit:"20", csrf_token:""}'
    params = get_params()
    encSecKey = get_encSecKey()
    json_text = get_json(url, params, encSecKey)
    json_dict = json.loads(json_text)
    return json_dict['total'], json_dict['comments']


if __name__ == "__main__":
    total=0
    pages=200
    songID = 37610720
    with open('pinglun.txt', 'w', encoding='utf-8') as f:
        for i in range(pages):
            total, comments = start(songID,i*20)
            for item in comments:
                f.write(item['content']+'\n')
                print(item['user']['nickname'],'----', item['content'])
    print(total)
