class Conjunto:
    def __init__(self, conjunto=None):
        # Como el atributo es mutable, si se crea sin parametro crear una *nueva* lista vacia
        if conjunto is None:
            conjunto = []
        self.conjunto = conjunto

    def __str__(self):
        # Devuelve una cadena de texto para no mostrar la direccion de memoria
        return str(self.conjunto.copy())

    def __eq__(self, other):
        # Si las dos listas ordenadas son iguales, los conjuntos son iguales
        a = sorted(self.conjunto.copy())
        b = sorted(other.conjunto.copy())
        return a == b

    def agregar_elemento(self, elemento):
        if not self.contiene_elemento(elemento):
            self.conjunto.append(elemento)
            return 'Agregado'
        return 'No agregado'

    def remover_elemento(self, elemento):
        if self.contiene_elemento(elemento):
            self.conjunto.remove(elemento)
            return 'Removido'
        return 'No removido'

    def contiene_elemento(self, elemento):
        return elemento in self.conjunto

    def union(self, conjunto):
        # Union: Los elementos que pertenecen a A y B
        buffer = Conjunto(self.conjunto.copy())
        for x in conjunto.conjunto:
            buffer.agregar_elemento(x)
        return buffer

    def interseccion(self, conjunto):
        # Interseccion: Los elementos que pertenecen simultaneamente a A y B
        buffer = Conjunto()
        for x in conjunto.conjunto:
            if self.contiene_elemento(x):
                buffer.agregar_elemento(x)
        return buffer

    def diferencia(self, conjunto):
        # Diferencia: Los elementos de A sin los elementos de B
        buffer = Conjunto(self.conjunto.copy())
        for x in conjunto.conjunto:
            if self.contiene_elemento(x):
                buffer.remover_elemento(x)
        return buffer

    def diferencia_simetrica(self, conjunto):
        # Diferencia Simetrica: Los elementos de A y B menos los elementos comunes a ambos
        buffer = Conjunto(self.conjunto.copy())
        for x in conjunto.conjunto:
            if not self.contiene_elemento(x):
                buffer.agregar_elemento(x)
            else:
                buffer.remover_elemento(x)
        return buffer

    def producto_cartesiano(self, conjunto):
        # Producto Cartesiano: Pares con elementos de A en la primera posicion y de B en la segunda
        buffer = Conjunto()
        for x in self.conjunto:
            for y in conjunto.conjunto:
                buffer.agregar_elemento((x, y))
        return buffer


if __name__ == '__main__':
    # Crear Conjuntos
    A = Conjunto([1, 2, 3])
    B = Conjunto([3, 4, 5])
    C = Conjunto([1, 3, 2])
    D = Conjunto()

    # Probar Clase y Metodos
    print('\n----- Pruebas sobre Conjuntos:',
        '\nContenido del conjunto D: ', D,
        '\n',
        '\nAgregar elemento 1 a D:   ', D.agregar_elemento(1),
        '\nAgregar elemento 2 a D:   ', D.agregar_elemento(2),
        '\nAgregar elemento 1 a D:   ', D.agregar_elemento(1),
        '\nContenido del conjunto D: ', D,
        '\n',
        '\nRemover elemento 1 de D:  ', D.remover_elemento(1),
        '\nRemover elemento 3 de D:  ', D.remover_elemento(3),
        '\nContenido del conjunto D: ', D,
        )

    print('\n----- Operaciones entre conjuntos:',
        '\nConjunto A:               ', A,
        '\nConjunto B:               ', B,
        '\nConjunto C:               ', C,
        '\nConjunto D:               ', D,
        '\n',
        '\n¿A es igual a A?          ', A == A,
        '\n¿A es igual a B?          ', A == B,
        '\n¿A es igual a C?          ', A == C,
        '\n¿A es igual a D?          ', A == D,
        '\n',
        '\nA Union B:                ', A.union(B),
        '\nA Interseccion B:         ', A.interseccion(B),
        '\nA Diferencia B:           ', A.diferencia(B),
        '\nB Diferencia A:           ', B.diferencia(A),
        '\nA Diferencia simetrica B: ', A.diferencia_simetrica(B),
        '\nA Producto cartesiano B:  ', A.producto_cartesiano(B),
        '\nB Producto cartesiano A:  ', B.producto_cartesiano(A)
        )
