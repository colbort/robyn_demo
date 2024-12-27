import json

from robyn.robyn import Identity


def get_user_id(identity: Identity) -> int:
    try:
        data = ""
        try:
            data = identity.claims['claims']
        except Exception as e:
            print(f"{e}")
        user_data = json.loads(data)
        return user_data["user_id"]
    except Exception as e:
        print(f"{e}")
        return -1


def get_user_name(identity: Identity) -> str:
    try:
        data = ""
        try:
            data = identity.claims['claims']
        except Exception as e:
            print(f"{e}")
        user_data = json.loads(data)
        return user_data["user_name"]
    except Exception as e:
        print(f"{e}")
        return ""
