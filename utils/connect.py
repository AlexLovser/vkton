from pymongo import MongoClient, ReturnDocument


class ConnectionManager:
    single = None
    PUBLIC = False

    def __new__(cls):
        if not cls.single:
            cls.single = super().__new__(cls)
        return cls.single

    def __init__(self):
        if self.PUBLIC:
            ip = '80.85.142.151'
        else:
            ip = '127.0.0.1'


        # mongodb://alex:EyKhxQBPWNbcCm63b4GKlkoo@127.0.0.1:38128/?authMechanism=DEFAULT
        client = MongoClient(f'mongodb://alex:EyKhxQBPWNbcCm63b4GKlkoo@{ip}:38128/?authMechanism=DEFAULT', serverSelectionTimeoutMS=5000)
        db = client['ston']
        self.configs = db['configs']

        self.users = db['users']
        self.teams = db['teams']
        self.tickets = db['tickets']
        self.stars = db['stars']

        
        ConnectionManager.single = self



        
    



    