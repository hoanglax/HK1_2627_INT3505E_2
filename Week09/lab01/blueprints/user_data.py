from threading import Lock


USERS = {
    1: {
        "first_name": "Văn",
        "last_name": "Nguyễn",
        "email": "a@vnu.vn"
    },
    2: {
        "first_name": "Trang",
        "last_name": "Trần",
        "email": "b@vnu.vn"
    }
}
_create_lock = Lock()
def get_user(uid):
    return USERS.get(uid)

def create_user(data):
    user = {
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "email": data["email"]
    }

    with _create_lock:
        uid = max(USERS, default=0) + 1
        USERS[uid] = user

    return uid, user
