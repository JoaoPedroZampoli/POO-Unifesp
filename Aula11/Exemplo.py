from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy.exc import IntegrityError


Base = declarative_base()


class Book(Base):
   __tablename__ = "books"
   id = Column(Integer, primary_key=True)
   title = Column(String(255), nullable=False)
   author = Column(String(255), nullable=False)
   items = relationship("BookItem", back_populates="book", cascade="all, delete-orphan")


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
  
   def return_item(self):
       if not self.is_available:
           self.is_available = True
           return True
       return False
  
# Database setup
engine = create_engine('mssql+pyodbc://JoaoPZampoli:04eidD(YQx7/2hMD@projetosjpzampoli-poo.database.windows.net:1433/livrariapoo?driver=ODBC+Driver+17+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no&Connection+Timeout=30')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def add_book_to_library(session, title, author, copies):
   book = Book(title=title, author=author)
   try:
       session.add(book)
       session.commit()
   except IntegrityError:
       return None
   for _ in range(copies):
       item = BookItem(book_id=book.id)
       session.add(item)
   session.commit()
   return book


def list_all_books_with_items(session):
   return session.query(Book).all()


def borrow_book_item_by_id(session, item_id):
   item = session.query(BookItem).get(item_id)
   if item and item.borrow():
       session.commit()
       return item
   return None


def return_book_item_by_id(session, item_id):
   item = session.query(BookItem).get(item_id)
   if item and item.return_item():
       session.commit()
       return item
   return None


def add_book_item(session, book_id):
    book = session.get(Book, book_id)
    if not book:
        return None
    new_item = BookItem(book_id=book_id)
    session.add(new_item)
    session.commit()
    return new_item


def list_book_items(session, book_id):
   book = session.query(Book).get(book_id)
   if not book:
       return None
   return book.items


def add_book_ui(session):
   title = input("Enter book title: ")
   author = input("Enter book author: ")
   copies = int(input("Enter number of copies: "))
   book = add_book_to_library(session, title, author, copies)
   if not book:
       print("Duplicate book.")
       return
   print(f"Book {book.title} by {book.author} with {copies} copies was added to the library.")


def list_books_ui(session):
   books = list_all_books_with_items(session)
   if not books:
       print("Library has no books.")
   else:
       for book in books:
           print(f"{book.id}: {book.title} by {book.author}")
           for item in book.items:
               status = "Available" if item.is_available else "Borrowed"
               print(f"   Copy ID {item.id}: {status}")


def borrow_book_ui(session):
   item_id = int(input("Enter the ID of the book copy to borrow:"))
   item = borrow_book_item_by_id(session, item_id)
   if item:
       print(f"You have borrowed '{item.book.title}'")
   else:
       print("Book copy not found or already borrowed.")


def return_book_ui(session):
   item_id = int(input("Enter the ID of the book copy to borrow:"))
   item = return_book_item_by_id(session, item_id)
   if item:
       print(f"You have returned book '{item.book.title}'")
   else:
       print("Book copy not found or not currently borrowed.")


def add_book_item_ui(session):
   book_id = int(input("Enter the ID of the book to add a copy: "))
   item = add_book_item(session, book_id)
   if item:
       print(f"New copy of '{item.book.title}' added with Copy ID {item.id}.")
   else:
       print(f"Book not found. Unable to add copy.")


def list_book_items_ui(session):
   book_id = int(input("Enter the ID of the book to list its copies: "))
   items = list_book_items(session, book_id)
   if items is None:
       print("Book not found or has no copies available.")
   else:
       print(f"Copies of '{items[0].book.title}' (Book ID {book_id}):")
       for item in items:
           status = "Available" if item.is_available else "Borrowed"
           print(f"   Copy ID {item.id}: {status}")
              


def main():
   session = Session()
   while True:
       print("\nLibrary Menu")
       print("1. Add Book")
       print("2. List Books")
       print("3. Borrow Book")
       print("4. Return Book")
       print("5. Add Book Copy")
       print("6. List Book Copies")
       print("7. Exit")
       choice = int(input("Enter your choice:"))


       if choice == 1:
           add_book_ui(session)
       elif choice == 2:
           list_books_ui(session)
       elif choice == 3:
           borrow_book_ui(session)
       elif choice == 4:
           return_book_ui(session)
       elif choice == 5:
           add_book_item_ui(session)
       elif choice == 6:
           list_book_items_ui(session)
       elif choice == 7:
           print("Goodbye!")
           break
       else:
           print("Invalid choice. Try again.")


if __name__ == "__main__":
   main()
