import aiofiles
import json
from loguru import logger
from consts import ENCODING
from exceptions import UserNotFoundError

class DatabaseClient:
    def __init__(self):
        self.db = None
    
    async def load_db(self) -> None:
        async with aiofiles.open("database.json", encoding=ENCODING) as db:
            if not self.db:
                logger.debug('Start to open and load database')
                data = await db.read()
                self.db = json.loads(data)
                logger.debug('Database successfully loaded')

    async def rewrite_db(self) -> None:
        async with aiofiles.open("database.json", 'w', encoding=ENCODING) as db:
            logger.debug('Start to save (rewrite) database')
            await db.write(json.dumps(self.db, ensure_ascii=False))
            logger.debug('Database successfully rewrited')


    async def add_user(self, user_name: str, notes: str) -> None:
        await self.load_db()
        self.db[user_name] = {'notes': notes}
        logger.debug(f'User {user_name} with note {notes} added to database')
        await self.rewrite_db()

    async def delete_user(self, user_name: str) -> None:
        await self.load_db()
        try:
            logger.debug(f'Try to delete {user_name} from database')
            self.db.pop(user_name)
            logger.debug(f'User {user_name} deleted from database')
            await self.rewrite_db()
        except KeyError:
            raise UserNotFoundError

    async def get_user_data(self, user_name: str) -> None:
        await self.load_db()
        try:
            logger.debug(f'Try to get data of user {user_name} from database')
            return self.db[user_name]['notes']
        except KeyError:
            raise UserNotFoundError
