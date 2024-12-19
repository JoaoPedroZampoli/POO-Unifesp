from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine, UniqueConstraint
from sqlalchemy.orm import declarative_base, sessionmaker, relationship


Base = declarative_base()


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    UniqueConstraint('title', 'author', name='uix_1')
    items = relationship("BookItem", back_populates="book")

class BookItem(Base):
    __tablename__ = "book_items"
    id = Column(Integer, primary_key=True)
    is_available = Column(Boolean, default=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    book = relationship("Book", back_populates="items")

    def borrow(self):
        if self.is_available:
            self.is_available = False
            return True
        return False
  
    def return_book(self):
        if not self.is_available:
            self.is_available = True
            return True
        return False
  
# Database setup
#Host do BD no Azure, em caso de qualquer problema, por favor entre em contato com joao.zampoli@unifesp.br
engine = create_engine('mssql+pyodbc://JoaoPZampoli:04eidD(YQx7/2hMD@projetosjpzampoli-poo.database.windows.net:1433/livrariapoo?driver=ODBC+Driver+17+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no&Connection+Timeout=30')
try:
    connection = engine.connect()
    print("Connection successful!")
    connection.close()
except Exception as e:
    print(f"Connection failed: {e}")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def add_book_to_library(session, title, author):
    book = Book(title=title, author=author)
    session.add(book)
    session.commit()

    book_item = BookItem(book_id=book.id)
    session.add(book_item)
    session.commit()
    return book


def list_all_books(session):
    return session.query(Book).all()


def borrow_book_by_id(session, book_id):
    book = session.get(Book, book_id)
    if book:
        available_item = next((item for item in book.items if item.is_available), None)
        if available_item and available_item.borrow():
            session.commit()
            return book
    return None

def return_book_by_id(session, book_id):
    book = session.get(Book, book_id)
    if book:
        borrowed_item = next((item for item in book.items if not item.is_available), None)
        if borrowed_item and borrowed_item.return_book():
            session.commit()
            return book
    return None


def add_book_ui(session):
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    book = add_book_to_library(session, title, author)
    print(f"Book '{book.title}' by {book.author} added to the library.")


def list_books_ui(session):
    books = list_all_books(session)
    if not books:
        print("No books in the library.")
    else:
        for book in books:
            available_items = [item for item in book.items if item.is_available]
            status = "Available" if available_items else "Borrowed"
            print(f"{book.id}: {book.title} by {book.author} - {status}")


def borrow_book_ui(session):
    book_id = int(input("Enter the ID of the book to borrow:"))
    book = borrow_book_by_id(session, book_id)
    if book:
        print(f"You have borrowed '{book.title}.'")
    else:
        print("Book not found or already borrowed.")


def return_book_ui(session):
    book_id = int(input("Enter the ID of the book to return:"))
    book = return_book_by_id(session, book_id)
    if book:
        print(f"You have returned '{book.title}.'")
    else:
        print("Book not found or was not borrowed.")


def main():
    session = Session()
    while True:
        print("\nLibrary Menu")
        print("1 - Add Book")
        print("2 - List Books")
        print("3 - Borrow Book")
        print("4 - Return Book")
        print("5 - Exit")
        choice = input("Enter your choice:")


        if choice == "1":
            add_book_ui(session)
        elif choice == "2":
            list_books_ui(session)
        elif choice == "3":
            borrow_book_ui(session)
        elif choice == "4":
            return_book_ui(session)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
