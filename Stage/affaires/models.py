from django.db import models


class Affaires(models.Model):
    type                   = models.CharField(max_length=120)
    destinataire           = models.CharField(max_length=120)
    produits               = models.TextField(blank=True, null=True)
    volume                 = models.CharField(max_length=120)
    packaging              = models.TextField(blank=True, null=True)
    origine                = models.CharField(max_length=120)
    prix                   = models.DecimalField(decimal_places=2, max_digits=1000000)
    devise                 = models.CharField(max_length=50)
    incoterm               = models.CharField(max_length=50)
    embarquement           = models.DateField()
    moyen_de_paiement      = models.CharField(max_length=50)
    reference_contrepartie = models.TextField(blank=True, null=True)
    commentaires           = models.TextField(blank=True, null=True)
    statut                 = models.TextField(blank=True, null=True)
    reference_contart      = models.CharField(max_length=50)


class Document(models.Model):
    affaire = models.ForeignKey(Affaires, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='documents/pdfs/', null=True, blank=True)
    cover = models.ImageField(upload_to='documents/covers/', null=True, blank=True)

    def __str__(self):
        return self.title


class SuiviDHL(models.Model):
    affaire = models.ForeignKey(Affaires, on_delete=models.CASCADE, null=True)
    num_dhl = models.IntegerField()
    date_arrive = models.DateField()

    def __str__(self):
        return self.num_dhl


class SuiviConteneur(models.Model):
    affaire = models.ForeignKey(Affaires, on_delete=models.CASCADE, null=True)
    num_bl = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=120)
    moves = models.CharField(max_length=120)
    date = models.DateField()
    vessel = models.CharField(max_length=120)

    def __str__(self):
        return self.num_bl



class SuiviPaiement(models.Model):
    affaire = models.ForeignKey(Affaires, on_delete=models.CASCADE, null=True)
    date_bl = models.DateField()
    date_arrivee = models.DateField()
    echeance_paiement = models.DateField()
    date_valeur = models.DateField()
    date_reception = models.DateField()
    date_bl_a_vue = models.DateField()
    date_arrivee_a_vue = models.DateField()
    echeance_paiement_a_vue = models.DateField()
    date_valeur_a_vue = models.DateField()
    date_reception_a_vue = models.DateField()

    def __str__(self):
        return self.date_bl