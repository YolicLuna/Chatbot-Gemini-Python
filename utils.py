def carga(filname):
    try:
        with open(filname, "rb") as archivo:
            datos = archivo.read()
            return datos
    except IOError as e:
        print(f"Error al cargar el archivo: {e}")

def guardar(filename, contenido):
    try: 
        with open(filename, "w", encoding="utf-8")as archivo:
            archivo.write(contenido)
    except IOError as e:
        print(f"Error al guardar el archivo: {e}")

        