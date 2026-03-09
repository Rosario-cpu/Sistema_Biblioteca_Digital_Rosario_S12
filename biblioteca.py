# Tarea: Sistema de Gestión de Biblioteca Digital
# Estudiante: Rosario
# Universidad Estatal Amazónica

class Libro:
    def __init__(self, titulo, autor, categoria, isbn):
        # REQUISITO: Usar una tupla para autor y título (inmutables)
        self.datos_inmutables = (titulo, autor)
        self.categoria = categoria
        self.isbn = isbn

    def __str__(self):
        return f"'{self.datos_inmutables[0]}' de {self.datos_inmutables[1]} (Categoría: {self.categoria})"

class Usuario:
    def __init__(self, nombre, user_id):
        self.nombre = nombre
        self.user_id = user_id
        # REQUISITO: Lista para gestionar libros prestados
        self.libros_prestados = []

    def __str__(self):
        return f"Usuario: {self.nombre} (ID: {self.user_id})"

class Biblioteca:
    def __init__(self):
        # REQUISITO: Diccionario para libros (clave: ISBN)
        self.libros = {}
        # REQUISITO: Conjunto para IDs de usuario únicos
        self.ids_usuarios = set()
        self.usuarios = {}

    # FUNCIONALIDAD: Añadir/quitar libros
    def añadir_libro(self, libro):
        self.libros[libro.isbn] = libro
        print(f"[CATÁLOGO] Libro añadido: {libro}")

    def quitar_libro(self, isbn):
        if isbn in self.libros:
            eliminado = self.libros.pop(isbn)
            print(f"[CATÁLOGO] Libro eliminado: {eliminado.datos_inmutables[0]}")
        else:
            print("[ERROR] El libro no existe en el catálogo.")

    # FUNCIONALIDAD: Registrar/dar de baja usuarios
    def registrar_usuario(self, usuario):
        if usuario.user_id not in self.ids_usuarios:
            self.ids_usuarios.add(usuario.user_id)
            self.usuarios[usuario.user_id] = usuario
            print(f"[SISTEMA] Usuario registrado: {usuario.nombre}")
        else:
            print("[ERROR] El ID de usuario ya está en uso.")

    def baja_usuario(self, user_id):
        if user_id in self.usuarios:
            del self.usuarios[user_id]
            self.ids_usuarios.remove(user_id)
            print(f"[SISTEMA] Usuario con ID {user_id} dado de baja.")
        else:
            print("[ERROR] Usuario no encontrado.")

    # FUNCIONALIDAD: Prestar/devolver libros
    def prestar_libro(self, isbn, user_id):
        if isbn in self.libros and user_id in self.usuarios:
            libro = self.libros.pop(isbn)
            self.usuarios[user_id].libros_prestados.append(libro)
            print(f"[PRÉSTAMO] '{libro.datos_inmutables[0]}' prestado a {self.usuarios[user_id].nombre}")
        else:
            print("[ERROR] No se pudo realizar el préstamo.")

    def devolver_libro(self, isbn, user_id):
        if user_id in self.usuarios:
            usuario = self.usuarios[user_id]
            for i, libro in enumerate(usuario.libros_prestados):
                if libro.isbn == isbn:
                    libro_devuelto = usuario.libros_prestados.pop(i)
                    self.libros[isbn] = libro_devuelto
                    print(f"[DEVOLUCIÓN] '{libro_devuelto.datos_inmutables[0]}' regresó a la biblioteca.")
                    return
        print("[ERROR] No se encontró el préstamo.")

    # FUNCIONALIDAD: Buscar libros
    def buscar_libros(self, busqueda):
        print(f"\n--- Resultados para '{busqueda}' ---")
        encontrados = [l for l in self.libros.values() if
                      busqueda.lower() in l.datos_inmutables[0].lower() or
                      busqueda.lower() in l.datos_inmutables[1].lower() or
                      busqueda.lower() in l.categoria.lower()]
        for l in encontrados: print(f"Encontrado: {l}")

    # FUNCIONALIDAD: Listar libros prestados
    def listar_prestados(self, user_id):
        if user_id in self.usuarios:
            u = self.usuarios[user_id]
            print(f"\nLibros de {u.nombre}:")
            if not u.libros_prestados: print("No tiene libros actualmente.")
            for l in u.libros_prestados: print(f"- {l}")

# --- PRUEBAS DEL SISTEMA (Lo que el licenciado quiere ver) ---
if __name__ == "__main__":
    biblioteca_uea = Biblioteca()

    # 1. Creamos algunos libros
    l1 = Libro("Python Essentials", "Cisco", "Programación", "101")
    l2 = Libro("Cálculo Stewart", "James Stewart", "Ciencia", "102")
    l3 = Libro("Redes Locales", "Pacho8", "TI", "103")

    # 2. Añadimos libros
    biblioteca_uea.añadir_libro(l1)
    biblioteca_uea.añadir_libro(l2)
    biblioteca_uea.añadir_libro(l3)

    # 3. Registramos usuarios
    u1 = Usuario("Rosario", "R2026")
    biblioteca_uea.registrar_usuario(u1)

    # 4. Operación de Préstamo
    biblioteca_uea.prestar_libro("101", "R2026")
    biblioteca_uea.prestar_libro("103", "R2026")

    # 5. Listar libros de Rosario
    biblioteca_uea.listar_prestados("R2026")

    # 6. Búsqueda en el catálogo
    biblioteca_uea.buscar_libros("Ciencia")

    # 7. Operación de Devolución
    biblioteca_uea.devolver_libro("101", "R2026")

    # 8. Quitar un libro y dar de baja usuario
    biblioteca_uea.quitar_libro("102")
    biblioteca_uea.baja_usuario("R2026")

