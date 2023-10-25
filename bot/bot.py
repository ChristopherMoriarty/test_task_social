import os
import random
import string
import json
from dataclasses import dataclass

import requests


@dataclass
class URLs:
    signup_user_url: str = "http://127.0.0.1:8000/api/v1.0/auth/register"
    login_user_url: str = "http://127.0.0.1:8000/api/v1.0/auth/login"
    post_create_url: str = "http://127.0.0.1:8000/api/v1.0/posts/me"
    post_get_url: str = "http://127.0.0.1:8000/api/v1.0/posts"


@dataclass
class UsersData:
    usernames: str = "bot/usernames.txt"
    emails: str = "bot/emails.txt"


class BotUtils(UsersData):
    @classmethod
    def _initialize_user_data(cls) -> dict:
        password = cls._generate_password()
        data = {
            "email": cls._get_random_element(cls.emails),
            "username": cls._get_random_element(cls.usernames),
            "password": password,
        }
        cls._save_registered_user_into_file(data)

        return json.dumps(data)

    @staticmethod
    def _read_file(file_path: str) -> list:
        with open(file_path, "r") as file:
            lines = file.readlines()

        return lines

    @classmethod
    def _get_random_element(cls, data_field: str) -> str:
        data_list = cls._read_file(data_field)
        return random.choice(data_list).replace("\n", "")

    @staticmethod
    def _generate_password() -> str:
        characters = string.ascii_letters + string.digits
        password = "".join(random.choice(characters) for i in range(8))
        return password

    @classmethod
    def _get_max_numbers_of_chosen_object(cls, choice_index: int) -> int:
        choice = cls._read_file("bot/config.csv")[choice_index]
        return int(choice.split(",")[1].replace("\n", ""))

    @staticmethod
    def _save_registered_user_into_file(user_data: dict) -> None:
        file_name = "bot/registered.csv"
        data = user_data.values()

        if os.path.exists(file_name):
            mode = "a"
        else:
            mode = "w"

        with open(file_name, mode) as file:
            file.write(",".join(data) + "\n")


class Bot(BotUtils, URLs):
    @classmethod
    def read_config(cls) -> list:
        users_count = cls._get_max_numbers_of_chosen_object(0)
        posts_count = cls._get_max_numbers_of_chosen_object(1)
        likes_count = cls._get_max_numbers_of_chosen_object(2)
        return [users_count, posts_count, likes_count]

    @classmethod
    def register_user(cls) -> None:
        data = cls._initialize_user_data()
        requests.post(cls.signup_user_url, data=data)

    @classmethod
    def login_user(cls) -> list:
        access_tokens = []
        with open("bot/registered.csv", "r") as file:
            lines = file.readlines()
            emails = [line.split(",")[0] for line in lines]
            passwords = [line.rstrip().split(",")[-1] for line in lines]
            for email, password in zip(emails, passwords):
                data = {
                    "grant_type": "",
                    "username": email,
                    "password": password,
                    "scope": "",
                    "client_id": "",
                    "client_secret": "",
                }

                response = requests.post(cls.login_user_url, data=data)

                jwt_token = response.cookies.get("token")
                access_tokens.append(jwt_token)

        return access_tokens

    @classmethod
    def create_post(cls, access_token: str) -> None:
        characters = string.ascii_letters + string.digits + string.punctuation
        title = "".join(random.choice(characters) for i in range(16))
        content = "".join(random.choice(characters) for i in range(64))

        data = {"title": title, "content": content}
        data = json.dumps(data)

        requests.post(cls.post_create_url, data=data, cookies={"token": access_token})

    @classmethod
    def get_posts(cls) -> list:
        response = requests.get(cls.post_get_url)
        posts = response.json()

        posts_ids = [post.get("id") for post in posts.get("data")]
        return posts_ids

    @classmethod
    def like_posts_randomly(cls, access_token: str, post_ids: list, likes: int):
        for i in range(likes):
            chosen_id = random.choice(post_ids)
            url = f"http://127.0.0.1:8000/api/v1.0/posts/me/{chosen_id}/like"
            requests.post(url, cookies={"token": access_token})


class Run(Bot):
    @classmethod
    def start_process(cls):
        users, posts, likes = cls.read_config()
        for i in range(users):
            cls.register_user()

        access_tokens = cls.login_user()
        for access_token in access_tokens:
            posts_to_create = random.randint(1, posts)

            for posts_count in range(posts_to_create):
                cls.create_post(access_token)

            posts_ids = cls.get_posts()
            cls.like_posts_randomly(access_token, posts_ids, likes)


Run().start_process()
