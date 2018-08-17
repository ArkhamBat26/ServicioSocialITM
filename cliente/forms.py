from django import forms
from cliente.models import FaceRecognizer

class FaceRecognizerForm(forms.ModelForm):
	class Meta:
		model = FaceRecognizer
		fields = ('sample1','sample2','sample3','sample4','sample5',)