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
    
    for isbn,title,author,year in reader:
        
        authors_arr = author.split(", ")
        
        for indiv_author in authors_arr:
            query = text("""
                        SELECT author_id FROM authors
                        WHERE author_name = :author
                        """) 
            author_id = db.execute(query,{"author": indiv_author }).fetchone()
            
            if author_id is None:
                query = text("""
                            INSERT INTO authors(author_name) VALUES(:author) RETURNING author_id
                            """)            
                resultado = db.execute(query,{"author": indiv_author })
                author_id = resultado.fetchone()[0]
            else:
                author_id = author_id.author_id
                
                # query = text("""
                #         SELECT author_id FROM authors
                #         WHERE author_name = :author
                #         """)
            
                # authorExists = db.execute(query,{"author": author }).fetchone()
                
        query = text("""
                        INSERT INTO books(ISBN, book_title, book_year) 
                        VALUES(:ISBN, :book_title, :book_year)
                        RETURNING book_id
                        """)
        
        resultado = db.execute(query,{"ISBN": isbn, "book_title": title, 
                            "book_year": year})     
        
        book_id = resultado.fetchone()[0]   
        
        query = text("""
                        INSERT INTO book_authors(id_author, id_book) 
                        VALUES(:id_author, :id_book)
                        """)
        
        db.execute(query,{"id_author": author_id, "id_book": book_id})  
        
    db.commit()

if __name__ == "__main__":
    main()