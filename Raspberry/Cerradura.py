import RPi.GPIO as GPIO#librerias que nos permite trabajar con los pines de la rasp
import time #Libreria para tiempos de espera 
from azure.iot.device import IoTHubDeviceClient#Libreria para hacer uso del servicio de Azure IoT Hub
GPIO.setwarnings(False)#No mostrar advertencias
CONNECTION_STRING = "Aqui la cadena de conexión" #Aquí pegamos la cadena de conexion tomada desde nuestro portal de azure
pin=16 #Pin positivo al que ira conectado el led verde
GPIO.setmode(GPIO.BOARD) #Numeraremos los pines del rasp con la numeración board (locación fisica)
GPIO.setup(pin,GPIO.OUT)#Indicamos que en el pin del led v estará mandando señal
def message_handler(message): #Recibe el mensaje con todos sus atributos y metodos
  if message.data.decode() == 'ON': #Si el mensaje que se recibe es un ON
      GPIO.output(pin,GPIO.LOW) #Dar una salida en bajo
      print("Luz encendida")
  else: #No se ha obtenido una entrada
      print("Luz apagada")
      GPIO.output(pin,GPIO.HIGH) #encender led 
  time.sleep(5)#Segundos para poder volver a recibir mensajes sin problemas
  print ("Esperando por un mensaje...")#Estamos esperando algún mensaje
def main():
    GPIO.output(pin,GPIO.HIGH)# iniciamos en alto el led rojo que indica que no se ha encontrado aún
    print ("Esperando por un mensaje...")#indicamos que se empieza la busqueda
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)#instanciamos el cliente 
    try:
        # Attach the handler to the client
        client.on_message_received = message_handler#Leemos el mensaje que se ha enviado a nuestro device 
        while True: 
            time.sleep(1000) #mil segundos esperando un mensaje, por poner un numero, puede ser otro.
    except KeyboardInterrupt:
        print("IoT Hub C2D Messaging stopped") #se detiene la ejecución debido a una interrupción de teclado
    finally:
        GPIO.cleanup()
        print("Shutting down IoT Hub Client")#Terminamos con éxito la ejecución del programa
        client.shutdown()#Se deja de esperar el envio de mensajes
if __name__ == '__main__':
    main()