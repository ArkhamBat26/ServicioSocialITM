import cv2
import numpy as np
import os
from reconocedorFacial.settings import STATIC_ROOT

class Reconocedor:

	def __init__(self,path = "recognizer.yml"):
		self.recognizer = cv2.face.LBPHFaceRecognizer_create()
		self.path = os.path.join(STATIC_ROOT,path)
		self.cargarReconocedor()

	def agregarCara(self,face,label):
		caras = []
		labels = []

		caras.append(face)
		labels.append(label)
		labels = np.array(labels)

	def entrenar(self,file = 'ITM_faces.txt'):
		#Crear arreglo de 'caras que conoce'
		caras =[]

		#Crear arreglo de 'etiquetas' para cada cara
		etiquetas = []

		#Antonio Bandera para ver si es la primera imagen
		flag = 0

		#Leer el csv linea por linea
		with open(file) as csv:
			#Objeto con todas las lineas
			lineas = csv.readlines()

			#leer una a una
			for linea in lineas:
				linea = linea[:-1]	#quitar el ultimo caracter
				img_lbl = linea.split(";")	#Separar en un arreglo por el ';'
				print img_lbl[0];
				#Agregar el objeto de la imagen y la etiqueta 
				cara = cv2.imread(img_lbl[0],0)
				print type(cara)
				print cara.shape
				caras.append(cara)	
				etiquetas.append(int(img_lbl[1]))
				flag = flag + 1
		etiquetas = np.array(etiquetas)

		#entrenarlo alv
		self.recognizer.train(caras,etiquetas)
		self.recognizer.save(self.path)
		return self.recognizer

	def actualizar(self,file = 'ITM_faces.txt'):
		#Crear arreglo de 'caras que conoce'
		caras =[]

		#Crear arreglo de 'etiquetas' para cada cara
		etiquetas = []

		#Antonio Bandera para ver si es la primera imagen
		flag = 0

		#Leer el csv linea por linea
		with open(file) as csv:
			#Objeto con todas las lineas
			lineas = csv.readlines()

			#leer una a una
			for linea in lineas:
				linea = linea[:-1]	#quitar el ultimo caracter
				img_lbl = linea.split(";")	#Separar en un arreglo por el ';'
				
				#Agregar el objeto de la imagen y la etiqueta 
				cara = cv2.imread(img_lbl[0],0)
				print cara.shape
				caras.append(cara)	
				etiquetas.append(int(img_lbl[1]))
				flag = flag + 1
		etiquetas = np.array(etiquetas)

		#entrenarlo alv
		self.recognizer.update(caras,etiquetas)
		self.recognizer.save(self.path)
	#end actualizar

	def cargarReconocedor(self):
		self.recognizer.read(self.path)
		return self.recognizer
		#end cargarReconocedor

	def guardarReconocedor(self):
		self.recognizer.save(self.path)
		#end guardarReconocedor

	def predecirCara(self,roi):
		#Predecir la cara, regresa el label del men que identifica, men
		#label,conf = face_recognizer.predict(roi)
		label,conf = self.recognizer.predict(roi)
		return label,conf
		#end predecirCara