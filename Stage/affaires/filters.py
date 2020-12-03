import django_filters
from django_filters import DateFilter

from .models import *


class AffairesFilter(django_filters.FilterSet):
    class Meta:
        model = Affaires
        fields = '__all__'
        exclude = ['type', 'volume', 'packaging', 'prix', 'devise', 'incoterm', 'embarquement', 'reference_contrepartie', 'commentaires', 'moyen_de_paiement']
