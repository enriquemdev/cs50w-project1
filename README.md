# Project 1

Web Programming with Python and JavaScript

Este proyecto es para crear una aplicacion sobre los libros, de distintas fuentes de datos:
-Base de datos de 5000 libros
-Api de Google (GoodRreads)

Primeramente hay un archivo llamado import.py en la raiz del proyecto que toma los datos de books.csv y los importa a la base de datos normalizada, con 5000 libros. Tarda una media hora en importarlo completamente ya que esta normalizada la base de datos y algunos libros tienen más de un autor.

Hay una carpeta que se llama DB, que contiene un archivo con la estructura de la base de datos que está montada en línea.

Tiene implementado registro de usuarios y login con sus respectivas vistas, que son requeridos para acceder a las vistas de la aplicación.

Pueden hacer su propio usuario, pero sino tambien esta disponible el siguiente:
user: enrique
password: 1

o

user: luis
password: 1

Las vistas disponibles son la raiz que cuando esta logueado muestra un buscador de libros parametrizado
por si se quiere buscar por nombre del libro, autor o numero ISBN.

Al hacer esa busqueda se muestra abajo una tabla con los resultados de la busqueda, y al final de cada 
resultado hay un boton para ver una pagina completa de informacion del libro. Esta es la segunda vista.

Es la ruta book/book_id
Donde book_id es el id del libro guardado en la base de datos mediante el cual se realizan todas las busquedas, tanto a la base de datos como a la api de google.
Aqui se muestra el titulo del libro, si esta disponible la información en la api se muestra una imagen y una descripcion y la puntuación de GoodReads. 

Si no, solo se muestran los datos de la base de datos, el formulario para dejar reseñas, que envia por el metodo POST a otra ruta llamada: saveReview que solo esta encargada de guardar los datos en la bd.
Este formulario consta de unas estrellas para puntuar que funcionan con javascript y el campo de texto para la reseña en si.

En la pagina de cada libro individual se muestra si tu usuario ya hizo un comentario y si no pues muestra el formulario para enviarlo. 

Abajo salen los comentarios, que son las reseñas que hayan hecho todos los demás usuarios aparte del que está logueado.

Tambien está hecha la ruta para la api, que busca en la bd segun ISBN, y si no la encuentra devuelve un status code 404: NOT FOUND. con un mensaje de error en JSON.

La pagina es responsive, ya que utiliza las clases de bootstrap y ciertas cosas custom con css y media queries.

Los iconos son de fontawesome.