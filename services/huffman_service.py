import heapq
from collections import Counter


class NodoHuffman:
    def __init__(self, simbolo, frecuencia):
        self.simbolo = simbolo
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia


def calcular_frecuencias(texto):
    total = len(texto)
    contador = Counter(texto)

    return {
        simbolo: {
            "cantidad": cantidad,
            "frecuencia": cantidad / total
        }
        for simbolo, cantidad in contador.items()
    }


def construir_arbol_huffman(frecuencias):
    heap = []

    for simbolo, datos in frecuencias.items():
        nodo = NodoHuffman(simbolo, datos["cantidad"])
        heapq.heappush(heap, nodo)

    if len(heap) == 1:
        unico = heapq.heappop(heap)
        padre = NodoHuffman(None, unico.frecuencia)
        padre.izquierda = unico
        return padre

    while len(heap) > 1:
        nodo1 = heapq.heappop(heap)
        nodo2 = heapq.heappop(heap)

        padre = NodoHuffman(None, nodo1.frecuencia + nodo2.frecuencia)
        padre.izquierda = nodo1
        padre.derecha = nodo2

        heapq.heappush(heap, padre)

    return heap[0]


def generar_codigos(nodo, codigo_actual="", codigos=None):
    if codigos is None:
        codigos = {}

    if nodo is None:
        return codigos

    if nodo.simbolo is not None:
        codigos[nodo.simbolo] = codigo_actual or "0"
        return codigos

    generar_codigos(nodo.izquierda, codigo_actual + "0", codigos)
    generar_codigos(nodo.derecha, codigo_actual + "1", codigos)

    return codigos


def codificar_texto(texto, codigos):
    return "".join(codigos[caracter] for caracter in texto)


def decodificar_huffman(cadena, codigos):
    codigos_invertidos = {codigo: simbolo for simbolo, codigo in codigos.items()}

    resultado = ""
    acumulador = ""

    for bit in cadena:
        acumulador += bit

        if acumulador in codigos_invertidos:
            resultado += codigos_invertidos[acumulador]
            acumulador = ""

    return resultado


def calcular_metricas(texto, codigos, frecuencias, texto_codificado):
    longitud_original = len(texto) * 8
    longitud_codificada = len(texto_codificado)

    longitud_promedio = 0

    for simbolo, datos in frecuencias.items():
        probabilidad = datos["frecuencia"]
        longitud_codigo = len(codigos[simbolo])
        longitud_promedio += probabilidad * longitud_codigo

    tasa_compresion = 0

    if longitud_original > 0:
        tasa_compresion = (1 - (longitud_codificada / longitud_original)) * 100

    return {
        "longitud_original_bits": longitud_original,
        "longitud_codificada_bits": longitud_codificada,
        "longitud_promedio": round(longitud_promedio, 3),
        "tasa_compresion": round(tasa_compresion, 2)
    }


def procesar_huffman(texto):
    frecuencias = calcular_frecuencias(texto)
    arbol = construir_arbol_huffman(frecuencias)
    codigos = generar_codigos(arbol)

    texto_codificado = codificar_texto(texto, codigos)
    metricas = calcular_metricas(texto, codigos, frecuencias, texto_codificado)

    tabla = []

    for simbolo, datos in frecuencias.items():
        tabla.append({
            "simbolo": simbolo,
            "cantidad": datos["cantidad"],
            "frecuencia": round(datos["frecuencia"], 3),
            "codigo": codigos[simbolo],
            "longitud": len(codigos[simbolo])
        })

    tabla.sort(key=lambda item: item["simbolo"])

    return {
        "frecuencias": frecuencias,
        "codigos": codigos,
        "tabla": tabla,
        "texto_codificado": texto_codificado,
        "metricas": metricas
    }