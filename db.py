from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean, func
import datetime

DATABASE_URL = "mysql+mysqlconnector://admin:Root*1234@localhost:3306/flaskdb"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

db = SessionLocal()


class AbstractModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    created_date = Column(DateTime, default=func.now(), server_default=func.now())


class User(AbstractModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(200))
    # Establish a one-to-many relationship with orders
    orders = relationship("Order", back_populates="user")
    todos = relationship("Todo", back_populates="user")  # Add this line


class Order(AbstractModel):
    __tablename__ = "orders"
    name = Column(String(50), index=True)
    quantity = Column(Integer, index=True)
    # Establish a foreign key relationship with users
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="orders")


class Todo(AbstractModel):
    __tablename__ = "todos"
    title = Column(String(255), nullable=False)
    description = Column(String(1000))
    due_date = Column(DateTime)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))  # Assuming you have a 'users' table

    # Define a relationship with the User model (assuming you have a User model)
    user = relationship("User", back_populates="todos")


def create(database: db, item):
    database.add(item)
    database.commit()
    database.refresh(item)
    return item


def get_user_by_id(database: db, user_id: int):
    return database.query(User).filter(User.id == user_id).first()
# Create database tables
# Base.metadata.create_all(bind=engine)
