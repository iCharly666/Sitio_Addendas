ruta_xml = '/home/hsanchez/Descargas/FACTURA-A-2745.xml'
    open_file = open(ruta_xml, 'r')
    print(ruta_xml) 
    xml_string = open_file.read()
    open_file.close
        #print(xml_string)
    xml_binario = etree.fromstring(xml_string.encode())
    addenda = etree.Element(etree.QName('{http://www.sat.gob.mx/cfd/3}Addenda'))
    
    knreception = etree.Element(etree.QName('{http://www.w3.org/2001/XMLSchema}KNRECEPCION'), nsmap = {'kn':'http://www.w3.org/2001/XMLSchema'})
    kntipo = etree.Element(etree.QName('{http://www.w3.org/2001/XMLSchema}Tipo'))
    facturaskn = etree.Element(etree.QName('{http://www.w3.org/2001/XMLSchema}FacturasKN'))
    purchase_order = etree.Element(etree.QName('{http://www.w3.org/2001/XMLSchema}Purchase_Order'))
    purchase_order.text = ''
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
    facturaskn.append(file_number_gl)
    facturaskn.append(branch_centre)
    facturaskn.append(transportes_ref)


    add_integrada = etree.tostring(addenda)

    ###Agregamos la adenda en el xml se agregará en el último nodo el cual es complemento.
    xml_binario.append(addenda)
    xml_con_addenda = etree.tostring(xml_binario, encoding='UTF-8', xml_declaration=True).decode()