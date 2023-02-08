# Aqui empieza la aplicacion

import PySimpleGUI as sg
# modulo donde se hace todo el procesamiento
import generator
URL = ""

#Este es el cuerpo de la interfaz grafica
layout = [
    [
        #Texto plano
        sg.Text("Pegar la URL aqui"),
        #Entrada de texto
        sg.In(size=(25, 1), enable_events=True, key="-URL-"),
        #Boton
        sg.Button("Generar", key="-START-"),
    ],
    [
        #Otro texto plano
        sg.Text("Grafica"), sg.Text(text = "",key="-WAIT-",justification = "right",expand_x = True,  enable_events = True)
    ],
    [
        #Imagen
        sg.Image(key="-IMAGE-"),
    ]
]

#Crear la ventana y mostrarla en pantalla con el nombre de ventana Saberes Previos y el layout
window = sg.Window("Saberes Previos", layout)
#Loop principal del entorno grafico (loop de eventos)
while True:
    #Obtener los eventos y sus parametros
    event, values = window.read(timeout=20)
    #El evento de salida ocurre cuando se cierra la pagina
    if event == "Exit" or event == sg.WIN_CLOSED:
        #Terminar el loop
        break
    #Al presionar el boton
    elif event == "-START-":
        #Actualizar un texto
        window["-WAIT-"].update("Espere un poco (un poquito mas)")
        #Actualizar la ventana (para que el texto anterior salga en pantalla)
        window.read(timeout = 20)
        #Aqui se llamo a mi libreria donde se hace todo el procesado y le paso como referencia la URL
        # La URL es una variable global que se actualiza cuando cambia el texto en el input field
        name = generator.parsePage(URL)
        if (name != ""):
            # Actualizar la imagen de la GUI con la imagen generada por la funcion
            window["-IMAGE-"].update(filename = f"{name}.png")
        # Si la funcion no devuelve nada,  hubo un error, lo mejor es ignorarlo y hacer como si no pasara nada
        else:
            pass
        #Actualizar le texto de espera
        window["-WAIT-"].update("")

    #Cambio el Texto de la URL
    elif values["-URL-"]:
        URL = values["-URL-"]
#Al terminar el loop de eventos, cerrar la ventana
window.close()