from conjunto import Conjunto


# Crear un conjunto vacio
def test001():
    conjunto = Conjunto()

    assert conjunto.conjunto == []


# Crear un conjunto en base a una lista de elementos
def test002():
    lista = [1, 2, 3]
    conjunto = Conjunto(lista)

    assert conjunto.conjunto == [1, 2, 3]


# Agregar un elemento a si mismo
def test003():
    conjunto = Conjunto([1, 2, 3])
    conjunto.agregar_elemento(4)

    assert conjunto.conjunto == [1, 2, 3, 4]


# Agregar un elemento que ya existe
def test004():
    conjunto = Conjunto([1, 2, 3])
    conjunto.agregar_elemento(1)

    assert conjunto.conjunto == [1, 2, 3]


# Remover un elemento que existe
def test005():
    conjunto = Conjunto([1, 2, 3, 4])
    conjunto.remover_elemento(4)

    assert conjunto.conjunto == [1, 2, 3]


# Remover un elemento que no existe
def test006():
    conjunto = Conjunto([1, 2, 3, 4])
    conjunto.remover_elemento(5)

    assert conjunto.conjunto == [1, 2, 3, 4]


# Comparar dos conjuntos identicos
def test007():
    conjunto_a = Conjunto([1, 2, 3])
    conjunto_b = Conjunto([1, 2, 3])

    assert conjunto_a.conjunto == conjunto_b.conjunto


# Comparar dos conjuntos con los mismos elementos pero desordenados
def test008():
    conjunto_a = Conjunto([1, 2, 3])
    conjunto_b = Conjunto([2, 1, 3])

    assert conjunto_a == conjunto_b


# Union de dos conjuntos
def test009():
    conjunto_a = Conjunto([1, 2, 3])
    conjunto_b = Conjunto([3, 4, 5])
    conjunto_c = conjunto_a.union(conjunto_b)

    assert conjunto_c.conjunto == [1, 2, 3, 4, 5]


# Interseccion de dos conjuntos
def test010():
    conjunto_a = Conjunto([1, 2, 3])
    conjunto_b = Conjunto([3, 4, 5])
    conjunto_c = conjunto_a.interseccion(conjunto_b)

    assert conjunto_c.conjunto == [3]


# Diferencia de dos conjuntos
def test011():
    conjunto_a = Conjunto([1, 2, 3])
    conjunto_b = Conjunto([3, 4, 5])
    conjunto_c = conjunto_a.diferencia(conjunto_b)

    assert conjunto_c.conjunto == [1, 2]


# Diferencia simetrica entre dos conjuntos
def test012():
    conjunto_a = Conjunto([1, 2, 3])
    conjunto_b = Conjunto([3, 4, 5])
    conjunto_c = conjunto_a.diferencia_simetrica(conjunto_b)

    assert conjunto_c.conjunto == [1, 2, 4, 5]


# Producto cartesiano entre dos conjuntos
def test013():
    conjunto_a = Conjunto([1, 2, 3])
    conjunto_b = Conjunto([3, 4, 5])
    conjunto_c = conjunto_a.producto_cartesiano(conjunto_b)

    assert conjunto_c.conjunto == [(1, 3), (1, 4), (1, 5),
                                   (2, 3), (2, 4), (2, 5),
                                   (3, 3), (3, 4), (3, 5)]