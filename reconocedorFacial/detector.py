import cv2
import numpy as np
from reconocedorFacial.settings import STATIC_ROOT,MEDIA_ROOT
from django.core.files import File
import os
HC_w = 200
HC_h = 200

class Detector:
	#este es el contructor
	def __init__(self,cascade = 'haarcascade_frontalface_default.xml'):
		#Crear el objeto clasificador
		self.classifier = cv2.CascadeClassifier(os.path.join(STATIC_ROOT,cascade))
		self.ojos = cv2.CascadeClassifier(os.path.join(STATIC_ROOT,'haarcasdade_eye.xml'))
	#end __init__ 

	def encontrarCaras(self,img, getRoi = False, escala = 1.3, vecinos = 10):
		clasificador = self.classifier
		faces = None
		caras = clasificador.detectMultiScale(img,escala,vecinos)
		for (x,y,w,h) in caras:
			roi = img[y:y+w,x:x+h]
			eyes = self.ojos.detectMultiScale(roi)
			for (ex,ey,ew,eh) in eyes:
				if faces is None:
					faces = np.array([x,y,w,h])
				else:
					facesAux = np.array([x,y,w,h])
					faces = np.concatenate((faces,facesAux))
		return caras
	#end encontrarCaras

	def prepararImagen(self,img):
		roi = cv2.resize(img,(200,200))
		roi = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		return roi
	#end prepararImagen

	def agregarLabel(self,img,label,conf,x,y):
		print "hola"
	#end agregarLabel

	def liveCapture(self,recognizer = None):
		#Objeto de la camara
		camara = cv2.VideoCapture(0);
		cv2.namedWindow('Video')
		loop = True
		while(loop):
			check,frame = camara.read()
			frameBN = cv2.cvtColor(frame, 0)
			frame_ = cv2.flip(frame,1)
			frameBN_ = cv2.flip(frame,1)
			faces = self.encontrarCaras(frameBN)
			for(x,y,w,h) in faces:
				roi = frameBN[y:y+w,x:x+h]
				if recognizer is not None:
					roi = self.prepararImagen(roi)
					label,conf = recognizer.predict(roi)
					labelConf = "%d (%d)" % (label,conf)
					if(conf > 60):
						labelConf = "NO MATCH"
					cv2.rectangle(frame,(x,y+h),(x+w,y+h+30),(0,0,0),cv2.FILLED)
					cv2.putText(frame,labelConf,(x,y+h+20),cv2.FONT_HERSHEY_SIMPLEX,0.56,(255,255,255),1)
				cv2.rectangle(frame,(x,y),(x+w,y+w),(255,0,0),2);
			cv2.imshow('Video',frame)
			key = cv2.waitKey(1) & 0xFF
			if key == ord("c"):
				print "CAPTURAA"
			elif (key == ord("q")):
				loop = False		#end while
		camara.release()
		cv2.destroyAllWindows()
	#end liveCapture

	def quienEs(self,recognizer,img):
		faces = self.encontrarCaras(img)
		if len(faces) == 0:
			return "SIN ROSTROS",0,None
		elif len(faces) == 1:
			for(x,y,w,h) in faces:
				roi = img[y:y+w,x:x+h]
				# Con esto se agrega el roi a la tupla, es una herramienta sorpresa que nos ayudara mas tarde.
				return recognizer.predict(roi) + (roi,)
		else:
			return "DEMASIADOS ROSTROS",0,None
	#end quienEs

	def agregarRostro(self,R,objetoCaras,label):
		samples = []
		samples.append(objetoCaras.sample1.url[1:])
		samples.append(objetoCaras.sample2.url[1:])
		samples.append(objetoCaras.sample3.url[1:])
		samples.append(objetoCaras.sample4.url[1:])
		samples.append(objetoCaras.sample5.url[1:])

		etiquetas = []
		caras = []
		for samp in samples:
			img = cv2.imread(samp,0)
			faces = self.encontrarCaras(img)
			for (x,y,w,h) in faces:
				roi = img[y:y+w,x:x+h]
				face = cv2.resize(roi,(200,200))
				caras.append(face)
				etiquetas.append(int(label))
				
		etiquetas = np.array(etiquetas)

		R.recognizer.update(caras,etiquetas)
		print "UPDATEE"
		R.recognizer.save(os.path.join(STATIC_ROOT,R.path))
		print "SAVEE"
		return "OK"
	#end agregarRostro