if __name__ == "__main__":
    from user import User


def main():
    user = User("Steve", "tests/Steve.json")
    user.try_load_data_from_json()


if __name__ == "__main__":
    main()
