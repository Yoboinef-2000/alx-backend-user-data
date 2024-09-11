#!/usr/bin/env python3

from sqlalchemy.orm.session import Session, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import User  # Assuming you already have the User model defined


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

    def find_user_by(self, **kwargs) -> User:
        """Finds a user by arbitrary keyword arguments."""
        try:
            # Dynamically build the query using filter_by and the **kwargs
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            # Raise NoResultFound if no results were found
            raise NoResultFound("No user found with the provided criteria.")
        except InvalidRequestError:
            # Raise InvalidRequestError if the query arguments are invalid
            raise InvalidRequestError("Invalid query arguments.")
