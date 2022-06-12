import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.messagebox import NO
from turtle import back
from criticalpath import Node
import math
import scipy.stats as st
import networkx as nx
import matplotlib.pyplot as plt

# Create an app with menu bar
# Options in menu bar: Create new pert, Open existing pert, Save pert, Exit

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pert App")
        self.geometry("800x600")
        self.state('zoomed')
        self.iconbitmap('descarga.ico')
        # Background color
        self.configure(background="#DECBB7")
        self.create_menu()

        self.initial_frame = tk.Frame(self, background="#DECBB7", pady=10)
        self.initial_frame.pack()

        #Create a label for the initial frame
        # fonts
        initial_label = ttk.Label(self.initial_frame, text="Pert App", font=("Helvetica", 50, "bold"), foreground="#5C5552", background="#DECBB7", width=15, anchor="center", padding=50)
        initial_label.pack()
        
        # Create instrucciones
        self.instrucciones_frame = tk.Frame(self, background="#DECBB7", pady=10)
        self.instrucciones_frame.pack()
        #Create a label for the instrucciones
        
        instrucciones_label = ttk.Label(self.instrucciones_frame, text="Instrucciones", font=("Helvetica", 20, "bold"), foreground="#5C5552", background="#DECBB7", width=40, anchor="center", relief="groove", padding=7)
        instrucciones_label.pack()

        primer_paso = ttk.Label(self.instrucciones_frame, text="1. Ingrese el número de actividades", font=("Helvetica", 15, "bold"), foreground="#5C5552", width=40, anchor="center", padding=4, background="#DECBB7")
        primer_paso.pack()

        segundo_paso = ttk.Label(self.instrucciones_frame, text="2. Ingrese los tiempos de cada actividad", font=("Helvetica", 15, "bold"), foreground="#5C5552", width=40, anchor="center", padding=4, background="#DECBB7")
        segundo_paso.pack()

        tercer_paso = ttk.Label(self.instrucciones_frame, text="3. Ingrese las dependencias entre actividades", font=("Helvetica", 15, "bold"), foreground="#5C5552", width=40, anchor="center", padding=4, background="#DECBB7")
        tercer_paso.pack()

        cuarto_paso = ttk.Label(self.instrucciones_frame, text="4. Ingrese el el tiempo deseado", font=("Helvetica", 15, "bold"), foreground="#5C5552", width=40, anchor="center", padding=4, background="#DECBB7")
        cuarto_paso.pack()


    def create_menu(self):
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Menu", menu=file_menu)
        file_menu.add_command(label="Nuevo Pert", command=self.new_pert, underline=0)
        file_menu.add_command(label="Instrucciones", command=self.instrucciones,underline=0)
        file_menu.add_command(label="Open Pert", command=self.open_pert,underline=0)
        file_menu.add_command(label="Save Pert", command=self.save_pert,underline=0)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit, accelerator="Ctrl+Q", underline=0)

        self.check_count_new_pert = 0

    def instrucciones(self):
        messagebox.showinfo("Instrucciones", "1. Ingrese el número de actividades\n2. Ingrese los tiempos de cada actividad\n3. Ingrese las dependencias entre actividades\n4. Ingrese el el tiempo deseado")
    
    def new_pert(self):
        
        self.initial_frame.pack_forget()
        self.instrucciones_frame.pack_forget()

        self.check_count_new_pert += 1
        for widget in self.winfo_children():
            if widget is not self.menu and self.check_count_new_pert > 1:
                widget.destroy()
        #Create a frame for the new pert
        self.new_pert_frame = tk.Frame(self, background="#DECBB7", pady=10)
        self.new_pert_frame.pack()
        #Create a label for the new pert
        # fonts
        new_pert_label = ttk.Label(self.new_pert_frame, text="Nuevo PERT", font=("Helvetica", 15, "bold"), foreground="#5C5552", background="#DECBB7", width=15, anchor="center", relief="groove", padding=3)
        new_pert_label.pack()
        #Label que indica cuantas actividades tiene el nuevo PERT
        new_pert_label = ttk.Label(self.new_pert_frame, text="Ingrese número de actividades", font=("Helvetica", 10, "bold"), foreground="#5C5552", width=40, anchor="center", padding=4, background="#DECBB7")
        new_pert_label.pack()
        #Create a text entry for the number of activities
        self.new_pert_text = ttk.Entry(self.new_pert_frame, width=15, font=("Helvetica", 10, "bold"), foreground="#5C5552", background="#DECBB7", justify="center")
        self.new_pert_text.pack()

        #Accept entry with an Enter
        self.new_pert_text.bind("<Return>", self.new_pert_button)
        #Create a button for the new pert
        self.np_button_frame = tk.Frame(self.new_pert_frame, background="#DECBB7", pady=10)
        self.np_button_frame.pack()

        self.np_button = tk.Button(self.np_button_frame, text="Aceptar", command=self.new_pert_button, bg="#DECBB7", fg="#5C5552", font=("Helvetica", 10, "bold"), width=15 )
        self.np_button.pack()

    def new_pert_button(self, event=None):

        if self.new_pert_text.get() == "" or self.new_pert_text.get() == "0":
            messagebox.showerror(message="Debe ingresar un numero mayor a 0", title="Error")
        else:
            self.np_button.configure(state="disabled")
            # print the text inside the text entry
            self.actividades = self.new_pert_text.get()
            # Limpiar el text entry 
            self.new_pert_text.delete(0, tk.END)
            # Create a Frame for the table
            self.table_frame = tk.Frame(background="#DECBB7", pady=10, padx=10)
            self.table_frame.pack()
            # Create a label for the table
            ttk.Label(self.table_frame, text="Actividades", background="#DECBB7", anchor="center", relief="groove", width=20).grid(column=0, row=0,  padx=5, pady=5, ipadx=5, ipady=5)
            ttk.Label(self.table_frame, text="Tiempo Optimista", background="#DECBB7", anchor="center", relief="groove" , width=20).grid(column=1, row=0,  padx=5, pady=5, ipadx=5, ipady=5 )
            ttk.Label(self.table_frame, text="Tiempo Probable", background="#DECBB7", anchor="center", relief="groove" , width=20).grid(column=2, row=0,  padx=5, pady=5, ipadx=5, ipady=5 )
            ttk.Label(self.table_frame, text="Tiempo Pesimista", background="#DECBB7", anchor="center", relief="groove" , width=20).grid(column=3, row=0,  padx=5, pady=5, ipadx=5, ipady=5 )
            ttk.Label(self.table_frame, text="Tiempo Esperado" ,background="#DECBB7", anchor="center", relief="groove", width=20).grid(column=4, row=0,  padx=5, pady=5, ipadx=5, ipady=5 )
            ttk.Label(self.table_frame, text="Varianza", background="#DECBB7", anchor="center", relief="groove" , width=20).grid(column=5, row=0,  padx=5, pady=5, ipadx=5, ipady=5)
        
            # Create an list of alphabets
            self.alphabets = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

            self.entries = []

            for i in range(1, int(self.actividades)+1): 
                # Create a label for the table
                ttk.Label(self.table_frame, text=self.alphabets[i-1], background="#DECBB7").grid(column=0, row=i, padx=5, pady=5, ipadx=5, ipady=5)
                for j in range(4):
                    if i != 0 and j != 0:
                        # Create the inputs for the table
                        self.table_input = tk.Entry(self.table_frame, width=7, font=("Helvetica", 10, "bold"), foreground="#5C5552", background="#F7F0F5", justify="center")
                        self.table_input.grid(column=j, row=i, padx=5, pady=5, ipadx=5, ipady=5)
                        self.entries.append(self.table_input)

            # Button frame
            self.btn_frame = ttk.Frame()
            self.btn_frame.pack()
            # Create a button for the table
            self.btn_tabla = tk.Button(self.btn_frame, text="Calcular", command=self.table_button, bg="#DECBB7", fg="#5C5552", font=("Helvetica", 10, "bold"), width=15 )
            self.btn_tabla.pack()
            

    def table_button(self):
        import numpy as np

        self.entries_text = []

        # Entries inputs to an array
        for i in self.entries:
            self.entries_text.append(int(i.get()) if i.get() != '' else 0)
        

        row = []
        self.matrix = []
        count = 0

        for i in self.entries_text:
            row.append(i)
            count = count + 1
            if count == 3:
                self.matrix.append(row)
                row = []
                count = 0



        for index, value in enumerate(self.matrix):
            # Insert the letter of the activity in the matrix
            value.insert(0, self.alphabets[index])
            t_e = "{:.2f}".format((value[1] + 4*value[2] + value[3])/6)
            varianza =  "{:.2f}".format(((value[1] - value[3])/6)**2)
            value.append(t_e)
            value.append(varianza)

        self.new_pert_frame.destroy()
        self.table_frame.destroy()
        self.btn_tabla.destroy()
        self.btn_frame.destroy()
        
         # Create a Frame for the table
        self.table_frame = tk.Frame(background="#DECBB7", pady=10, padx=10)
        self.table_frame.pack()
        # Create a label for the table
        ttk.Label(self.table_frame, text="Actividades", background="#DECBB7", anchor="center", relief="groove", width=20).grid(column=0, row=0,  padx=5, pady=5, ipadx=5, ipady=5)
        ttk.Label(self.table_frame, text="Tiempo Optimista", background="#DECBB7", anchor="center", relief="groove" , width=20).grid(column=1, row=0,  padx=5, pady=5, ipadx=5, ipady=5 )
        ttk.Label(self.table_frame, text="Tiempo Probable", background="#DECBB7", anchor="center", relief="groove" , width=20).grid(column=2, row=0,  padx=5, pady=5, ipadx=5, ipady=5 )
        ttk.Label(self.table_frame, text="Tiempo Pesimista", background="#DECBB7", anchor="center", relief="groove" , width=20).grid(column=3, row=0,  padx=5, pady=5, ipadx=5, ipady=5 )
        ttk.Label(self.table_frame, text="Tiempo Esperado" ,background="#DECBB7", anchor="center", relief="groove", width=20).grid(column=4, row=0,  padx=5, pady=5, ipadx=5, ipady=5 )
        ttk.Label(self.table_frame, text="Varianza", background="#DECBB7", anchor="center", relief="groove" , width=20).grid(column=5, row=0,  padx=5, pady=5, ipadx=5, ipady=5)
       

        for i in range(1, len(self.matrix)+1):
            for j in range(6):
                # Create the label of the matrix
                ttk.Label(self.table_frame, text=self.matrix[i-1][j], background="#DECBB7").grid(column=j, row=i, padx=5, pady=5, ipadx=5, ipady=5)


        # Se crea el proyecto 

        self.proyecto = Node('Proyecto')
        # DESDE HASTA
        
        self.desdeHasta_frame = ttk.Label(self, text="Ingrese dependencias (Desde - Hasta)", font=("Helvetica", 15, "bold"), foreground="#5C5552" , background="#DECBB7", anchor="center", width=50)
        self.desdeHasta_frame.pack()
        self.dependecies_table = tk.Frame(background="#DECBB7", pady=10, padx=10)
        self.dependecies_table.pack()

        ttk.Label(self.dependecies_table, text="Desde", background="#DECBB7", anchor="center", relief="groove", width=10).grid(column=0, row=0,  padx=5, pady=5, ipadx=5, ipady=5)
        ttk.Label(self.dependecies_table, text="Hasta", background="#DECBB7", anchor="center", relief="groove" , width=10).grid(column=1, row=0,  padx=5, pady=5, ipadx=5, ipady=5)


        self.desde = tk.Entry(self.dependecies_table, width=10, font=("Helvetica", 10, "bold"), foreground="#5C5552", background="#F7F0F5")
        self.desde.grid(column=0, row=1, padx=5, pady=5, ipadx=5, ipady=5)
        self.hasta = tk.Entry(self.dependecies_table, width=10, font=("Helvetica", 10, "bold"), foreground="#5C5552", background="#F7F0F5")
        self.hasta.grid(column=1, row=1, padx=5, pady=5, ipadx=5, ipady=5)

        # Button frame
        self.btn_frame = tk.Frame(pady=5, background="#DECBB7")
        self.btn_frame.pack()
        
        self.btn_dependecies = tk.Button(self.btn_frame, text="Agregar dependencia", command=self.dependecies_button, bg="#DECBB7", fg="#5C5552", font=("Helvetica", 10, "bold"))
        self.btn_dependecies.pack()

        self.dependencias_text = []

        # Button frame
        self.ruta_critica_frame = tk.Frame(background="#DECBB7", pady=5)
        self.ruta_critica_frame.pack()
        # Create a button for the table
        self.btn_ruta_critica = tk.Button(self.ruta_critica_frame, text="Calcular Ruta Critica", command=self.ruta_critica, bg="#DECBB7", fg="#5C5552", font=("Helvetica", 10, "bold"))
        self.btn_ruta_critica.pack()
    
    def dependecies_button(self):
        # Create a tuple with the data of desde and hasta
        self.tuple = (self.desde.get().upper(), self.hasta.get().upper())
        self.dependencias_text.append(self.tuple)
        
        #Clear input dede and hasta
        self.desde.delete(0, 'end')
        self.hasta.delete(0, 'end')

    def ruta_critica(self):
        # Cargar al proyecto las tareas y sus duraciones
        for index, value in enumerate(self.matrix):
            self.proyecto.add(Node(value[0], duration=float(value[4])))

        # Cargar al proyecto sus dependencias (secuencias)
        for i in self.dependencias_text:
            self.proyecto.link(i[0],i[1])
        
        # Actualizar proyecto
        self.proyecto.update_all()

        #Obtener la Ruta Crítica del modelo
        self.rutaCritica = self.proyecto.get_critical_path()

        #Sumar varianzas
        self.sumaVarianza = []
        
        for value in self.rutaCritica:
            for valor in self.matrix:
                if str(value) == str(valor[0]):
                    self.sumaVarianza.append(float(valor[5]))
        
        self.varianza_result = sum(self.sumaVarianza)


        self.desdeHasta_frame.destroy()
        self.dependecies_table.destroy()
        self.btn_frame.destroy()
        self.ruta_critica_frame.destroy()


        self.resultados = tk.Frame(background="#DECBB7", pady=10, padx=10)
        self.resultados.pack()

        
        self.ruta_critica_label = ttk.Label(self.resultados, text="Ruta Critica", font=("Helvetica", 10, "bold"), foreground="#5C5552", background="#DECBB7", anchor="center", relief="groove", width=50)
        self.ruta_critica_label.grid(column=0, row=0, padx=5, pady=5, ipadx=5, ipady=5)

        self.ruta_critica_result = ttk.Label(self.resultados, text=self.rutaCritica, font=("Helvetica", 10, "bold"), foreground="#5C5552", background="#DECBB7", anchor="center", relief="groove", width=50)
        self.ruta_critica_result.grid(column=1, row=0, padx=5, pady=5, ipadx=5, ipady=5)

        self.duration_label = ttk.Label(self.resultados, text="Duración", font=("Helvetica", 10, "bold"), foreground="#5C5552", background="#DECBB7", anchor="center", relief="groove", width=50)
        self.duration_label.grid(column=0, row=2, padx=5, pady=5, ipadx=5, ipady=5)

        self.duration_results = ttk.Label(self.resultados, text=self.proyecto.duration, font=("Helvetica", 10, "bold"), foreground="#5C5552", background="#DECBB7", anchor="center", relief="groove", width=50)
        self.duration_results.grid(column=1, row=2, padx=5, pady=5, ipadx=5, ipady=5)


        self.tiempo_deseado_frame = tk.Frame(background="#DECBB7", pady=10, padx=10)
        self.tiempo_deseado_frame.pack()

        self.ingrese_tiempo_deseado_label = ttk.Label(self.tiempo_deseado_frame, text="Ingrese el tiempo deseado", font=("Helvetica", 10, "bold"), foreground="#5C5552", background="#DECBB7", anchor="center", relief="groove", width=50)
        self.ingrese_tiempo_deseado_label.grid(column=0, row=0, padx=5, pady=5, ipadx=5, ipady=5)

        self.tiempo_deseado_input = tk.Entry(self.tiempo_deseado_frame, width=10, font=("Helvetica", 10, "bold"), foreground="#5C5552")
        self.tiempo_deseado_input.grid(column=1, row=0, padx=5, pady=5, ipadx=5, ipady=5)

        #Ingresar tiempo deseado button
        self.btn_tiempo_deseado = tk.Button(self, text="Ingresar", command=self.tiempo_deseado, bg="#DECBB7", fg="#5C5552", font=("Helvetica", 10, "bold"), width=15 )
        self.btn_tiempo_deseado.pack()

        self.resultados_probabilidad_frame = tk.Frame(background="#DECBB7", pady=10, padx=10)
        self.resultados_probabilidad_frame.pack()

        self.contador_tiempo_deseado = 0

    def tiempo_deseado(self):

        self.contador_tiempo_deseado += 1  

        if self.contador_tiempo_deseado == 4:
            self.resultados_probabilidad_frame.destroy()
            self.resultados_probabilidad_frame = tk.Frame(background="#DECBB7", pady=10, padx=10)
            self.resultados_probabilidad_frame.pack()
            self.contador_tiempo_deseado = 0

        #Calculamos normal
        normal = (int(self.tiempo_deseado_input.get()) - self.proyecto.duration )/math.sqrt(self.varianza_result) 
        formato = "%.2f" % normal
        normalTotal = st.norm.sf(abs(float(formato)))
        probabilidad = "%.5f" % (1 - normalTotal)
        
        #Format probability with %
        probabilidad = float(probabilidad) * 100

        self.probabilidad_frame = tk.Frame(self.resultados_probabilidad_frame, background="#DECBB7", pady=10, padx=10)
        self.probabilidad_frame.pack()

        self.probabilidad_label = ttk.Label(self.probabilidad_frame, text="Probabilidad de que ocurra en "+ self.tiempo_deseado_input.get() + " es", font=("Helvetica", 10, "bold"), foreground="#5C5552", background="#DECBB7", anchor="center",relief="groove", width=50, padding=10)
        self.probabilidad_label.pack()

        self.resultados_probabilidad_label = ttk.Label(self.probabilidad_frame, text=str("{:0.4f}".format(probabilidad)) + "%", font=("Helvetica", 10, "bold"), foreground="#5C5552", background="#DECBB7", anchor="center", relief="groove", width=50, padding=10)
        self.resultados_probabilidad_label.pack()

        self.tupla_tareas = []

        for i in self.matrix:
            self.tupla_tareas.append((i[0], {'duration': i[4]}))


        # initialize (directed) graph
        self.g = nx.DiGraph() 

        # add tasks and dependencies (edges)
        self.g.add_nodes_from(self.tupla_tareas)
        self.g.add_edges_from(self.dependencias_text)

        # set up the (arbitrary) positions of the tasks (nodes):
        pos_nodes = {"A": (1, 3), 
                    "B": (1, 1), 
                    "C": (2, 3), 
                    "D": (3, 3), 
                    "E": (4, 2),
                    "F": (4, 3), 
                    "G": (4, 1), 
                    "H": (5, 1), 
                    "I": (5, 2),
                    "J": (5, 3), 
                    "K": (5, 4), 
                    "L": (5, 5), 
                    "M": (6, 1),
                    "N": (6, 2), 
                    "O": (6, 3), 
                    "P": (7, 1), 
                    "Q": (7, 2),
                    "R": (7, 3), 
                    "S": (8, 1), 
                    "T": (8, 2), 
                    "U": (8, 3),
                    "V": (9, 1), 
                    "W": (9, 2), 
                    "X": (9, 3), 
                    "Y": (10, 1),
                    "Z": (10, 2),
        }

        # set up the (arbitrary) positions of the durations labels (attributes):
        pos_attrs = {node:(coord[0], coord[1] + 0.2) for node, coord in pos_nodes.items()}
        attrs = nx.get_node_attributes(self.g, 'Duration')

        # draw the nodes
        nx.draw(self.g, with_labels=True, pos=pos_nodes, node_color='lightblue', arrowsize=20)
        # draw (write) the node attributes (duration)
        nx.draw_networkx_labels(self.g, pos=pos_attrs, labels=attrs)

        crit_path = [str(n) for n in self.proyecto.get_critical_path()]
        crit_edges = [(n, crit_path[i+1]) for i, n in enumerate(crit_path[:-1])]
        nx.draw(self.g, with_labels=True, pos=pos_nodes, node_color='lightblue', arrowsize=20)
        nx.draw_networkx_labels(self.g, pos=pos_attrs, labels=attrs)
        nx.draw_networkx_edges(self.g, pos=pos_nodes, edgelist=crit_edges, width=10, alpha=0.5, edge_color='r')

        plt.margins(0.1)
        plt.title("Ruta critica")

        plt.show()

    def grid_button(self):
        print("Crear Pert")

    def open_pert(self):
        print("Open Pert")

    def save_pert(self):
        print("Save Pert")
    
    def quit(self):
        self.destroy()

# Run the app
if __name__ == "__main__":
    
    app = App()
    app.mainloop()
