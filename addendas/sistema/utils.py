#from io import BytesIO
#
#from django.template.loader import get_template
#
#
#from xhtml2pdf import pisa
#
#
#
#def render_to_pdf(template_src, context_dict={}):
#    template = get_template(template_src)
#    html = template.render(context_dict)
#    result = BytesIO
#    pdf = pisa.pisaDocument(BytesIO(html), result)
#    if not pdf.err:
#        return HttpResponse(result.getvalue(), context_type='application/pdf')
#        
#    return None
