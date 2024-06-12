from src.models.message import Message
from src.models.user import User
from sqlalchemy import select


class DBManager:
    @staticmethod
    async def get_user_by_id(session, user_id: int) -> User:
        query = select(User).where(User.id == user_id)
        return await session.scalar(query)

    @staticmethod
    async def get_user_by_username(session, username: str) -> User:
        query = select(User).where(User.username == username)
        return await session.scalar(query)

    @staticmethod
    async def create_user(session, user_obj):
        if await DBManager.get_user_by_id(session, user_obj.id):
            raise ValueError("User exists")
        session.add(user_obj)
        await session.commit()

    @staticmethod
    async def create_message(session, message_obj: Message):

        session.add(message_obj)
        await session.commit()

    @staticmethod
    async def get_chats(session, username):
        user = await DBManager.get_user_by_username(session, username)
        if not user:
            raise ValueError("User not exists!")
        query = select(Message.text, Message.author_username, Message.recipient_username).where(
            Message.author_username == username or Message.recipient_username == username)
        res = await session.execute(query)
        response = []
        for row in res:
            response.append(row._mapping)
        return response
