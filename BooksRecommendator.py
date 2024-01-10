import pandas as pd
import numpy as np
import sklearn
from sklearn.decomposition import TruncatedSVD
import warnings
warnings.filterwarnings("ignore",category =RuntimeWarning)


books = pd.read_csv('books.csv', sep=',')
books = books.iloc[:, :16]
books = books.drop(columns=['title', 'best_book_id', 'work_id', 'books_count', 'isbn', 'isbn13', 'original_publication_year','language_code','work_ratings_count','work_text_reviews_count'])
ratings = pd.read_csv('ratings.csv', sep=',')
df = pd.merge(ratings, books, on="book_id")
df1= df.drop_duplicates(['user_id','original_title'])
df1= df.drop_duplicates(['user_id','book_id'])

books_matrix = df1.pivot_table(index = 'user_id', columns = 'original_title', values = 'rating').fillna(0)

X = books_matrix.values.T
SVD = TruncatedSVD(n_components=12, random_state=0)
matrix = SVD.fit_transform(X)

corr = np.corrcoef(matrix)

title = books_matrix.columns
title_list = list(title)
maze_runner = title_list.index('The Maze Runner')
corr_maze_runner  = corr[maze_runner]
list(title[(corr_maze_runner >= 0.9)])