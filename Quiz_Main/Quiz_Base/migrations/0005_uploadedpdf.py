# Generated by Django 5.1.2 on 2024-11-07 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz_Base', '0004_quizsession_delete_document'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedPDF',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('pdf_file', models.FileField(upload_to='pdfs/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
