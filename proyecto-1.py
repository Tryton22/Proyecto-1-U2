# Proyecto Número 1 de la Unidad 2 /Programación 1/ Matías Fonseca, Claudio Larosa
import json
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

def open_file():
    """Se abre el archivo JSON creado para este proyecto"""
    try:
        with open("libreria.json", 'r') as archivo:
            data = json.load(archivo)
    except IOError:
        data = []
    return data

def save_file(data):
    """Guarda los datos ingresados en el archivo JSON"""
    with open("libreria.json", 'w') as archivo:
        json.dump(data, archivo, indent=4)

class Ventana_inicio():
    def __init__(self):

        builder = Gtk.Builder()
        builder.add_from_file("proyecto-1.ui")
        
        # Configuración ventana de inicio.
        self.ventana = builder.get_object("1inicio")
        self.ventana.set_default_size(1080, 600)
        self.ventana.set_title("Biblioteca BookWorm")
        self.ventana.connect("destroy", Gtk.main_quit)

        # Configuramos los botones del inicio.
        # Botón ventana bibliotecario.
        bton1 = builder.get_object("cario")
        bton1.connect("clicked", self.abrir_cario)
        bton1.set_label("Bibliotecario")

        # Botón ventana usuario.
        bton2 = builder.get_object("usuario")
        bton2.connect("clicked", self.abrir_usuario)
        bton2.set_label("Usuario")

        # Botón para salir.
        bton3 = builder.get_object("salir")
        bton3.connect("clicked", self.cerrar)
        # bton3.set_label("Salir")
    
        self.ventana.show_all()

    # Funcion que te cierra la ventana.
    def cerrar(self, btn=None):
        Gtk.main_quit()

    # Funcion que te abre las funciones del Bibliotecario.
    def abrir_cario(self, btn=None):
        ventana_dialogo_1 = Ventana_dialogo_inicio()
        ventana_dialogo_1.dialogo_inicio.run() 
        # print("Hice click!!")
        # print(response)

        
    # Funcion que te lleva a las funciones del Usuario.
    def abrir_usuario(self, btn=None):
        # print("Hice click!!")
        ventana_usuario_dialogo = Ventana_usuario_inicio()
        ventana_usuario_dialogo.dialogo_3.run()


class Ventana_dialogo_inicio():

    def __init__(self):

        builder = Gtk.Builder()
        builder.add_from_file("proyecto-1.ui")

        # Se nombra la ventana de dialogo del inicio.
        self.dialogo_inicio = builder.get_object("dialogo_1")
        self.dialogo_inicio.set_title("Biblioteca Bookworm")

        # Configuramos los botones de esta ventana de dialogo.
        # Botón para ir a la ventana del Bibliotecario.
        btn = builder.get_object("aceptar")
        btn.connect("clicked", self.bibliotecario)
        btn.set_label("Aceptar")

        # Botón para cerrar.
        btn1 = builder.get_object("sali")
        btn1.connect("clicked", self.cerrar_1)
        #btn1.set_label("Salir")

        # Configuramos la entrada de esta ventana de dialogo.
        self.password = builder.get_object("contra")
        self.password.connect("activate", self.bibliotecario)

        # Contraseña para ingresar a la ventana del Bibliotecario.
        self.contraseña = "Chuleta"

    # Funcion que cierra la ventana de dialogo.
    def cerrar_1(self, btn=None):
        self.dialogo_inicio.destroy()

    # Funcion que me abre la interfaz del Bibliotecario.
    def bibliotecario(self, enter=None):
        if self.password.get_text() == self.contraseña:
            # print("Correcto!!!!")
            ventana_bibliotecario = Ventana_bibliotecario()
            self.dialogo_inicio.destroy()
        else:
            # print(ingresado)
            print("Se ha equivocado de contraseña")

class Ventana_bibliotecario():

    def __init__(self):

        builder = Gtk.Builder()
        builder.add_from_file("proyecto-1.ui")

        # Configuramos la ventana de interfaz del Bibliotecario.
        ventana1 = builder.get_object("2cario")
        ventana1.set_default_size(1000, 800)
        ventana1.set_title("Biblioteca BookWorm, Modo Privado")
        ventana1.close()

        # Configuramos un Tree para que contenga los datos de los libros.
        self.tree = builder.get_object("libros")
        self.modelo = Gtk.ListStore(str, str, str, str)
        self.tree.set_model(model=self.modelo)
        
        nombre_columnas = ("Código", "Nombre", "Autor", "Estado")
        cell = Gtk.CellRendererText()
        for item in range(len(nombre_columnas)):
            column = Gtk.TreeViewColumn(nombre_columnas[item],
                                        cell,
                                        text=item)
            self.tree.append_column(column)
        
        # self.modelo.append(["1", "2", "3", "4"])
        # Se cargan los datos en la interfaz
        self.load_data_from_json()

        # Configuramos los botones de la interfaz.
        # Botón para agregar libros.
        buton_agregar = builder.get_object("more")
        buton_agregar.set_label("Agregar Libro")
        buton_agregar.connect("clicked", self.abre_dialogo2)

        # Boton para eliminar libros seleccionados.
        buton_eliminar = builder.get_object("delete")
        buton_eliminar.set_label("Eliminar Libro")
        buton_eliminar.connect("clicked", self.delete_select_data)

        ventana1.show_all()

    # Cargar los datos del JSON creado para su manipulación en la ventana.
    def load_data_from_json(self):
        datos = open_file()

        for item in datos:
            line = [x for x in item.values()]
            # print(line)
            self.modelo.append(line)
    
    # Abre la ventana de dialogo para ingresar los datos.
    def abre_dialogo2(self, btn=None):
        ventana_dialogo_2 = Dialogo_bibliotecario()
        response = ventana_dialogo_2.dialogo_2.run()

        if response == Gtk.ResponseType.OK:
            self.delete_all_data()
            self.load_data_from_json()
        elif response == Gtk.ResponseType.CANCEL:
            # print("Cancelar")
            pass

        ventana_dialogo_2.dialogo_2.destroy()
    
    # Se elimina el contenido del tree para su actualización.
    def delete_all_data(self):
        for index in range(len(self.modelo)):
            iter_ = self.modelo.get_iter(0)
            self.modelo.remove(iter_)
    
    # Se elimina el libro seleccionados.
    def delete_select_data(self, btn=None):
        model, it = self.tree.get_selection().get_selected()
        # Por si no se seleccionada nada.
        if model is None or it is None:
            print("Seleccione un libro.")
            return
            
        data = open_file()
        for item in data:
            if item['codigo'] == model.get_value(it, 0):
                data.remove(item)
        save_file(data)

        self.delete_all_data()
        self.load_data_from_json()

class Dialogo_bibliotecario:

    def __init__(self):
        
        builder = Gtk.Builder()
        builder.add_from_file("proyecto-1.ui")

        self.dialogo_2 = builder.get_object("dialogo_2")
        self.dialogo_2.set_title("Biblioteca BookWorm")

        # Configuración del boton "Aceptar" de esta ventana.
        butonOK = builder.get_object("OK")
        butonOK.connect("clicked", self.butonOK_clicked)

        # Configuración los cuadros de texto.
        self.codigo = builder.get_object("entry_codigo")
        self.nombre = builder.get_object("entry_nombre")
        self.autor = builder.get_object("entry_autor")

        self.dialogo_2.show_all()

    # Se ingresan los datos y se agrega el nuevo libro a la lista mostrada en pantalla y al JSON.
    def butonOK_clicked(self, btn=None):
        codigo = self.codigo.get_text()
        nombre = self.nombre.get_text()
        autor = self.autor.get_text()

        data = open_file()
        new_data = {"codigo": codigo,
                    "nombre": nombre,
                    "autor": autor,
                    "estado": "Disponible"}
        data.append(new_data)
        save_file(data)

class Ventana_usuario_inicio():

    def __init__(self):

        builder = Gtk.Builder()
        builder.add_from_file("proyecto-1.ui")

        self.dialogo_3 = builder.get_object("dialogo_3")
        self.dialogo_3.set_title("Biblioteca BookWorm")

        # Configuramos los botones de esta ventana.
        # Boton para ir a la interfaz del Usuario.
        boton_si = builder.get_object("si")
        boton_si.set_label("Aceptar")
        boton_si.connect("clicked", self.usuario)

        # Boton para cerrar ventana.
        boton_no = builder.get_object("no")
        #boton_no.set_label("Salir")
        boton_no.connect("clicked", self.cerrado)

        # Configuramos las entradas de texto de esta ventana.
        self.nombre = builder.get_object("name")
        self.nombre.connect("activate", self.usuario)
        self.dias = builder.get_object("day")
        self.dias.connect("activate", self.usuario)

        # El máximo y el mínimo de días que se puede pedir un libro.
        self.max = "30"
        self.min = "1"

        self.dialogo_3.show_all()

    # Funcion que cierra la ventana.
    def cerrado(self, btn=None):
        self.dialogo_3.destroy()

    # Funcion que me abre la interfaz de Usuario.    
    def usuario(self, enter=None): 
        if self.min <= self.dias.get_text() < self.max:
            #print("hola mundo")
            # Variables ingresadas en la ventana anterior.
            self.dias = self.dias.get_text()
            self.nombre = self.nombre.get_text()

            # Se abre la ventana del Usuario
            self.ventana_usuario = Ventana_usuario()
            
            # Se pide un libro.
            self.ventana_usuario.boton_pedir.connect("clicked", self.pedir_libro)

            # Se deja un libro.
            self.ventana_usuario.boton_devolver.connect("clicked", self.dejar_libro)

            self.dialogo_3.destroy()
        else:
            print("Ingrese un número permitido.")

    # Funcion que te pide un libro escogido con los días y el nombre ingresados.
    def pedir_libro(self, btn=None):
        model, it = self.ventana_usuario.tree.get_selection().get_selected()
        # Si no se selecciona nada.
        if model is None or it is None:
            return

        # Se dan los valores para cambiarlos en los datos.
        data = open_file()
        data_1 = {"codigo": model.get_value(it, 0),
                  "nombre": model.get_value(it, 1),
                  "autor": model.get_value(it, 2),
                  "estado": f"Pedido hecho por {self.nombre} ({self.dias} dias)"}
        data_2 = {"codigo": model.get_value(it, 0),
                  "nombre": model.get_value(it, 1),
                  "autor": model.get_value(it, 2),
                  "estado": model.get_value(it, 3)}
        data.remove(data_2)
        data.append(data_1)

        save_file(data)
        self.delete_all_data()
        self.load_data_from_json()

    # Funcion que hace que los datos de libros pedidos vuelvan a como estaban ingresados en el JSON.
    def dejar_libro(self, btn=None):
        model, it = self.ventana_usuario.tree.get_selection().get_selected()
        # Si no se selecciona nada.
        if model is None or it is None:
            return

        # Se dan los valores para cambiarlos en los datos.
        data = open_file()
        data_1 = {"codigo": model.get_value(it, 0),
                  "nombre": model.get_value(it, 1),
                  "autor": model.get_value(it, 2),
                  "estado": "Disponible"}
        data_2 = {"codigo": model.get_value(it, 0),
                  "nombre": model.get_value(it, 1),
                  "autor": model.get_value(it, 2),
                  "estado": model.get_value(it, 3)}
        data.remove(data_2)
        data.append(data_1)

        save_file(data)
        self.delete_all_data()
        self.load_data_from_json()

    # Cargar los datos del JSON creado para su manipulación en la ventana.
    def load_data_from_json(self):
        datos = open_file()

        for item in datos:
            line = [x for x in item.values()]
            # print(line)
            self.ventana_usuario.modelo.append(line)
    
    # Borra los datos y los vuelve a cargar.
    def delete_all_data(self):
        for index in range(len(self.ventana_usuario.modelo)):
            iter_ = self.ventana_usuario.modelo.get_iter(0)
            self.ventana_usuario.modelo.remove(iter_)


class Ventana_usuario():

    def __init__(self):

        builder = Gtk.Builder()
        builder.add_from_file("proyecto-1.ui")

        # Configuramos la ventana de interfaz del Usuario.
        self.ventana2 = builder.get_object("3usuario")
        self.ventana2.set_default_size(1000, 800)
        self.ventana2.set_title("Biblioteca BookWorm, Modo Público")
        self.ventana2.close()

        # Configuramos un Tree para que contenga los datos de los libros.
        self.tree = builder.get_object("libro")
        self.modelo = Gtk.ListStore(str, str, str, str)
        self.tree.set_model(model=self.modelo)
        
        nombre_columnas = ("Código", "Nombre", "Autor", "Estado")
        cell = Gtk.CellRendererText()
        for item in range(len(nombre_columnas)):
            column = Gtk.TreeViewColumn(nombre_columnas[item],
                                        cell,
                                        text=item)
            self.tree.append_column(column)
        
        # self.modelo.append(["1", "2", "3", "4"])
        # Se cargan los datos en la interfaz
        self.load_data_from_json()

        # Nombramos a los botones que estan en esta ventana.
        # Botón para pedir libro.
        self.boton_pedir = builder.get_object("pedir")
        self.boton_pedir.set_label("Pedir Libro")

        # Botón para devolver libro.
        self.boton_devolver = builder.get_object("dejar")
        self.boton_devolver.set_label("Devolver Libro")

        # Botón para salir y poder actualizar los valres.
        self.boton_reset = builder.get_object("reset")
        
        self.ventana2.show_all()

    # Cargar los datos del JSON creado para su manipulación en la ventana.
    def load_data_from_json(self):
        datos = open_file()

        for item in datos:
            line = [x for x in item.values()]
            # print(line)
            self.modelo.append(line)

if __name__ == "__main__":
    # Se llama a la Ventana inicial y principal del programa.
    Ventana_inicio()
    Gtk.main()
