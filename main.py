from machine import Pin, UART
import time


uart = UART(1, baudrate=115200, tx=1, rx=3)  


led_pins = [2, 4, 5, 18, 19] 
leds = [Pin(pin, Pin.OUT) for pin in led_pins]  

while True:
    if uart.any():  
        data = uart.read().decode('utf-8').strip() 
        try:
            dedos_levantados = int(data)  
            print(f"Dedos levantados: {dedos_levantados}")

            
            for i in range(5):
                if i < dedos_levantados:
                    leds[i].on()  # Enciende el LED
                else:
                    leds[i].off()  # Apaga el LED
        except ValueError:
            print("Comando no válido")
    time.sleep(0.1) 
