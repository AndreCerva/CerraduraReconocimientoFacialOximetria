import os, io, json,cv2
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import requests
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")                            
ENDPOINT = os.getenv("ENDPOINT")
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))

camera=cv2.VideoCapture(0,cv2.CAP_DSHOW)
while (camera.isOpened()):
    ret, image = camera.read()
    if ret==True:
        cv2.imshow('video',image)
        if cv2.waitKey(1) & 0xFF == ord('t'):
            cv2.imwrite('target.jpg', image)
            camera.release()
            cv2.destroyAllWindows()
            break
    else:
        print('Error al intentar ingresar a la camara')
        break

img_target=open(r'target.jpg', 'rb')
response_face_target = face_client.face.detect_with_stream(
    image=img_target,detection_model='detection_03', recognition_model='recognition_04')

if not response_face_target:
    raise Exception('No face detected')
else:
    face_id_target = response_face_target[0].face_id

with os.scandir('.\DB') as ficheros:
    ficheros = [fichero.name for fichero in ficheros if fichero.is_file() and fichero.name.endswith('.jpg')]
for fichero in ficheros:
    img_source = open(f'.\DB\{fichero}', 'rb')
    response_face_source = face_client.face.detect_with_stream(
        image=img_source,detection_model='detection_03', recognition_model='recognition_04')
    face_id_source = response_face_source[0].face_id
    face_verified = face_client.face.verify_face_to_face(face_id1=face_id_source,
        face_id2=face_id_target)
    if face_verified.is_identical:
        img=Image.open("target.jpg")
        draw = ImageDraw.Draw(img)
        for face in response_face_target:
              rect = face.face_rectangle
              left = rect.left
              top = rect.top
              right = rect.width + left
              bottom = rect.height + top
              draw.rectangle(((left, top), (right, bottom)), outline='green', width=5)
              break
    else:
        print('No se encontro el rostro de la persona')
        print(face_verified.is_identical)
        print(face_verified.confidence)
        face_id_target.faceRectangle
img.show()
