from .all_db import legend_db


def get_seven_code():
    return legend_db.get_key("SCODE") or []


def add_seven_code(code):
    ok = get_seven_code()
    if not code in ok:
        ok.append(code)
        return legend_db.set_key("SCODE", ok)


def remove_seven_code(code):
    ok = get_seven_code()
    ok.remove(code)
    return legend_db.set_key("SCODE", ok)


def get_monthly_code():
    return legend_db.get_key("MCODE") or []


def add_monthly_code(code):
    ok = get_monthly_code()
    if not code in ok:
        ok.append(code)
        return legend_db.set_key("MCODE", ok)


def remove_monthly_code(code):
    ok = get_monthly_code()
    ok.remove(code)
    return legend_db.set_key("MCODE", ok)


def user_expiration():
    return legend_db.get_key("EXPIRATION") or {}


def add_expiration(user_id, expire):
    ok = user_expiration()
    ok[user_id] = expire
    legend_db.set_key("EXPIRATION", ok)
    return
