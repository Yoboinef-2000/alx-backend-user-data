#!/usr/bin/env python3

from sqlalchemy import create_engine, tuple_
from sqlalchemy.orm.session import Session, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from user import User, Base


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database and return the User object"""
        # Create a new User instance
        new_user = User(email=email, hashed_password=hashed_password)

        # Add the new user to the session
        self._session.add(new_user)

        # Commit the transaction to save the new user to the database
        self._session.commit()

        # Return the newly created user
        return new_user
