from django.contrib import admin
from .models import Affaires, Document, SuiviDHL, SuiviConteneur, SuiviPaiement


admin.site.register(Affaires)
admin.site.register(Document)
admin.site.register(SuiviDHL)
admin.site.register(SuiviConteneur)
admin.site.register(SuiviPaiement)