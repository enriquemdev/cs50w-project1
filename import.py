import csv
import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    next(reader)
    
    # for each row in the csv file
    for isbn,title,author,year in reader:
        # Save the book and get its id
        query = text("""
                        INSERT INTO books(ISBN, book_title, book_year) 
                        VALUES(:ISBN, :book_title, :book_year)
                        RETURNING book_id
                        """)
        
        resultado = db.execute(query,{"ISBN": isbn, "book_title": title, 
                            "book_year": year})     
        
        book_id = resultado.fetchone()[0] 
        
        # split the authors column if it has multiple authors
        authors_arr = author.split(", ")
        
        #iterate over the authors of the book
        for indiv_author in authors_arr:
            # looks if it is already in db
            query = text("""
                        SELECT author_id FROM authors
                        WHERE author_name = :author
                        """) 
            author_id = db.execute(query,{"author": indiv_author }).fetchone()
            
            #if it wasnt in the db
            if author_id is None:
                #insert it and get its id
                query = text("""
                            INSERT INTO authors(author_name) VALUES(:author) RETURNING author_id
                            """)            
                resultado = db.execute(query,{"author": indiv_author })
                author_id = resultado.fetchone()[0]
            else:
                # get its id if it was inserted
                author_id = author_id.author_id
            
            # insert the relationship between author & book in db    
            query = text("""
                            INSERT INTO book_authors(id_author, id_book) 
                            VALUES(:id_author, :id_book)
                            """)
            
            db.execute(query,{"id_author": author_id, "id_book": book_id})  
    db.commit()

if __name__ == "__main__":
    main()