import shelve
import json


class Agenda:
    def __init__(self):
        # La agenda es un diccionario de diccionarios del tipo {nombre: Contacto}
        self.contactos = {str: Contacto}
        self.contactos.clear()

    def agregar_contacto(self, nombre, etq_tel, tel, mail, calle, nro, localidad, piso=None, depto=None):
        self.contactos.update({nombre: Contacto(nombre, etq_tel, tel, mail, calle, nro, localidad, piso, depto)})

    def agregar_telefono(self, nombre, etiqueta, numero):
        self.contactos[nombre].agregar_telefono(etiqueta, numero)

    def agregar_mail(self, nombre, mail):
        self.contactos[nombre].agregar_mail(mail)

    def agregar_domicilio(self, nombre, calle, nro, localidad, piso=None, depto=None):
        self.contactos[nombre].agregar_domicilio(calle, nro, localidad, piso, depto)

    def agregar_datos_opcionales(self, nombre, piso=None, depto=None):
        self.contactos[nombre].agregar_datos_opcionales(piso, depto)

    def existe_contacto(self, nombre):
        return nombre in self.contactos

    def mostrar_contacto(self, nombre):
        return str(self.contactos[nombre]) if self.existe_contacto(nombre) else 'El contacto ' + nombre + ' no existe.'

    def obtener_contacto(self, nombre):
        return self.contactos[nombre].obtener_datos()

    def listar_contactos(self):
        buffer = ''
        for contacto in self.contactos.keys():
            buffer += str(self.contactos[contacto]) + '\n'
        return buffer

    def exportar(self, nombre_de_archivo):
        try:
            with shelve.open(nombre_de_archivo, 'c') as db:
                for contacto in self.contactos.keys():
                    db[contacto] = self.contactos[contacto]
        except Exception:
            return 'Ocurrio un error al exportar los contactos.'
        return 'Los contactos se exportaron correctamente.'

    def importar(self, nombre_de_archivo):
        try:
            with shelve.open(nombre_de_archivo, 'r') as db:
                for (key, value) in db.items():
                    self.contactos.update({key: value})
        except Exception:
            return 'Ocurrio un error al importar los contactos.'
        return 'Los contactos se importaron correctamente.'


class Contacto:
    def __init__(self, nombre, etq_tel, tel, mail, calle, nro, localidad, piso=None, depto=None):
        self.datos = {
            'nombre': nombre,
            'tel': {etq_tel: tel},
            'mail': mail,
            'domicilio': {'calle': calle, 'nro': nro, 'localidad': localidad}
        }
        self.agregar_datos_opcionales(piso, depto)

    def __str__(self):
        # Uso el dump de json para poder representar rapidamente el diccionario
        return json.dumps(self.datos, sort_keys=False, indent=4)

    def obtener_datos(self):
        return self.datos

    def obtener_nombre(self):
        return self.datos['nombre']

    def agregar_mail(self, mail):
        self.datos.update({'mail': mail})

    def agregar_telefono(self, etiqueta, numero):
        self.datos['tel'].update({etiqueta: numero})

    def agregar_domicilio(self, calle, nro, localidad, piso=None, depto=None):
        self.datos['domicilio'].update({'calle': calle, 'nro': nro, 'localidad': localidad})
        self.agregar_datos_opcionales(piso, depto)

    def agregar_datos_opcionales(self, piso=None, depto=None):
        if depto is not None:
            self.datos['domicilio'].update({'depto': depto})
        if piso is not None:
            self.datos['domicilio'].update({'piso': piso})


if __name__ == '__main__':
    # Demostracion

    print('\n----- Crear agenda')
    agenda = Agenda()

    print('\n----- Crear un contacto llamado Juan solo con datos obligatorios')
    agenda.agregar_contacto('Juan', 'celular', '11 2345-6789', 'juan@gmail.com', 'Magallanes', '1123', 'Sarmiento')

    print('\n----- Crear un contacto llamado Flor con todos los datos')
    agenda.agregar_contacto('Flor', 'casa', '2345-6789', 'flor@gmail.com', 'Azara', '879', 'CABA', '2', 'B')

    print('\n----- Agregar un telefono adicional a Flor (celular: 11 2323-4567)')
    agenda.agregar_telefono('Flor', 'celular', '11 2323-4567')

    print('\n----- Buscar/Mostrar un contacto existente (Juan)')
    print(agenda.mostrar_contacto('Juan'))

    print('\n----- Buscar/Mostrar un contacto inexistente (Pablo)')
    print(agenda.mostrar_contacto('Pablo'))

    print('\n----- Agregar datos opcionales a Juan (piso: 1, depto: A)')
    agenda.agregar_datos_opcionales('Juan', '1', 'A')

    print('\n----- Verificar que hayan impactado los datos opcionales de Juan')
    print(agenda.mostrar_contacto('Juan'))

    print('\n----- Guardar datos con shelve en un archivo agenda.dat')
    print(agenda.exportar('agenda'))

    print('\n----- Crear una nueva_agenda e importar con shelve el archivo agenda.dat')
    nueva_agenda = Agenda()
    print(nueva_agenda.importar('agenda'))

    print('\n----- Mostrar todo el contenido de nueva_agenda')
    print(nueva_agenda.listar_contactos())
