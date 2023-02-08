import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload




# If modifying these scopes, delete the file token.json.
# Aqui va que tanto permiso se le da a la aplicacion (drive.file permite crear y modificar archivos)
# https://developers.google.com/drive/api/guides/api-specific-auth
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Inicio de sesion y creacion de un token
def OAuth():
    creds = None
    #El token.json se crea automaticamente con las credenciales de la API
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # Si aun no hay token, hacer que el usuario ingrese
    if not creds or not creds.valid:
        # Expiro el token
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Abre una pestaña para que el usuario ingrese (solo cuentas autorizados pueden ingresar a aplicaciones que no estan verificadas)
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Guardar el token
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

# Busca archivos en el drive que contengan el query 
def search(query,service):
    try:
        #Ejecutar la busqueda
        results = service.files().list(
            pageSize=30, q = f"name = '{query}'", fields="nextPageToken, files(id, name)").execute()
            #pageSize=30, f = query,fields="nextPageToken, files(id, name)").execute()
        # Guardar el campo files en una lista
        items = results.get('files', [])
        if not items:
            return []
        return items
    except HttpError as error:
        # Murio :(
        print(f'Error: {error}')
        return []

#Se supone que se puede cambiar el color de la carpeta, pero no funciono, esta funcion lista los colores disponibles
def getAvailableFolderColors():
    #Hacer la autorisizacion 
    creds = OAuth()
    try:
        #iniciar la comunicacion
        service = build('drive', 'v3', credentials=creds)
        # Call the Drive v3 API
        about = service.about()
        colors = about.get(fields = "folderColorPalette").execute()
        return colors['folderColorPalette']
    except HttpError as error:
        print(f'Error: {error}')
        return False

# Funcion que sube un archivo al drive
def saveDrive(filename,driveFolder,driveFilename,folderColor = "#FFFFFF"):
    #Hacer la autorisizacion 
    creds = OAuth()
    try:
        #iniciar la comunicacion
        service = build('drive', 'v3', credentials=creds)
        files = service.files()
        folderId = ""
        #Verificar si ya existe la carpeta
        query = search(driveFolder,service)
        for item in query:
            # Si ya existe la carpeta con ese nombre, guardar su ID
            if item["name"] == driveFolder:
                folderId = item["id"]
                break
        # Si no existe la carpeta, crearla
        if folderId == "":
            #Crear un directorio, esto se logra con el mimeType
            folder = files.create(body = {"name":f"{driveFolder}","mimeType":"application/vnd.google-apps.folder"})
            folderId = folder.execute().get("id","")
            #cambiar color (no funciono)
            files.update(fileId=folderId,body = {"folderColorRGB":f"{folderColor}"}).execute()
        #Subir el contenido del archivo
        media = MediaFileUpload(filename)
                                #,mimetype='image/jpeg')
        #Crear un nuevo archivo con el contenido que ya esta cargado
        newFile = files.create(body = {"parents":[folderId],"name":f"{driveFilename}"},media_body = media)
        # Ejecutar el comando
        print(f"Subiendo {driveFilename}")
        newFile.execute()
        print("Subido con exito")
        return True
    
    except HttpError as error:
        # Error: error
        print(f'Error: {error}')
        return False
