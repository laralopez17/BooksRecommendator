#book_recommendation_logic.py

import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

class BookRecommender:
    def __init__(self):
        self.df_filtered = None
        self.average_ratings = None
        self.books_matrix_filtered = None
        self.SVD = TruncatedSVD(n_components=12, random_state=0)

        #inicializamos datos llamando a los métodos correspondientes
        self.load_data()
        self.filter_books()
        self.calculate_average_ratings()
        self.filter_and_select_books()

    def load_data(self):
    #aquí se cargan los datos desde archivos CSV y realizamos manipulaciones en el DataFrame
        #leemos el archivo 'books.csv' como un DataFrame utilizando Pandas, utilizando ',' como delimitador de columnas.
        books = pd.read_csv('books.csv', sep=',')
        
        #tomamos solo las 16 primeras columnas con iloc de pandas
        books = books.iloc[:, :16]
        
        #le sacamos las columnas que no nos serán utiles (drop tambien es de pandas)
        books = books.drop(columns=['title', 'best_book_id', 'work_id', 'books_count', 'isbn', 'isbn13', 'original_publication_year', 'language_code', 'work_ratings_count', 'work_text_reviews_count'])
        
        #leemos el archivo 'ratings.csv' con pandas
        ratings = pd.read_csv('ratings.csv', sep=',')
        
        #combinamos los datos de ambos datasets usando la columna "book_id"
        df = pd.merge(ratings, books, on="book_id")
        
        #eliminamos duplicados en combinaciones por pares de user_id y original_title
        df1 = df.drop_duplicates(['user_id', 'original_title'])
        
        #eliminamos duplicados en combinaciones por pares de user_id y book_id
        df1 = df1.drop_duplicates(['user_id', 'book_id'])
        self.df_filtered = df1

    def filter_books(self, good_ratings_threshold=2.0, min_ratings_threshold=5):
        #aquí filtramos libros basandonos en el umbral de ratings y el número mínimo de ratings (ambos seteados por nosotros)
        books_counts = self.df_filtered['original_title'].value_counts()
        
        #min_ratings_threshold = es el numero minimo de ratings para ser considerado como recomendable.
        selected_books = books_counts[books_counts >= min_ratings_threshold].index
        self.df_filtered = self.df_filtered[self.df_filtered['original_title'].isin(selected_books)]

    def calculate_average_ratings(self):
        #calculamos el promedio de ratings por libro
        self.average_ratings = self.df_filtered.groupby('original_title')['rating'].mean()

    def filter_and_select_books(self, good_ratings_threshold=0.0, min_ratings_threshold=5):
        #filtramos los libros con buenos ratings
        selected_books_filtered = self.average_ratings[self.average_ratings >= good_ratings_threshold].index
    
        #creamos la matriz de libros por los libros seleccionados y con buenos ratings
        #la función pivot crea una tabla dinámica donde los usuarios = filas, los libros = columnas y los valores de los ratings respectivos dentro de esa tabla con una forma (m * n).
        self.books_matrix_filtered = self.df_filtered.pivot_table(index='user_id', columns='original_title', values='rating', fill_value=0)
    
        # Seleccionar solo los libros filtrados
        self.books_matrix_filtered = self.books_matrix_filtered[selected_books_filtered]

    def find_partial_matches(self, user_input):
        #encuentra coincidencias parciales en los títulos según lo ingresado por el usuario
        matching_titles = [title for title in self.books_matrix_filtered.columns if user_input.lower() in title.lower()]
        return matching_titles

    def get_user_choice(self, user_input, matching_titles):
        #muestra las opciones al usuario y permitirle elegir
        return matching_titles
        
    def recommend_books_for_user_choice(self, user_choice, corr_threshold=0.8, rating_threshold=0.0, min_ratings_threshold=10):
        #realizar recomendaciones en base al titulo ingresado/elegido por el usuario
        if user_choice:
            #user_choice ya es el título seleccionado por el usuario
            user_input = user_choice
        else:
            #si no hay user_choice, no es necesario solicitar entrada en este punto
            user_input = None
        
        #X se convierte en la transposición de la matriz de libros filtrada
        X = self.books_matrix_filtered.values.T
        #utilizamos una técnica de reducción de dimensionalidad y ajustamos la matriz X al modelo.
        matrix = self.SVD.fit_transform(X)
        #ahora matrix contiene la representación reducida de la matriz original de libros.
        #calculamos la correlación de Pearson para las filas.
        corr = np.corrcoef(matrix)
        
        if user_input and user_input in self.books_matrix_filtered.columns:
            #obtenemos el indice del libro seleccionado en la matriz
            book_index = list(self.books_matrix_filtered.columns).index(user_input)
            
            #extraemos la columna de la matriz que corresponde a ese libro
            corr_book = corr[:, book_index]
    
            books_counts = self.df_filtered['original_title'].value_counts()
            
            #filtramos los índices de libros similares según correlación, rating promedio y cant. rating
            similar_books_indices = [
                i for i, corr_value in enumerate(corr_book)
                #este if, establece las condiciones para incluir un libro en las recomendaciones
                if corr_value >= corr_threshold and                                                         #indice de correlación >= correlación seteada
                   self.average_ratings[self.books_matrix_filtered.columns[i]] >= rating_threshold and      #rating promedio >= rating promedio seteado
                   books_counts[self.books_matrix_filtered.columns[i]] >= min_ratings_threshold             #cant. rating >= cant. rating seteada
            ]
    
            #excluimos el título ingresado de las recomendaciones
            similar_books_indices = [i for i in similar_books_indices if i != book_index]
    
            #crea una lista de recomendaciones, cada una con:
            recommendations = [
                (f"{self.books_matrix_filtered.columns[i]}",                          #título
                f"{self.df_filtered['authors'].loc[self.df_filtered['original_title'] == self.books_matrix_filtered.columns[i]].iloc[0]}",  # Autor
                corr_book[i],                                                         #correlación
                self.average_ratings[self.books_matrix_filtered.columns[i]],          #rating promedio
                books_counts[self.books_matrix_filtered.columns[i]] )                 #cant. rating
                for i in similar_books_indices
                ]
    
            return recommendations[:20]  #devolvemos hasta 20 libros recomendados
        else:
            raise ValueError("\nLo siento, el título no está en la lista de títulos con buenos ratings.")
