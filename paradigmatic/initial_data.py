#!/usr/bin/env python3
from paradigmatic.app.v1.users.controller import create_user

from paradigmatic.app.v1.users.schemas import UserCreate


def init() -> None:
    new_user = {"email": "kushagra.mittal@cognostics.de",
                "first_name": "Kshitij",
                "last_name": "Mittal",
                "password": "password",
                "is_superuser": True}
    create_user(UserCreate(**new_user))


if __name__ == "__main__":
    print("Creating superuser kshitij.mittal@cognostics.de")
    init()
    print("Superuser created")
