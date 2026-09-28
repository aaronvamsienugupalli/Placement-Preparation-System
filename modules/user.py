from utils.file_handler import load_json, add_data


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password
        }

    @staticmethod
    def register(username, password):
        users_file = "data/users.json"

        users = load_json(users_file)

        # Check whether username already exists
        for user in users:
            if user["username"] == username:
                return False

        new_user = User(username, password)
        add_data(users_file, new_user.to_dict())

        return True

    @staticmethod
    def login(username, password):
        users_file = "data/users.json"

        users = load_json(users_file)

        for user in users:
            if user["username"] == username and user["password"] == password:
                return True

        return False