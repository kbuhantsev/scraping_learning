import logging
from typing import Any, Union

from mongoengine import connect, ConnectionFailure


def get_connection() -> Union[Any, None]:
    try:
        return connect(
            host="mongodb+srv://kbuhantsev:masterkey@database.6eflooc.mongodb.net/\
                  database?retryWrites=true&w=majority",
            ssl=True,
        )
    except ConnectionFailure as error:
        logging.error(error)
        return None
