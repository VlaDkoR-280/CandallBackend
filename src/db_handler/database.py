from sqlalchemy import create_engine, Column, Integer, String, MetaData, DateTime, Time, Boolean, select, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# from ..config import db_url
from dotenv import load_dotenv
import os

load_dotenv()
engine = create_async_engine(os.getenv('DB_URL'))

Base = declarative_base()

class UserData(Base):
    __tablename__ = 'user_data'

    id = Column(Integer, primary_key=True)
    tg_id = Column(String)

    groups = relationship("UsersOfGroup", back_populates="user_data")

class GroupData(Base):
    __tablename__ = 'group_data'
    id = Column(Integer, primary_key=True)
    tg_id = Column(String)
    isgroup = Column(Boolean)
    name = Column(String)
    date_last_use = Column(DateTime)
    sub_end_date = Column(DateTime)
    time_last_update = Column(Time)

    users = relationship("UsersOfGroup", back_populates="group_data")

class UsersOfGroup(Base):
    __tablename__ = 'users_of_group'
    user_id = Column(Integer, ForeignKey('user_data.id'), primary_key=True)
    group_id = Column(Integer, ForeignKey('group_data.id'), primary_key=True)

    group_data = relationship("GroupData", back_populates="users")
    user_data = relationship("UserData", back_populates="groups")

sm = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_groups() -> list[GroupData]:
    async with sm() as session:
        stmt = select(GroupData)
        groups = await session.scalars(stmt)
        return groups.all()

async def get_groups_of_user(user_id: str) -> list[GroupData]:
    async with sm() as session:
        groups = await session.scalars(
            select(GroupData).join(UsersOfGroup, UsersOfGroup.group_id==GroupData.id)
            .join(UserData, UserData.id==UsersOfGroup.user_id)
            .where(UserData.tg_id==user_id)
            .where(GroupData.isgroup)
        )

        return groups.all()

# async def get_users(group_tg_id: str) -> list[str]:
#     async with sm() as session:
#         stmt = select(GroupData).where(GroupData.tg_id==group_tg_id)
#         group_id = await session.scalars(stmt).first().id
#         stmt = select(UsersOfGroup).where(UsersOfGroup.group_id==group_id)
#         users_of_group: list[UsersOfGroup] = await session.scalars(stmt).all()
#         users_tg_id = []
#         for user in users_of_group:
#             stmt = select(UserData).where(UserData.id==user.user_id)
#             users_tg_id.append(await session.scalars(stmt).first().tg_id)
#         return users_tg_id
#     return []