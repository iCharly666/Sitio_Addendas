     ###Ruta del XML que se le agregará la addenda
    ruta_xml = '/home/hsanchez/Descargas/A7D05CBF-C250-4DA9-8BF3-10912FA8E318.xml'
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


    addenda = etree.Element(etree.QName('{http://www.sat.gob.mx/cfd/3}Addenda'), nsmap = {'cfdi':'http://www.sat.gob.mx/cfd/3'})
    #print(addenda)

    AddendaCFDServicios = etree.Element(etree.QName('Unique'))
    ##print(AddendaCFDServicios)
#
    nodo_bit = etree.tostring(AddendaCFDServicios)
#
    AddendaCFDServicios.set('Contenedor', 'PCDJ040594')#Campo obligatorio
    AddendaCFDServicios.set('Referencia', '20PAC44DT')#Campo opcional
    AddendaCFDServicios.set('Reservación', '293569')#Campo obligatorio
    AddendaCFDServicios.set('total', '') #Campo obligatorio si contiene valor
    AddendaCFDServicios.set('IVA', '')#Campo obligatorio si contiene valor
    AddendaCFDServicios.set('retencion', '')#Campo obligatorio si contiene valor
    AddendaCFDServicios.set('descripcion', '')#Campo opcional
    #print(etree.tostring(AddendaCFDServicios))
##
    notaentrega = etree.Element(etree.QName('NotaEntrega'))
    notaentrega.text = 'TEFFDFD'
    #print(etree.tostring(notaentrega))
#
    ordencompra = etree.Element(etree.QName('OrdenCompra'))
    ordencompra.text = 'FT'
    #print(etree.tostring(ordencompra))
#
#
    ###En este apartado agregamos los nodos nietos al hijo AddendaCFDservicios 
    AddendaCFDServicios.append(notaentrega)
    AddendaCFDServicios.append(ordencompra)
    ##print(etree.tostring(AddendaCFDServicios))
#
    addenda.append(AddendaCFDServicios)
    add_integrada = etree.tostring(addenda)
#
#
#
    ###Agregamos la adenda en el xml se agregará en el último nodo el cual es complemento.
    xml_binario.append(addenda)
    xml_con_addenda = etree.tostring(xml_binario, encoding='UTF-8', xml_declaration=True).decode()
