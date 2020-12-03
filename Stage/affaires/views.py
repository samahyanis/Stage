import csv
import random
from django.shortcuts import render, get_object_or_404, redirect, reverse

from .api_test import get_shipsgo
from .models import Affaires, SuiviDHL, SuiviConteneur, SuiviPaiement
from django.http import JsonResponse, HttpResponse
import datetime
from .filters import AffairesFilter
#from django.views.generic import View
#from .utils import render_to_pdf
#from django.template.loader import get_template
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.http import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseNotFound, Http404,  HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from .forms import DocumentForm
from .models import Document
from django.views.generic import TemplateView
from django.utils.crypto import get_random_string
import string


def affaires(request):
    obj = Affaires.objects.all()

    myFilter = AffairesFilter(request.GET, queryset=obj)
    obj = myFilter.qs

    return render(request, "affaires.html", {'Affaires': obj, 'myFilter': myFilter})


def add_affaires(request):
    if request.method == 'POST':
        type = request.POST["type"]
        destinataire = request.POST["destinataire"]
        produits = request.POST["produits"]
        volume = request.POST["volume"]
        packaging = request.POST["packaging"]
        origine = request.POST["origine"]
        prix = request.POST["prix"]
        devise = request.POST["devise"]
        incoterm = request.POST["incoterm"]
        embarquement = request.POST["embarquement"]
        moyen_de_paiement = request.POST["moyen_de_paiement"]
        reference_contrepartie = request.POST["reference_contrepartie"]
        commentaires = request.POST["commentaires"]

        affaires_info = Affaires(type=type, destinataire=destinataire, produits=produits, volume=volume,
                                 packaging=packaging, origine=origine, prix=prix, devise=devise, incoterm=incoterm,
                                 embarquement=embarquement, moyen_de_paiement=moyen_de_paiement,
                                 reference_contrepartie=reference_contrepartie, commentaires=commentaires)
        affaires_info.save()
    else:
        return render(request, "add_affaires.html")


def export_csv(request, id=None):
    response = HttpResponse(content_type='text/CSV')
    response['content-Disposition'] = 'attachment; filename=Affaires' + str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['type', 'destinataire', 'produits', 'volume', 'packaging', 'origine', 'prix', 'devise', 'incoterm',
                     'embarquement', 'moyen_de_paiement', 'reference_contrepartie', 'commentaires'])

    affaires = Affaires.objects.get(pk=id)

    for affaire in affaires:
        writer.writerow(affaire.type, affaire.destinataire, affaire.produits, affaire.volume, affaire.packaging,
                        affaire.origine, affaire.prix, affaire.devise, affaire.incoterm, affaire.embarquement,
                        affaire.moyen_de_paiement, affaire.reference_contrepartie, affaire.commentaires)
    return response



def export_pdf(request, id=None):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=Affaires' + \
                                      str(datetime.datetime.now())+'.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    affaires = Affaires.objects.get(pk=id)




    html_string = render_to_string(
        'pdf-output.html', {'affaire': affaires})
    html = HTML(string=html_string)

    result = html.write_pdf()


    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()

        output = open(output.name, 'rb')
        response.write(output.read())

    return response


def edit_affaires(request, slug):
    affaires = get_object_or_404(Affaires, slug=slug)
    if request.method == "POST":
        form = add_affaires(request.POST, instance=affaires)
        if form.is_valid():
            affaires = form.save(commit=False)
            affaires.author = request.user
            affaires.save()
            return redirect('affaires')
    else:
        form = add_affaires(instance=affaires)
    template = 'add_affaires'
    context = {'form': form}
    return render(request, template, context)


def delete_affaires(request, id=None):
    instance = get_object_or_404(Affaires, id=id)
    instance.delete()
    return redirect('affaires')


def upload(request, id=None):
    context = {'id': id}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, "upload.html", context)


def document_list(request, id=None):

    documents = Document.objects.filter(affaire=id)
    return render(request, 'document_list.html', {
        'documents': documents
    })


def upload_document(request, id=None):
    if request.method == 'POST':

        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('document_list', args=(id)))
    else:
        affaire = Affaires.objects.get(pk=id)
        form = DocumentForm(initial = {'affaire': affaire.id})
    return render(request, 'upload_document.html', {
        'form': form
    })


def suivi_paiement(request):
    if request.method == 'POST':
        date_bl = request.POST["date_bl"]
        date_arrivee = request.POST["date_arrivee"]
        echeance_paiement = request.POST["echeance_paiement"]
        date_valeur = request.POST["date_valeur"]
        date_reception = request.POST["date_reception"]
        date_bl_a_vue = request.POST["date_bl_a_vue"]
        date_arrivee_a_vue = request.POST["date_arrivee_a_vue"]
        echeance_paiement_a_vue = request.POST["echeance_paiement_a_vue"]
        date_valeur_a_vue = request.POST["date_valeur_a_vue"]
        date_reception_a_vue = request.POST["date_reception_a_vue"]
        paiement_info = SuiviDHL(num_dhl=date_bl, date_arrive=date_arrivee, echeance_paiement=echeance_paiement, date_valeur=date_valeur, date_reception=date_reception,
                              date_bl_a_vue=date_bl_a_vue, date_arrivee_a_vue=date_arrivee_a_vue, echeance_paiement_a_vue=echeance_paiement_a_vue,
                              date_valeur_a_vue=date_valeur_a_vue, date_reception_a_vue=date_reception_a_vue)
        paiement_info.save()
    return render(request, "suivi_paiement.html")


def suivi_originaux(request):
    if request.method == 'POST':
        num_dhl = request.POST["num_dhl"]
        date_arrive = request.POST["date_arrive"]
        suivi_info = SuiviDHL(num_dhl=num_dhl, date_arrive=date_arrive)
        suivi_info.save()
    else:
        return render(request, "suivi_originaux.html")




class suivi_container(TemplateView):
    template_name = 'suivi_container.html'
    def suivi_container(self, *args, **kwargs):
        context = {
            """'suivi_container': suivi_container(),"""
            'suivi_container': get_shipsgo(),
        }
        return context



def generate_contrat(request, id=None):
    achat = 'BX'
    vente = 'SX'
    année = '2020'
    number = int(Affaires.objects.get(pk=id), 2)
    if type == achat:
        contrat = achat + '-' + année + '-' + str(number).zfill(4)
        return print(contrat)
    else:
        contrat = vente + '-' + année + '-' + str(number).zfill(4)
        return print(contrat)








