from sqlalchemy import Column, Integer, String, Table, TIMESTAMP, Text, MetaData, ForeignKey
from src.database import Base
from src.models.user import User

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey(User.id), nullable=False)
    recipient_id = Column(Integer, ForeignKey(User.id), nullable=False)
    text = Column(Text, nullable=False)
    date = Column(TIMESTAMP, nullable=False)
