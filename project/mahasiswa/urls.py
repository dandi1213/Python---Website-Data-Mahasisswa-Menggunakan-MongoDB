from django.urls import path
from . import views

urlpatterns = [
    path('', views.mahasiswa_list, name='home'),
    path('mahasiswa/', views.mahasiswa_list, name='mahasiswa_list'),
    path('tambah/', views.tambah_mahasiswa, name='tambah_mahasiswa'),
    path('grafik/', views.grafik, name='grafik'),
    path('hapus/<str:mahasiswa_id>/', views.hapus_mahasiswa, name='hapus_mahasiswa'),  # URL for delete action
    path('edit/<str:mahasiswa_id>/', views.edit_mahasiswa, name='edit_mahasiswa'),  # Edit URL
    path('export/csv/', views.export_csv, name='export_csv'),
    path('export/xlsx/', views.export_xlsx, name='export_xlsx'),
]
