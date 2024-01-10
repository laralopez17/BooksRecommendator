#Recomendador de Libros en Python 📚
Este proyecto consiste en un simple recomendador de libros implementado en Python con una interfaz gráfica construida con Tkinter. 
El objetivo es proporcionar sugerencias de libros basadas en las preferencias del usuario, utilizando un algoritmo de recomendación que tiene en cuenta la correlación entre libros y sus calificaciones promedio.

El proyecto se basa en los lineamientos y el tutorial proporcionado por Jonathan Peñaloza en el artículo ["Crear un Sistema de Recomendación de Libros usando Factorización de Matrices"](https://www.purocodigo.net/articulo/crear-un-sistema-de-recomendacion-de-libros-usando-factorizacion-de-matrices) en [PuroCodigo](https://www.purocodigo.net/).
Agradecimientos especiales a Jonathan Peñaloza por compartir su conocimiento y proporcionar una guía detallada que sirvió como inspiración y referencia clave en el desarrollo de este proyecto.

🚧 ##Estructura del Proyecto 🚧
**book_recommendation_gui.py**: Este archivo contiene la interfaz gráfica del recomendador. Utiliza la biblioteca Tkinter para crear una aplicación con una entrada de texto para ingresar el título del libro, 
un botón para buscar libros relacionados, una lista para mostrar coincidencias parciales, un cuadro de texto para mostrar recomendaciones y un botón para reiniciar la aplicación.

**book_recommendation_logic.py**: Aquí se encuentra la lógica del recomendador. Se carga y filtra un conjunto de datos de libros desde archivos CSV, calcula el promedio de calificaciones por libro y realiza 
recomendaciones basadas en la correlación entre libros. Utiliza la técnica de descomposición de valores singulares truncados (TruncatedSVD) para reducir la dimensionalidad de la matriz de libros.

##Instalación y Uso 🧐
###Clona el repositorio:

`git clone https://github.com/laralopez17/BooksRecommendator.git`
`cd BooksRecommendator`

###Ejecuta la aplicación: ⏯️

`python book_recommendation_gui.py`

La interfaz gráfica se abrirá, y podrás ingresar el título del libro para recibir recomendaciones.

##Dependencias 🧰
Asegúrate de tener las siguientes bibliotecas instaladas:

`pip install pandas numpy scikit-learn`

##Datos 😶‍🌫️
El proyecto utiliza archivos CSV (books.csv y ratings.csv) como fuente de datos. Asegúrate de que estos archivos estén presentes y contengan la información necesaria.
En el repositorio, encontraras dos archivos de cada uno - books.csv y ratings.csv -, uno corresponde a una base de datos más extensa que el otro para que puedas entrenar la red!

##Contribución 
¡Las contribuciones son bienvenidas! Si encuentras errores, tienes ideas para mejorar el código o quieres agregar nuevas características, no dudes en abrir problemas o enviar solicitudes de extracción.

## Acerca de Mí

¡Hola! Soy Lara, una estudiante de ingeniería informática 🧑‍🎓

- 🌐 Encuéntrame en [LinkedIn]([https://www.linkedin.com/in/tu-usuario/](https://www.linkedin.com/in/laralopez17/)
- 📧 Contáctame por correo electrónico: laralopez219@gmail.com

