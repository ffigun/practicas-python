from nltk.stem import SnowballStemmer   # Stemmer
from nltk.corpus import stopwords       # Stopwords
import string


class IndiceInvertido:
    def __init__(self, documentos=None):
        """
        Recibe una lista con los documentos.
        """
        if documentos is None:
            documentos = []
        self.stop_words = frozenset(stopwords.words('spanish'))  # lista de stop words
        self._docs = documentos
        self._spanish_stemmer = SnowballStemmer('spanish', ignore_stopwords=False)
        self.__docs_to_docID()
        self.__generar_indice()

    def __docs_to_docID(self):
        """
        Asigna a cada documento un número y guarda dos diccionarios:
        el primero que tiene como clave el nombre del documento y como valor el
        numero de documento docID asociado y el segundo que permite realizar la
        operación inversa y tiene como clave los docID y como valor el nombre del
        documento
        """
        self._doc_to_docID = {}
        docID = 0
        for doc in self._docs:
            self._doc_to_docID[doc] = docID
            docID += 1
        self._docID_to_doc = dict((v, k) for k, v in self._doc_to_docID.items())

    def __lematizar_palabra(self, palabra):
        """
        Usa el stemmer para lematizar o recortar la palabra, previamente elimina todos
        los signos de puntuación que pueden aparecer. El stemmer utilizado también se
        encarga de eliminar acentos y convertir a minuscula, sino habria que hacerlo
        a mano
        """
        # \x97 es un guion. Al ejemplo agregue las comillas inglesas de apertura: «
        palabra = palabra.strip(string.punctuation + "«" + "»" + "\x97" + "¿" + "¡")

        palabra_lematizada = self._spanish_stemmer.stem(palabra)
        return palabra_lematizada

    def __generar_indice(self):
        """
        Genera los pares de la lista de pares (palabra, docID)
        """
        pares = []
        indice = {}
        for doc in self._docs:
            with open(doc, "r", encoding='utf-8') as documento:
                buffer = documento.read()
                lista_palabras = [palabra for palabra in buffer.split() if palabra not in self.stop_words]
                lista_palabras = [self.__lematizar_palabra(palabra) for palabra in lista_palabras]

            pares = pares + [(palabra, self._doc_to_docID[doc]) for palabra in lista_palabras]

        for par in pares:
            posting = indice.setdefault(par[0], set())
            posting.add(par[1])

        self._indice = indice

    def buscar(self, palabra):
        salida = []
        palabra_lematizada = self.__lematizar_palabra(palabra)
        if palabra_lematizada in self._indice:
            for docID in self._indice[palabra_lematizada]:
                salida.append(self._docID_to_doc[docID])
        return set(salida)


class ConsultaIndiceInvertido:
    def consultar(self, indice_invertido):
        """
        Realiza consultas al indice_invertido, en caso de consultar por una única palabra
        devuelve los documentos en los que aparece, y en en caso de consultar por varias palabras
        (separadas por blancos) busca alguna de las palabras (OR) y todas las palabras (AND)
        """
        while True:
            op = input("\nIntroduce tu búsqueda(Enter para finalizar):\n>>> ")
            if len(op) == 0: break
            busq = op.split()
            if len(busq) == 1:  # op es una sola palabra
                print(self.formatear_resultados(indice_invertido.buscar(busq[0])))
            elif len(busq) > 1:
                archivos_encontrados_or = indice_invertido.buscar(busq[0])
                archivos_encontrados_and = archivos_encontrados_or.copy()
                for palabra in busq:
                    nuevo_resultado = indice_invertido.buscar(palabra)
                    archivos_encontrados_or = archivos_encontrados_or | nuevo_resultado
                    archivos_encontrados_and = archivos_encontrados_and & nuevo_resultado
                print("\nDocumentos en donde aparece al menos una palabra buscada (OR):")
                print(self.formatear_resultados(archivos_encontrados_or))
                print("\nDocumentos en donde aparecen todas las palabras buscadas (AND):")
                print(self.formatear_resultados(archivos_encontrados_and))

    def formatear_resultados(self, archivos_encontrados):
        resultado = ''
        for archivo in archivos_encontrados:
            resultado = resultado + archivo + '\n'
        return resultado + '\n' + str(len(archivos_encontrados)) + ' documento(s) encontrado(s).'


if __name__ == "__main__":
    lista_docs = ["./archivos/Bombadil.txt",
                  "./archivos/Egidio.txt",
                  "./archivos/Introduccion.txt",
                  "./archivos/Niggle.txt",
                  "./archivos/Roverandom.txt",
                  "./archivos/Wootton.txt"]

    # Generar el indice invertido y una consulta
    ii_tolkien = IndiceInvertido(lista_docs)
    consulta_ii = ConsultaIndiceInvertido()

    # Ejecutar el menu
    consulta_ii.consultar(ii_tolkien)
