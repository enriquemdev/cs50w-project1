CREATE TABLE users (
    user_id SERIAL PRIMARY KEY NOT NULL,
    username VARCHAR(40) NOT NULL,
    hashed_pass VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE authors (
    author_id SERIAL PRIMARY KEY NOT NULL,
    author_name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE books (
    book_id SERIAL PRIMARY KEY NOT NULL,
    ISBN VARCHAR(80) NOT NULL UNIQUE,
    book_title VARCHAR(150) NOT NULL,
    book_year INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE book_authors (
    book_author_id SERIAL PRIMARY KEY NOT NULL,
    id_author INT NOT NULL,
    id_book INT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (id_author) REFERENCES authors(author_id),
    FOREIGN KEY (id_book) REFERENCES books(book_id)
);

CREATE TABLE book_reviews (
    review_id SERIAL PRIMARY KEY NOT NULL,
    review_book INT NOT NULL,
    review_user INT NOT NULL,
    review_points INTEGER NOT NULL,
    review_content TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (review_book) REFERENCES books(book_id),
    FOREIGN KEY (review_user) REFERENCES users(user_id)
);

CREATE INDEX idx_ISBN ON books (ISBN);
CREATE INDEX idx_titulo_libro ON books (book_title);
CREATE INDEX idx_nombre_autor ON authors (author_name);