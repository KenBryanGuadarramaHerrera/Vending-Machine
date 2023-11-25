import datetime

class MaquinaExpendedora:
    def __init__(self):
        # Contraseña para el modo de soporte
        self.contrasena_soporte = "123"

        # Definir productos y sus precios
        self.productos = {
            1: {"nombre": "Galletas", "precio": 1.50},
            2: {"nombre": "Refresco", "precio": 2.00},
            3: {"nombre": "Chocolate", "precio": 1.75},
            4: {"nombre": "Agua", "precio": 1.00},
            5: {"nombre": "Papas", "precio": 1.25},
            6: {"nombre": "Barra de cereal", "precio": 1.80},
            7: {"nombre": "Jugo", "precio": 2.50},
            8: {"nombre": "Frutas", "precio": 2.20},
            9: {"nombre": "Yogurt", "precio": 1.90},
            10: {"nombre": "Sándwich", "precio": 3.00},
        }

        # Cargar inventario desde un archivo (considerando que inicialmente hay 10 unidades de cada producto)
        self.inventario = self.cargar_inventario("inventario.txt")

    def cargar_inventario(self, nombre_archivo):
        try:
            with open(nombre_archivo, "r") as archivo:
                # Inicialmente, consideramos que hay 10 unidades de cada producto en el inventario
                return {int(codigo): int(cantidad) for linea in archivo.readlines() for codigo, cantidad in [linea.strip().split(":")]}
        except FileNotFoundError:
            # Si el archivo no existe, creamos un inventario inicial
            return {codigo: 10 for codigo in self.productos}

    def guardar_inventario(self, inventario, nombre_archivo):
        with open(nombre_archivo, "w") as archivo:
            for codigo, cantidad in inventario.items():
                archivo.write(f"{codigo}:{cantidad}\n")

    def mostrar_menu(self):
        print("===== Máquina Expendedora =====")
        print("Productos disponibles:")
        for codigo, producto in self.productos.items():
            print(f"{codigo}. {producto['nombre']} - ${producto['precio']:.2f}")
        print("===============================")

    def comprar_producto(self):
        self.mostrar_menu()

        # Solicitar al usuario que elija un producto
        while True:
            try:
                seleccion = int(input("Seleccione un producto (1-10): "))
                if seleccion in self.productos:
                    break
                else:
                    print("Opción no válida. Inténtelo de nuevo.")
            except ValueError:
                print("Por favor, ingrese un número válido.")

        producto_seleccionado = self.productos[seleccion]

        # Verificar si hay suficiente inventario
        if self.inventario[seleccion] <= 0:
            print(f"Lo siento, el producto {producto_seleccionado['nombre']} está agotado. No se puede comprar.")
            return

        # Solicitar al usuario que ingrese dinero
        while True:
            try:
                cantidad_pesos = float(input(f"Ingrese ${producto_seleccionado['precio']:.2f} en pesos mexicanos: "))
                if cantidad_pesos >= producto_seleccionado['precio']:
                    break
                else:
                    print("Dinero insuficiente. Inténtelo de nuevo.")
            except ValueError:
                print("Por favor, ingrese una cantidad válida.")

        # Calcular el cambio
        cambio_pesos = cantidad_pesos - producto_seleccionado['precio']
        cambio_pesos = round(cambio_pesos, 2)

        print(f"\nCompra exitosa. ¡Disfruta de tu {producto_seleccionado['nombre']}!")
        if cambio_pesos > 0:
            print(f"Tu cambio: ${cambio_pesos:.2f} en pesos mexicanos")

        # Registrar la compra en el historial
        self.registrar_historial(producto_seleccionado)

        # Actualizar el inventario
        self.actualizar_inventario(seleccion)

    def mostrar_inventario(self):
        # Mostrar el inventario actual
        print("\nInventario actual:")
        for codigo, cantidad in self.inventario.items():
            producto = self.productos[codigo]
            print(f"{producto['nombre']}: {cantidad} unidades")

    def mostrar_historial(self):
        # Mostrar el historial de compras
        print("\nHistorial de compras:")
        with open("historial.txt", "r") as archivo:
            for linea in archivo.readlines():
                print(linea.strip())

    def registrar_historial(self, producto):
        # Registrar la compra en el historial
        with open("historial.txt", "a") as archivo:
            archivo.write(f"{producto['nombre']}, Precio: ${producto['precio']:.2f}, "
                           f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    def actualizar_inventario(self, seleccion):
        # Actualizar el inventario
        self.inventario[seleccion] -= 1

        # Guardar el inventario actualizado en el archivo
        self.guardar_inventario(self.inventario, "inventario.txt")

    def surtir_inventario(self):
        # Solicitar la contraseña al soporte
        contrasena_ingresada = input("Ingrese la contraseña de soporte: ")
        if contrasena_ingresada != self.contrasena_soporte:
            print("Contraseña incorrecta. Modo de soporte no autorizado.")
            return

        # Permitir a soporte surtir el inventario
        while True:
            print("\n===== Modo Soporte =====")
            print("Opciones:")
            print("1. Mostrar Inventario")
            print("2. Mostrar Historial de Compras")
            print("3. Surtir Inventario")
            print("0. Salir")

            # Solicitar al soporte que elija una opción
            opcion = input("Seleccione una opción: ")

            if opcion == "0":
                print("Saliendo del Modo Soporte.")
                break
            elif opcion == "1":
                self.mostrar_inventario()
            elif opcion == "2":
                self.mostrar_historial()
            elif opcion == "3":
                self.surtir_opcion()
            else:
                print("Opción no válida. Inténtelo de nuevo.")

    def surtir_opcion(self):
        # Solicitar al soporte que elija un producto para surtir
        while True:
            self.mostrar_menu()

            try:
                seleccion = int(input("Seleccione un producto para surtir (1-10) o ingrese 0 para terminar: "))
                if seleccion == 0:
                    break
                elif seleccion in self.productos:
                    cantidad_surtir = int(input("Ingrese la cantidad a surtir: "))
                    if cantidad_surtir >= 0:
                        # Surtir el inventario
                        self.inventario[seleccion] += cantidad_surtir

                        print(f"\nSe surtieron {cantidad_surtir} unidades de {self.productos[seleccion]['nombre']}.")

                        # Guardar el inventario actualizado en el archivo
                        self.guardar_inventario(self.inventario, "inventario.txt")
                    else:
                        print("La cantidad a surtir debe ser mayor o igual a 0. Inténtelo de nuevo.")
                else:
                    print("Opción no válida. Inténtelo de nuevo.")
            except ValueError:
                print("Por favor, ingrese un número válido.")

if __name__ == "__main__":
    maquina = MaquinaExpendedora()

    # Preguntar si es cliente o soporte
    while True:
        modo = input("¿Eres un cliente o soporte? (cliente/soporte): ")
        if modo.lower() == "cliente":
            maquina.comprar_producto()
            break
        elif modo.lower() == "soporte":
            maquina.surtir_inventario()
            break
        else:
            print("Modo no válido. Por favor, ingresa 'cliente' o 'soporte'.")
