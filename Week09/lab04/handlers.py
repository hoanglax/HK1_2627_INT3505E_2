def handle_v1(account_id):
    return {"account_id": account_id, "status": "accepted"}, 200, {
        "X-Order-Handler": "v1",
    }


def handle_v2(account_id):
    return {"account_id": account_id, "status": "created"}, 201, {
        "X-Order-Handler": "v2",
    }
