import random   # Importa el módulo random para seleccionar palabras aleatorias

# Función para cargar categorías y palabras desde un archivo
def categorias(menu):
    archivo = open("proyecto_final/palabras.txt", "r")   # Abre el archivo de palabras en modo lectura
    lineas = archivo.readlines()                         # Lee todas las líneas del archivo

    categorias = {}               # Diccionario que almacenará las categorías con sus listas de palabras
    categoria_actual = ""         # Variable temporal para saber en qué categoría estamos

    for linea in lineas:          # Recorre cada línea del archivo
        linea = linea.strip()     # Elimina espacios y saltos de línea

        if linea.startswith("categoria:"):   # Si la línea define una categoría nueva...
            categoria_actual = linea.split("categoria:")[1].strip()  # Extrae el nombre de categoría
            categorias[categoria_actual] = []    # Crea la lista vacía para esa categoría

        elif linea:               # Si la línea no está vacía, debe contener palabras
            palabras = [palabra.strip() for palabra in linea.split(",")]  # Separa palabras por comas
            categorias[categoria_actual].extend(palabras)  # Agrega las palabras a la categoría correspondiente

    archivo.close()               # Cierra el archivo
    return categorias             # Retorna el diccionario de categorías y palabras


# Función que carga el ranking desde archivo
def cargar_ranking():
    """
    Carga el ranking desde proyecto_final/ranking.txt y lo devuelve como dict.
    """
    jugadores = {}   # Diccionario con formato {apodo: {'puntos': int, 'victorias': int}}

    try:
        with open("proyecto_final/ranking.txt", "r") as archivo:   # Abre ranking en modo lectura
            for linea in archivo:          # Recorre cada línea
                linea = linea.strip()      # Limpia espacios
                if not linea:              # Si la línea está vacía, se salta
                    continue

                # Intenta el formato apodo,puntos,victorias
                if "," in linea:
                    partes = [p.strip() for p in linea.split(",")]  # Separa por coma

                    if len(partes) == 3:     # Formato nuevo válido
                        apodo = partes[0]
                        puntos = int(partes[1]) if partes[1].isdigit() else 0
                        victorias = int(partes[2]) if partes[2].isdigit() else 0

                    elif len(partes) == 2 and partes[1] in ("victoria", "derrota"):
                        # Formato antiguo tipo apodo,victoria
                        apodo = partes[0]
                        puntos = 0
                        victorias = 1 if partes[1] == "victoria" else 0
                    else:
                        continue   # Si el formato es raro, se ignora la línea

                elif ":" in linea:
                    # Formato más antiguo apodo: puntos
                    apodo, pts = [p.strip() for p in linea.split(":", 1)]
                    puntos = int(pts) if pts.isdigit() else 0
                    victorias = 0

                else:
                    continue  # Si no coincide ninguno, se descarta

                # Acumula datos si el jugador ya existe
                if apodo in jugadores:
                    jugadores[apodo]['puntos'] += puntos
                    jugadores[apodo]['victorias'] += victorias
                else:
                    jugadores[apodo] = {'puntos': puntos, 'victorias': victorias}

    except FileNotFoundError:
        pass    # Si no existe archivo, se retorna diccionario vacío

    return jugadores


# Función que guarda el ranking actualizado
def guardar_ranking(jugadores):
    with open("proyecto_final/ranking.txt", "w") as archivo:   # Abre archivo en modo escritura
        for apodo, datos in jugadores.items():                 # Recorre los jugadores
            archivo.write(f"{apodo},{datos['puntos']},{datos['victorias']}\n")  # Escribe línea por jugador


# Función para registrar el resultado de una partida
def registrar_resultado(alias, puntos, victoria):
    jugadores = cargar_ranking()    # Carga el ranking actual

    if alias not in jugadores:      # Si el alias es nuevo, se inicializa
        jugadores[alias] = {'puntos': 0, 'victorias': 0}

    jugadores[alias]['puntos'] += int(puntos)    # Suma puntos logrados

    if victoria:                    # Si ganó, suma una victoria
        jugadores[alias]['victorias'] += 1

    guardar_ranking(jugadores)      # Guarda el ranking actualizado


# Carga categorías desde el archivo
categorias = categorias("proyecto_final/palabras.txt")


# --- PROCESO PRINCIPAL DEL JUEGO ---
while True:

    alias = input("Ingresa tu alias (o 'salir' para terminar): ").strip()  # Nombre del jugador
    if alias.lower() == 'salir':                                           # Si escribe salir, termina
        print("Gracias por jugar. ¡Hasta luego!")
        break

    puntaje = 0      # Puntaje inicial del jugador

    # Selección de categoría
    categoria_elegida = input(f"Elige una categoria {list(categorias.keys())}: ").strip().lower()

    while categoria_elegida not in categorias:   # Validación de categoría
        categoria_elegida = input(f"Categoria no valida. Elige una categoria {list(categorias.keys())}: ").strip().lower()

    palabra_elegida = random.choice(categorias[categoria_elegida])  # Selecciona una palabra aleatoria
    print(f"Categoria elegida: {categoria_elegida}")

    letras_adivinadas = []   # Lista de letras que el jugador ha dicho
    intentos = 6             # Intentos del ahorcado

    while intentos > 0:
        # Construye la palabra mostrando letras adivinadas y guiones bajos
        palabra_mostrada = ''.join([letra if letra in letras_adivinadas else '_' for letra in palabra_elegida])

        print(f"Palabra: {palabra_mostrada}")
        print(f"Intentos restantes: {intentos}")

        letra = input("Adivina una letra: ").lower()   # Pide una letra

        if letra in letras_adivinadas:                 # Si ya la dijo, se avisa
            print("Ya has adivinado esa letra. Intenta con otra.")
            continue

        letras_adivinadas.append(letra)                # Agrega la letra a la lista

        if letra not in palabra_elegida:               # Si la letra es incorrecta...
            intentos -= 1                              # Pierde un intento
            print("Letra incorrecta.")

            # Dibujos ASCII del ahorcado según intentos restantes
            if intentos == 5:
                print(" ####### \n #     #\n #     #\n #     # \n ####### ")

            elif intentos == 4:
                print(" ####### \n #     #\n #     #\n #     # \n ####### ")
                print("    #    \n    #    \n    #    \n    #    \n    #    ")

            elif intentos == 3:
                print(" ####### \n #     #\n #     #\n #     # \n ####### ")
                print("    #    \n  # #    \n #  #    \n#   #    \n    #    ")

            elif intentos == 2:
                print(" ####### \n #     #\n #     #\n #     # \n ####### ")
                print("    #    \n  # # #   \n #  #  #  \n#   #    #\n    #    ")

            elif intentos == 1:
                print(" ####### \n #     #\n #     #\n #     # \n ####### ")
                print("    #    \n  # # #   \n #  #  #  \n#   #    #\n    #    ")
                print("   #     \n  #     \n #     \n#     \n   ")
                print("¡Cuidado! Te queda un intento.")

            elif intentos == 0:
                print(" ####### \n #     #\n #     #\n #     # \n ####### ")
                print("    #    \n  # # #   \n #  #  #  \n#   #    #\n    #    ")
                print("   #  #     \n  #     #    \n #       #   \n ")
                print("¡Has sido ahorcado!")

        # Si ya adivinó todas las letras
        if all(letra in letras_adivinadas for letra in palabra_elegida):
            print(f"¡Felicidades! Has adivinado la palabra: {palabra_elegida}")

            puntaje += intentos * 10         # Calcula puntaje según intentos restantes
            print(f"Tu puntaje actual es: {puntaje}")

            registrar_resultado(alias, puntaje, True)   # Registra victoria y puntaje
            break   # Termina la partida

    else:
        # Se ejecuta si while termina sin break → perdió
        print(f"Has perdido. La palabra era: {palabra_elegida}")
        registrar_resultado(alias, 0, False)   # Registra derrota

