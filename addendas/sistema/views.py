# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from lxml import etree
from pdb import set_trace
from sistema.models import Add_xml, Xml_Addenda
from django.template.loader import render_to_string
import xml.etree.ElementTree as ET


from django.views.generic import ListView, View
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
import os
# Create your views here.



def Inicio(request):
   

    return render(request, 'inicio.html')


def Terra_Multi(request):
    xml_string = ''
    xml_en_binario = ''
    xml_con_addenda = ''
    try:

        xml_upload = request.FILES.get('file_xml')
        add_contenedor = request.POST.get('contenedor')
        add_referencia = request.POST.get('referencia')
        add_reservacion = request.POST.get('reservacion')
        add_total = request.POST.get('total')
        add_iva = request.POST.get('iva')
        add_retencion = request.POST.get('retencion')
        add_valor = request.POST.get('valor')
        add_descripcion = request.POST.get('descripcion')


        print(add_contenedor)
        print(add_referencia)
        print(add_reservacion)
        print(add_total)
        print(add_iva)
        print(add_retencion)
        print(add_valor)
        print(add_descripcion)
        
        if xml_upload:
            xml_string = xml_upload.read()

            xml_en_binario =etree.fromstring(xml_string)
            
            ##Apartado para crear nodos
            addenda = etree.Element(etree.QName('{http://www.sat.gob.mx/cfd/3}Addenda'))
            unique = etree.Element(etree.QName('Unique'))
            unique.set('Contenedor', add_contenedor)
            unique.set('Referencia', add_referencia)
            unique.set('Reservacion', add_reservacion)
            unique.set('total', add_total)
            unique.set('iva', add_iva)
            unique.set('retencion', add_retencion)
            unique.set('valor', add_valor)
            unique.set('descripcion', add_descripcion)
    
            nodo_bit = etree.tostring(unique)
    
            addenda.append(unique)
    
            add_integrada = etree.tostring(addenda)
    
            ###Agregamos la adenda en el xml se agregará en el último nodo el cual es complemento.
            xml_en_binario.append(addenda)
            xml_con_addenda = etree.tostring(xml_en_binario, encoding='UTF-8', xml_declaration=True).decode()
            print(type(xml_con_addenda))
    except NameError:
        print("Error")

    return render(request, 'addenda_terra_multi.html',{'xml_ade':xml_con_addenda})


##Código de la addenda de open_lenguage------------------------------------------
def open_lenguge(request):

    xml_string = ''
    xml_en_binario = ''
    xml_con_addenda = ''
    c = ''
    try:

        xml_upload = request.FILES.get('file_xml')
        add_Purchase_Order = request.POST.get('Purchase_Order')
        add_FileNumber_GL = request.POST.get('FileNumber_GL')
        add_Branch_Centre = request.POST.get('Branch_Centre')
        add_TransportRef = request.POST.get('TransportRef')

        print(add_Purchase_Order)
        print(add_FileNumber_GL)
        print(add_Branch_Centre)
        print(add_TransportRef)
        
        if xml_upload:
            xml_string = xml_upload.read()

            xml_en_binario =etree.fromstring(xml_string)
            

            addenda = etree.Element(etree.QName('{http://www.sat.gob.mx/cfd/3}Addenda'))

            knreception = etree.Element(etree.QName('{http://www.w3.org/2001/XMLSchema}KNRECEPCION'), nsmap = {'kn':'http://www.w3.org/2001/XMLSchema'})
            kntipo = etree.Element(etree.QName('{http://www.w3.org/2001/XMLSchema}Tipo'))
            facturaskn = etree.Element(etree.QName('{http://www.w3.org/2001/XMLSchema}FacturasKN'))
            purchase_order = etree.Element(etree.QName('{http://www.w3.org/2001/XMLSchema}Purchase_Order'))
            purchase_order.text = add_Purchase_Order
            branch_centre = etree.Element(etree.QName('{http://www.w3.org/2001/XMLSchema}Branch_Centre'))
            branch_centre.text = add_Branch_Centre
            transportes_ref = etree.Element(etree.QName('{http://www.w3.org/2001/XMLSchema}TransportRef'))
            transportes_ref.text = add_TransportRef
            file_number_gl = etree.Element(etree.QName('{http://www.w3.org/2001/XMLSchema}FileNumber_GL'))
            file_number_gl.text = add_FileNumber_GL
    
            nodo_bit = etree.tostring(knreception)
    
            addenda.append(knreception)
            knreception.append(kntipo)
    
            kntipo.append(facturaskn)
    
            facturaskn.append(purchase_order)  
            facturaskn.append(file_number_gl)
            facturaskn.append(branch_centre)   
            facturaskn.append(transportes_ref)
    
            add_integrada = etree.tostring(addenda)
    
            ###Agregamos la adenda en el xml se agregará en el último nodo el cual es complemento.
            #set_trace()
            xml_en_binario.append(addenda)
            xml_con_addenda = etree.tostring(xml_en_binario, encoding='UTF-8', xml_declaration=True).decode()
            print(type(xml_con_addenda))
            
            data = xml_con_addenda
            response = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            
            #request.build_absolute_uri(reverse('Descargar_xml', args=(xml_con_addenda)))

             ##----Extraer los valores del XML
            
            print("-----Datos Comprobante-----")
            #Datos comprobante
            folio = xml_en_binario.get('Folio')
            print('folio', folio)
            serie = xml_en_binario.get('Serie')
            print('folio', serie)
            no_certificado = xml_en_binario.get('NoCertificado')
            print('no_certificado', no_certificado)
            fecha_emision = xml_en_binario.get('Fecha')
            print('fecha emision', fecha_emision)
            sello = xml_en_binario.get('Sello')
            print('sello', sello)
            tipo_comprobante = xml_en_binario.get('TipoComprobante')
            print('tipo comprobante', tipo_comprobante)

            print("-----Datos SAT-----")
            #Datos del sat
            uid = xml_en_binario[4][0].get('UUID')
            print('UUID', uid)
            fecha_timbrado = xml_en_binario[4][0].get('FechaTimbrado')
            print('Fecha timbrado', fecha_timbrado)
            sello_sat = xml_en_binario[4][0].get('SelloSat')
            print('Sello SAT', sello_sat)
            csd_sat = xml_en_binario[4][0].get('NoCertificadoSAT')
            print('csd sat', csd_sat)

            print("-----Datos Pago-----")
            #Datos de pago
            metodo_pago = xml_en_binario.get('MetodoPago')
            print('metodo pago', metodo_pago)
            forma_pago = xml_en_binario.get('FormaPago')
            print('forma pago', forma_pago)
            moneda = xml_en_binario.get('Moneda')
            print('moneda', moneda)
            tipo_cambio = xml_en_binario.get('TipoCambio')
            print('moneda', tipo_cambio)
            subtotal = xml_en_binario.get('SubTotal')
            print('sub total', subtotal)
            total = xml_en_binario.get('Total')
            print('total', total)

            print("-----Emisor-----")
            #Datos del emisor
            razon_social_emisor = xml_en_binario[0].get('Nombre')
            print('Razon social Emisor', razon_social_emisor)
            regimen_fiscal_emisor = xml_en_binario[0].get('RegimenFiscal')
            print('regimen fiscal Emisor', regimen_fiscal_emisor)
            rfc_emisor = xml_en_binario[0].get('Rfc')
            print('Razon social Emisor', rfc_emisor)

            print("-----Receptor-----")
            #Datos del receptor
            razon_social_receptor = xml_en_binario[1].get('Nombre')
            print('Razon social receptor', razon_social_receptor)
            regimen_fiscal_receptor = xml_en_binario[1].get('UsoCFDI')
            print('regimen fiscal receptor', regimen_fiscal_receptor)
            rfc_receptor = xml_en_binario[1].get('Rfc')
            print('Razon social receptor', rfc_receptor)
            
            print("-----Addenda-----")
            #Datos de la addenda Open League
            purchase_order = xml_en_binario[5][0][0][0][0].text
            print('orden de compra', purchase_order)
            no_expedientegl = xml_en_binario[5][0][0][0][1].text
            print('no. expediente GL', no_expedientegl)
            centro_sucursal = xml_en_binario[5][0][0][0][2].text
            print('centro sucursal', centro_sucursal)
            ref_transporte = xml_en_binario[5][0][0][0][3].text
            print('ref transporte', ref_transporte)

            #list_xml = list(xml_en_binario)
            #print(list_xml)


            
            opcion = request.POST.get('opcion')
            if opcion == 'descargar':
                response = HttpResponse(content_type='applicaction/pdf')
                response['Content-Disposition'] = 'attachment; filename=XML con Addenda.pdf'
                buffer = BytesIO()
                c = canvas.Canvas(buffer, pagesize=A4)
                c.setLineWidth(.3)
                c.setFont('Helvetica', 22)
                c.drawString(30, 750, folio)
                c.save()
                pdf = buffer.getvalue()
                buffer.close()
                response.write(pdf)
        
                return response

    except Exception as e:
        print('ecepcion en la vista open leguage => {}'.format(str(e)))

    return render(request, 'addenda_open_lenguage.html',{'xml_ade':xml_con_addenda} )


def Descargar_xml(request, xml_con_addenda):
    response['Content-Disposition'] = 'attachment; xml_con_addenda={}'.format(xml_con_addenda)

    return render(request)







###Opción 1
##--------------------------------------------------------------------------------

#    xml_con_addenda = ''
#    
#    if request.method == 'POST':
#
#        #set_trace()
#        xml_upload = request.FILES.get('file_xml')
#        print('UUID-Docuemnto agregado por usuario:', xml_upload)
#        
#        add_xml_bd = Add_xml.objects.create(
#            file_xml = xml_upload,
#        )
#        
#        xml_consulting = Add_xml.objects.all()
#        for xmls in xml_consulting:
#            url_xml = xmls.file_xml
#            #print('ruta xml en base de datos: ', url_xml)
#
#       
#       
#        r_x = url_xml.path
#        print(r_x)        
#        open_file = open(r_x, 'r')
#        xml_string = open_file.read()
#        open_file.close
#        #print(xml_string)
#
#        xml_en_binario =etree.fromstring(xml_string.encode())
#        #print(xml_en_binario)
#        
#        
#
#        #version = xml_en_binario.get('Version')
#        #print(version)
#        addenda = etree.Element(etree.QName('{http://www.sat.gob.mx/cfd/3}Addenda'))
#
#        knreception = etree.Element(etree.QName('{http://www.w3.org/2001/XMLSchema}KNRECEPCION'), nsmap = {'kn':'http://www.w3.org/2001/XMLSchema'})
#
#        kntipo = etree.Element(etree.QName('{http://www.w3.org/2001/XMLSchema}Tipo'))
#        facturaskn = etree.Element(etree.QName('{http://www.w3.org/2001/XMLSchema}FacturasKN'))
#        purchase_order = etree.Element(etree.QName('{http://www.w3.org/2001/XMLSchema}Purchase_Order'))
#        branch_centre = etree.Element(etree.QName('{http://www.w3.org/2001/XMLSchema}Branch_Centre'))
#        branch_centre.text = '10DWT'
#        transportes_ref = etree.Element(etree.QName('{http://www.w3.org/2001/XMLSchema}TransportRef'))
#        transportes_ref.text = '2886541'
#        file_number_gl = etree.Element(etree.QName('{http://www.w3.org/2001/XMLSchema}FileNumber_GL'))
#        file_number_gl.text = '4554584231778522'
#
#        nodo_bit = etree.tostring(knreception)
#
#        addenda.append(knreception)
#        knreception.append(kntipo)
#
#        kntipo.append(facturaskn)
#
#        facturaskn.append(purchase_order)  
#
#        facturaskn.append(branch_centre)
#
#        facturaskn.append(transportes_ref)
#
#        purchase_order.append(file_number_gl)
#        add_integrada = etree.tostring(addenda)
#
#        ###Agregamos la adenda en el xml se agregará en el último nodo el cual es complemento.
#        xml_en_binario.append(addenda)
#        xml_con_addenda = etree.tostring(xml_en_binario, encoding='UTF-8', xml_declaration=True).decode()
#        print(type(xml_con_addenda))
#
#
#
#
#        #Xml_Addenda.objects.create(
#        #    file_addenda = xml_con_addenda
#        #)


##----------------------------------------------------------------------------------------
  
    