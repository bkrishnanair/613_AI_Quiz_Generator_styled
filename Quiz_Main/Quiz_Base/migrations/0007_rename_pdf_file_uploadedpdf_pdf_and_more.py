# Generated by Django 5.1.2 on 2024-11-11 03:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz_Base', '0006_delete_quizsession'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uploadedpdf',
            old_name='pdf_file',
            new_name='pdf',
        ),
        migrations.RemoveField(
            model_name='uploadedpdf',
            name='title',
        ),
    ]
