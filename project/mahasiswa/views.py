from django.shortcuts import render, redirect, get_object_or_404
from .models import Mahasiswa
from mongoengine.errors import DoesNotExist  # Import for handling not found errors
from django.db.models import Count
import json
import csv
import io
import openpyxl
from django.http import HttpResponse

def mahasiswa_list(request):
    mahasiswa = Mahasiswa.objects.all()  # Ambil semua mahasiswa
    total_mahasiswa = mahasiswa.count()   # Hitung total mahasiswa

    return render(request, 'mahasiswa_list.html', {
        'mahasiswa': mahasiswa,
        'total_mahasiswa': total_mahasiswa,  # Kirim total mahasiswa ke template
    })

def tambah_mahasiswa(request):
    if request.method == 'POST':
        # Get the form data from POST request
        nama = request.POST.get('Nama')
        nim = request.POST.get('Nim')
        ttl = request.POST.get('Ttl')
        jenis_kelamin = request.POST.get('Jenis_Kelamin')
        no_telepon = request.POST.get('No_Telepon')

        # Create a new Mahasiswa instance and save it to MongoDB
        mahasiswa = Mahasiswa(
            Nama=nama,
            Nim=nim,
            Ttl=ttl,
            Jenis_Kelamin=jenis_kelamin,
            No_Telepon=no_telepon
        )
        mahasiswa.save()  # Save to MongoDB

        # Redirect to the mahasiswa list page after saving
        return redirect('mahasiswa_list')

    # If the request is GET, render the form
    return render(request, 'tambah_mahasiswa.html')

def hapus_mahasiswa(request, mahasiswa_id):
    try:
        mahasiswa = Mahasiswa.objects.get(id=mahasiswa_id)  # Fetch the Mahasiswa object using MongoDB's query
        mahasiswa.delete()  # Delete the student from MongoDB
    except DoesNotExist:
        # Handle the case where the Mahasiswa doesn't exist
        return render(request, 'error.html', {'message': 'Mahasiswa tidak ditemukan.'})

    return redirect('mahasiswa_list')  # Redirect back to the student list after deletion

def edit_mahasiswa(request, mahasiswa_id):
    try:
        mahasiswa = Mahasiswa.objects.get(id=mahasiswa_id)  # Fetch the Mahasiswa object from MongoDB
    except DoesNotExist:
        # Handle the case where the Mahasiswa doesn't exist
        return render(request, 'error.html', {'message': 'Mahasiswa tidak ditemukan.'})

    if request.method == 'POST':
        # Update the Mahasiswa fields from the form data
        mahasiswa.Nama = request.POST.get('Nama')
        mahasiswa.Nim = request.POST.get('Nim')
        mahasiswa.Ttl = request.POST.get('Ttl')
        mahasiswa.Jenis_Kelamin = request.POST.get('Jenis_Kelamin')
        mahasiswa.No_Telepon = request.POST.get('No_Telepon')
        
        mahasiswa.save()  # Save the updated Mahasiswa document in MongoDB
        return redirect('mahasiswa_list')  # Redirect back to the list after saving

    return render(request, 'edit_mahasiswa.html', {'mahasiswa': mahasiswa})  # Display form with the current data

def grafik(request):
    # Count the number of male and female students
    laki_laki_count = Mahasiswa.objects.filter(Jenis_Kelamin='Laki-Laki').count()
    perempuan_count = Mahasiswa.objects.filter(Jenis_Kelamin='Perempuan').count()

    # Pass the counts to the template
    context = {
        'laki_laki_count': laki_laki_count,
        'perempuan_count': perempuan_count,
    }
    
    return render(request, 'grafik.html', context)

def export_csv(request):
    # Create the HTTP response object with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mahasiswa.csv"'

    # Create a CSV writer
    writer = csv.writer(response)
    
    # Write the header
    writer.writerow(['Nama', 'NIM', 'TTL', 'Jenis Kelamin', 'No Telepon'])

    # Write the data rows
    for mahasiswa in Mahasiswa.objects.all():
        writer.writerow([mahasiswa.Nama, mahasiswa.Nim, mahasiswa.Ttl, mahasiswa.Jenis_Kelamin, mahasiswa.No_Telepon])

    return response

def export_xlsx(request):
    # Create the HTTP response object with XLSX header
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="mahasiswa.xlsx"'

    # Create a workbook and a sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Mahasiswa'

    # Write the header
    headers = ['Nama', 'NIM', 'TTL', 'Jenis Kelamin', 'No Telepon']
    sheet.append(headers)

    # Write the data rows
    for mahasiswa in Mahasiswa.objects.all():
        sheet.append([mahasiswa.Nama, mahasiswa.Nim, mahasiswa.Ttl, mahasiswa.Jenis_Kelamin, mahasiswa.No_Telepon])

    # Save the workbook to the response stream
    workbook.save(response)

    return response

    