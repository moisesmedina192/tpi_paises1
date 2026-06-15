import csv
import unicodedata
ARCHIVO_CSV = "paises.csv"

def quitar_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

def cargar_paises():
    paises = []

    try:
        with open(ARCHIVO_CSV, "r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            for fila in lector:
                paises.append({
                    "nombre": fila["nombre"],
                    "poblacion": int(fila["poblacion"]),
                    "superficie": int(fila["superficie"]),
                    "continente": fila["continente"]
                })

    except FileNotFoundError:
        print("No se encontró el archivo CSV. Se iniciará una lista vacía.")

    except Exception as e:
        print("Error al leer CSV:", e)

    print("Cantidad de países cargados:", len(paises))
    return paises
def guardar_paises(paises):
    campos = ["nombre", "poblacion", "superficie", "continente"]

    with open(ARCHIVO_CSV, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()

        for pais in paises:
            escritor.writerow(pais)


def mostrar_paises(lista):
    if not lista:
        print("No hay resultados.")
        return

    for pais in lista:
        print("-" * 40)
        print("Nombre:", pais["nombre"])
        print("Población:", pais["poblacion"])
        print("Superficie:", pais["superficie"], "km²")
        print("Continente:", pais["continente"])


def agregar_pais(paises):
    nombre = input("Nombre: ").strip()

    if nombre == "":
        print("El nombre no puede estar vacío.")
        return

    for pais in paises:
        if pais["nombre"].lower() == nombre.lower():
            print("Ese país ya existe.")
            return

    try:
        poblacion = int(input("Población: "))
        superficie = int(input("Superficie km²: "))
    except ValueError:
        print("Debe ingresar números válidos.")
        return

    continente = input("Continente: ").strip()

    if continente == "":
        print("El continente no puede estar vacío.")
        return

    paises.append({
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    })

    print("País agregado correctamente.")


def actualizar_pais(paises):
    nombre = input("Ingrese país a actualizar: ").strip()

    for pais in paises:
        if pais["nombre"].lower() == nombre.lower():
            try:
                pais["poblacion"] = int(input("Nueva población: "))
                pais["superficie"] = int(input("Nueva superficie: "))
                print("Datos actualizados.")
            except ValueError:
                print("Valores inválidos.")
            return

    print("País no encontrado.")


def buscar_pais(paises):
    texto = quitar_acentos(
        input("Ingrese nombre a buscar: ").lower()
    )

    for pais in paises:
        print(pais["nombre"])

    resultados = []

    for pais in paises:
        nombre = quitar_acentos(
            pais["nombre"].lower()
        )

        if texto in nombre:
            resultados.append(pais)

    mostrar_paises(resultados)

def filtrar_continente(paises):
    continente = input("Continente: ").lower()

    resultados = []

    for pais in paises:
        if pais["continente"].lower() == continente:
            resultados.append(pais)

    mostrar_paises(resultados)


def filtrar_poblacion(paises):
    try:
        minimo = int(input("Población mínima: "))
        maximo = int(input("Población máxima: "))
    except ValueError:
        print("Valores inválidos.")
        return

    resultados = []

    for pais in paises:
        if minimo <= pais["poblacion"] <= maximo:
            resultados.append(pais)

    mostrar_paises(resultados)


def filtrar_superficie(paises):
    try:
        minimo = int(input("Superficie mínima: "))
        maximo = int(input("Superficie máxima: "))
    except ValueError:
        print("Valores inválidos.")
        return

    resultados = []

    for pais in paises:
        if minimo <= pais["superficie"] <= maximo:
            resultados.append(pais)

    mostrar_paises(resultados)


def ordenar_paises(paises):
    print("1. Nombre")
    print("2. Población")
    print("3. Superficie")

    opcion = input("Opción: ")
    orden = input("Ascendente (A) o Descendente (D): ").upper()

    reverse = orden == "D"

    if opcion == "1":
        resultado = sorted(paises, key=lambda x: x["nombre"], reverse=reverse)
    elif opcion == "2":
        resultado = sorted(paises, key=lambda x: x["poblacion"], reverse=reverse)
    elif opcion == "3":
        resultado = sorted(paises, key=lambda x: x["superficie"], reverse=reverse)
    else:
        print("Opción inválida.")
        return

    mostrar_paises(resultado)


def mostrar_estadisticas(paises):
    if not paises:
        print("No hay datos.")
        return

    mayor = max(paises, key=lambda x: x["poblacion"])
    menor = min(paises, key=lambda x: x["poblacion"])

    promedio_poblacion = sum(p["poblacion"] for p in paises) / len(paises)
    promedio_superficie = sum(p["superficie"] for p in paises) / len(paises)

    continentes = {}

    for pais in paises:
        cont = pais["continente"]
        continentes[cont] = continentes.get(cont, 0) + 1

    print("\nESTADÍSTICAS")
    print("Mayor población:", mayor["nombre"], "-", mayor["poblacion"])
    print("Menor población:", menor["nombre"], "-", menor["poblacion"])
    print("Promedio población:", round(promedio_poblacion, 2))
    print("Promedio superficie:", round(promedio_superficie, 2))

    print("\nCantidad de países por continente")
    for cont, cantidad in continentes.items():
        print(cont, ":", cantidad)


def menu():
    print("\n===== GESTIÓN DE PAÍSES =====")
    print("1. Agregar país")
    print("2. Actualizar país")
    print("3. Buscar país")
    print("4. Filtrar por continente")
    print("5. Filtrar por población")
    print("6. Filtrar por superficie")
    print("7. Ordenar países")
    print("8. Mostrar estadísticas")
    print("9. Mostrar todos")
    print("0. Salir")


def main():
    paises = cargar_paises()

    while True:
        menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_pais(paises)

        elif opcion == "2":
            actualizar_pais(paises)

        elif opcion == "3":
            buscar_pais(paises)

        elif opcion == "4":
            filtrar_continente(paises)

        elif opcion == "5":
            filtrar_poblacion(paises)

        elif opcion == "6":
            filtrar_superficie(paises)

        elif opcion == "7":
            ordenar_paises(paises)

        elif opcion == "8":
            mostrar_estadisticas(paises)

        elif opcion == "9":
            mostrar_paises(paises)

        elif opcion == "0":
            guardar_paises(paises)
            print("Programa finalizado.")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()