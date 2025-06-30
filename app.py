from flask import Flask,render_template, request, Response
import google.generativeai as genai
from dotenv import load_dotenv
import os
from time import sleep
from utils import carga, guardar
from personas import personas, seleccionar_personalidad
from gestion_historial import eliminar_mensajes_antiguos
import uuid
from gestion_imagen import generar_imagen_gemini

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
modelo = "gemini-1.5-flash"   
genai.configure(api_key=api_key)

app = Flask(__name__)
app.secret_key = 'aluralatam'

@app.route("/")
def home():
    return render_template("index.html")

contexto = carga("datos/utils.txt")

camino_imagen_enviada = None
upload_folder = 'imagenes_temporales'

def crear_chatbot():
    personalidad ='neutro'
    prompt_sistema = f"""
                        # PERSONA
                        Eres un chatbot de atención al cliente de una e-commerce. No debes
                        responder preguntas que no sean referentes a los datos del ecommerce
                        informado.

                        # CONTENIDO
                        {contexto}

                        # PERSONALIDAD
                        {personalidad}

                        # HISTORIAL
                        Accede siempre al historial de mensajes, y recupera la informacion previamente mencionada.
                        """
    configuracion_modelo = {
                "temperature":0.2,
                "max_output_tokens": 8192
            }

    llm = genai.GenerativeModel(
                model_name = modelo,
                system_instruction = prompt_sistema,
                generation_config = configuracion_modelo 
            )
    chatbot = llm.start_chat(history=[])
    return chatbot

chatbot = crear_chatbot()

def bot(prompt):
    #número máximo de intentos 
    max_intentos = 1
    repeticion = 0
    global camino_imagen_enviada
    while True:
        try:
            personalidad = personas[seleccionar_personalidad(prompt)]
            mensaje_usuario = f"""
                                Considera esta personalidad para responder al mensaje:
                                {personalidad}.

                                Responde al siguiente mensaje recordando el historial:
                                {prompt}.
                                """
            if camino_imagen_enviada:
                mensaje_usuario += '\nUtiliza las caracteristicas de la imagen en tu respuesta.'
                archivo_imagen = generar_imagen_gemini(camino_imagen_enviada)
                respuesta = chatbot.send_message([archivo_imagen,mensaje_usuario])
                os.remove(camino_imagen_enviada)
                camino_imagen_enviada = None
                
            if len(chatbot.history) > 4:
                chatbot.history = eliminar_mensajes_antiguos(chatbot.history)
            print(f'La cantidad de mensajes es: {len(chatbot.history)}\n{chatbot.history}')
            return respuesta.text
        
        except Exception as e:
            repeticion += 1
            if repeticion >= max_intentos:
                return "Error con Gemini: %s" % e
            if camino_imagen_enviada:
                os.remove(camino_imagen_enviada)
                camino_imagen_enviada = None
            sleep(50)

@app.route("/cargar_imagen", methods=["POST"])
def cargar_imagen():
    global camino_imagen_enviada

    if "imagen" in request.files:
        imagen_enviada = request.files["imagen"]
        nombre_archivo = str(uuid.uuid4()) + os.path.splitext(imagen_enviada.filename)[1]
        camino_archivo = os.path.join(upload_folder, nombre_archivo)
        imagen_enviada.save(camino_archivo)
        camino_imagen_enviada = camino_archivo
        return "Imagen enviada con éxito", 200
    return "Ningún archivo enviado", 400

def resumir_historico(historico):
    """
    Resumir el historial de mensajes para mantener la relevancia y la coherencia.
    Este método se llama cuando el historial alcanza 10 mensajes.
    """
    # Uniendo las partes del historial en un único texto para sumarización
    texto_completo = " ".join([ 
        parte.text if hasattr(parte, 'text') else parte 
        for mensaje in historico for parte in mensaje['parts'] 
    ])

    # Creando el prompt para resumir el historial
    prompt_resumo = f"""
    Resume el siguiente historial manteniendo la información esencial para continuar una conversación coherente:
    {texto_completo}
    """

    # Configurando el modelo para generar el resumen
    llm = genai.GenerativeModel(
        model_name = 'gemini-1.5-flash',
        system_instruction="Eres un asistente de resumen.",
        generation_config={"temperature": 0.5, "max_output_tokens": 512}
    )

    # Generando el resumen del historial
    respuesta = llm.generate_content(prompt_resumo)
    resumen = respuesta.text.strip()

    # Creando una nueva entrada de resumen en el historial
    historico_resumido = [{'role': 'model', 'parts': [resumen]}]

    return historico_resumido

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json['msg']
    respuesta = bot(prompt)
    return respuesta


if __name__ == "__main__":
    app.run(debug = True)
