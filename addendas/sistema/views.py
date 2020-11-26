from django.shortcuts import render
from lxml import etree
from pdb import set_trace
from sistema.models import Add_xml
from django.template.loader import render_to_string
import xml.etree.ElementTree as ET


# Create your views here.


def Inicio(request):

    #if request.method == 'POST':

        #set_trace()

    #    xml_upload = request.FILES.get('file_xml')
    #    print(xml_upload)
    #    
    #    #Add_xml.objects.create(
    #    #    file_xml = xml_upload,
    #    #)
    #    url_xml = Add_xml.objects.get()
    #    #ff = xml_upload.readlines()
    #    #print(ff)
    #    r_x = url_xml.file_xml.url
    #    print(r_x)        
    #    open_file = open(r_x, 'r')
    #    xml_string = open_file.read()
    #    open_file.close
    #    print(xml_string)

        ###Ruta del XML que se le agregará la addenda
    #ruta_xml = '/home/hsanchez/Descargas/A7D05CBF-C250-4DA9-8BF3-10912FA8E318.xml'
    ruta_xml = '/home/hsanchez/Descargas/FACTURA-A-2745.xml'
    
    
    #print(routa_xml)
        
    open_file = open(ruta_xml, 'r')
    print(ruta_xml) 
    xml_string = open_file.read()
    open_file.close
        #print(xml_string)
    xml_binario = etree.fromstring(xml_string.encode())
    #print(xml_binario)

    #version = xml_binario.get('Version')    
    #print(version)


    addenda = etree.Element(etree.QName('{http://www.sat.gob.mx/cfd/3}Addenda'))
    #print(addenda)

    knreception = etree.Element(etree.QName('{http://www.w3.org/2001/XMLSchema}KNRECEPCION'), nsmap = {'kn':'http://www.w3.org/2001/XMLSchema'})
    kntipo = etree.Element(etree.QName('{http://www.w3.org/2001/XMLSchema}Tipo'))
    facturaskn = etree.Element(etree.QName('{http://www.w3.org/2001/XMLSchema}FacturasKN'))
    purchase_order = etree.Element(etree.QName('{http://www.w3.org/2001/XMLSchema}Purchase_Order'))
    branch_centre = etree.Element(etree.QName('{http://www.w3.org/2001/XMLSchema}Branch_Centre'))
    branch_centre.text = '10DWT'
    transportes_ref = etree.Element(etree.QName('{http://www.w3.org/2001/XMLSchema}TransportRef'))
    transportes_ref.text = '2886541'
    file_number_gl = etree.Element(etree.QName('{http://www.w3.org/2001/XMLSchema}FileNumber_GL'))
    file_number_gl.text = '4554584231778522'
#
    nodo_bit = etree.tostring(knreception)

    addenda.append(knreception)
    knreception.append(kntipo)

    kntipo.append(facturaskn)

    facturaskn.append(purchase_order)  

    facturaskn.append(branch_centre)

    facturaskn.append(transportes_ref)

    purchase_order.append(file_number_gl)

    add_integrada = etree.tostring(addenda)

    ###Agregamos la adenda en el xml se agregará en el último nodo el cual es complemento.
    xml_binario.append(addenda)
    xml_con_addenda = etree.tostring(xml_binario, encoding='UTF-8', xml_declaration=True).decode()

    return render(request, 'inicio.html', {'xml_ade':xml_con_addenda})