import sqlite3
import pandas as pd
from os import path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter as tk
from tkinter import messagebox

estadisticas_solicitadas = "name, japanese_name, hp, attack, defense, sp_attack, sp_defense, speed, generation, base_total, pokedex_number, is_legendary, type1, type2"

def crear_db(conn):

    df = pd.read_csv("pokemon.csv")
    df.to_sql("pokemon", conn, if_exists = "replace", index = False)

def elegir_pokemon(cursor, busqueda, root):

    estadisticas = None

    try:
        busqueda = int(busqueda)
        estadisticas = buscar(cursor, busqueda)
    except:
        if busqueda == "":
            messagebox.showerror("Entrada vacia", "Debes ingresar un nombre o numero")
        else:
            busqueda = str(busqueda)
            busqueda = busqueda.capitalize()
            estadisticas = buscar(cursor, busqueda)

    crear_grafico(estadisticas, root)

def buscar(cursor, busqueda):

    if type(busqueda) == str:
        cursor.execute("""SELECT {} FROM pokemon
        WHERE name = '{}'
        """.format(estadisticas_solicitadas, busqueda))
    else:
        cursor.execute("""SELECT {} FROM pokemon
        WHERE pokedex_number = '{}'
        """.format(estadisticas_solicitadas, busqueda))
    
    dato = cursor.fetchone()
    return dato

def crear_grafico(estadisticas, root):

    try:
        estadisticas = list(estadisticas)
        stats = estadisticas[2:8]
    except:
        messagebox.showerror("No encontrado", "Por favor ingresa de nuevo el nombre/numero o busca uno diferente")

    titulo = str(estadisticas[0]) + " / " + str(estadisticas[1])

    graficar_datos = tk.Toplevel(root)
    graficar_datos.title(titulo)
    frame_left = tk.Frame(graficar_datos)
    frame_right = tk.Frame(graficar_datos)
    frame_left.grid(column = 0)
    frame_right.grid(column = 1)

    etiquetas = np.array([
        "HP: " + str(estadisticas[2]),
        "Attack: " + str(estadisticas[3]), 
        "Defense: " + str(estadisticas[4]), 
        "Special Attack: " + str(estadisticas[5]), 
        "Special Defense: " + str(estadisticas[6]), 
        "Speed: " + str(estadisticas[7])])
    
    angulos = np.linspace(0, 2 * np.pi, len(etiquetas), endpoint = False)
    fig = plt.figure()
    ax = fig.add_subplot(111, polar = True)
    ax.plot(angulos, stats, 'o-', linewidth = 2)
    ax.fill(angulos, stats, alpha = 0.25)
    ax.set_thetagrids(angulos * 180 / np.pi, etiquetas)
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master = frame_right)
    canvas.draw()
    canvas.get_tk_widget().grid(row = 1, column = 1)

    label_titulo = tk.Label(frame_left, text = "Nombre: " + str(titulo))
    label_titulo.config(font = (60))
    label_titulo.pack(anchor = "nw")

    label_numero = tk.Label(frame_left, text = "Numero: " + str(estadisticas[10]))
    label_numero.config(font = (40))
    label_numero.pack(anchor = "nw")

    label_generacion = tk.Label(frame_left, text = "Generacion: " + str(estadisticas[8]))
    label_generacion.config(font = (40))
    label_generacion.pack(anchor = "nw")

    label_total = tk.Label(frame_left, text = "Puntos totales: " + str(estadisticas[9]))
    label_total.config(font = (40))
    label_total.pack(anchor = "nw")

    label_tipo1 = tk.Label(frame_left, text = "Tipo primario: " + str(estadisticas[12]).capitalize())
    label_tipo1.config(font = (40))
    label_tipo1.pack(anchor = "nw")

    tipo_secundario = str(estadisticas[13])
    if tipo_secundario == "None":
        tipo_secundario = "Ninguno"
    else:
        tipo_secundario = tipo_secundario.capitalize()

    label_tipo2 = tk.Label(frame_left, text = "Tipo secundario: " + str(tipo_secundario))
    label_tipo2.config(font = (40))
    label_tipo2.pack(anchor = "nw")

    legendario = str(estadisticas[11])
    if legendario == "1":
        label_legendario = tk.Label(frame_left, text = "¡Es legendario!")
        label_legendario.config(font = (40))
        label_legendario.pack(anchor = "nw")
    else:
        pass

def gui_inicio(cursor):

    root = tk.Tk()
    root.title("Pokedex v2")
    root.geometry("300x100")
    
    bienvenida = tk.Label(root, text = "Bienvenid@")
    bienvenida.config(font = (40))
    bienvenida.pack(anchor = "center")

    mensaje = tk.Label(root, text = "Puedes buscar por nombre o numero")
    mensaje.config(font = 25)
    mensaje.pack(anchor = "center")

    cuadro_busqueda = tk.Entry(root)
    cuadro_busqueda.pack()

    boton_buscar = tk.Button(root, text = "Buscar", command = lambda : elegir_pokemon(cursor, cuadro_busqueda.get(), root))
    boton_buscar.pack()

    root.mainloop()

def main():

    conn = sqlite3.connect("pokemon.db")
    cursor = conn.cursor()

    if path.exists("pokemon.db") == False:
        crear_db(conn)
    else:
        pass
    
    gui_inicio(cursor)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()