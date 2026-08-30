import os
import asyncio
import threading
import pygame
import edge_tts
import speech_recognition as sr
from google import genai

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Line
from kivy.core.window import Window

Window.size = (360, 640)

def obtener_imagen(nombre_base):
    for ext in ['.png.jpeg', '.jpg.jpeg', '.png', '.jpg', '.jpeg']:
        posible = nombre_base + ext
        if os.path.exists(posible):
            return posible
    if os.path.exists(nombre_base):
        return nombre_base
    return ""

LOGO_FILE = obtener_imagen("logo")
KEFLA_ABIERTA = obtener_imagen("kefla_abierta")
KEFLA_CERRADA = obtener_imagen("kefla_cerrada")

NOMBRE_ASISTENTE = "Kefla"
GEMINI_API_KEY = "AQ.Ab8RN6LIc-H7wH4zHsR-CwHK8p7J1r2OwpgmwN86VhV9LOXXJw"
VOZ_NEURONAL = "es-MX-DaliaNeural"

client = None

if GEMINI_API_KEY:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        print("✅ Cliente de Gemini inicializado.")
    except Exception as e:
        print(f"⚠️ Error al inicializar Gemini: {e}")

pygame.mixer.init()
hablando = False

async def ejecutar_audio(texto, callback_hablar):
    global hablando
    archivo_temp = "kefla_voice_temp.mp3"
    try:
        comm = edge_tts.Communicate(texto, VOZ_NEURONAL, rate="+10%")
        await comm.save(archivo_temp)
        pygame.mixer.music.load(archivo_temp)
        
        hablando = True
        callback_hablar(True) 
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.05)
            
        pygame.mixer.music.unload()
    except Exception as e:
        print(f"⚠️ Error en audio: {e}")
    finally:
        hablando = False
        callback_hablar(False)
        if os.path.exists(archivo_temp):
            try: os.remove(archivo_temp)
            except: pass

def hablar_async(texto, callback_hablar):
    asyncio.run(ejecutar_audio(texto, callback_hablar))

def escuchar():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Kefla está escuchando... Habla ahora.")
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            texto = recognizer.recognize_google(audio, language="es-MX")
            print(f"👤 Tú dijiste: {texto}")
            return texto.lower()
        except:
            return ""

def procesar_entrada(entrada):
    if not entrada or not client:
        return ""
    
    prompt = (
        f"Eres {NOMBRE_ASISTENTE}, una asistente carismática, alegre y directa. "
        f"Responde a esto en máximo 3 oraciones cortas: {entrada}"
    )

    # Usamos el modelo exacto que requiere el servidor en 2026
    try:
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        print(f"⚠️ Error al generar contenido: {e}")
        return "Tuve un pequeño problema de conexión con mi cerebro digital."

# BOTÓN VERDE FLUORESCENTE VISIBLE
class BotonVerdeNeon(Widget):
    def _init_(self, **kwargs):
        super()._init_(**kwargs)
        self.bind(pos=self.dibujar, size=self.dibujar)

    def dibujar(self, *args):
        self.canvas.clear()
        with self.canvas:
            # Fondo Verde Neón Brillante
            Color(0, 1, 0.4, 1)
            Ellipse(pos=self.pos, size=self.size)
            # Borde Cian/Azul Neón
            Color(0, 0.8, 1, 1)
            Line(ellipse=(self.pos[0], self.pos[1], self.size[0], self.size[1]), width=3)

class KeflaApp(App):
    def build(self):
        self.title = "Kefla IA"
        if LOGO_FILE: self.icon = LOGO_FILE
        
        # Usamos BoxLayout vertical para forzar la división del espacio de pantalla
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 1. Área superior: Imagen del personaje (80% de la pantalla)
        self.personaje = Image(
            source=KEFLA_CERRADA if KEFLA_CERRADA else "",
            size_hint=(1, 0.8),
            allow_stretch=True,
            keep_ratio=True
        )
        root.add_widget(self.personaje)
        
        # 2. Área inferior: Contenedor exclusivo para el botón (20% de la pantalla)
        area_boton = BoxLayout(size_hint=(1, 0.2))
        
        self.btn_verde = BotonVerdeNeon(
            size_hint=(None, None),
            size=(80, 80)
        )
        # Centrado manual dentro de su área reservada
        self.btn_verde.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        
        area_boton.add_widget(Widget()) # Espaciador izquierdo
        area_boton.add_widget(self.btn_verde)
        area_boton.add_widget(Widget()) # Espaciador derecho
        
        root.add_widget(area_boton)
        
        threading.Thread(target=self.bucle_voz, daemon=True).start()
        return root

    def cambiar_pose(self, esta_hablando):
        def _update(dt):
            if esta_hablando and KEFLA_ABIERTA:
                self.personaje.source = KEFLA_ABIERTA
            elif KEFLA_CERRADA:
                self.personaje.source = KEFLA_CERRADA
            self.personaje.reload()
        Clock.schedule_once(_update)

    def bucle_voz(self):
        threading.Thread(target=hablar_async, args=("¡Hola! Soy Kefla. ¿En qué te ayudo?", self.cambiar_pose), daemon=True).start()
        while True:
            if not hablando:
                entrada = escuchar()
                if entrada:
                    respuesta = procesar_entrada(entrada)
                    if respuesta:
                        threading.Thread(target=hablar_async, args=(respuesta, self.cambiar_pose), daemon=True).start()
                asyncio.run(asyncio.sleep(0.1))
            else:
                asyncio.run(asyncio.sleep(0.5))

if __name__ == "__main__":
    KeflaApp().run()