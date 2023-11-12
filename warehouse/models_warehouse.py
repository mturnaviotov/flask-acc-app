from datetime import date
from ..database import Base
from typing import List
from sqlalchemy.orm import relationship, backref, Mapped, mapped_column
import uuid
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey, Uuid

class Warehouse(Base):
    __tablename__ = 'warehouses'
    id = Column(Uuid, nullable=False, default=uuid.uuid4(), primary_key=True)
    name = Column(String(80), primary_key=True, unique=True)
    #deliveries = relationship('Delivery', backref='warehouses')
    deliveries: Mapped[List["Delivery"]] = relationship()
    def to_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    def __repr__(self):
        return f"{self.name}:{self.id}"        

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
    partner = relationship('Partner', backref='agreements')
    name = Column(String(80), primary_key=True, unique=True)
    def to_dict(self):
       src = {c.name: getattr(self, c.name) for c in self.__table__.columns}
       src['partner_name'] = self.partner.name #.to_dict()
       return src
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
    delivery_id: Mapped[Uuid] = mapped_column(ForeignKey("deliveries.id"))
    def to_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    def __repr__(self):
        return f"{self.name}:{self.id}"

class Delivery(Base):
    __tablename__ = 'deliveries'
    id = Column(Uuid, nullable=False, default=uuid.uuid4(), primary_key=True)
    num = Column(Integer())
    date = Column(DateTime())
    type = Column(Boolean())
    partner_id = Column('partner_id', Uuid(), ForeignKey('partners.id'))
    partner = relationship('Partner', backref='deliveries')
    warehouse_id: Mapped[Uuid] = mapped_column(ForeignKey("warehouses.id"))
    warehouse: Mapped["Warehouse"] = relationship(back_populates="deliveries")
    items: Mapped[List["Item"]] = relationship(backref="Delivery")
    def to_dict(self):  
       src = {c.name: getattr(self, c.name) for c in self.__table__.columns}
       src['partner_name'] = self.partner.name #.to_dict()
       src['warehouse_name'] = self.warehouse.name #.to_dict()
       return src
    def __repr__(self):
        return f"{self.num}:{self.id}"
