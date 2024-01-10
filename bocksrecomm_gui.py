import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from book_recommendation_logic import load_data, filter_books, calculate_average_ratings, filter_and_select_books, recommend_books

class BookRecommendationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Recommendation App")

        self.load_data()
        self.filter_books()
        self.calculate_average_ratings()
        self.filter_and_select_books()

        self.create_gui()

    # Las funciones de carga de datos y procesamiento se llaman desde aquí

    def create_gui(self):
        # Crear la interfaz gráfica
        self.label = ttk.Label(self.root, text="Ingrese el título del libro:")
        self.label.pack(pady=10)

        self.entry = ttk.Entry(self.root, width=30)
        self.entry.pack(pady=10)

        self.button = ttk.Button(self.root, text="Recomendar Libros", command=self.show_recommendations)
        self.button.pack(pady=10)

    def show_recommendations(self):
        user_input = self.entry.get()
        if user_input:
            try:
                recommend_books(self.books_matrix_filtered, self.SVD, self.title_list, user_input=user_input)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un título de libro.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BookRecommendationApp(root)
    root.mainloop()
