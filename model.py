from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, CHAR, Numeric, Table, DateTime
import uuid

Base = declarative_base()

# Device encryption association table
device_encryptions = Table('device_has_encryption', Base.metadata,
     Column('device_id', ForeignKey('device.id'), primary_key=True),
     Column('encryption_type_id', ForeignKey('encryption_type.id'), primary_key=True)
)

class Device(Base):
    __tablename__ = 'device'
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid1()))
    ssid = Column(String(255))
    mac = Column(CHAR(17))
    channel = Column(Integer)

    manufacturer = relationship("Manufacturer")
    manufacturer_id = Column(Integer, ForeignKey('manufacturer.id'))
    type = relationship("DeviceType")
    type_id = Column(Integer, ForeignKey('device_type.id'))

    encryptions = relationship('EncryptionType',
                             secondary=device_encryptions)

    locations = relationship("DeviceLocation")

    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class DeviceLocation(Base):
    __tablename__ = 'device_location'
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid1()))
    latitude = Column(Numeric(precision=9, scale=6))
    longitude = Column(Numeric(precision=9, scale=6))
    device = relationship("Device")
    device_id = Column(CHAR(36), ForeignKey('device.id'))

class EncryptionType(Base):
    __tablename__ = 'encryption_type'
    #name = "WPA+PSK"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    devices = relationship('Device',
                          secondary=device_encryptions)

class Manufacturer(Base):
    __tablename__ = 'manufacturer'
    #name = "Zete"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))

class DeviceType(Base):
    __tablename__ = 'device_type'
    #name = "intraesctructure" #también he visto probe
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
