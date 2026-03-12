import re
import sqlite3
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.app import App
from kivy.factory import Factory
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, ListProperty, NumericProperty

from base_datos import BaseDatos, hashear_password

class RoundedButton(ButtonBehavior, Label):
    bg_color = ListProperty([0.31, 0.27, 0.9, 1])

class SidebarButton(ButtonBehavior, BoxLayout):
    bg_color = ListProperty([0, 0, 0, 0])
    icon = StringProperty('')
    text = StringProperty('')
    active = BooleanProperty(False)

class ProductTableRow(BoxLayout):
    codigo = StringProperty('')
    nombre = StringProperty('')
    categoria = StringProperty('')
    cantidad = NumericProperty(0)
    precio = NumericProperty(0.0)
    mostrar_botones = BooleanProperty(True)
    
class UserTableRow(BoxLayout):
    usuario = StringProperty('')
    nombre = StringProperty('')
    email = StringProperty('')
    rol = StringProperty('') # <--- ¡NUEVA PROPIEDAD!

class PantallaLogin(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = BaseDatos()

    def iniciar_sesion(self):
        usuario = self.ids.usuario_input.text.strip()
        password_raw = self.ids.password_input.text.strip()
        
        if not usuario or not password_raw:
            self.mostrar_mensaje("Todos los campos son obligatorios")
            return
            
        password = hashear_password(password_raw)
        
        try:
            self.db.cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND password = ?", (usuario, password))
            usuario_data = self.db.cursor.fetchone()
            if usuario_data:
                self.manager.current = 'main'
                self.manager.get_screen('main').usuario_actual = usuario_data
                self.manager.get_screen('main').actualizar_bienvenida()
                self.limpiar_campos()
            else:
                self.mostrar_mensaje("Usuario o contraseña incorrectos")
        except Exception as e:
            self.mostrar_mensaje(f"Error: {str(e)}")

    def ir_registro(self):
        self.manager.current = 'registro'
        self.limpiar_campos()

    def mostrar_mensaje(self, texto):
        self.ids.mensaje_label.text = texto
        Clock.schedule_once(lambda dt: self.limpiar_mensaje(), 3)

    def limpiar_mensaje(self):
        self.ids.mensaje_label.text = ''

    def limpiar_campos(self):
        self.ids.usuario_input.text = ''
        self.ids.password_input.text = ''

class PantallaRegistro(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = BaseDatos()

    def registrar_usuario(self):
        nombre = self.ids.nombre_input.text.strip()
        usuario = self.ids.usuario_input.text.strip()
        password_raw = self.ids.password_input.text.strip()
        email = self.ids.email_input.text.strip()

        if not nombre or not usuario or not password_raw or not email:
            self.mostrar_mensaje("Todos los campos son obligatorios")
            return

        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
            self.mostrar_mensaje("El nombre solo debe contener letras")
            return

        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            self.mostrar_mensaje("Ingresa un correo electrónico válido")
            return

        if len(usuario) < 4 or not usuario.isalnum():
            self.mostrar_mensaje("Usuario: mínimo 4 caracteres, sin espacios")
            return

        if len(password_raw) < 6:
            self.mostrar_mensaje("La contraseña debe tener al menos 6 caracteres")
            return

        password = hashear_password(password_raw)
        
        try:
            # Magia: Si es el primer usuario, lo hacemos ADMIN automáticamente
            self.db.cursor.execute("SELECT COUNT(*) FROM usuarios")
            total = self.db.cursor.fetchone()[0]
            rol = 'admin' if total == 0 else 'empleado'

            self.db.cursor.execute("INSERT INTO usuarios (nombre, usuario, password, email, rol) VALUES (?, ?, ?, ?, ?)", (nombre, usuario, password, email, rol))
            self.db.conexion.commit()
            self.limpiar_campos()
            self.mostrar_popup("Registro exitoso", "Usuario creado correctamente", exito=True)
            
        except sqlite3.IntegrityError:
            self.mostrar_mensaje("Error: El usuario ya existe en el sistema")
        except Exception as e:
            self.mostrar_mensaje(f"Error crítico: {str(e)}")

    def mostrar_popup(self, titulo, mensaje, exito=False): 
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        lbl = Label(text=mensaje, color=(1, 1, 1, 1), font_size='16sp', halign='center', valign='middle')
        lbl.bind(size=lbl.setter('text_size'))
        layout.add_widget(lbl)
        
        btn = Factory.RoundedButton(text='EXCELENTE', size_hint_y=None, height=45)
        popup = Factory.ModernPopup(title=titulo, content=layout, size_hint=(0.55, 0.35))
        
        def cerrar_y_redirigir(instance):
            popup.dismiss()
            if exito:
                self.volver() 

        btn.bind(on_release=cerrar_y_redirigir)
        layout.add_widget(btn)
        popup.open()

    def volver(self):
        self.manager.current = 'login'

    def mostrar_mensaje(self, texto):
        self.ids.mensaje_label.text = texto
        Clock.schedule_once(lambda dt: self.limpiar_mensaje(), 3)

    def limpiar_mensaje(self):
        self.ids.mensaje_label.text = ''

    def limpiar_campos(self):
        self.ids.nombre_input.text = ''
        self.ids.usuario_input.text = ''
        self.ids.password_input.text = ''
        self.ids.email_input.text = ''

class MainDashboard(Screen):
    current_tab = StringProperty('dash')
    sidebar_open = BooleanProperty(True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.usuario_actual = None
        self.db = BaseDatos()

    def actualizar_bienvenida(self):
        if self.usuario_actual:
            nombre = self.usuario_actual[3]
            rol = self.usuario_actual[5] if len(self.usuario_actual) > 5 else 'empleado'
            
            self.ids.bienvenida_label.text = f'Hola, {nombre} ({rol})'
            
            if rol != 'admin':
                # Ocultar botones del menú
                self.ids.btn_usr.opacity = 0
                self.ids.btn_usr.disabled = True
                self.ids.btn_rep.opacity = 0
                self.ids.btn_rep.disabled = True
                # Ocultar formulario de agregar producto
                try:
                    self.ids.pantalla_listar_interna.ids.formulario_agregar_producto.opacity = 0
                    self.ids.pantalla_listar_interna.ids.formulario_agregar_producto.disabled = True
                except:
                    pass
                # Ocultar botón PDF
                try:
                    self.ids.pantalla_listar_interna.ids.btn_pdf.opacity = 0
                    self.ids.pantalla_listar_interna.ids.btn_pdf.disabled = True
                except:
                    pass
            else:
                # Mostrar botones del menú
                self.ids.btn_usr.opacity = 1
                self.ids.btn_usr.disabled = False
                self.ids.btn_rep.opacity = 1
                self.ids.btn_rep.disabled = False
                # Mostrar formulario de agregar producto
                try:
                    self.ids.pantalla_listar_interna.ids.formulario_agregar_producto.opacity = 1
                    self.ids.pantalla_listar_interna.ids.formulario_agregar_producto.disabled = False
                except:
                    pass
                # Mostrar botón PDF
                try:
                    self.ids.pantalla_listar_interna.ids.btn_pdf.opacity = 1
                    self.ids.pantalla_listar_interna.ids.btn_pdf.disabled = False
                except:
                    pass
                
        self.switch_tab('dash')

    def toggle_sidebar(self):
        self.sidebar_open = not self.sidebar_open
        if self.sidebar_open:
            self.ids.sidebar.width = 250
            self.ids.menu_title.text = 'MENÚ PRINCIPAL'
            self.ids.btn_dash.text = 'Dashboard'
            self.ids.btn_inv.text = 'Inventario'
            self.ids.btn_usr.text = 'Usuarios'
            self.ids.btn_rep.text = 'Reportes'
        else:
            self.ids.sidebar.width = 80
            self.ids.menu_title.text = ''
            self.ids.btn_dash.text = ''
            self.ids.btn_inv.text = ''
            self.ids.btn_usr.text = ''
            self.ids.btn_rep.text = ''

    def switch_tab(self, tab_name):
        self.current_tab = tab_name
        self.ids.sm_interna.current = tab_name
        
        if tab_name == 'dash':
            self.cargar_dashboard()
        elif tab_name == 'inv':
            App.get_running_app().cargar_lista_productos()
        elif tab_name == 'usr':
            App.get_running_app().cargar_lista_usuarios()
        elif tab_name == 'rep':
            App.get_running_app().generar_reporte()

    def cargar_dashboard(self):
        try:
            self.db.cursor.execute("SELECT COUNT(*) FROM productos")
            total = self.db.cursor.fetchone()[0]
            self.db.cursor.execute("SELECT SUM(cantidad) FROM productos")
            items = self.db.cursor.fetchone()[0] or 0
            self.db.cursor.execute("SELECT SUM(cantidad * precio) FROM productos")
            valor = self.db.cursor.fetchone()[0] or 0
            
            self.ids.stat_total.text = str(total)
            self.ids.stat_unidades.text = str(items)
            self.ids.stat_valor.text = f"${valor:,.2f}"
            
        except Exception as e:
            print("Error cargando dashboard:", e)

    def cerrar_sesion(self):
        self.usuario_actual = None
        self.manager.current = 'login'