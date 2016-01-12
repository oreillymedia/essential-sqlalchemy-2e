from datetime import datetime

from sqlalchemy import (Column, Integer, Numeric, String, DateTime, ForeignKey,
                        Boolean, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker


conn_string = 'some conn string'
Base = declarative_base()


class Cookie(Base):
    __tablename__ = 'cookies'

    cookie_id = Column(Integer, primary_key=True)
    cookie_name = Column(String(50), index=True)
    cookie_recipe_url = Column(String(255))
    cookie_sku = Column(String(55))
    quantity = Column(Integer())
    unit_cost = Column(Numeric(12, 2))

    def __repr__(self):
        return "Cookie(cookie_name='{self.cookie_name}', " \
            "cookie_recipe_url='{self.cookie_recipe_url}', " \
            "cookie_sku='{self.cookie_sku}', " \
            "quantity={self.quantity}, " \
            "unit_cost={self.unit_cost})".format(self=self)


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer(), primary_key=True)
    username = Column(String(15), nullable=False, unique=True)
    email_address = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    password = Column(String(25), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return "User(username='{self.username}', " \
            "email_address='{self.email_address}', " \
            "phone='{self.phone}', " \
            "password='{self.password}')".format(self=self)


class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.user_id'))
    shipped = Column(Boolean(), default=False)

    user = relationship("User", backref=backref('orders', order_by=order_id))

    def __repr__(self):
        return "Order(user_id={self.user_id}, " \
            "shipped={self.shipped})".format(self=self)


class LineItem(Base):
    __tablename__ = 'line_items'
    line_item_id = Column(Integer(), primary_key=True)
    order_id = Column(Integer(), ForeignKey('orders.order_id'))
    cookie_id = Column(Integer(), ForeignKey('cookies.cookie_id'))
    quantity = Column(Integer())
    extended_cost = Column(Numeric(12, 2))

    order = relationship("Order", backref=backref('line_items',
                                                  order_by=line_item_id))
    cookie = relationship("Cookie", uselist=False)

    def __repr__(self):
        return "LineItems(order_id={self.order_id}, " \
            "cookie_id={self.cookie_id}, " \
            "quantity={self.quantity}, " \
            "extended_cost={self.extended_cost})".format(
                self=self)


class DataAccessLayer:

    def __init__(self):
        self.engine = None
        self.session = None
        self.conn_string = conn_string

    def connect(self):
        self.engine = create_engine(self.conn_string)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)


dal = DataAccessLayer()


def prep_db(session):
    c1 = Cookie(cookie_name='dark chocolate chip',
                cookie_recipe_url='http://some.aweso.me/cookie/dark_cc.html',
                cookie_sku='CC02',
                quantity=1,
                unit_cost=0.75)
    c2 = Cookie(cookie_name='peanut butter',
                cookie_recipe_url='http://some.aweso.me/cookie/peanut.html',
                cookie_sku='PB01',
                quantity=24,
                unit_cost=0.25)
    c3 = Cookie(cookie_name='oatmeal raisin',
                cookie_recipe_url='http://some.okay.me/cookie/raisin.html',
                cookie_sku='EWW01',
                quantity=100,
                unit_cost=1.00)
    session.bulk_save_objects([c1, c2, c3])
    session.commit()

    cookiemon = User(username='cookiemon',
                     email_address='mon@cookie.com',
                     phone='111-111-1111',
                     password='password')
    cakeeater = User(username='cakeeater',
                     email_address='cakeeater@cake.com',
                     phone='222-222-2222',
                     password='password')
    pieperson = User(username='pieperson',
                     email_address='person@pie.com',
                     phone='333-333-3333',
                     password='password')
    session.add(cookiemon)
    session.add(cakeeater)
    session.add(pieperson)
    session.commit()

    o1 = Order()
    o1.user = cookiemon
    session.add(o1)

    line1 = LineItem(cookie=c1, quantity=2, extended_cost=1.00)

    line2 = LineItem(cookie=c3, quantity=12, extended_cost=3.00)

    o1.line_items.append(line1)
    o1.line_items.append(line2)
    session.commit()

    o2 = Order()
    o2.user = cakeeater

    line1 = LineItem(cookie=c1, quantity=24, extended_cost=12.00)
    line2 = LineItem(cookie=c3, quantity=6, extended_cost=6.00)

    o2.line_items.append(line1)
    o2.line_items.append(line2)

    session.add(o2)
    session.commit()
