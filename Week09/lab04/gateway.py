import hashlib

from handlers import handle_v1, handle_v2

V2_COHORTS = {"beta", "internal"}
V2_ACCOUNTS = {"acct_42", "acct_99"}


def select_handler(cohort, account_id, v2_percent):
    if cohort in V2_COHORTS:
        return handle_v2

    if account_id in V2_ACCOUNTS:
        return handle_v2

    digest = hashlib.md5(account_id.encode("utf-8"), usedforsecurity=False)
    bucket = int(digest.hexdigest(), 16) % 100
    if bucket < v2_percent:
        return handle_v2

    return handle_v1
