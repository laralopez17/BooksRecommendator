#book_recommendation_gui.py

import tkinter as tk
from tkinter import ttk, messagebox
from book_recommendation_logic import BookRecommender

class BookRecommendationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recomendador de Libros")

        #inicializar el objeto de la lógica
        self.book_recommender = BookRecommender()

        self.create_gui()

    def create_gui(self):
        #aquí creamos la interfaz gráfica
        self.label = ttk.Label(self.root, text="Ingrese el título del libro:")
        self.label.pack(pady=10)

        self.entry = ttk.Entry(self.root, width=30)
        self.entry.pack(pady=10)
        
        #creamos un botón para llamar la función titulos_relacionados
        #asociamos también la tecla Enter con la función titulos_relacionados
        self.entry.bind("<Return>", lambda event: self.titulos_relacionados())
        self.button = ttk.Button(self.root, text="Buscar Libros", command=self.titulos_relacionados)
        self.button.pack(pady=10)
        
        self.label = ttk.Label(self.root, text="Seleccione el libro de referencia del siguiente listado")
        self.label.pack(pady=10)
        
        #creamos un Listbox para mostrar las coincidencias parciales
        self.matching_titles_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, exportselection=False, width=100)
        self.matching_titles_listbox.pack(pady=10)

        #asociamos la selección del libro a buscar en el Listbox con la función select_user_choice
        self.matching_titles_listbox.bind("<<ListboxSelect>>", self.select_user_choice)
        
        #creamos un cuadro de texto para mostrar las recomendaciones
        self.recommendations_text = tk.Text(self.root, wrap=tk.WORD, width=100, height=10)
        self.recommendations_text.pack(pady=10)
        
        #creamos un botón para reiniciar la aplicación
        restart_button = ttk.Button(self.root, text="Reiniciar", command=self.restart_app)
        restart_button.pack(pady=10)
        
    def titulos_relacionados(self):
        #esta función busca los titulos que contienen parte de lo ingresado por el usuario
        user_input = self.entry.get()
        if user_input:
            #llama a la función en la lógica que encuentra libros relacionados con lo que ingreso el usuario.
            matching_titles = self.book_recommender.find_partial_matches(user_input)
            
            #si hay coincidencia
            if matching_titles:
                #aquí se limpia el listbox
                self.matching_titles_listbox.delete(0, tk.END)
                for title in matching_titles:
                    #aquí se insertan los titulos
                    self.matching_titles_listbox.insert(tk.END, title)

            else:
                #si no hay coincidencias, mostrar un mensaje en el Listbox
                self.matching_titles_listbox.delete(0, tk.END)
                self.matching_titles_listbox.insert(tk.END, "No hay coincidencias")

    def select_user_choice(self, event):
        selected_index = self.matching_titles_listbox.curselection()
        if selected_index:
            # Obtener el título seleccionado
            selected_title = self.matching_titles_listbox.get(selected_index)
            # Establecer el título seleccionado en la entrada de texto
            self.entry.delete(0, tk.END)
            self.entry.insert(0, selected_title)
            
            # Obtener las recomendaciones para el título seleccionado
            recommendations = self.book_recommender.recommend_books_for_user_choice(selected_title)
            
            # Llamar a la función para mostrar las recomendaciones
            self.show_recommendation_dialog(recommendations)


    def show_recommendation_dialog(self, recommendations):
        # Limpiar el contenido anterior
        self.recommendations_text.delete(1.0, tk.END)

        if recommendations:
        #muestra las recomendaciones en la pantalla de recomendaciones
            for recommendation in recommendations:
                #aquí se arma el texto teniendo en cuenta lo pasado por parámetro desde la lógica.
                book_info = f"- {recommendation[0]} por {recommendation[1]}\n  Correlación: {recommendation[2]:.2f}, Promedio de Rating: {recommendation[3]:.2f}, Cant. Ratings: {recommendation[4]}\n\n"
                #acá se inserta en la pantalla de recomendaciones
                self.recommendations_text.insert(tk.END, book_info)
        else:
            #muestra un mensaje si no hay recomendaciones
            self.recommendations_text.insert(tk.END, "Lo siento, no hay recomendaciones para mostrar.")

    def restart_app(self):
        # Restablecer el estado inicial de la aplicación
        self.entry.delete(0, tk.END)  #se limpia la entrada de texto
        self.recommendations_text.delete(1.0, tk.END)  #se limpia la cuadro de recomendaciones
        self.matching_titles_listbox.delete(0, tk.END)  #se limpia el Listbox de matching_titles

if __name__ == "__main__":
    root = tk.Tk()
    app = BookRecommendationApp(root)
    root.mainloop()
