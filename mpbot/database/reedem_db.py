from .all_db import legend_db

def get_seven_code():
    return legend_db.get_key("REEDEM") or ["afff", "afds"]

def add_reedem(chat_id):




def get_monthly_code():
    return legend_db.get_key("REEDEM") or ["aaf", "adfas"]


def user_expiration():
    return legend_db.get_key("EXPIRATION") or {}

def add_expiration(user_id, expiration):
    ok = user_expiration()
    ok.update

    
