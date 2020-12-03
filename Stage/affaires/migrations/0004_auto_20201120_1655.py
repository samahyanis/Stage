# Generated by Django 3.1.3 on 2020-11-20 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('affaires', '0003_document_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='affaire',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='affaires.affaires'),
        ),
        migrations.AlterField(
            model_name='document',
            name='pdf',
            field=models.FileField(null=True, upload_to='documents/pdfs/'),
        ),
    ]