const inputTexto = document.getElementById("inputTexto");
const btnCodificar = document.getElementById("btnCodificar");
const btnLimpiar = document.getElementById("btnLimpiar");
const mensajeCodificacion = document.getElementById("mensajeCodificacion");

const tablaSimbolos = document.getElementById("tablaSimbolos");

const huffmanOriginal = document.getElementById("huffmanOriginal");
const huffmanCodificado = document.getElementById("huffmanCodificado");
const huffmanPromedio = document.getElementById("huffmanPromedio");
const huffmanTasa = document.getElementById("huffmanTasa");

const shannonOriginal = document.getElementById("shannonOriginal");
const shannonCodificado = document.getElementById("shannonCodificado");
const shannonPromedio = document.getElementById("shannonPromedio");
const shannonTasa = document.getElementById("shannonTasa");

const textoHuffman = document.getElementById("textoHuffman");
const textoShannon = document.getElementById("textoShannon");

const btnDecodificarHuffman = document.getElementById("btnDecodificarHuffman");
const btnDecodificarShannon = document.getElementById("btnDecodificarShannon");

const resultadoDecodificacion = document.getElementById("resultadoDecodificacion");

const graficoCodigos = document.getElementById("graficoCodigos");

let chartCodigos = null;
let codigosHuffman = {};
let codigosShannon = {};

btnCodificar.addEventListener("click", async () => {
    mensajeCodificacion.textContent = "";
    resultadoDecodificacion.textContent = "-";

    const texto = inputTexto.value;

    if (!texto.trim()) {
        mensajeCodificacion.textContent = "Tenés que ingresar un texto.";
        return;
    }

    try {
        btnCodificar.disabled = true;
        btnCodificar.textContent = "Codificando...";

        const respuesta = await fetch("/api/codificar", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ texto })
        });

        const datos = await respuesta.json();

        if (!respuesta.ok) {
            mensajeCodificacion.textContent = datos.error || "Ocurrió un error.";
            return;
        }

        mostrarResultados(datos);

    } catch (error) {
        mensajeCodificacion.textContent = "No se pudo codificar el texto.";
        console.error(error);
    } finally {
        btnCodificar.disabled = false;
        btnCodificar.textContent = "Codificar";
    }
});

btnLimpiar.addEventListener("click", () => {
    inputTexto.value = "";
    tablaSimbolos.innerHTML = "";
    textoHuffman.value = "";
    textoShannon.value = "";
    resultadoDecodificacion.textContent = "-";
    mensajeCodificacion.textContent = "";

    if (chartCodigos !== null) {
        chartCodigos.destroy();
        chartCodigos = null;
    }
});

function mostrarResultados(datos) {
    const huffman = datos.huffman;
    const shannon = datos.shannon_fano;

    codigosHuffman = huffman.codigos;
    codigosShannon = shannon.codigos;

    huffmanOriginal.textContent = huffman.metricas.longitud_original_bits;
    huffmanCodificado.textContent = huffman.metricas.longitud_codificada_bits;
    huffmanPromedio.textContent = huffman.metricas.longitud_promedio;
    huffmanTasa.textContent = huffman.metricas.tasa_compresion;

    shannonOriginal.textContent = shannon.metricas.longitud_original_bits;
    shannonCodificado.textContent = shannon.metricas.longitud_codificada_bits;
    shannonPromedio.textContent = shannon.metricas.longitud_promedio;
    shannonTasa.textContent = shannon.metricas.tasa_compresion;

    textoHuffman.value = huffman.texto_codificado;
    textoShannon.value = shannon.texto_codificado;

    construirTabla(huffman.tabla, shannon.tabla);
    construirGrafico(huffman.tabla, shannon.tabla);
}

function construirTabla(tablaHuffman, tablaShannon) {
    tablaSimbolos.innerHTML = "";

    tablaHuffman.forEach(itemHuffman => {
        const itemShannon = tablaShannon.find(
            item => item.simbolo === itemHuffman.simbolo
        );

        const fila = document.createElement("tr");

        fila.innerHTML = `
            <td>${mostrarSimbolo(itemHuffman.simbolo)}</td>
            <td>${itemHuffman.cantidad}</td>
            <td>${itemHuffman.frecuencia}</td>
            <td>${itemHuffman.codigo}</td>
            <td>${itemShannon ? itemShannon.codigo : "-"}</td>
        `;

        tablaSimbolos.appendChild(fila);
    });
}

function mostrarSimbolo(simbolo) {
    if (simbolo === " ") {
        return "[espacio]";
    }

    if (simbolo === "\n") {
        return "[salto]";
    }

    return simbolo;
}

btnDecodificarHuffman.addEventListener("click", async () => {
    await decodificar("/api/decodificar-huffman", textoHuffman.value, codigosHuffman);
});

btnDecodificarShannon.addEventListener("click", async () => {
    await decodificar("/api/decodificar-shannon", textoShannon.value, codigosShannon);
});

async function decodificar(url, cadena, codigos) {
    try {
        const respuesta = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ cadena, codigos })
        });

        const datos = await respuesta.json();

        if (!respuesta.ok) {
            resultadoDecodificacion.textContent = datos.error || "Error al decodificar.";
            return;
        }

        resultadoDecodificacion.textContent = datos.texto;

    } catch (error) {
        resultadoDecodificacion.textContent = "No se pudo decodificar.";
        console.error(error);
    }
}

function construirGrafico(tablaHuffman, tablaShannon) {
    const simbolos = tablaHuffman.map(item => mostrarSimbolo(item.simbolo));

    const longitudesHuffman = tablaHuffman.map(item => item.longitud);

    const longitudesShannon = tablaHuffman.map(itemHuffman => {
        const itemShannon = tablaShannon.find(
            item => item.simbolo === itemHuffman.simbolo
        );

        return itemShannon ? itemShannon.longitud : 0;
    });

    if (chartCodigos !== null) {
        chartCodigos.destroy();
    }

    chartCodigos = new Chart(graficoCodigos, {
        type: "bar",
        data: {
            labels: simbolos,
            datasets: [
                {
                    label: "Longitud Huffman",
                    data: longitudesHuffman
                },
                {
                    label: "Longitud Shannon-Fano",
                    data: longitudesShannon
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: "Comparación de longitud de códigos por símbolo"
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    },
                    title: {
                        display: true,
                        text: "Longitud en bits"
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: "Símbolos"
                    }
                }
            }
        }
    });
}