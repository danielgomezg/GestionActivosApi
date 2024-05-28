from sqlalchemy import Column, Integer, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class ProfileAction(Base):
    __tablename__ = 'perfil_accion'
    id = Column(Integer, primary_key=True, autoincrement=True)
    removed = Column(Integer, default=0, nullable=False)

    #Relacion con perfil
    profile_id = Column(Integer, ForeignKey('perfil.id'))
    profile = relationship('Profile', back_populates='profileActions')

    # Relacion con accion
    action_id = Column(Integer, ForeignKey('accion.id'))
    action = relationship('Action', back_populates='profileActions')
