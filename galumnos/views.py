from django.shortcuts import render
from django.core.mail import send_mail

from django.core.mail import EmailMessage
from galumnos.models import Alumnos, Modulos

import csv
from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer,
Paragraph, Table, TableStyle)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

from barcode.codex import Code128
from barcode.writer import ImageWriter

def creararchivoPDFC():
    doc = SimpleDocTemplate("galumnos/pdf/codigobarra.pdf", pagesize=A4)
    story = []
    datos = [['barcode', "nombre", "apellido Paterno", "Apellido Materno"]]
    listaalum = Alumnos.objects.all()
    for alum in listaalum:
        barcode = Image('cfttalcaalumnos/static/barcode/'+alum.rut+'.jpg', width=100, height=50)
        datos.append([barcode,alum.nombre, alum.apellidop, alum.apellidom])
    tabla = Table(data=datos,
                  style=[
                      ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                      ('BOX', (0, 0), (-1, -1), 2, colors.black),
                      ('BACKGROUND', (0, 0), (-1, 0), colors.pink),
                  ])
    story.append(tabla)
    story.append(Spacer(0, 15))
    doc.build(story)



def creabarcode(numero):
    with open('cfttalcaalumnos/static/barcode/'+numero+'.jpg', 'wb') as f:
        Code128(numero, writer=ImageWriter()).write(f)

def creararchivoPDF(nombre):
    rutt = nombre[0] + nombre[1] + nombre[2]
    doc = SimpleDocTemplate("galumnos/pdf/"+nombre+".pdf", pagesize=A4, encrypt=str(rutt))
    story = []
    datos = [['Nombre Modulo', "Carrera", "Docente", "nhoras"]]
    listamodulos = Modulos.objects.filter(docente="Maximiliano Vilches Castillo")
    for modul in listamodulos:
        datos.append([modul.nombremodulo, modul.carrera, modul.docente, modul.nhoras])
    tabla = Table(data=datos,
                  style=[
                      ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                      ('BOX', (0, 0), (-1, -1), 2, colors.black),
                      ('BACKGROUND', (0, 0), (-1, 0), colors.pink),
                  ])
    story.append(tabla)
    story.append(Spacer(0, 15))
    doc.build(story)

def importdat():
    cargarcsv = 'C:/csv/alumnos.csv'
    with open(cargarcsv) as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            nalumno = Alumnos(rut=row[0],nombre=row[3],apellidop=row[1],apellidom=row[2],email=row[5],telefono=row[4])
            nalumno.save()


def graficos(request):
    listalumnos = Alumnos.objects.all()
    return render(request, "grafico.html",{"alumnott": listalumnos})

def datos(request):
    alumnos = Alumnos.objects.all()
    for al in alumnos:
        creabarcode(al.rut)
    creararchivoPDFC()
    return render(request, "datos.html", {"alumnott": alumnos})

def correoadjunto(request):
    if request.method == "POST":
        creararchivoPDF("pruebadeadjunto")
        nombre = request.POST['name']
        correo = request.POST['correo']
        mensaje = request.POST['mensaje']
        lista = Alumnos.objects.all()
        for alum in lista:
            creararchivoPDF(alum.rut)
            email = EmailMessage(
                    'Hola '+alum.nombre,
                    'Este es un correo de prueba',
                    'pvilches1987@gmail.com',
                    [alum.email],
                    ['tekikomujito@mgmail.com'],
                    reply_to=['noresponder@ggfetfmail.com'],
                    headers={'Message-ID': 'foo'},
                )
            email.attach_file("galumnos/pdf/"+alum.rut+".pdf")
            email.send()
        return render(request, "enviado.html")
    return render(request, "formulario.html")



def correo(request):
    if request.method == "POST":
        nombre = request.POST['name']
        correo = request.POST['correo']
        mensaje = request.POST['mensaje']
        send_mail(
            'Hola LUCENA soy '+nombre,
            mensaje,
            'pvilches1987@gmail.com',
            [correo],
            fail_silently=False,)
        return render(request, "enviado.html")
    return render(request, "formulario.html")