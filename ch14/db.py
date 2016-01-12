# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, Numeric, Unicode
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Album(Base):
    __tablename__ = 'Album'

    AlbumId = Column(Integer, primary_key=True, unique=True)
    Title = Column(Unicode(160), nullable=False)
    ArtistId = Column(ForeignKey(u'Artist.ArtistId'), nullable=False, index=True)

    Artist = relationship(u'Artist')


class Artist(Base):
    __tablename__ = 'Artist'

    ArtistId = Column(Integer, primary_key=True, unique=True)
    Name = Column(Unicode(120))


class Genre(Base):
    __tablename__ = 'Genre'

    GenreId = Column(Integer, primary_key=True, unique=True)
    Name = Column(Unicode(120))


class MediaType(Base):
    __tablename__ = 'MediaType'

    MediaTypeId = Column(Integer, primary_key=True, unique=True)
    Name = Column(Unicode(120))


class Track(Base):
    __tablename__ = 'Track'

    TrackId = Column(Integer, primary_key=True, unique=True)
    Name = Column(Unicode(200), nullable=False)
    AlbumId = Column(ForeignKey(u'Album.AlbumId'), index=True)
    MediaTypeId = Column(ForeignKey(u'MediaType.MediaTypeId'), nullable=False, index=True)
    GenreId = Column(ForeignKey(u'Genre.GenreId'), index=True)
    Composer = Column(Unicode(220))
    Milliseconds = Column(Integer, nullable=False)
    Bytes = Column(Integer)
    UnitPrice = Column(Numeric(10, 2), nullable=False)

    Album = relationship(u'Album')
    Genre = relationship(u'Genre')
    MediaType = relationship(u'MediaType')
