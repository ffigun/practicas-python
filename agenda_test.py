from agenda import *


# Crear un contacto con parametros obligatorios
def test001():
    a = Agenda()
    a.agregar_contacto('Juan Perez', 'cel', '11 1234-5678', 'juanperez@gmail.com', 'Magallanes', '1234', 'CABA')

    assert 'Juan Perez' in a.contactos


# Crear un contacto con parametros opcionales
def test002():
    a = Agenda()
    a.agregar_contacto('Lucas', 'cel', '11 1234-5678', 'lucas@gmail.com', 'Magallanes', '1234', 'CABA', '1', 'B')
    comp = {
        'nombre': 'Lucas',
        'tel': {'cel': '11 1234-5678'},
        'mail': 'lucas@gmail.com',
        'domicilio': {'calle': 'Magallanes', 'nro': '1234', 'localidad': 'CABA', 'piso': '1', 'depto': 'B'}
    }

    assert a.obtener_contacto('Lucas') == comp


# Crear un contacto y agregar un telefono adicional
def test003():
    a = Agenda()
    a.agregar_contacto('Lucas', 'cel', '11 1234-5678', 'lucas@gmail.com', 'Magallanes', '1234', 'CABA')
    a.agregar_telefono('Lucas', 'casa', '1234-5678')
    comp = {
        'nombre': 'Lucas',
        'tel': {'cel': '11 1234-5678', 'casa': '1234-5678'},
        'mail': 'lucas@gmail.com',
        'domicilio': {'calle': 'Magallanes', 'nro': '1234', 'localidad': 'CABA'}
    }

    assert a.obtener_contacto('Lucas') == comp
