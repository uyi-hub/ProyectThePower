# PROYECTO LÓGICA: Katas de Python

Este repositorio contiene la resolución del proyecto **"Katas de Python"**, cuyo objetivo es afianzar los conocimientos adquiridos en el módulo de Python mediante la resolución de 41 katas (ejercicios prácticos) de dificultad progresiva.

## 📂 Estructura del repositorio

```
├── katas_python.py   # Todas las katas resueltas, comentadas y con casos de uso
└── README.md          # Este archivo
```

## 🧠 ¿Qué es una Kata?

Una kata es un ejercicio práctico de programación diseñado para mejorar las habilidades de un desarrollador mediante la repetición y el perfeccionamiento de técnicas de codificación. Cada kata plantea un problema concreto que hay que resolver aplicando los conocimientos del módulo.

## ✅ Conocimientos demostrados

A lo largo de las 41 katas se ponen en práctica:

- **Tipos de datos básicos y funciones incorporadas**: strings, listas, tuplas, diccionarios, sets, `len()`, `sorted()`, `sum()`, etc.
- **Estructuras de datos y sus métodos**: manipulación de listas, diccionarios y conjuntos (`.get()`, `.append()`, `.pop()`, `.split()`, `.join()`, `.startswith()`...).
- **Condicionales**: `if` / `elif` / `else` para lógica de negocio (calificaciones, franjas horarias, descuentos, áreas de figuras...).
- **Estructuras de iteración**: bucles `for` y comprensiones de listas.
- **Funciones**: funciones con parámetros por defecto (`*args`), funciones recursivas (factorial), funciones de orden superior (`map`, `filter`, `reduce`) y funciones `lambda`.
- **Programación orientada a objetos**: clases `Arbol` y `UsuarioBanco`, con atributos, métodos y manejo de excepciones personalizadas dentro de los métodos.
- **Manejo de excepciones**: excepciones estándar (`ValueError`, `ZeroDivisionError`) y excepciones personalizadas (`ListaVaciaError`, `NombreNoEncontradoError`, `SaldoInsuficienteError`).
- **Módulos**: uso de `functools.reduce` y `math`.
- **Buenas prácticas**: nombres descriptivos, comentarios explicando los pasos más complejos, separación clara entre lógica y casos de prueba (`if __name__ == "__main__":`).

## 🚀 Pasos seguidos durante el proyecto

1. **Lectura y análisis del enunciado**: se revisaron los 41 ejercicios agrupándolos mentalmente por bloque temático (funciones de orden superior, POO, condicionales, excepciones...).
2. **Resolución kata a kata**: cada ejercicio se resolvió en una función (o clase) independiente, encabezada por un comentario con el enunciado literal, tal y como exige el proyecto.
3. **Comentarios explicativos**: se añadieron comentarios en los pasos que requerían más razonamiento (por ejemplo, el uso de `reduce` para construir un número a partir de dígitos, o la decisión de que `cuenta_corriente` permita descubierto en `UsuarioBanco`).
4. **Casos de uso / pruebas**: al final del archivo, dentro de un bloque `if __name__ == "__main__":`, se ejecutan ejemplos de cada función para comprobar que el comportamiento es el esperado. Los ejercicios que requieren `input()` del usuario (8, 11, 31, 38, 41) se han dejado comentados en la sección de pruebas para no bloquear la ejecución automática del script, pero pueden descomentarse para probarlos de forma interactiva.
5. **Verificación**: se ejecutó el script completo para comprobar que no había errores y que las salidas eran coherentes con lo esperado.
6. **Uso de IA**: se ha utilizado una herramienta de IA como apoyo puntual (revisión de sintaxis, sugerencias de estructura), siguiendo la recomendación del enunciado de usarla con moderación y entendiendo cada paso del código resultante.

## ▶️ Cómo ejecutar el proyecto

```bash
python3 katas_python.py
```

Esto imprimirá por consola el resultado de cada uno de los casos de uso definidos para las katas no interactivas. Para probar las katas que piden datos por teclado (8, 11, 31, 38, 41), basta con descomentar la línea correspondiente dentro del bloque `if __name__ == "__main__":`.

## 📌 Nota sobre la Kata 36 (UsuarioBanco)

El caso de uso de la clase `UsuarioBanco` transfiere 80€ desde "Bob" (que solo tiene 70€ tras agregarle 20€) hacia "Alicia". Para que esta operación tenga sentido, se ha interpretado que el atributo `cuenta_corriente` determina si un usuario puede quedarse en **descubierto** (saldo negativo): si `cuenta_corriente = True`, se le permite; si es `False`, se lanza `SaldoInsuficienteError` al intentar retirar más dinero del que tiene.
