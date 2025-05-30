from sqlmodel import SQLModel, create_engine, Session

engine = create_engine("sqlite:///database.db", echo=True)

def get_session():
    with Session(engine) as session:
        yield session
    
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)