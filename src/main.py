from configs import CONTACT, TITLE
from db import DBConnectionHandler


def main() -> None:
    print(TITLE)
    print(f"Contact: {CONTACT['name']} <{CONTACT['email']}>")
    print(f"Project URL: {CONTACT['url']}")

    db_session = DBConnectionHandler.create_session(write=True)
    DBConnectionHandler.test_connection(db_session)


if __name__ == "__main__":
    main()
