import cv2
import mediapipe as mp
import time
import serial


ser = serial.Serial('COMX', 115200)  # CHANGE THE 'COMX' EXAMPLE COM3
time.sleep(2)  


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

fps = 10
last_time = time.time()

def contar_dedos(hand_landmarks):
    dedos_levantados = 0
    puntos = hand_landmarks.landmark
    palma_x = puntos[0].x 

   
    if puntos[4].x > puntos[3].x if palma_x < puntos[0].x else puntos[4].x < puntos[3].x:
        dedos_levantados += 1

    
    for i in [8, 12, 16, 20]:  # IDs de las puntas de los dedos
        if puntos[i].y < puntos[i - 2].y:  # Puntas por encima de las articulaciones
            dedos_levantados += 1

    return dedos_levantados

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al acceder a la cámara.")
        break

   
    if time.time() - last_time < 1.0 / fps:
        continue
    last_time = time.time()

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            dedos_levantados = contar_dedos(hand_landmarks)
            print(f"Dedos levantados: {dedos_levantados}")

            
            ser.write(str(dedos_levantados).encode())

    cv2.imshow('Detección de Manos', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
