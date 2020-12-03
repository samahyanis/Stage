from django.conf.urls import url
#from django.contrib.auth.views import LoginView
from . import views
from django.urls import path
#from .views import GeneratePDF


urlpatterns = [
    url(r'^affaires/$', view=views.affaires, name="affaires"),
    url(r'^suivi_paiement/$', view=views.suivi_paiement, name="suivi_paiement"),
    url(r'^suivi_originaux/$', view=views.suivi_originaux, name="suivi_originaux"),
    url(r'^suivi_container/$', view=views.suivi_container, name="suivi_container"),
    url(r'^add_affaires/$', view=views.add_affaires, name="add_affaires"),
    #url(r'^pdf/$', view=views.GeneratePDF, name="GeneratePDF"),
    #url(r'^affaires/pdf/$', GeneratePDF.as_view()),
    url(r'^affaires/(?P<id>\d+)/edit$', view=views.edit_affaires, name="edit_affaires"),
    url(r'^affaires/(?P<id>\d+)/delete$', view=views.delete_affaires, name="delete_affaires"),
    url(r'^affaires/generate_contrat', view=views.generate_contrat, name="generate_contrat"),
    url(r'^export_pdf/(?P<id>\d+)', view=views.export_pdf, name="export-pdf"),
    url(r'^export_csv/(?P<id>\d+)', view=views.export_csv, name="export-csv"),
    url(r'^upload/(?P<id>\d+)$', view=views.upload, name="upload"),
    url(r'^documents/(?P<id>\d+)$', view=views.document_list, name="document_list"),
    url(r'^documents/upload/(?P<id>\d+)', view=views.upload_document, name="upload_document"),


]