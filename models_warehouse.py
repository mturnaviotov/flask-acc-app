from datetime import date
from .database import Base
from typing import List
#from flask_security import UserMixin, RoleMixin, AsaList
from sqlalchemy.orm import relationship, backref, Mapped,mapped_column
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import Boolean, DateTime, Column, Integer, \
                    String, ForeignKey

class Warehouse(Base):
    __tablename__ = 'warehouses'
    warehouse_id = Column(Integer, primary_key=True, autoincrement=True)
    warehouse_name = Column(String(80))
    def to_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f'{self.warehouse_name}>'

class Partner(Base):
    __tablename__ = 'partners'
    partner_id = Column(Integer, primary_key=True, autoincrement=True)
    partner_name = Column(String(80))
    def to_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f'{self.partner_name}>'

class Agreement(Base):
    __tablename__ = 'agreements'
    agreement_id = Column(Integer(), primary_key=True, autoincrement=True)
    partner_id = Column('partner_id', Integer(), ForeignKey('partners'))
    agreement_name = Column(String(80))
    def to_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f'{self.agreement_name}>'

class DeliveryOperation(Base):
    __tablename__ = 'delivery_operations'
    delivery_operation_id = Column(Integer, primary_key=True, autoincrement=True)
    delivery_operation_name = Column(String(80))
    def to_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f'{self.delivery_operation_name}>'

class Item(Base):
    __tablename__ = 'items'
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    item_name = Column(String(80))    
    item_count = Column(Integer())
    item_units = Column(String(80), unique=False)
    item_price = Column(Integer(), unique=False) # incl VAT
    item_price_vat = Column(Integer(), unique=False, default=20)
    delivery_id = Column('delivery_id', Integer(), ForeignKey('deliveries'))
    def to_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f'{self.item_name}>'

class Delivery(Base):
    __tablename__ = 'deliveries'
    delivery_id = Column(Integer, primary_key=True, autoincrement=True)
    delivery_num = Column(Integer(), unique=True)
    delivery_date = Column(DateTime())    
    delivery_type = Column(Integer())
    partner_id = Column('partner_id', Integer(), ForeignKey('partners'))
    delivery_operation_id = Column('delivery_operation_id', Integer(), ForeignKey('delivery_operations'))
    warehouse_id = Column('warehouse_id', Integer(), ForeignKey('warehouses'))
    items = relationship('Item', backref=backref('deliveries'))
#    items: Mapped[List["Item"]] = relationship(backref="deliveries")
#    items = items
    def to_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f'{self.delivery_id}>'
