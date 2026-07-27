"""
PROYECTO LÓGICA: Katas de Python
---------------------------------
Solución a las 41 katas propuestas en el enunciado del proyecto.
Cada ejercicio incluye:
    - El enunciado original como comentario.
    - La función/clase que lo resuelve.
    - Comentarios explicando los pasos que puedan resultar más complejos.

Al final del archivo, dentro de `if __name__ == "__main__":`, se ejecutan
casos de uso / pruebas de cada ejercicio para comprobar que todo funciona.
"""

from functools import reduce
import math


# ============================================================
# 1. Diccionario con la frecuencia de cada letra de una cadena
# (sin contar los espacios).
# ============================================================
def frecuencia_letras(cadena):
    frecuencias = {}
    for letra in cadena:
        if letra == " ":
            continue  # ignoramos los espacios, tal y como pide el enunciado
        # .get(letra, 0) evita tener que comprobar "si la clave existe"
        frecuencias[letra] = frecuencias.get(letra, 0) + 1
    return frecuencias


# ============================================================
# 2. Dada una lista de números, devolver una nueva lista con el
# doble de cada valor. Usar map().
# ============================================================
def duplicar_lista(lista_numeros):
    return list(map(lambda x: x * 2, lista_numeros))


# ============================================================
# 3. Dada una lista de palabras y una palabra objetivo, devolver
# las palabras de la lista que contengan la palabra objetivo.
# ============================================================
def palabras_con_objetivo(lista_palabras, objetivo):
    return [palabra for palabra in lista_palabras if objetivo in palabra]


# ============================================================
# 4. Calcular la diferencia entre los valores de dos listas.
# Usar map().
# ============================================================
def diferencia_listas(lista1, lista2):
    # map() puede recibir varios iterables: itera ambas listas a la vez
    return list(map(lambda x, y: x - y, lista1, lista2))


# ============================================================
# 5. Media de una lista de números y estado ("aprobado"/"suspenso")
# respecto a una nota_aprobado (por defecto 5). Devuelve una tupla
# (media, estado).
# ============================================================
def calcular_media_estado(lista_numeros, nota_aprobado=5):
    media = sum(lista_numeros) / len(lista_numeros)
    estado = "aprobado" if media >= nota_aprobado else "suspenso"
    return (media, estado)


# ============================================================
# 6. Factorial de un número de manera recursiva.
# ============================================================
def factorial(n):
    # Caso base: 0! = 1! = 1
    if n in (0, 1):
        return 1
    return n * factorial(n - 1)


# ============================================================
# 7. Convertir una lista de tuplas a una lista de strings.
# Usar map().
# ============================================================
def tuplas_a_strings(lista_tuplas):
    return list(map(str, lista_tuplas))


# ============================================================
# 8. Pedir dos números al usuario e intentar dividirlos,
# manejando errores de valor no numérico y división por cero.
# ============================================================
def dividir_numeros():
    try:
        num1 = float(input("Introduce el primer número: "))
        num2 = float(input("Introduce el segundo número: "))
        resultado = num1 / num2
    except ValueError:
        print("División fallida: debes introducir valores numéricos.")
    except ZeroDivisionError:
        print("División fallida: no se puede dividir entre cero.")
    else:
        # El bloque else solo se ejecuta si NO hubo excepción
        print(f"División exitosa. Resultado: {resultado}")


# ============================================================
# 9. Excluir mascotas prohibidas en España de una lista de
# nombres de mascotas. Usar filter().
# ============================================================
def filtrar_mascotas_prohibidas(lista_mascotas):
    prohibidas = ["Mapache", "Tigre", "Serpiente Pitón", "Cocodrilo", "Oso"]
    return list(filter(lambda mascota: mascota not in prohibidas, lista_mascotas))


# ============================================================
# 10. Promedio de una lista de números. Si la lista está vacía,
# lanzar una excepción personalizada y manejarla.
# ============================================================
class ListaVaciaError(Exception):
    """Excepción personalizada para listas vacías."""
    pass


def calcular_promedio_seguro(lista_numeros):
    try:
        if len(lista_numeros) == 0:
            raise ListaVaciaError("No se puede calcular el promedio de una lista vacía.")
        return sum(lista_numeros) / len(lista_numeros)
    except ListaVaciaError as error:
        print(f"Error: {error}")
        return None


# ============================================================
# 11. Pedir la edad al usuario, manejando valores no numéricos
# o fuera del rango [0, 120].
# ============================================================
def pedir_edad():
    try:
        edad = int(input("Introduce tu edad: "))
        if edad < 0 or edad > 120:
            # Lanzamos una excepción "genérica" con un mensaje claro
            raise ValueError("La edad debe estar entre 0 y 120.")
    except ValueError as error:
        print(f"Error: entrada no válida ({error})")
    else:
        print(f"Tu edad es {edad} años.")


# ============================================================
# 12. Dada una frase, devolver una lista con la longitud de
# cada palabra. Usar map().
# ============================================================
def longitudes_palabras(frase):
    return list(map(len, frase.split()))


# ============================================================
# 13. Dado un conjunto de caracteres, devolver una lista de
# tuplas (mayúscula, minúscula) sin letras repetidas. Usar map().
# ============================================================
def mayus_minus(conjunto_caracteres):
    # set() ya elimina duplicados por definición
    letras_unicas = set(conjunto_caracteres)
    return list(map(lambda letra: (letra.upper(), letra.lower()), letras_unicas))


# ============================================================
# 14. Devolver las palabras de una lista que empiecen por una
# letra específica. Usar filter().
# ============================================================
def palabras_por_letra_inicial(lista_palabras, letra):
    return list(filter(lambda palabra: palabra.startswith(letra), lista_palabras))


# ============================================================
# 15. Función lambda que suma 3 a cada número de una lista.
# ============================================================
sumar_tres_a_lista = lambda lista: list(map(lambda x: x + 3, lista))


# ============================================================
# 16. Dado un texto y un número n, devolver las palabras cuya
# longitud sea mayor que n. Usar filter().
# ============================================================
def palabras_mas_largas_que(texto, n):
    return list(filter(lambda palabra: len(palabra) > n, texto.split()))


# ============================================================
# 17. Dada una lista de dígitos, devolver el número que forman.
# Ej: [5,7,2] -> 572. Usar reduce().
# ============================================================
def digitos_a_numero(lista_digitos):
    # En cada paso: acumulado = acumulado * 10 + siguiente_digito
    return reduce(lambda acumulado, digito: acumulado * 10 + digito, lista_digitos)


# ============================================================
# 18. Lista de diccionarios de estudiantes (nombre, edad,
# calificación). Extraer los que tienen calificación >= 90.
# Usar filter().
# ============================================================
def estudiantes_con_calificacion_alta(lista_estudiantes):
    return list(filter(lambda estudiante: estudiante["calificacion"] >= 90, lista_estudiantes))


# ============================================================
# 19. Función lambda que filtra los números impares de una
# lista dada.
# ============================================================
filtrar_impares = lambda lista: list(filter(lambda x: x % 2 != 0, lista))


# ============================================================
# 20. De una lista con elementos int y string, quedarse solo
# con los valores int. Usar filter().
# ============================================================
def filtrar_solo_enteros(lista_mixta):
    # Se usa type() en lugar de isinstance() para excluir explícitamente
    # los booleanos (que en Python son subclase de int)
    return list(filter(lambda elemento: type(elemento) == int, lista_mixta))


# ============================================================
# 21. Función lambda que calcula el cubo de un número.
# ============================================================
cubo = lambda x: x ** 3


# ============================================================
# 22. Producto total de los valores de una lista numérica.
# Usar reduce().
# ============================================================
def producto_lista(lista_numeros):
    return reduce(lambda acumulado, x: acumulado * x, lista_numeros)


# ============================================================
# 23. Concatenar una lista de palabras. Usar reduce().
# ============================================================
def concatenar_palabras(lista_palabras):
    return reduce(lambda acumulado, palabra: acumulado + " " + palabra, lista_palabras)


# ============================================================
# 24. Diferencia total entre los valores de una lista.
# Usar reduce().
# ============================================================
def diferencia_total(lista_numeros):
    return reduce(lambda acumulado, x: acumulado - x, lista_numeros)


# ============================================================
# 25. Contar el número de caracteres de una cadena de texto.
# ============================================================
def contar_caracteres(cadena):
    return len(cadena)


# ============================================================
# 26. Función lambda que calcula el resto de la división entre
# dos números.
# ============================================================
resto_division = lambda a, b: a % b


# ============================================================
# 27. Promedio de una lista de números (versión simple, sin
# manejo de excepciones; ver ejercicio 10 para la versión segura).
# ============================================================
def promedio(lista_numeros):
    return sum(lista_numeros) / len(lista_numeros)


# ============================================================
# 28. Buscar y devolver el primer elemento duplicado de una
# lista dada.
# ============================================================
def primer_duplicado(lista):
    vistos = set()
    for elemento in lista:
        if elemento in vistos:
            return elemento
        vistos.add(elemento)
    return None  # no había duplicados


# ============================================================
# 29. Convertir una variable en cadena de texto y enmascarar
# todos los caracteres con '#', excepto los últimos cuatro.
# ============================================================
def enmascarar_variable(variable):
    texto = str(variable)
    if len(texto) <= 4:
        # Si no hay más de 4 caracteres, no hay nada que enmascarar
        return texto
    parte_enmascarada = "#" * (len(texto) - 4)
    parte_visible = texto[-4:]
    return parte_enmascarada + parte_visible


# ============================================================
# 30. Determinar si dos palabras son anagramas.
# ============================================================
def son_anagramas(palabra1, palabra2):
    # Al ordenar las letras de cada palabra, dos anagramas producen
    # exactamente la misma secuencia de letras
    return sorted(palabra1.lower()) == sorted(palabra2.lower())


# ============================================================
# 31. Pedir una lista de nombres y luego un nombre a buscar.
# Si está, se imprime un mensaje; si no, se lanza una excepción.
# ============================================================
class NombreNoEncontradoError(Exception):
    """Excepción para cuando un nombre no aparece en la lista."""
    pass


def buscar_nombre_en_lista():
    entrada = input("Introduce una lista de nombres separados por comas: ")
    nombres = [nombre.strip() for nombre in entrada.split(",")]
    buscado = input("Introduce el nombre que quieres buscar: ").strip()
    try:
        if buscado not in nombres:
            raise NombreNoEncontradoError(f"'{buscado}' no se encuentra en la lista.")
        print(f"'{buscado}' fue encontrado en la lista.")
    except NombreNoEncontradoError as error:
        print(f"Error: {error}")


# ============================================================
# 32. Dado un nombre completo y una lista de empleados, buscar
# el nombre y devolver el puesto (o mensaje de que no trabaja
# aquí).
# ============================================================
def buscar_puesto_empleado(nombre_completo, lista_empleados):
    for empleado in lista_empleados:
        if empleado["nombre"] == nombre_completo:
            return empleado["puesto"]
    return f"{nombre_completo} no trabaja aquí."


# ============================================================
# 33. Función lambda que suma los elementos correspondientes
# de dos listas dadas.
# ============================================================
sumar_listas = lambda lista1, lista2: list(map(lambda x, y: x + y, lista1, lista2))


# ============================================================
# 34. Clase Arbol: representa un árbol genérico con tronco y
# ramas.
# ============================================================
class Arbol:
    def __init__(self):
        self.tronco = 1          # longitud inicial del tronco
        self.ramas = []          # lista de longitudes de ramas

    def crecer_tronco(self):
        self.tronco += 1

    def nueva_rama(self):
        self.ramas.append(1)  # cada rama nueva empieza con longitud 1

    def crecer_ramas(self):
        # Reconstruimos la lista sumando 1 a cada rama existente
        self.ramas = [longitud + 1 for longitud in self.ramas]

    def quitar_rama(self, posicion):
        # Comprobamos que la posición sea válida antes de eliminar
        if 0 <= posicion < len(self.ramas):
            self.ramas.pop(posicion)
        else:
            print(f"No existe ninguna rama en la posición {posicion}.")

    def info_arbol(self):
        return {
            "longitud_tronco": self.tronco,
            "numero_ramas": len(self.ramas),
            "longitudes_ramas": self.ramas,
        }


# ============================================================
# 36. Clase UsuarioBanco: representa un usuario de banco con
# nombre, saldo y si tiene cuenta corriente.
# ============================================================
class SaldoInsuficienteError(Exception):
    """Excepción para operaciones bancarias sin saldo suficiente."""
    pass


class UsuarioBanco:
    def __init__(self, nombre, saldo, cuenta_corriente):
        self.nombre = nombre
        self.saldo = saldo
        self.cuenta_corriente = cuenta_corriente  # True / False

    def retirar_dinero(self, cantidad):
        # Si el usuario NO tiene cuenta corriente, no puede quedarse
        # en negativo: el saldo debe alcanzar para cubrir la retirada.
        # Si SÍ tiene cuenta corriente, se le permite tener "descubierto"
        # (saldo negativo), que es precisamente la ventaja de este
        # tipo de cuenta.
        if not self.cuenta_corriente and cantidad > self.saldo:
            raise SaldoInsuficienteError(
                f"{self.nombre} no tiene saldo suficiente para retirar {cantidad}."
            )
        self.saldo -= cantidad

    def transferir_dinero(self, usuario_origen, cantidad):
        # Primero intentamos retirar del usuario origen; si falla,
        # la excepción se propaga y la transferencia no se completa
        usuario_origen.retirar_dinero(cantidad)
        self.saldo += cantidad

    def agregar_dinero(self, cantidad):
        self.saldo += cantidad


# ============================================================
# 37. procesar_texto: procesa un texto según la opción indicada
# (contar_palabras, reemplazar_palabras, eliminar_palabra).
# ============================================================
def contar_palabras(texto):
    conteo = {}
    for palabra in texto.split():
        conteo[palabra] = conteo.get(palabra, 0) + 1
    return conteo


def reemplazar_palabras(texto, palabra_original, palabra_nueva):
    return texto.replace(palabra_original, palabra_nueva)


def eliminar_palabra(texto, palabra):
    palabras = texto.split()
    palabras_filtradas = [p for p in palabras if p != palabra]
    return " ".join(palabras_filtradas)


def procesar_texto(texto, opcion, *args):
    # *args permite pasar un número variable de argumentos según la opción:
    # - "reemplazar" necesita 2 args (palabra_original, palabra_nueva)
    # - "eliminar" necesita 1 arg (palabra)
    # - "contar" no necesita argumentos adicionales
    if opcion == "contar":
        return contar_palabras(texto)
    elif opcion == "reemplazar":
        return reemplazar_palabras(texto, *args)
    elif opcion == "eliminar":
        return eliminar_palabra(texto, *args)
    else:
        return "Opción no reconocida. Usa 'contar', 'reemplazar' o 'eliminar'."


# ============================================================
# 38. Indicar si es de noche, de día o de tarde según la hora.
# ============================================================
def periodo_del_dia():
    hora = int(input("Introduce la hora (0-23): "))
    if 6 <= hora < 12:
        print("Es de día.")
    elif 12 <= hora < 20:
        print("Es de tarde.")
    else:
        print("Es de noche.")


# ============================================================
# 39. Calificación en texto según calificación numérica.
# ============================================================
def calificacion_en_texto(nota):
    if 0 <= nota <= 69:
        return "insuficiente"
    elif 70 <= nota <= 79:
        return "bien"
    elif 80 <= nota <= 89:
        return "muy bien"
    elif 90 <= nota <= 100:
        return "excelente"
    else:
        return "nota fuera de rango (0-100)"


# ============================================================
# 40. Calcular el área de una figura ("rectangulo", "circulo",
# "triangulo") a partir de una tupla de datos.
# ============================================================
def calcular_area(figura, datos):
    if figura == "rectangulo":
        base, altura = datos
        return base * altura
    elif figura == "circulo":
        radio = datos[0]
        return math.pi * radio ** 2
    elif figura == "triangulo":
        base, altura = datos
        return (base * altura) / 2
    else:
        return "Figura no reconocida. Usa 'rectangulo', 'circulo' o 'triangulo'."


# ============================================================
# 41. Calcular el monto final de una compra aplicando un
# descuento (cupón) si el usuario lo tiene.
# ============================================================
def calcular_precio_final_compra():
    precio_original = float(input("Introduce el precio original del artículo: "))
    tiene_cupon = input("¿Tienes un cupón de descuento? (si/no): ").strip().lower()

    if tiene_cupon == "si":
        descuento = float(input("Introduce el valor del cupón de descuento: "))
        if descuento > 0:
            precio_final = precio_original - descuento
        else:
            # Cupón no válido (0 o negativo): no se aplica descuento
            print("El valor del cupón no es válido, no se aplicará descuento.")
            precio_final = precio_original
    elif tiene_cupon == "no":
        precio_final = precio_original
    else:
        print("Respuesta no reconocida, no se aplicará ningún descuento.")
        precio_final = precio_original

    print(f"Precio final de la compra: {precio_final}€")


# ============================================================
# CASOS DE USO / PRUEBAS
# ============================================================
if __name__ == "__main__":

    print("--- 1. Frecuencia de letras ---")
    print(frecuencia_letras("hola mundo"))

    print("\n--- 2. Duplicar lista (map) ---")
    print(duplicar_lista([1, 2, 3, 4]))

    print("\n--- 3. Palabras que contienen objetivo ---")
    print(palabras_con_objetivo(["casa", "casita", "perro", "gato"], "cas"))

    print("\n--- 4. Diferencia entre listas (map) ---")
    print(diferencia_listas([10, 20, 30], [1, 2, 3]))

    print("\n--- 5. Media y estado (aprobado/suspenso) ---")
    print(calcular_media_estado([4, 6, 8]))
    print(calcular_media_estado([4, 6, 8], nota_aprobado=7))

    print("\n--- 6. Factorial recursivo ---")
    print(factorial(5))

    print("\n--- 7. Tuplas a strings (map) ---")
    print(tuplas_a_strings([(1, 2), (3, 4)]))

    # print("\n--- 8. División con manejo de excepciones ---")
    # dividir_numeros()  # Descomentar para probar de forma interactiva

    print("\n--- 9. Filtrar mascotas prohibidas (filter) ---")
    print(filtrar_mascotas_prohibidas(["Perro", "Gato", "Tigre", "Oso", "Canario"]))

    print("\n--- 10. Promedio seguro con excepción personalizada ---")
    print(calcular_promedio_seguro([1, 2, 3]))
    print(calcular_promedio_seguro([]))

    # print("\n--- 11. Pedir edad con manejo de excepciones ---")
    # pedir_edad()  # Descomentar para probar de forma interactiva

    print("\n--- 12. Longitudes de palabras (map) ---")
    print(longitudes_palabras("el sol brilla hoy"))

    print("\n--- 13. Mayúsculas/minúsculas sin repetir (map) ---")
    print(mayus_minus("aabbc"))

    print("\n--- 14. Palabras por letra inicial (filter) ---")
    print(palabras_por_letra_inicial(["casa", "coche", "perro", "cielo"], "c"))

    print("\n--- 15. Lambda sumar 3 ---")
    print(sumar_tres_a_lista([1, 2, 3]))

    print("\n--- 16. Palabras más largas que n (filter) ---")
    print(palabras_mas_largas_que("el gato negro salta muy alto", 4))

    print("\n--- 17. Dígitos a número (reduce) ---")
    print(digitos_a_numero([5, 7, 2]))

    print("\n--- 18. Estudiantes con calificación alta (filter) ---")
    estudiantes = [
        {"nombre": "Ana", "edad": 20, "calificacion": 95},
        {"nombre": "Luis", "edad": 22, "calificacion": 70},
        {"nombre": "Marta", "edad": 21, "calificacion": 91},
    ]
    print(estudiantes_con_calificacion_alta(estudiantes))

    print("\n--- 19. Lambda filtrar impares ---")
    print(filtrar_impares([1, 2, 3, 4, 5, 6]))

    print("\n--- 20. Filtrar solo enteros (filter) ---")
    print(filtrar_solo_enteros([1, "hola", 2, "mundo", 3]))

    print("\n--- 21. Lambda cubo ---")
    print(cubo(3))

    print("\n--- 22. Producto total (reduce) ---")
    print(producto_lista([1, 2, 3, 4]))

    print("\n--- 23. Concatenar palabras (reduce) ---")
    print(concatenar_palabras(["Hola", "mundo", "cruel"]))

    print("\n--- 24. Diferencia total (reduce) ---")
    print(diferencia_total([10, 2, 3]))

    print("\n--- 25. Contar caracteres ---")
    print(contar_caracteres("hola mundo"))

    print("\n--- 26. Lambda resto de división ---")
    print(resto_division(10, 3))

    print("\n--- 27. Promedio simple ---")
    print(promedio([2, 4, 6]))

    print("\n--- 28. Primer duplicado ---")
    print(primer_duplicado([1, 2, 3, 2, 4]))

    print("\n--- 29. Enmascarar variable ---")
    print(enmascarar_variable("123456789"))
    print(enmascarar_variable(1234))

    print("\n--- 30. Anagramas ---")
    print(son_anagramas("roma", "amor"))
    print(son_anagramas("hola", "adios"))

    # print("\n--- 31. Buscar nombre en lista ---")
    # buscar_nombre_en_lista()  # Descomentar para probar de forma interactiva

    print("\n--- 32. Buscar puesto de empleado ---")
    empleados = [
        {"nombre": "Juan Pérez", "puesto": "Desarrollador"},
        {"nombre": "Ana López", "puesto": "Diseñadora"},
    ]
    print(buscar_puesto_empleado("Juan Pérez", empleados))
    print(buscar_puesto_empleado("Pedro Gómez", empleados))

    print("\n--- 33. Lambda sumar listas ---")
    print(sumar_listas([1, 2, 3], [10, 20, 30]))

    print("\n--- 34. Clase Arbol ---")
    mi_arbol = Arbol()
    mi_arbol.crecer_tronco()
    mi_arbol.nueva_rama()
    mi_arbol.crecer_ramas()
    mi_arbol.nueva_rama()
    mi_arbol.nueva_rama()
    mi_arbol.quitar_rama(2)
    print(mi_arbol.info_arbol())

    print("\n--- 36. Clase UsuarioBanco ---")
    alicia = UsuarioBanco("Alicia", 100, True)
    bob = UsuarioBanco("Bob", 50, True)
    bob.agregar_dinero(20)
    alicia.transferir_dinero(bob, 80)
    alicia.retirar_dinero(50)
    print(f"Saldo de Alicia: {alicia.saldo}")
    print(f"Saldo de Bob: {bob.saldo}")

    print("\n--- 37. Procesar texto ---")
    texto_ejemplo = "el perro corre el gato duerme el perro ladra"
    print(procesar_texto(texto_ejemplo, "contar"))
    print(procesar_texto(texto_ejemplo, "reemplazar", "perro", "lobo"))
    print(procesar_texto(texto_ejemplo, "eliminar", "gato"))

    # print("\n--- 38. Periodo del día ---")
    # periodo_del_dia()  # Descomentar para probar de forma interactiva

    print("\n--- 39. Calificación en texto ---")
    print(calificacion_en_texto(95))
    print(calificacion_en_texto(72))

    print("\n--- 40. Calcular área de figuras ---")
    print(calcular_area("rectangulo", (4, 5)))
    print(calcular_area("circulo", (3,)))
    print(calcular_area("triangulo", (6, 4)))

    # print("\n--- 41. Precio final de compra ---")
    # calcular_precio_final_compra()  # Descomentar para probar de forma interactiva
