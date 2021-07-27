from .database import Base
from flask import jsonify
from flask_security import UserMixin, RoleMixin, AsaList
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import Boolean, DateTime, Column, Integer, \
                    String, ForeignKey

class RolesUsers(Base):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('users.id'))
    role_id = Column('role_id', Integer(), ForeignKey('roles.id'))

class Role(Base, RoleMixin):
    __tablename__ = 'roles'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))
    permissions = Column(MutableList.as_mutable(AsaList()), nullable=True)
    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'description': self.description, 'permissions': self.permissions}

class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    fs_uniquifier = Column(String(64), unique=True, nullable=False)
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users',backref=backref('users', lazy='dynamic'))
    def to_dict(self):
        props = {'id': self.id, 'email': self.email, 'username': self.username, 'last_login_at': self.last_login_at, 'current_login_ip':
        self.current_login_ip, 'login_count': self.login_count, 'active': self.active, 'confirmed_at': self.confirmed_at}
        return props
    
