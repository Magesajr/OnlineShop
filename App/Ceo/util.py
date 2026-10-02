from supabase import Client,create_client
import secrets
import os
from flask import jsonify
from App.config import config as c


URL:str=c.SUPABASE_URL
KEY:str=c.SUPABASE_KEY
supabase : Client= create_client(URL,KEY)

def save_img(img):
    token=secrets.token_hex(4)
    _, f_ext=os.path.splitext(img.filename)
    img_name=token+f_ext
    supabase.storage.from_('onlineshop').upload(
        path=img_name,file=img.read(),
        file_options={
            'content-type':img.mimetype
        })
    return img_name


def update_img(img,old_img):
    token=secrets.token_hex(4)
    _, f_ext=os.path.splitext(img.filename)
    img_name=token+f_ext
    supabase.storage.from_('onlineshop').update(
        path=f'{old_img}',file=img.read(),
        file_options={
            'content-type':img.mimetype
        })
    return img_name


def clean_bucket():
        return supabase.storage.empty_bucket('onlineshop')