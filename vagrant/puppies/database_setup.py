from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)
    maximum_capacity = Column(Integer, default=0)
    current_occupancy = Column(Integer, default=0)

adoptions = Table('adoptions', Base.metadata, Column('puppy_id', Integer, ForeignKey('puppy.id')), Column('adopter_id', Integer, ForeignKey('adopter.id')))

class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(6), nullable=False)
    dateOfBirth = Column(Date)
    picture = Column(String)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)
    weight = Column(Integer)
    breed = Column(Numeric(10))
    profile = relationship('PuppyProfile', uselist=False)
    adopter = relationship('Adopter', secondary=adoptions)


class PuppyProfile(Base):
    __tablename__ = 'puppy_profile'
    id = Column(Integer, primary_key=True)
    photo = Column(String(200))
    description = Column(String(500))
    special_needs = Column(String(500))
    puppy_id = Column(Integer, ForeignKey('puppy.id'), nullable=False)
    puppy = relationship('Puppy', uselist=False)

class Adopter(Base):
    __tablename__ = 'adopter'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    puppy = relationship('Puppy', secondary=adoptions)

def puppy_to_shelter(puppy, shelter):
    if shelter.current_occupancy >= shelter.maximum_capacity:
        print 'try another shelter'
    else:
        puppy.shelter = shelter
        shelter.current_occupancy += 1
        session.add(shelter)
        session.commit()

def adopt_puppy(puppy_id, *args):
    puppy = session.query(Puppy).filter_by(id=puppy_id).first()
    for adopter_id in args:
        adopter = session.query(Adopter).filter_by(id=adopter_id).first()
        puppy.adopter.append(adopter)
    puppy.shelter.current_occupancy -= 1
    session.add(puppy)
    session.commit()



engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.create_all(engine)

DBSession = sessionmaker(engine)
session = DBSession()