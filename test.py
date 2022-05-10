import os,io,json,requests
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY")                            
ENDPOINT = os.getenv("ENDPOINT")
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))

img_file = open(r'.\DB\victor.jpg', 'rb')

response_detected_faces = face_client.face.detect_with_stream(image=img_file,detection_model='detection_03',
    recognition_model='recognition_04',return_face_landmarks=True)

if not response_detected_faces:
    raise Exception('No face detected')
img =Image.open(img_file)
draw = ImageDraw.Draw(img)
for face in response_detected_faces:
    rect = face.face_rectangle
    left = rect.left
    top = rect.top
    right = rect.width + left
    bottom = rect.height + top
    draw.rectangle(((left, top), (right, bottom)), outline='green', width=5)
img.show()