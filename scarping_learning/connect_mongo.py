import logging
from typing import Union

from mongoengine import connect, ConnectionFailure, connection


def get_connection() -> Union[connection, None]:
    try:
        return connect(
            host=f"""mongodb+srv://kbuhantsev:masterkey@database.6eflooc.mongodb.net/database?retryWrites=true&w=majority""",
            ssl=True)
    except ConnectionFailure as error:
        logging.error(error)
        return None
