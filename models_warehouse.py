from datetime import date
from .database import Base
from typing import List
#from flask_security import UserMixin, RoleMixin, AsaList
from sqlalchemy.orm import relationship, backref, Mapped, mapped_column
#from sqlalchemy.ext.mutable import MutableList
import uuid
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey, Uuid

class Warehouse(Base):
    __tablename__ = 'warehouses'
    id = Column(Uuid, nullable=False, default=uuid.uuid4(), primary_key=True)
    name = Column(String(80), primary_key=True, unique=True)
    deliveries = relationship('Delivery', backref='warehouses')
    def to_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    def __repr__(self):
        return f"{self.name}:{self.id}"
    def test(self):
        return [self.__table__.columns]
        

class Partner(Base):
    __tablename__ = 'partners'
    id = Column(Uuid, nullable=False, default=uuid.uuid4(), primary_key=True)
    name = Column(String(80), primary_key=True, unique=True)
    def to_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    def __repr__(self):
        return f"{self.name}:{self.id}"

class Agreement(Base):
    __tablename__ = 'agreements'
    id = Column(Uuid, nullable=False, default=uuid.uuid4(), primary_key=True)
    partner_id = Column('partner_id', Uuid, ForeignKey('partners.id'), nullable=False)
    name = Column(String(80), primary_key=True, unique=True)
    def to_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    def __repr__(self):
        return f"{self.name}:{self.id}"

class DeliveryOperation(Base):
    __tablename__ = 'delivery_operations'
    id = Column(Uuid, nullable=False, default=uuid.uuid4(), primary_key=True)
    name = Column(String(80), primary_key=True, unique=True)
    def to_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    def __repr__(self):
        return f"{self.name}:{self.id}"

class Item(Base):
    __tablename__ = 'items'
    id = Column(Uuid, default=uuid.uuid4(), primary_key=True)
    name = Column(String(80))
    count = Column(Integer())
    units = Column(String(80))
    price = Column(Integer()) # incl VAT
    price_vat = Column(Integer(), default=20)
    delivery_id = Column('delivery_id', Uuid(), ForeignKey('deliveries.id'), nullable=False)
    #delivery = mapped_column(ForeignKey("deliveries.id"))
    #delivery: Mapped["Delivery"] = relationship(back_populates="items")
    delivery_id: Mapped[int] = mapped_column(ForeignKey("deliveries.id"))
    def to_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    def __repr__(self):
        return f"{self.name}:{self.id}"

class Delivery(Base):
    __tablename__ = 'deliveries'
    id = Column(Uuid, nullable=False, default=uuid.uuid4(), primary_key=True)
    num = Column(Integer())
    date = Column(DateTime()) 
    partner_id = Column('partner_id', Uuid(), ForeignKey('partners.id'))
    delivery_operation_id = Column('delivery_operation_id', Uuid(), ForeignKey('delivery_operations.id'))
    warehouse_id = Column('warehouse_id', Uuid(), ForeignKey('warehouses.id'))
    items = relationship('Item', backref=backref('deliveries.id'))
    #items: Mapped[List["Item"]] = relationship()
    items: Mapped[List["Item"]] = relationship(backref="Delivery")
    def to_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    def __repr__(self):
        return f"{self.num}:{self.id}"
        

