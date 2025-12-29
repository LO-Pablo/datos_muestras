from django import template
# Filtros personalizados para plantillas de Django
register = template.Library()
# Filtro para verificar si una cadena comienza con un prefijo específico
@register.filter
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False
# Filtro para obtener un valor de un diccionario dado una clave
@register.filter
def get_item(dictionary, key):
    try:
        return dictionary.get(key)
    except:
        return ''

