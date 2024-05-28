from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Profile(Base):
    __tablename__ = 'perfil'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    removed = Column(Integer, default=0, nullable=False)

    # Relacion con usuario
    users = relationship('Usuario', back_populates='profile')

    # Relacion con sucursales
    profileActions = relationship('ProfileAction', back_populates='profile')