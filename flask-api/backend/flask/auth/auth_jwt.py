import os

import jwt

class Auth:
    def __init__(self):
        self.secret = os.getenv("SECRET","ss")



    