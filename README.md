# Sistema de control por gestos de TikTok 🖐️📱

Sistema de control sin contacto para aplicaciones móviles (TikTok) utilizando Visión por Computadora (OpenCV + MediaPipe) y automatización asíncrona mediante ADB sobre Wi-Fi.

## 🚀 Características

- **Procesamiento de baja latencia:** MediaPipe Hands Lite con cola de fotogramas reducida (<40 ms).
- **Análisis vectorial:** clasificación por velocidad y dominancia de ejes para evitar falsos positivos al regresar la mano.
- **Conexión inalámbrica:** control remoto de eventos táctiles en Android vía ADB Shell.

## 📋 Requisitos

- Python 3.10+
- Dispositivo Android con **Depuración inalámbrica** activa.
- Cámara web.
- [ADB (Android Platform Tools)](https://developer.android.com/tools/releases/platform-tools) instalado y disponible en el `PATH`.

## 🛠️ Instalación y uso

1. **Clonar el repositorio:**

   ```bash
   git clone Jordanjr1/Sistema-de-control-por-gestos-de-TikTok.git
   cd tiktok-gesture-controller
   ```

2. **Crear e iniciar el entorno virtual:**

   ```bash
   python -m venv venv

   # En Windows:
   venv\Scripts\activate

   # En Linux / macOS:
   source venv/bin/activate
   ```

3. **Instalar dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Conectar el dispositivo Android por ADB:**

   ```bash
   adb connect IP_DE_TU_CELULAR:PUERTO
   ```

   Puedes verificar la conexión con `adb devices`.

5. **Ejecutar el script:**

   ```bash
   python main.py
   ```

## 📁 Estructura del proyecto

```
tiktok-gesture-controller/
├── main.py            # Script principal
├── requirements.txt   # Dependencias
├── .gitignore
└── README.md
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Abre un *issue* o envía un *pull request* con tus mejoras.

## 📄 Licencia

jordanjr1.
