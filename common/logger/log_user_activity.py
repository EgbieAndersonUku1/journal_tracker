from common.errors import CouldNotLogUserActivity
from models.users.user import Account, History


def log_account_activity(username, log):

    account = Account.find_account_by_username(username).first()

    if account:
        hist = History(activity=log, live=True)
        hist.account = account
        hist.save()
        return True
