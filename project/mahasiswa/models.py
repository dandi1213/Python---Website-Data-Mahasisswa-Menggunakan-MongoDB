from django.db import models

from mongoengine import Document, StringField, DateField

class Mahasiswa(Document):
    Nama = StringField(required=True)
    Nim = StringField(required=True)
    Ttl = StringField(required=True)
    Jenis_Kelamin = StringField(required=True)
    No_Telepon = StringField(required=True)