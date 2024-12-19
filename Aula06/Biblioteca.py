from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
import datetime

LOAN_PERIOD_DAYS = 14
COOLDOWN_DAYS = 7

class LibraryError(Exception):
    def __init__(self, message: str = "An Error Occurred in the Library System"):
        super().__init__(message)

class NonMemberError(LibraryError):
    def __init__(self, member_name: str):
        message = f"{member_name} is not registered"
        super().__init__(message)

class BookNotAvaliableError(LibraryError):
    def __init__(self, book_title: str):
        message = f"The book '{book_title}' is not available"
        super().__init__(message)

class CooldownPeriodError(LibraryError):
    def __init__(self, member_name: str, cooldown_end_date: datetime.datetime):
        message = f"{member_name} is in a cooldown period until {cooldown_end_date}"
        super().__init__(message)

class NoLoanedBooksError(LibraryError):
    def __init__(self, member_name: str):
        message = f"{member_name} has no loaned books"
        super().__init__(message)

class DifferentBookError(LibraryError):
    def __init__ (self, member_name: str, book_title: str):
        message = f"{member_name} is trying to return a different book: '{book_title}'"
        super().__init__(message)

class BookNotLoanedError(LibraryError):
    def __init__(self, book_title:str):
        message = f"The book '{book_title}' is not loaned"
        super().__init__(message)

@dataclass
class Book:
    title: str
    authors: List[str]
    edition: int

class Status(Enum):
    AVAILABLE = 1
    LOANED = 2
    LOST = 3

@dataclass
class BookItem:
    book: Book
    status: Status = Status.AVAILABLE

@dataclass
class Member:
    name: str
    cooldown_end_date: Optional[datetime.datetime] = None
    current_loan: Optional[BookItem] = None

@dataclass
class Loan:
    book_item: BookItem
    member: Member
    date_borrowed: datetime.datetime
    date_returned: Optional[datetime.datetime] = None
    due_date: datetime.datetime = None

@dataclass
class Library:
    items: List[BookItem] = field(default_factory=list)
    loan_history: List[Loan] = field(default_factory=list)
    members: List[Member] = field(default_factory=list)

    def add_book_item(self, book_item: BookItem):
        self.items.append(book_item)

    def add_member(self, member: Member):
        self.members.append(member)

    def checkout(self, book_item: BookItem, member: Member) -> None:
        self.validate_checkout(book_item, member)
        
        book_item.status = Status.LOANED
        date_borrowed = datetime.datetime.now()
        due_date = date_borrowed + datetime.timedelta(days=LOAN_PERIOD_DAYS)
        loan = Loan(book_item=book_item, member=member, date_borrowed=date_borrowed, due_date=due_date)
        member.current_loan = loan
        self.loan_history.append(loan)

    def validate_checkout(self, book_item: BookItem, member: Member) -> None:
        if member not in self.members:
            raise NonMemberError(member.name)
        if book_item.status != Status.AVAILABLE:
            raise BookNotAvaliableError(book_item.book.title)
        if member.cooldown_end_date and member.cooldown_end_date > datetime.datetime.now():
            raise CooldownPeriodError(member.name, member.cooldown_end_date)

    def return_book(self, book_item: BookItem, member: Member) -> None:
        self.validate_return(book_item, member)

        # return_date = datetime.datetime.now()
        # member.current_loan.date_returned = return_date

        # if return_date > member.current_loan.due_date:
        #     member.cooldown_end_date = return_date + datetime.timedelta(days=COOLDOWN_DAYS)
    
        member.current_loan = None
        book_item.status = Status.AVAILABLE
        loan = next(loan for loan in self.loan_history if loan.book_item == book_item and loan.member == member)

        if loan:
            loan.date_returned = datetime.datetime.now()
            if loan.date_returned > loan.due_date:
                member.cooldown_end_date = loan.date_returned + datetime.timedelta(days=COOLDOWN_DAYS)
                return False
            return True

    def validate_return(self, book_item: BookItem, member: Member) -> None:
        if member not in self.members:
            raise NonMemberError(member.name)

        if member.current_loan is None:
            raise NoLoanedBooksError(member.name)

        if book_item.status != Status.LOANED:
            raise BookNotLoanedError(book_item.book.title)
        
        if member.current_loan.book != book_item:
            raise DifferentBookError(member.name, book_item.book.title)

def main():
    book1 = Book("The Great Gatsby", ["F. Scott Fitzgerald"], 1)
    book2 = Book("The Catcher in the Rye", ["J.D. Salinger"], 1)
    book_item1 = BookItem(book1)
    book_item2 = BookItem(book2)

    library = Library()
    library.add_book_item(book_item1)
    library.add_book_item(book_item2)

    member = Member("Alice")
    library.add_member(member)

    try:
        library.checkout(book_item1, member)
        print(f"'{book_item1.book.title}' checked out by {member.name}")
        library.checkout(book_item1, member)

    except LibraryError as e:
        print(e)

if __name__ == "__main__":
    main()