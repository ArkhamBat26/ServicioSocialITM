# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import JsonResponse

from django.db.utils import OperationalError

from forms import FaceRecognizerForm

from models import FaceRecognizer

import sys

import numpy as np
import cv2


# PUSE AQUI LOS DETECTORES EN UN INTENTO DE QUE SIEMPRE ESTEN EN MEMORIA Y NO SE CARGUEN EN CADA PINCHE PETICION
from reconocedorFacial.detector import Detector
from reconocedorFacial.reconocedor import Reconocedor
RECOGNIZER = Reconocedor()
DETECTOR = Detector()

import collections
# Create your views here.

CONF = 45
dCONF = 70

def index(request):
	return render(request,'./captura.html')

def faceTest(request):
	#	Si en el objeto de la peticion ya viene con el metodo POST es que ya viene con las imagenes del formulario.

	if request.method == "POST":
		#	Crear el formulario a partir del Modelo (Sample1, Sample2 .... Sample5) podria omitirse esto
		form = FaceRecognizerForm(request.POST,request.FILES)
		if form.is_valid():

			# Guardar las imagenes en el servidor
			form.save()

			# Obtener el id del ultimo objeto guardado, para rescatar las imagenes despues
			id_form = FaceRecognizer.objects.last().id

			#Crear las imagenes de opencv (mat en C++) a partir de los strings que se envian en el formulario
			sample1 = cv2.imdecode(np.fromstring(request.FILES['sample1'].read(),np.uint8), 0)
			sample2 = cv2.imdecode(np.fromstring(request.FILES['sample2'].read(),np.uint8), 0)
			sample3 = cv2.imdecode(np.fromstring(request.FILES['sample3'].read(),np.uint8), 0)
			sample4 = cv2.imdecode(np.fromstring(request.FILES['sample4'].read(),np.uint8), 0)
			sample5 = cv2.imdecode(np.fromstring(request.FILES['sample5'].read(),np.uint8), 0)

			# Meramente debug
			print "#"*20,'\tRESULTADO\t',"#"*20

			#Arreglo de tuplas con los resultados
			resultados = [];

			#	HACER LA PREDICCION PARA CADA IMAGEN
			try:
				resultados.append(DETECTOR.quienEs(RECOGNIZER.recognizer,sample1))
				resultados.append(DETECTOR.quienEs(RECOGNIZER.recognizer,sample2))
				resultados.append(DETECTOR.quienEs(RECOGNIZER.recognizer,sample3))
				resultados.append(DETECTOR.quienEs(RECOGNIZER.recognizer,sample4))
				resultados.append(DETECTOR.quienEs(RECOGNIZER.recognizer,sample5))

				
				# LINEAS SUMAMENTE IMPORTANTES, NO DEJAR CERCA DE NORMA

				respuesta = "NO MATCH"
				counter = []
				for tupla in resultados:
					########## Aqui empieza el algoritmo mamalon ###############
					print str(tupla[0])+" : "+str(tupla[1])
					if respuesta == "NO MATCH" and tupla[1] <= CONF:	##	confX < CONF
						respuesta = tupla[0]							##	respuesta = labelX
					counter.append(tupla[0])

				#	Se crea la colecion de los labels para determinar cual es el mas comun
				counter = collections.Counter(counter)
				#	Si no se manda el 1 se regresa la cuenta de todos. 
				#	El pop() saca el primer elemento. Que seria algo asi como (LABELX:n), LABELX se repite 'n' veces.
				labelMasComun = counter.most_common(1).pop()[0]
				cuentaLabelMasComun = counter.most_common(1).pop()[1]

				if cuentaLabelMasComun >= 3 and respuesta == "NO MATCH" or respuesta == "SIN ROSTROS":	
					respuesta = labelMasComun

				## Promedio de conf, si es muy grande se envia "NO MATCH"
				sumaConf = 0
				for tupla in resultados:	## tupla = (labelX,confX)
					if labelMasComun == tupla[0]:
						sumaConf += tupla[1]
				promedioConf = sumaConf/cuentaLabelMasComun

				print "## PROMEDIO CONF : "+str(promedioConf) 

				if promedioConf > dCONF:
					respuesta = "NO MATCH"

				return JsonResponse({"data":respuesta,"id":id_form})
			except:
				print "ERROR", sys.exc_info()[0]
				return JsonResponse({"data":"ERROR"})

	#	Si el formulario no viene con el metodo POST, se renderiza el formulario 
	else:
		form = FaceRecognizerForm()
		return render(request,'./formulario.html',{'form':form})
#end facetest

def entrenar(request):
	print "ENTRENAR"
#end entrenar

def agregarRostro(request):
	label = request.POST["label"]
	target = FaceRecognizer.objects.get(id=request.POST["id"])
	resp = DETECTOR.agregarRostro(RECOGNIZER,target,label)
	return JsonResponse({"status":"OK","message":"Rostros aprendidos"})
#end agregarRostro

def borrarCapturas(request):
	target = FaceRecognizer.objects.get(id=request.POST["id"])
	target.delete()
	return JsonResponse({"status":"OK","message":"Borrado alv"})
#end borrarCapturas