import hashlib

from src.database import DB
from itsdangerous import (
        TimedJSONWebSignatureSerializer as Serializer,
        BadSignature,
        SignatureExpired
        )

SECRET_KEY = "YwY[IA,LWgZxxCmX8Mug;t2Do}}1?%Fd$:2zx!mKP9#52F[>IQb_I2aek!e,ktV"

class User:
    def __init__(self, id, first_name, last_name, password, age, gender, email, address):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.age = age
        self.gender = gender
        self.email = email
        self.address = address

    def create(self):
        with DB() as db:
            values = (self.first_name, self.last_name, self.age, self.gender, self.email, self.password, self.address)
            db.execute('''
                INSERT INTO User(user_first_name, user_last_name, age, gender, user_mail, password, address) VALUES(?, ?, ?, ?, ?, ?, ?)
                ''', values)

            return self

    def delete(self):
        with DB() as db:
            db.execute('''
                DELETE FROM User WHERE user_id = ?
                ''', self.id)

    @staticmethod
    def find_by_firstname(first_name):
        with DB() as db:
            values = db.execute('''
                SELECT * FROM User WHERE user_first_name = ?
            ''', (first_name,)).fetchone()
            if values:
                return User(*values)
            return None

    @staticmethod
    def find_by_lastname(last_name):
        with DB() as db:
            values = db.execute('''
                SELECT * FROM User WHERE user_last_name = ?
            ''', (last_name,)).fetchone()
            if values:
                return User(*values)
            return None
    
    @staticmethod
    def find_by_email(email):
        with DB() as db:
            values = db.execute('''
                SELECT id, user_first_name, user_last_name, password, age, gender, user_mail, address FROM User WHERE user_mail = ?
            ''', (email,)).fetchone()
            if values:
                return User(*values)
            return None

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def verify_password(self, new_password):
        return self.password == User.hash_password(new_password)

    def generate_token(self):
        s = Serializer(SECRET_KEY, expires_in=1000)
        return s.dumps({'email': self.email})

    @staticmethod
    def verify_token(token):
        s = Serializer(SECRET_KEY)
        try:
            s.loads(token)
        except SignatureExpired:
            return False
        except BadSignature:
            return False
        return True