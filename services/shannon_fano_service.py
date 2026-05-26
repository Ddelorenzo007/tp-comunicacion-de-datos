from collections import Counter


def calcular_frecuencias(texto):
    total = len(texto)
    contador = Counter(texto)

    simbolos = []

    for simbolo, cantidad in contador.items():
        simbolos.append({
            "simbolo": simbolo,
            "cantidad": cantidad,
            "frecuencia": cantidad / total,
            "codigo": ""
        })

    simbolos.sort(key=lambda item: item["cantidad"], reverse=True)

    return simbolos


def dividir_lista(simbolos):
    total = sum(item["cantidad"] for item in simbolos)
    acumulado = 0
    mejor_indice = 1
    menor_diferencia = total

    for i in range(1, len(simbolos)):
        acumulado = sum(item["cantidad"] for item in simbolos[:i])
        resto = total - acumulado
        diferencia = abs(acumulado - resto)

        if diferencia < menor_diferencia:
            menor_diferencia = diferencia
            mejor_indice = i

    return mejor_indice


def generar_codigos_shannon_fano(simbolos):
    if len(simbolos) <= 1:
        if len(simbolos) == 1 and simbolos[0]["codigo"] == "":
            simbolos[0]["codigo"] = "0"
        return

    indice = dividir_lista(simbolos)

    grupo_izquierdo = simbolos[:indice]
    grupo_derecho = simbolos[indice:]

    for item in grupo_izquierdo:
        item["codigo"] += "0"

    for item in grupo_derecho:
        item["codigo"] += "1"

    generar_codigos_shannon_fano(grupo_izquierdo)
    generar_codigos_shannon_fano(grupo_derecho)


def codificar_texto(texto, codigos):
    return "".join(codigos[caracter] for caracter in texto)


def decodificar_shannon_fano(cadena, codigos):
    codigos_invertidos = {codigo: simbolo for simbolo, codigo in codigos.items()}

    resultado = ""
    acumulador = ""

    for bit in cadena:
        acumulador += bit

        if acumulador in codigos_invertidos:
            resultado += codigos_invertidos[acumulador]
            acumulador = ""

    return resultado


def calcular_metricas(texto, codigos, simbolos, texto_codificado):
    longitud_original = len(texto) * 8
    longitud_codificada = len(texto_codificado)

    longitud_promedio = 0

    for item in simbolos:
        probabilidad = item["frecuencia"]
        longitud_codigo = len(codigos[item["simbolo"]])
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


def procesar_shannon_fano(texto):
    simbolos = calcular_frecuencias(texto)
    generar_codigos_shannon_fano(simbolos)

    codigos = {
        item["simbolo"]: item["codigo"]
        for item in simbolos
    }

    texto_codificado = codificar_texto(texto, codigos)
    metricas = calcular_metricas(texto, codigos, simbolos, texto_codificado)

    tabla = []

    for item in simbolos:
        tabla.append({
            "simbolo": item["simbolo"],
            "cantidad": item["cantidad"],
            "frecuencia": round(item["frecuencia"], 3),
            "codigo": item["codigo"],
            "longitud": len(item["codigo"])
        })

    tabla.sort(key=lambda item: item["simbolo"])

    return {
        "codigos": codigos,
        "tabla": tabla,
        "texto_codificado": texto_codificado,
        "metricas": metricas
    }