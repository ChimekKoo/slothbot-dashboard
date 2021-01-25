from app import session


def check_if_authorized():
    for key in ["authed", "user", "guilds"]:
        try:
            session[key]
        except KeyError:
            return False
        else:
            if session[key]:
                continue
            else:
                return False
    return True
