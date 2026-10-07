import os
import cv2
import mediapipe as mp
import time
import subprocess
from collections import deque

# ==========================================
# 1. CONFIGURACIÓN DE DISPOSITIVO ADB (SANEADO)
# ==========================================
# Puedes definir tu dispositivo mediante variable de entorno o directamente aquí.
# Para GitHub, se mantiene en blanco o genérico por seguridad.
ADB_DEVICE_ID = os.getenv("ADB_DEVICE_ID", "")  # Ej: "192.168.1.87:35105"

def enviar_comando_adb(comando):
    """Ejecuta comando ADB de forma asíncrona permitiendo target específico."""
    if ADB_DEVICE_ID:
        comando = comando.replace("adb shell", f"adb -s {ADB_DEVICE_ID} shell")
    subprocess.Popen(comando, shell=True)

# ==========================================
# 2. CÁMARA Y MEDIAPIPE ULTRA-FAST
# ==========================================
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=0,          # Modelo Lite ultra-rápido
    min_detection_confidence=0.4,
    min_tracking_confidence=0.4
)

# ==========================================
# 3. VARIABLES DE ESTADO Y UMBRALES
# ==========================================
history = deque(maxlen=3)

VELOCIDAD_UMBRAL_Y = 0.65
VELOCIDAD_UMBRAL_X = 0.65
FACTOR_DOMINANCIA = 1.3
COOLDOWN_TIME = 0.9
cooldown_until = 0

ultimo_gesto_texto = ""
tiempo_gesto_mostrar = 0

print("==================================================")
print(" CONTROL HÍBRIDO (GESTOS EN PC + VOZ EN CELULAR)")
print(" 🖐️ GESTOS: Arriba = Siguiente | Derecha = Anterior")
print(" 🎤 VOZ: Di 'Sube' o 'Baja' directamente a tu teléfono")
print("==================================================")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    tiempo_actual = time.time()
    en_cooldown = tiempo_actual < cooldown_until

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            x_norm = hand_landmarks.landmark[8].x
            y_norm = hand_landmarks.landmark[8].y
            x_px = int(x_norm * w)
            y_px = int(y_norm * h)

            # FIX: Asignación de color en ambos estados para evitar UnboundLocalError
            if en_cooldown:
                history.clear()
                color_nodo = (128, 128, 128)  # Gris cuando está en reposo
            else:
                history.append((x_norm, y_norm, tiempo_actual))
                color_nodo = (0, 255, 0)      # Verde cuando está capturando

            cv2.circle(frame, (x_px, y_px), 8, color_nodo, -1)

            # EVALUACIÓN DE GESTOS FÍSICOS
            if len(history) >= 2 and not en_cooldown:
                dx = history[-1][0] - history[0][0]
                dy = history[-1][1] - history[0][1]
                dt = history[-1][2] - history[0][2]

                if dt > 0.01:
                    vx = dx / dt
                    vy = dy / dt

                    abs_vx = abs(vx)
                    abs_vy = abs(vy)

                    # GESTO ARRIBA -> Siguiente Video
                    if vy < -VELOCIDAD_UMBRAL_Y and abs_vy > (abs_vx * FACTOR_DOMINANCIA):
                        ultimo_gesto_texto = "🖐️ SIGUIENTE VIDEO"
                        tiempo_gesto_mostrar = tiempo_actual + 1.0
                        enviar_comando_adb("adb shell input swipe 360 1100 360 300 250")
                        cooldown_until = tiempo_actual + COOLDOWN_TIME
                        history.clear()

                    # GESTO DERECHA -> Video Anterior
                    elif vx > VELOCIDAD_UMBRAL_X and abs_vx > (abs_vy * FACTOR_DOMINANCIA):
                        ultimo_gesto_texto = "🖐️ VIDEO ANTERIOR"
                        tiempo_gesto_mostrar = tiempo_actual + 1.0
                        enviar_comando_adb("adb shell input swipe 360 300 360 1100 250")
                        cooldown_until = tiempo_actual + COOLDOWN_TIME
                        history.clear()

    else:
        history.clear()

    # CONFIRMACIÓN VISUAL EN PANTALLA
    if tiempo_actual < tiempo_gesto_mostrar:
        color_borde = (0, 255, 0) if "SIGUIENTE" in ultimo_gesto_texto else (0, 165, 255)
        cv2.putText(frame, ultimo_gesto_texto, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color_borde, 2)

    cv2.imshow("Controlador TikTok Instantaneo", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()