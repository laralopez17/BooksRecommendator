import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD
import warnings

# Desactivar advertencias
warnings.filterwarnings("ignore", category=RuntimeWarning)

def load_data():
    # Cargar datos
    books = pd.read_csv('books.csv', sep=',')
    books = books.iloc[:, :16]
    books = books.drop(columns=['title', 'best_book_id', 'work_id', 'books_count', 'isbn', 'isbn13', 'original_publication_year', 'language_code', 'work_ratings_count', 'work_text_reviews_count'])
    ratings = pd.read_csv('ratings.csv', sep=',')
    df = pd.merge(ratings, books, on="book_id")
    df1 = df.drop_duplicates(['user_id', 'original_title'])
    df1 = df1.drop_duplicates(['user_id', 'book_id'])
    return df1

def filter_books(df, good_ratings_threshold=0.0, min_ratings_threshold=0):
    # Definir umbrales para buenos ratings
    books_counts = df['original_title'].value_counts()
    selected_books = books_counts[books_counts >= min_ratings_threshold].index

    # Filtrar DataFrame original por los libros seleccionados
    df_filtered = df[df['original_title'].isin(selected_books)]
    return df_filtered

def calculate_average_ratings(df_filtered):
    # Calcular el promedio de ratings por libro
    average_ratings = df_filtered.groupby('original_title')['rating'].mean()
    return average_ratings

def filter_and_select_books(df, good_ratings_threshold=0.0, min_ratings_threshold=0):
    # Filtrar libros con buenos ratings (por ejemplo, con un promedio mayor o igual a 4.0)
    selected_books_filtered = average_ratings[average_ratings >= good_ratings_threshold].index

    # Filtrar la matriz de libros por los libros seleccionados y con buenos ratings
    books_matrix_filtered = df.pivot_table(index='user_id', columns='original_title', values='rating').fillna(0)
    books_matrix_filtered = books_matrix_filtered[selected_books_filtered]

    return books_matrix_filtered

def recommend_books(books_matrix_filtered, SVD, title_list, corr_threshold=0.9, rating_threshold=0.0, min_ratings_threshold=10):
    X = books_matrix_filtered.values.T
    matrix = SVD.fit_transform(X)
    corr = np.corrcoef(matrix)

    # Solicitar entrada del usuario para el título
    user_input = input("Ingrese el título del libro: ")

    # Verificar si el título está en la lista
    if user_input in books_matrix_filtered.columns:
        # Obtener el índice del libro ingresado por el usuario
        book_index = title_list.index(user_input)

        # Obtener la fila de correlación para ese índice
        corr_book = corr[:, book_index]

        # Obtener los índices de libros con alta correlación, buen rating y al menos 50 ratings
        books_counts = df_filtered['original_title'].value_counts()
        similar_books_indices = [i for i, corr_value in enumerate(corr_book) if corr_value >= corr_threshold and average_ratings[title_list[i]] >= rating_threshold and books_counts[title_list[i]] >= min_ratings_threshold]

        # Imprimir hasta 20 libros
        print("\nListado de libros similares con buen rating:")
        for i in similar_books_indices[:20]:
            print(f"- {title_list[i]}: Correlación {corr_book[i]:.2f}, Rating Promedio {average_ratings[title_list[i]]:.2f}, Ratings Count {books_counts[title_list[i]]}")
    else:
        print(f"\nLo siento, '{user_input}' no está en la lista de títulos con buenos ratings.")

#if __name__ == "__main__":
#    # Cargar datos
#    df1 = load_data()

    # Filtrar libros
#    df_filtered = filter_books(df1)

    # Calcular promedio de ratings
#    average_ratings = calculate_average_ratings(df_filtered)

    # Filtrar y seleccionar libros
#    books_matrix_filtered = filter_and_select_books(df_filtered)

    # Verificar si hay suficientes libros después del filtro
#    if books_matrix_filtered.shape[1] == 0:
#        print("Lo siento, no hay suficientes libros con buenos ratings para realizar recomendaciones.")
#    else:
#        SVD = TruncatedSVD(n_components=12, random_state=0)
#        title_list = list(books_matrix_filtered.columns)

        # Realizar recomendaciones
#        recommend_books(books_matrix_filtered, SVD, title_list)
