# Para descargar la pagina
import urllib.request
# Para sacar el texto de la pagina (ya deja todo bien ordenado en un diccionario)
from bs4 import BeautifulSoup

# Para la grafica
import matplotlib.pyplot as plt

import os
# Modulo propio donde se procesa todo lo del drive
import drive

#Aqui se definen las letras del abecedario, la ventaja es que se le pueden añadir simbolos y otras letras como la ñ
abecedario = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
#En la peticion HTTP, el servidor solo responde si tiene los headers necesarios, en este caso es la aplicacion que mando la peticion y el tipo
# de datos que espera recibir
defaultHeaders = {
'User-Agent':'python 3.10.7',
	'Accept' :'text/html,application/xhtml+xml,application/xml;q=0.9',
}

#Esta funcion descarga la pagina en formato de texto y devuelve el host (e.g. www.google.com) y la pagina en texto plano
def downloadPage(url):
    try:
        #Foormar la peticion
        req = urllib.request.Request(url,headers=defaultHeaders)
        # El nombre del Host
        host = req.host
        #Hacer la peticion y decodificarla a texto
        datos = urllib.request.urlopen(req).read().decode()
    except:
        #Ocurrio algun error , asi que no hay que devolver nada
        return None,None
    return datos, host

#Esta funcion hace la mayor parte del trabajo principal, y procesa la pagina
def parsePage(url):
    #Descargar la pagina
    page, host = downloadPage(url)
    if (page==None or host==None):
        #Abortar la mision
        print("Error, Bad URL")
        return ""
    
    #Casi todos los host tienen el formato de xxx.xxxxxxx.xxx
    # Entonces, para obtener el nombre de la pagina, solo hay que dividirla
    # Por cada punto y tomar la segunda cadena de caracteres
    #En caso de que la pagina tenga formato xxx.xxxxx, entonces el dns sera el indice 0
    h = host.split(".")
    dns = ""
    if len(h) == 3: dns = host.split(".")[1]
    elif len(h) < 3: dns = host.split(".")[0]
    filename = dns
    # BeautifulSoup procesa el HTML incluyendo etiquetas y el texto que contienen y crea un objeto con toda la info
    soup =  BeautifulSoup(page,features="html.parser")
    i=0
    while (os.path.exists(f"./{filename}.csv")):
        filename = f"{dns} ({i})"
        i+=1
    #Aqui se guarda todo el texto de la pagina
    allText = ""
    with open(f"{filename}.txt","wb") as f: 
        for string in soup.strings:
            txt = string
            #print(txt)
            #Guardar texto plano
            f.write(txt.encode('utf8'))
    with open(f"{filename}.txt","rb") as f:
        #Leer todo el texto de nuevo
        allText = f.read().decode("utf8")
    #contar las letras
    #Pasar todo a mayusculas
    allText = allText.upper()
    count = []
    #Estos son los headers del archivo .csv que se va a generar
    headers = ["Letra","Frecuencia"]
    #Iterar las letras del abecedario
    for letra in abecedario:
        #Usar el metodo count para contar el numero de apariciones del caracter
        conteo = allText.count(letra)
        count.append(conteo)
        #Esta va a ser la siguiente columna del archivo csv
        row = [letra,conteo]
        #Guardar el csv con el nombre de la pagina
        saveCsv(row,headers,f"{filename}")

    #Hacer la grafica de barras con los datos contenidos en count, barras cafes y anchura de 0.4
    plt.bar(abecedario,count, color ='maroon',width = 0.4)
    #Titulo del grafico
    plt.title(f"Frecuencia de letras de {host}")
    #Guardar el grafico como png
    plt.savefig(f'{filename}.png')
    #Guardar todo en el drive
    drive.saveDrive(f"{filename}.csv","Saberes Previos",f"{filename}.csv")
    drive.saveDrive(f'{filename}.png',"Saberes Previos",f'{filename}.png')
    print ("Listo :>")
    return filename
    #print ("Pongame 10 porfa >;")

#Funcion que guarda los datos en un nuevo csv
def saveCsv(freq: list,headers: list, file: str):
    # Si no existe el archivo
    if (not os.path.exists(f"./{file}.csv")):
        #Crear uno nuevo
        with open(f"{file}.csv", 'w') as csvfile:
            #Agregar los headers
            txt = ""
            for header in headers:
                txt += header + ","
            #Para quitar la ultima ,
            csvfile.write(txt[:-1] + "\n")
    #Si ya existe el archivo
    with open(f"{file}.csv", 'a') as csvfile:
        txt = ""
        letra, conteo = freq
        txt = f"{letra},{conteo}"
        #Solo guardar la columna
        csvfile.write(txt+'\n')

