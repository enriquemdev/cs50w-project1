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
    count = 0
    
    for isbn,title,author,year in reader:
        if count != 0:
            query = text("""
                        SELECT author_id FROM authors
                        WHERE author_name = :author
                        """)
            
            authorExists = db.execute(query,{"author": author }).fetchone()
            
            
            if authorExists is None:
                query = text("""
                            INSERT INTO authors(author_name) VALUES(:author)
                            """)
                db.execute(query,{"author": author })
                query = text("""
                        SELECT author_id FROM authors
                        WHERE author_name = :author
                        """)
            
                authorExists = db.execute(query,{"author": author }).fetchone()    
                
            
            query = text("""
                            INSERT INTO books(ISBN, book_title, book_author, book_year) 
                            VALUES(:ISBN, :book_title, :book_author, :book_year)
                            """)
            db.execute(query,{"ISBN": isbn, "book_title": title, 
                              "book_author": authorExists.author_id, "book_year": year})   
            print(count)
        count += 1
        
    db.commit()

if __name__ == "__main__":
    main()
    
    
    # for isbn,title,author,year in reader:
    #     query = text("""
    #                 INSERT INTO authors(author_name)  
    #                 SELECT :author
    #                 WHERE NOT EXISTS(SELECT 1 FROM authors WHERE author_name = :author)
    #                 """)
        
    #     db.execute(query,{"author": author })
        
    #     query = text("""
    #                 SELECT author_id FROM authors
    #                 WHERE author_name = :author
    #                 """)
        
    #     authorExists = db.execute(query,{"author": author }).fetchone()
        
    #     query = text("""
    #                 INSERT INTO books(ISBN, book_title, book_author, book_year) 
    #                 VALUES(:ISBN, :book_title, :book_author, :book_year)
    #                 """)
    #     db.execute(query,{"ISBN": isbn, "book_title": title, 
    #                         "book_author": authorExists.author_id, "book_year": year})   
    
    
    # tbody
    {% if libro %}
                    <tr>
                        <td>{{ loop.index }}</td>
                        <td>{{ libro.book_title }}</td>
                        <td>{{ libro.isbn }}</td>
                        <td>{{ libro.authors }}</td>
                    </tr>
                {% else %}
                    <tr>
                        <td colspan="4">No hay datos para mostrar</td>
                    </tr>
                {% endfor %}
                
                
                
  # mi api: AIzaSyArH5L21QIcx-C2tb_eO315X9rdXfH5vuM