# Python y Gemini: Crea tu chatbot con IA Generativa

Este proyecto del chatbot creado durante el curso **"Gemini y Python: crea tu chatbot con IA generativa"** de Alura Latam.

En el proyecto, yo solo escribi el codigo en JavaScript y Python, el diseño de la interfaz fue realizado por el equipo de Alura Latam. 

Integra la API de Gemini en una aplicación web construida con Flask y JavaScript. El chatbot cuenta con personalidades configurables para adaptar el tono de las respuestas, automatización en la selección de personalidad según el contexto, gestión de historial de conversación y la capacidad de interpretar tanto texto como imágenes.

## 🔨 Funcionalidades del proyecto

En este proyecto vamos a construir un chatbot utilizando la API de Gemini. Para ello, emplearemos una aplicación base escrita en Flask, utilizando Python y con una interfaz diseñada con HTML, CSS y JS. 

![](img/amostra.gif)

## ✔️ Técnicas e tecnologías utilizadas

Las técnicas y tecnologías utilizadas para este fin son:

- Programación en Python
- Construcción de aplicaciones con Flask
- Uso de la API de Gemini
- Lectura de archivos CSV y tratamiento de datos


## 🛠️ Abrir y ejecutar el proyecto

Tras descargar el proyecto, vamos a abrirlo con Visual Studio Code. Posteriormente, es necesario preparar el ambiente. Para ello:

### venv en Windows:

```bash
python -m venv .venv-gemini-2
.\.venv-gemini-2\Scripts\activate
```

### venv en Mac/Linux:

```bash
python3 -m venv .venv-gemini-2
source .venv-gemini-2/bin/activate
```

El siguiente paso es la instalación de los módulos utilizando:

```bash
pip install -r requirements.txt
```

## 🔑 Generar la API_KEY y asociarla al archivo .env

```python
GEMINI_API_KEY = "API_KEY_AQUI"
```
