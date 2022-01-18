import csv
import struct


class Estadisticas:
    def __init__(self):
        self.total_provincias = {}
        self.total_condicion = {}
        self.total_sexo = {}
        self.total_dosis_1 = 0
        self.total_dosis_2 = 0

    def extraer_datos(self, archivo_a_importar, delimitador=";"):
        """ Extrae la informacion de un archivo_a_importar en formato .csv separado por un delimitador. """
        with open(archivo_a_importar, 'r') as tabla:
            lector = csv.DictReader(tabla, delimiter=delimitador)
            for linea in lector:
                numero_de_dosis = linea['orden_dosis']
                self.actualizar_cant_por_provincia(numero_de_dosis, linea['jurisdiccion_residencia'])
                self.actualizar_cant_por_condicion(numero_de_dosis, linea['condicion_aplicacion'])
                self.actualizar_cant_por_sexo(numero_de_dosis, linea['sexo'])
                self.actualizar_cant_total_de_dosis(numero_de_dosis)

    def actualizar_cant_por_provincia(self, dosis, provincia):
        """ Actualiza el diccionario de cantidad de vacunados segun su provincia.
            Por cada provincia hay un subdiccionario con la cantidad de primeras y segundas dosis. """
        if provincia not in self.total_provincias:
            self.total_provincias.update({provincia: {'1': 0, '2': 0}})

        self.total_provincias[provincia].update({dosis: self.total_provincias[provincia][dosis] + 1})

    def actualizar_cant_por_condicion(self, dosis, condicion):
        """ Actualiza el diccionario de cantidad de vacunados segun su condicion de salud.
            Por cada condicion hay un subdiccionario con la cantidad de primeras y segundas dosis. """
        if condicion not in self.total_condicion:
            self.total_condicion.update({condicion: {'1': 0, '2': 0}})

        self.total_condicion[condicion].update({dosis: self.total_condicion[condicion][dosis] + 1})

    def actualizar_cant_por_sexo(self, dosis, sexo):
        """ Actualiza el diccionario de cantidad de vacunados segun su sexo.
            Por cada sexo hay un subdiccionario con la cantidad de primeras y segundas dosis. """
        if sexo not in self.total_sexo:
            self.total_sexo.update({sexo: {'1': 0, '2': 0}})

        self.total_sexo[sexo].update({dosis: self.total_sexo[sexo][dosis] + 1})

    def actualizar_cant_total_de_dosis(self, dosis):
        if dosis == '1':
            self.total_dosis_1 += 1
        if dosis == '2':
            self.total_dosis_2 += 1

    def exportar_por_provincia(self, archivo_a_exportar):
        formato = '%ds%ds%ds%ds' % (20, 8, 8, 9)    # Provincia(20), Dosis 1(8), Dosis 2(8), Aplicadas total(9)

        with open(archivo_a_exportar, 'wb') as datos:
            for provincia in self.total_provincias.keys():
                datos.write(struct.pack(formato,
                                        str(provincia).encode(),
                                        str(self.total_provincias[provincia]['1']).encode(),
                                        str(self.total_provincias[provincia]['2']).encode(),
                                        str(self.total_provincias[provincia]['1'] +
                                            self.total_provincias[provincia]['2']).encode()))

    def exportar_por_condicion(self, archivo_a_exportar):
        formato = '%ds%ds%ds%ds' % (36, 8, 8, 9)    # Condicion(36), Dosis 1(8), Dosis 2(8), Aplicadas total(9)

        with open(archivo_a_exportar, 'wb') as datos:
            for condicion in self.total_condicion.keys():
                datos.write(struct.pack(formato,
                                        str(condicion).encode(),
                                        str(self.total_condicion[condicion]['1']).encode(),
                                        str(self.total_condicion[condicion]['2']).encode(),
                                        str(self.total_condicion[condicion]['1'] +
                                            self.total_condicion[condicion]['2']).encode()))

    def exportar_por_sexo(self, archivo_a_exportar):
        formato = '%ds%ds%ds%ds' % (4, 8, 8, 9)     # Sexo(4), Dosis 1(8), Dosis 2(8), Aplicadas total(9)

        with open(archivo_a_exportar, 'wb') as datos:
            for sexo in self.total_sexo.keys():
                datos.write(struct.pack(formato,
                                        str(sexo).encode(),
                                        str(self.total_sexo[sexo]['1']).encode(),
                                        str(self.total_sexo[sexo]['2']).encode(),
                                        str(self.total_sexo[sexo]['1'] +
                                            self.total_sexo[sexo]['2']).encode()))

    def exportar_totales(self, archivo_a_exportar):
        formato = '%ds%ds%ds' % (8, 8, 9)           # Total dosis 1(8), Total dosis 2(8), Aplicadas total(9)

        with open(archivo_a_exportar, 'wb') as datos:
            datos.write(struct.pack(formato,
                                    str(self.total_dosis_1).encode(),
                                    str(self.total_dosis_2).encode(),
                                    str(self.total_dosis_1 +
                                        self.total_dosis_2).encode()))


if __name__ == '__main__':
    estadisticas_covid = Estadisticas()

    # Elegir el archivo del cual extraer datos y el separador de campos
    estadisticas_covid.extraer_datos('archivos/covid19.csv', ';')

    # Se pueden abrir en un bloc de notas con codificacion utf-8
    estadisticas_covid.exportar_por_provincia('_porprovincia.bin')
    estadisticas_covid.exportar_por_condicion('_porcondicion.bin')
    estadisticas_covid.exportar_por_sexo('_porsexo.bin')
    estadisticas_covid.exportar_totales('_totales.bin')
