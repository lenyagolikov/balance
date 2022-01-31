from app.db.session import engine
from app.models import Base, Transaction, User  # noqa


def main():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    main()
