from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload$', views.faceTest, name='subir-imagenes'),
    url(r'^agregar$', views.agregarRostro, name='agregar-rostro'),
    url(r'^borrar$', views.borrarCapturas, name='borrar-capturas')
] 