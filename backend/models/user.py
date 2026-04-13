from sqlalchemy import Column, BigInteger, String, Text
from sqlalchemy.orm import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(String(50), nullable=False, default="user")

    def set_password(self,password) :
        self.password_hash  = generate_password_hash(password)

    def check_password(self,password) :
        return check_password_hash(self.password_hash,password)
