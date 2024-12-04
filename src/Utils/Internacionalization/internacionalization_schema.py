# from tinydb.storages import JSONStorage, MemoryStorage, Storage
# from tinydb.table import Table


# class MessagesTable(Table):
#     def __init__(self) -> None:
#         super().__init__(storage=MemoryStorage  , name="messages")
from tinydb.queries import Query, where
from tinydb.storages import JSONStorage
from tinydb.table import Table

Translations = Query()
