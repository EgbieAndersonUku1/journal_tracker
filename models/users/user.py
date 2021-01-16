from datetime import datetime

from app import cache
from app import db
from common.date import seconds_till_midnight as seconds_till_midnight
from models.db_saver_helper import db_saver_helper


class AccountType:
    BASIC = 0
    INTERMEDIATE = 1
    PRIVILEGED = 2


class Account(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.String, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    history = db.relationship("History", backref="account", lazy="dynamic")
    live = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    @classmethod
    def activate_user_account(cls, username: str) -> "Account":
        """activate_user_account(username: str) -> Account

           If an account has been deactivated, by calling this the method along
           with a username(the username must exists) the de-activated account
           can be re-activated.

           Returns an Account object.

           :parameter
                username: The username for the account to be activated

           :returns
                the user Account object

           :Usage:
                Account.activate_user_account(username)
        """
        account = cls.find_account_by_username(username).first()

        if account and not account.live:
            account.live = True
            account.save()
        return account

    @classmethod
    def de_activate_user_account(cls, username: str) -> "Account":
        """de_activate_user_account(username: str) -> Account

           This method takes in a username as a string and de-activate
           the account only if the account exists and it is live.
           Returns an Account object.

           :parameter
               username: The username for the account to be activated

           :returns
                the user Account object

           :Usage:
               Account.de_activate_user_account(username)
        """
        account = cls.find_account_by_username(username).first()

        if account and account.live:
            account.live = False
            account.save()


        return account

    @classmethod
    def find_account_by_username(cls, username: str):
        """find_account_by_username(username: str) SQLAlchemy query object

           Takes a username as a string and if that username is found in the database
           returns that user account as a SQLAlchemy base query object.

           :parameter
                :username: The username that will be queried in the database

           :Returns:
                a SQLAlchemy base query object or None

           :Usage:
                Account.find_account_by_username(username)
        """
        id = db.session.query(User.id).filter_by(username=username.lower()).first()

        return cls.query.filter_by(id=id[0]) if id else None

    @classmethod
    def get_account_activity_history_by_username(cls, username: str, descending_order: bool = True) -> "Account.query":
        """get_account_activity_history_by_username(username: str, descending_order: live) -> Account query object

           Takes two parameters a username (str) and a descending_order (bool) and if user is found
           returns all the user's account history. If the descending_order is set to True
           returns the result in descending order and if set to false returns the
           result in ascending order.

           :parameter
                username: str: The username to be queried in the database
                descending_order: bool: Default value True. The order the data will be returned.
                                        If default of order of True is used returns the latest activity
                                        on top
           :returns
                Returns either a Account object query or None

           :usage
                - Account.get_account_activity_history_by_username(username, live=True)
                - Account.get_account_activity_history_by_username(username, live=False)

        """
        account = cls.find_account_by_username(username.lower())

        if account and descending_order:
            return account[0].history.order_by(History.id.desc())
        elif account and not descending_order:
            return account[0].history

    @classmethod
    def revoke_admin_status(cls, username: str) -> "Account":
        """revoke_admin_status(username: str) -> Account

           Takes a username and no matter the level for the
           account revokes the admin status

           :parameter
                username: The username(str) to be queried in the database

           :Returns
                An account object

           :usage:
                Account.revoke_admin_status(username)
        """
        account = cls.find_account_by_username(username).first()

        if account and account.admin:
            account.admin = None
            account.save()
        return account

    @classmethod
    def set_account_admin_access(cls, username: str, access_type: int = AccountType.BASIC) -> "Account":
        """set_account_admin_access(username: str, access_type: int) -> Account object

           Takes in two parameters a username(str) and access_type(int) and sets
           the administration levels to that account. The access_type has three
           levels BASIC -> 0, INTERMEDIATE -> 1, PRIVILEGED -> 2.

           :parameter
                username: str: The username belonging to the account
                access_type: int: The level to set the account to BASIC -> 1, INTERMEDIATE -> 2, PRIVILEGED -> 3

           :returns
                Returns an account object

           :usage:
                - Account.set_account_admin_access(username, BASIC)
                - Account.set_account_admin_access(username, INTERMEDIATE)
                - Account.set_account_admin_access(username, PRIVILEGED)

        """
        account = cls.find_account_by_username(username).first()

        if account and not account.admin:
            if access_type in [AccountType.BASIC, AccountType.INTERMEDIATE, AccountType.PRIVILEGED]:
                account.admin = access_type
                account.save()
        return account

    def save(self):
        """Saves the users parameters to the database

            :returns
              returns an instance of the class

           :usage
                Account(parameter1, parameter2.....parameter(N-1) ).save()

                acc = Account(parameter1, parameter2.....parameter(N-1) ).
                acc.save()
        """
        return db_saver_helper(db, self)


    @classmethod
    def setup_user_account(cls, username: str) -> "Account":
        """setup_user_account(username: str) -> Account

           Takes a username and if the account does not yet exists
           setup the user account by linking the user account to the user
           model. Note the user must first exists before the account can
           be setup.

           :parameter
                username: The username belonging to the account to setup

           :returns
                if the account is successfully setup returns an account object
                or none otherwise

           :usage
                Account.setup_user_account(username)
        """

        user = User.find_by_username(username)

        if not user.account:
            account = cls(live=True)
            account.user = user
            account.save()
            return account

    def __repr__(self):
        return f"i<Account name:{self.user.username.title()}>"


class History(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=True)
    activity = db.Column(db.String, nullable=False)
    live = db.Column(db.Boolean, default=False)

    def __int__(self, activity):
        self.activity = activity

    @classmethod
    def get_all_user_history_by_username(cls, username, live=True) -> "History.query.filter(id=self.id)":
        """get_all_user_history_by_username(username: str, live: bool) -> History query object

           Takes two parameters username -> string and live -> bool. if the user is found
           and the live parameter is set to True returns all the user's account history.

           :parameter
                username: The username to query in the database
                live: default -> True. Returns all the user's account activity if the user is live

           :returns
                Returns an SQLAlchemy query object or none if the user is not found

           :usage
                - Account.get_all_user_history_by_username(cls, username)
                - Account.get_all_user_history_by_username(cls, username, live=False)

        """
        id = db.session.query(User.id).filter_by(username=username.lower()).first()

        if id:
            return cls.query.filter(cls.id == id[0], cls.live == live)

    def save(self) -> "self":
        """Saves the user's details to the database

           :returns
              returns an instance of the class

           :usage
                hist = History(activity="some activity here...")
                hist.save()

                History(activity="some activity here...").save()
        """

        return db_saver_helper(db, self)

    def __repr__(self):
        return f"i<User history for the user :{self.account.user.username.title()}>"


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    account = db.relationship('Account', backref="user", lazy=True)
    country = db.Column(db.String(22), nullable=True)
    email = db.Column(db.String, nullable=False, unique=True)
    email_confirmed = db.Column(db.Boolean, default=False)
    email_confirmed_on = db.Column(db.DateTime, nullable=True)
    email_confirmation_sent_on = db.Column(db.DateTime, default=datetime.utcnow())
    last_login = db.Column(db.DateTime, default=datetime.utcnow())
    password = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    token = db.Column(db.String(90), nullable=True)
    username = db.Column(db.String(80), nullable=False, unique=True)

    @classmethod
    def find_by_email(cls, email: str) -> "User":
        """find_by_email(email: str) -> User sqlalchemy object

           Takes an email address in the form of a string and returns
           a User sqlalchemy query object.

           :parameter
                email: str : The email belonging to user which will be queried in the database

           :usage:
                User.find_by_email('example@gmail.com")
        """
        return cls.query.filter_by(email=email.lower()).first()

    @classmethod
    def get_user_jobs(cls, username: str, live: bool = True) -> "User.jobs":
        """get_user_jobs(username: str, live: bool) -> User.job sqlalchemy query

           Takes a username and default boolean object and queries the database
           for all the user jobs that have a set parameter of True.
           If the jobs are found it returns all a User Sqlalchemy query object
           containing the user's job or returns None.

           :parameter
                username:str: The username to be queried in the database
                live: boolean -> default True: Returns all jobs in the database are set to True

          :usage:
            User.get_user_jobs("username")
        """

        return cls.find_by_username(username).jobs.filter_by(live=live)

    @classmethod
    def find_by_username(cls, username: str) -> "User":
        """find_by_username(username:str) -> returns User object

           Takes a username in the form of a string and queries the database
           for the user. If the user is found it returns a User object or None

           :parameter
                username: Takes a username to be queried in the database

           :usage:
                User.find_by_username(username)

        """
        return cls.query.filter_by(username=username.lower()).first()

    def save(self) -> "User":
        """Saves the user's details to the database. Returns None"""

        return db_saver_helper(db, self)

    def __repr__(self):
        return f"i<User: {self.username.title()}>"

