from datetime import datetime

from .all_db import legend_db


def get_seven_code():
    return legend_db.get_key("SCODE") or []


def add_seven_code(code):
    ok = get_seven_code()
    if not code in ok:
        ok.append(code)
        return legend_db.set_key("SCODE", ok)


def get_monthly_code():
    return legend_db.get_key("MCODE") or []


def add_monthly_code(code):
    ok = get_monthly_code()
    if not code in ok:
        ok.append(code)
        return legend_db.set_key("MCODE", ok)


def user_expiration():
    return legend_db.get_key("EXPIRATION") or {}


def add_expiration(user_id, expiration):
    ok = user_expiration()
    if user_id in ok:
        days_left = ok[user_id] - datetime.now()
        total_add = days_left + expiration
        print(total_add)
        ok.update({user_id: total_add})
        legend_db.set_key("EXPIRATION", ok)
        return false
    ok.update({user_id: expiration})
    return legend_db.set_key("EXPIRATION", ok)
