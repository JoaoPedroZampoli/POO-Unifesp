from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker, Session


Base = declarative_base()


class Author(Base):
   __tablename__ = 'Author'
   id = Column(Integer, primary_key=True)
   name = Column(String(256))
   books = relationship("Book", back_populates="author")


class Book(Base):
   __tablename__ = 'Book'
   id = Column(Integer, primary_key=True)
   title = Column(String(256))
   author_id = Column(Integer, ForeignKey("Author.id"))
   author = relationship("Author", back_populates="books")


engine = create_engine('mysql+mysqlconnector://....') # ALTERAR PARA O SEU BANCO!
Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()


author = Author(name="J.K. Rowling")
book1 = Book(title="Harry Potter and the Sourcerer's Stone", author=author)
book2 = Book(title="Harry Potter and the Chamber of Secrets", author=author)


session.add(author)
session.commit()


result = session.query(Author).filter_by(name="J.K. Rowling").first()
print(f"Author: {result.name}, Books: {[book.title for book in result.books]}")
