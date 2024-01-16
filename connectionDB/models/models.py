from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class User_Data(Base):
    __tablename__ = 'user_data'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    apellido = Column(String(100))
    edad = Column(Integer)
    username = Column(String(50), unique=True)
    password = Column(String(250), nullable=False)
    bloqueado = Column(Boolean, default=False)

    banking = relationship('Banking', back_populates='user_data')
    failed_login_attempts = relationship('Failed_Attempts', back_populates='user_data')
    user_square_program_campus = relationship('User_Square_Program_Campus', back_populates='user_data')
    shipping_item = relationship(
        'Shipping_item',
        back_populates='user_data_issuer',
        primaryjoin='User_Data.id == Shipping_item.user_issuer'
    )
    financial_management = relationship('Financial_Management', back_populates='user_data')

class Banking(Base):
    __tablename__ = 'banking'

    id = Column(Integer, primary_key=True)
    account_number = Column(String(20), unique=True)
    balance = Column(Float)
    user_id = Column(Integer, ForeignKey('user_data.id'))

    user_data = relationship('User_Data', back_populates='banking')

class Failed_Attempts(Base):
    __tablename__ = 'failed_attempts'

    id = Column(Integer, primary_key=True)
    failed_attempts = Column(Float)
    time_first_failed = Column(DateTime, default=datetime.datetime.utcnow)
    time_last_attempt = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user_data.id'))

    user_data = relationship('User_Data', back_populates='failed_login_attempts')

class Currency(Base):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True)
    currency = Column(String(10), unique=True)
    value = Column(Float)

class Program(Base):
    __tablename__ = 'program'

    id = Column(Integer, primary_key=True)
    Name = Column(String(50))

    square_program_campus = relationship('Square_Program_Campus', back_populates='program')

class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    Name = Column(String)

    campus = relationship('Campus', back_populates='city')


class Campus(Base):
    __tablename__ = 'campus'

    id = Column(Integer, primary_key=True)
    Name = Column(String)
    square_max = Column(Integer)
    program_max = Column(Integer)
    city_id = Column(Integer, ForeignKey('city.id'))

    city = relationship('City', back_populates='campus')
    square_program_campus = relationship('Square_Program_Campus', back_populates='campus')


class Square_Program_Campus(Base):
    __tablename__ = 'square_program_campus'

    id = Column(Integer, primary_key=True)
    name = Column(String) #Londres_Campus_Sqre_1_Informatica, Manchester_Campus_Sqre_1_Medicina... Liverpool_Campus_Sqre_1_Medicina....
    campus_id = Column(Integer, ForeignKey('campus.id')) #1::Londres_Campus, 2::Manchester_Campus.....
    program_id = Column(Integer, ForeignKey('program.id')) #1::Informatica, 2::Medicina.....
    quota_max = Column(Integer) #--Cuota maxima: 5
    quota_used = Column(Integer) #--Cuota usada: 1...5

    program = relationship('Program', back_populates='square_program_campus')
    campus = relationship('Campus', back_populates='square_program_campus')
    user_square_program_campus = relationship('User_Square_Program_Campus', back_populates='square_program_campus')


class User_Square_Program_Campus(Base):
    __tablename__ = 'user_square_program_campus'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_data.id')) # 1::Javier
    square_program_campus_id = Column(Integer, ForeignKey('square_program_campus.id'))

    square_program_campus = relationship('Square_Program_Campus', back_populates='user_square_program_campus')
    user_data = relationship('User_Data', back_populates='user_square_program_campus')


class Shipping_item(Base):
    __tablename__ = 'shipping_item'

    id = Column(Integer, primary_key=True)
    serial = Column(String)
    name = Column(String)
    weight = Column(Float)
    user_issuer = Column(Integer, ForeignKey('user_data.id'))
    user_receiver = Column(Integer, ForeignKey('user_data.id'))
    shipping_date = Column(DateTime, default=datetime.datetime.utcnow)
    amount = Column(Float)
    received_status = Column(Boolean, default=False)

    user_data_issuer = relationship('User_Data', back_populates='shipping_item', foreign_keys='[Shipping_item.user_issuer]')
    user_data_receiver = relationship('User_Data', back_populates='shipping_item', foreign_keys='[Shipping_item.user_receiver]')



class Financial_Management(Base):
    __tablename__ = 'financial_management'

    id = Column(Integer, primary_key=True)
    movement = Column(String)
    category_id = Column(Integer, ForeignKey('financial_category.id'))
    user_id = Column(Integer, ForeignKey('user_data.id'))
    status_movement = Column(Boolean, default=False) #False: Expense, True: Income

    financial_category = relationship('Financial_Category', back_populates='financial_management')
    user_data = relationship('User_Data', back_populates='financial_management')


class Financial_Category(Base):
    __tablename__ = 'financial_category'

    id = Column(Integer, primary_key=True)
    category = Column(String)

    financial_management = relationship('Financial_Management', back_populates='financial_category')
    tip_financial_category = relationship('Tip_Financial_Category', back_populates='financial_category')

class Tip_Financial_Category(Base):
    __tablename__ = 'tip_financial_category'

    id = Column(Integer, primary_key=True)
    tip = Column(String)
    category_id = Column(Integer, ForeignKey('financial_category.id'))

    financial_category = relationship('Financial_Category', back_populates='tip_financial_category')