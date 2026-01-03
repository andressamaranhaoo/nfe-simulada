from app.infrastructure.db.session import engine
from app.infrastructure.db.models import Base


def init():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init()
