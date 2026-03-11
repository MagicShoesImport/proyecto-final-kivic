import sqlite3
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, ListProperty, NumericProperty
from kivy.uix.behaviors import ButtonBehavior

Window.clearcolor = (0.96, 0.97, 0.98, 1) # #F5F7FA
Window.size = (1000, 700) # Slightly larger default window

KV = '''
<RoundedButton>:
    background_color: 0,0,0,0
    canvas.before:
        Color:
            rgba: self.bg_color if self.state == 'normal' else (self.bg_color[0]*0.8, self.bg_color[1]*0.8, self.bg_color[2]*0.8, 1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [8,]
    color: 1, 1, 1, 1
    bold: True

<ModernTextInput@TextInput>:
    background_color: 0,0,0,0
    cursor_color: 0.31, 0.27, 0.9, 1
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [6,]
        Color:
            rgba: (0.31, 0.27, 0.9, 1) if self.focus else (0.8, 0.8, 0.8, 1)
        Line:
            rounded_rectangle: (self.x, self.y, self.width, self.height, 6)
            width: 1.2

<CardLayout@BoxLayout>:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [15,]
        Color:
            rgba: 0, 0, 0, 0.05
        BoxShadow:
            pos: self.pos
            size: self.size
            offset: 0, -2
            spread_radius: -2, -2
            border_radius: 15, 15, 15, 15
            blur_radius: 10

<SidebarButton>:
    canvas.before:
        Color:
            rgba: (0.9, 0.9, 0.95, 1) if self.active else ( (0.95, 0.95, 0.95, 1) if self.state == 'down' else self.bg_color )
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [8,]
    Label:
        text: root.text
        color: (0.31, 0.27, 0.9, 1) if root.active else (0.3, 0.3, 0.3, 1)
        bold: root.active
        halign: 'left'
        valign: 'center'
        text_size: self.size
        padding: [20, 0]

<ModernHeader@Label>:
    color: 0.1, 0.1, 0.1, 1
    font_size: '24sp'
    bold: True
    halign: 'left'
    valign: 'center'
    text_size: self.size

<ModernSubtext@Label>:
    color: 0.4, 0.4, 0.4, 1
    font_size: '14sp'
    halign: 'left'
    valign: 'center'
    text_size: self.size

<PantallaLogin>:
    BoxLayout:
        padding: [0, 0, 0, 0]
        # Fondo general
        canvas.before:
            Color:
                rgba: 0.96, 0.97, 0.98, 1
            Rectangle:
                pos: self.pos
                size: self.size
                
        AnchorLayout:
            CardLayout:
                orientation: 'vertical'
                orientation: 'vertical'
                size_hint: 0.8, None
                height: 500
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                padding: 40
                spacing: 20
                
                ModernHeader:
                    text: 'Bienvenido de nuevo'
                    halign: 'center'
                    size_hint_y: None
                    height: 40
                
                ModernSubtext:
                    text: 'Inicia sesión en tu cuenta de InventarioApp'
                    halign: 'center'
                    size_hint_y: None
                    height: 30
                    
                BoxLayout:
                    orientation: 'vertical'
                    spacing: 5
                    size_hint_y: None
                    height: 65
                    ModernSubtext:
                        text: 'Usuario'
                    ModernTextInput:
                        id: usuario_input
                        multiline: False
                        write_tab: False

                BoxLayout:
                    orientation: 'vertical'
                    spacing: 5
                    size_hint_y: None
                    height: 65
                    ModernSubtext:
                        text: 'Contraseña'
                    ModernTextInput:
                        id: password_input
                        multiline: False
                        password: True
                        write_tab: False
                
                Label:
                    id: mensaje_label
                    text: ''
                    color: 1, 0.3, 0.3, 1
                    size_hint_y: None
                    height: 20
                    font_size: '13sp'
                    
                RoundedButton:
                    text: 'INICIAR SESIÓN'
                    size_hint_y: None
                    height: 45
                    on_release: root.iniciar_sesion()
                    
                BoxLayout:
                    size_hint_y: None
                    height: 45
                    ModernSubtext:
                        text: '¿No tienes cuenta?'
                        halign: 'right'
                    Button:
                        text: 'Regístrate aquí'
                        color: 0.31, 0.27, 0.9, 1
                        bold: True
                        halign: 'left'
                        text_size: self.size
                        background_color: 0, 0, 0, 0
                        size_hint_x: 0.5
                        on_release: root.ir_registro()

<PantallaRegistro>:
    BoxLayout:
        padding: [0, 0, 0, 0]
        canvas.before:
            Color:
                rgba: 0.96, 0.97, 0.98, 1
            Rectangle:
                pos: self.pos
                size: self.size
                
        AnchorLayout:
            CardLayout:
                orientation: 'vertical'
                orientation: 'vertical'
                size_hint: 0.85, None
                height: 600
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                padding: 40
                spacing: 15
                
                ModernHeader:
                    text: 'Crear Cuenta'
                    halign: 'center'
                    size_hint_y: None
                    height: 40
                
                ModernSubtext:
                    text: 'Regístrate para gestionar tu inventario'
                    halign: 'center'
                    size_hint_y: None
                    height: 30
                
                ScrollView:
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: 15
                        padding: [5, 5, 5, 5]

                        BoxLayout:
                            orientation: 'vertical'
                            spacing: 5
                            size_hint_y: None
                            height: 65
                            ModernSubtext:
                                text: 'Nombre Completo'
                            ModernTextInput:
                                id: nombre_input
                                multiline: False
                                write_tab: False

                        BoxLayout:
                            orientation: 'vertical'
                            spacing: 5
                            size_hint_y: None
                            height: 65
                            ModernSubtext:
                                text: 'Usuario'
                            ModernTextInput:
                                id: usuario_input
                                multiline: False
                                write_tab: False
                                
                        BoxLayout:
                            orientation: 'vertical'
                            spacing: 5
                            size_hint_y: None
                            height: 65
                            ModernSubtext:
                                text: 'Email'
                            ModernTextInput:
                                id: email_input
                                multiline: False
                                write_tab: False

                        BoxLayout:
                            orientation: 'vertical'
                            spacing: 5
                            size_hint_y: None
                            height: 65
                            ModernSubtext:
                                text: 'Contraseña'
                            ModernTextInput:
                                id: password_input
                                multiline: False
                                password: True
                                write_tab: False
                
                Label:
                    id: mensaje_label
                    text: ''
                    color: 1, 0.3, 0.3, 1
                    size_hint_y: None
                    height: 20
                    font_size: '13sp'
                    
                BoxLayout:
                    spacing: 10
                    size_hint_y: None
                    height: 45
                    RoundedButton:
                        text: 'VOLVER'
                        bg_color: 0.6, 0.6, 0.6, 1
                        on_release: root.volver()
                    RoundedButton:
                        text: 'REGISTRARSE'
                        on_release: root.registrar_usuario()

<MainDashboard>:
    BoxLayout:
        orientation: 'vertical'
        
        # Navbar
        CardLayout:
            size_hint_y: None
            height: 70
            padding: [20, 10, 20, 10]
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
                Color:
                    rgba: 0.9, 0.9, 0.9, 1
                Line:
                    points: [self.x, self.y, self.right, self.y]
                    width: 1

            RoundedButton:
                text: '☰'
                bg_color: 0.31, 0.27, 0.9, 1
                size_hint_x: None
                width: 50
                size_hint_y: None
                height: 40
                pos_hint: {'center_y': 0.5}
                on_release: root.toggle_sidebar()

            Label:
                text: 'InventarioApp'
                color: 0.31, 0.27, 0.9, 1
                font_size: '22sp'
                bold: True
                halign: 'left'
                valign: 'center'
                text_size: self.size
                size_hint_x: 0.4
                padding: [15, 0]
                
            Label:
                id: bienvenida_label
                text: 'Bienvenido, Usuario'
                color: 0.3, 0.3, 0.3, 1
                halign: 'right'
                valign: 'center'
                text_size: self.size
                size_hint_x: 0.4
                padding: [20, 0]
                
            RoundedButton:
                text: 'SALIR'
                bg_color: 0.9, 0.3, 0.3, 1
                size_hint_x: None
                width: 100
                size_hint_y: None
                height: 40
                pos_hint: {'center_y': 0.5}
                on_release: root.cerrar_sesion()

        BoxLayout:
            # Sidebar
            BoxLayout:
                id: sidebar
                orientation: 'vertical'
                size_hint_x: None
                width: 250
                padding: [15, 20, 15, 20]
                spacing: 10
                canvas.before:
                    Color:
                        rgba: 1, 1, 1, 1
                    Rectangle:
                        pos: self.pos
                        size: self.size
                    Color:
                        rgba: 0.9, 0.9, 0.9, 1
                    Line:
                        points: [self.right, self.y, self.right, self.top]
                        width: 1
                
                ModernSubtext:
                    id: menu_title
                    text: 'MENÚ PRINCIPAL'
                    size_hint_y: None
                    height: 30
                    font_size: '12sp'
                    bold: True
                    
                SidebarButton:
                    text: 'Dashboard'
                    size_hint_y: None
                    height: 45
                    id: btn_dash
                    active: root.current_tab == 'dash'
                    on_release: root.switch_tab('dash')

                SidebarButton:
                    text: 'Inventario'
                    size_hint_y: None
                    height: 45
                    id: btn_inv
                    active: root.current_tab == 'inv'
                    on_release: root.switch_tab('inv')
                    
                SidebarButton:
                    text: 'Usuarios'
                    size_hint_y: None
                    height: 45
                    id: btn_usr
                    active: root.current_tab == 'usr'
                    on_release: root.switch_tab('usr')
                    
                SidebarButton:
                    text: 'Reportes'
                    size_hint_y: None
                    height: 45
                    id: btn_rep
                    active: root.current_tab == 'rep'
                    on_release: root.switch_tab('rep')
                    
                Widget:
                    # Spacer

            # Main content area
            BoxLayout:
                padding: 20
                ScreenManager:
                    id: sm_interna
                    Screen:
                        name: 'dash'
                        BoxLayout:
                            orientation: 'vertical'
                            spacing: 20
                            ModernHeader:
                                text: 'Dashboard General'
                                size_hint_y: None
                                height: 50
                            GridLayout:
                                cols: 3
                                spacing: 20
                                size_hint_y: None
                                height: 150
                                CardLayout:
                                    orientation: 'vertical'
                                    padding: 20
                                    ModernSubtext:
                                        text: 'Total Productos'
                                    Label:
                                        id: stat_total
                                        text: '0'
                                        color: 0.31, 0.27, 0.9, 1
                                        font_size: '35sp'
                                        bold: True
                                        halign: 'left'
                                        text_size: self.size
                                CardLayout:
                                    orientation: 'vertical'
                                    padding: 20
                                    ModernSubtext:
                                        text: 'Unidades en Stock'
                                    Label:
                                        id: stat_unidades
                                        text: '0'
                                        color: 0.1, 0.7, 0.4, 1
                                        font_size: '35sp'
                                        bold: True
                                        halign: 'left'
                                        text_size: self.size
                                CardLayout:
                                    orientation: 'vertical'
                                    padding: 20
                                    ModernSubtext:
                                        text: 'Valor de Inventario'
                                    Label:
                                        id: stat_valor
                                        text: '$0.00'
                                        color: 0.9, 0.6, 0.1, 1
                                        font_size: '35sp'
                                        bold: True
                                        halign: 'left'
                                        text_size: self.size
                            Widget:
                                # Spacer
                    Screen:
                        name: 'inv'
                        PantallaListarInterna:
                            id: pantalla_listar_interna
                    Screen:
                        name: 'usr'
                        PantallaUsuariosInterna:
                            id: pantalla_usuarios_interna
                    Screen:
                        name: 'rep'
                        PantallaReporteInterna:
                            id: pantalla_reporte_interna

<ProductTableRow@BoxLayout>:
    size_hint_y: None
    height: 40
    padding: [15, 0, 15, 0]
    spacing: 5
    codigo: ''
    nombre: ''
    categoria: ''
    cantidad: 0
    precio: 0.0
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: 0.9, 0.9, 0.9, 1
        Line:
            points: [self.x, self.y, self.right, self.y]
            width: 1
    Label:
        text: root.codigo
        color: 0.1, 0.1, 0.1, 1
        size_hint_x: 0.15
        text_size: self.size
        halign: 'left'
        valign: 'center'
    Label:
        text: root.nombre
        color: 0.1, 0.1, 0.1, 1
        size_hint_x: 0.3
        text_size: self.size
        halign: 'left'
        valign: 'center'
    Label:
        text: root.categoria
        color: 0.1, 0.1, 0.1, 1
        size_hint_x: 0.2
        text_size: self.size
        halign: 'left'
        valign: 'center'
    Label:
        text: str(root.cantidad)
        color: (0.8, 0.2, 0.2, 1) if root.cantidad < 5 else (0.1, 0.1, 0.1, 1)
        bold: root.cantidad < 5
        size_hint_x: 0.15
        text_size: self.size
        halign: 'center'
        valign: 'center'
    Label:
        text: f"${root.precio:.2f}"
        color: 0.1, 0.1, 0.1, 1
        size_hint_x: 0.15
        text_size: self.size
        halign: 'right'
        valign: 'center'
    Label:
        text: f"${(root.cantidad * root.precio):.2f}"
        color: 0.31, 0.27, 0.9, 1
        bold: True
        size_hint_x: 0.15
        text_size: self.size
        halign: 'right'
        valign: 'center'

<PantallaListarInterna@BoxLayout>:
    orientation: 'vertical'
    spacing: 15
    ModernHeader:
        text: 'Gestión de Inventario'
        size_hint_y: None
        height: 40
        
    # Form to add product
    CardLayout:
        size_hint_y: None
        height: 60
        padding: 10
        spacing: 10
        ModernTextInput:
            id: p_codigo
            hint_text: 'Código'
            multiline: False
            size_hint_x: 0.15
        ModernTextInput:
            id: p_nombre
            hint_text: 'Nombre'
            multiline: False
            size_hint_x: 0.25
        ModernTextInput:
            id: p_categoria
            hint_text: 'Categoría'
            multiline: False
            size_hint_x: 0.15
        ModernTextInput:
            id: p_cantidad
            hint_text: 'Cant.'
            multiline: False
            size_hint_x: 0.1
        ModernTextInput:
            id: p_precio
            hint_text: 'Precio'
            multiline: False
            size_hint_x: 0.1
        RoundedButton:
            text: 'AÑADIR'
            size_hint_x: 0.15
            height: 40
            on_release: app.guardar_producto_handler()
            
    # Search bar
    BoxLayout:
        size_hint_y: None
        height: 40
        spacing: 10
        ModernTextInput:
            id: b_input
            hint_text: 'Buscar por código o nombre...'
            multiline: False
        RoundedButton:
            text: 'BUSCAR'
            size_hint_x: None
            width: 120
            on_release: app.buscar_producto_handler()
        RoundedButton:
            text: 'MOSTRAR TODOS'
            size_hint_x: None
            width: 150
            bg_color: 0.5, 0.5, 0.5, 1
            on_release: app.cargar_lista_productos()

    Label:
        id: p_mensaje
        text: ''
        color: 1, 0.3, 0.3, 1
        size_hint_y: None
        height: 20
        font_size: '13sp'
        
    # Table Header
    CardLayout:
        size_hint_y: None
        height: 40
        padding: [15, 0, 15, 0]
        spacing: 5
        canvas.before:
            Color:
                rgba: 0.9, 0.9, 0.95, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [8,]
        Label:
            text: 'CÓDIGO'
            color: 0.3, 0.3, 0.3, 1
            bold: True
            size_hint_x: 0.15
            text_size: self.size
            halign: 'left'
            valign: 'center'
        Label:
            text: 'NOMBRE'
            color: 0.3, 0.3, 0.3, 1
            bold: True
            size_hint_x: 0.3
            text_size: self.size
            halign: 'left'
            valign: 'center'
        Label:
            text: 'CATEGORÍA'
            color: 0.3, 0.3, 0.3, 1
            bold: True
            size_hint_x: 0.2
            text_size: self.size
            halign: 'left'
            valign: 'center'
        Label:
            text: 'CANTIDAD'
            color: 0.3, 0.3, 0.3, 1
            bold: True
            size_hint_x: 0.15
            text_size: self.size
            halign: 'center'
            valign: 'center'
        Label:
            text: 'PRECIO'
            color: 0.3, 0.3, 0.3, 1
            bold: True
            size_hint_x: 0.15
            text_size: self.size
            halign: 'right'
            valign: 'center'
        Label:
            text: 'TOTAL'
            color: 0.3, 0.3, 0.3, 1
            bold: True
            size_hint_x: 0.15
            text_size: self.size
            halign: 'right'
            valign: 'center'

    ScrollView:
        BoxLayout:
            id: p_lista
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            spacing: 0
            padding: [0, 5, 0, 5]

<UserTableRow@BoxLayout>:
    size_hint_y: None
    height: 40
    padding: [15, 0, 15, 0]
    spacing: 5
    usuario: ''
    nombre: ''
    email: ''
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: 0.9, 0.9, 0.9, 1
        Line:
            points: [self.x, self.y, self.right, self.y]
            width: 1
    Label:
        text: root.usuario
        color: 0.1, 0.1, 0.1, 1
        size_hint_x: 0.2
        text_size: self.size
        halign: 'left'
        valign: 'center'
    Label:
        text: root.nombre
        color: 0.1, 0.1, 0.1, 1
        size_hint_x: 0.4
        text_size: self.size
        halign: 'left'
        valign: 'center'
    Label:
        text: root.email
        color: 0.1, 0.1, 0.1, 1
        size_hint_x: 0.4
        text_size: self.size
        halign: 'left'
        valign: 'center'

<PantallaUsuariosInterna@BoxLayout>:
    orientation: 'vertical'
    spacing: 15
    ModernHeader:
        text: 'Directorio de Usuarios'
        size_hint_y: None
        height: 50
        
    # Table Header
    CardLayout:
        size_hint_y: None
        height: 40
        padding: [15, 0, 15, 0]
        spacing: 5
        canvas.before:
            Color:
                rgba: 0.9, 0.9, 0.95, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [8,]
        Label:
            text: 'USUARIO'
            color: 0.3, 0.3, 0.3, 1
            bold: True
            size_hint_x: 0.2
            text_size: self.size
            halign: 'left'
            valign: 'center'
        Label:
            text: 'NOMBRE'
            color: 0.3, 0.3, 0.3, 1
            bold: True
            size_hint_x: 0.4
            text_size: self.size
            halign: 'left'
            valign: 'center'
        Label:
            text: 'EMAIL'
            color: 0.3, 0.3, 0.3, 1
            bold: True
            size_hint_x: 0.4
            text_size: self.size
            halign: 'left'
            valign: 'center'

    ScrollView:
        BoxLayout:
            id: u_lista
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            spacing: 0
            padding: [0, 5, 0, 5]

<PantallaReporteInterna@BoxLayout>:
    orientation: 'vertical'
    spacing: 15
    ModernHeader:
        text: 'Reportes de Sistema'
        size_hint_y: None
        height: 50
    ScrollView:
        BoxLayout:
            id: r_lista
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            spacing: 10
            padding: [5, 5, 5, 5]

'''

Builder.load_string(KV)

class RoundedButton(ButtonBehavior, Label):
    bg_color = ListProperty([0.31, 0.27, 0.9, 1])

class SidebarButton(ButtonBehavior, BoxLayout):
    bg_color = ListProperty([0, 0, 0, 0])
    icon = StringProperty('')
    text = StringProperty('')
    active = BooleanProperty(False)

class BaseDatos:
    def __init__(self):
        self.conexion = sqlite3.connect('inventario.db')
        self.cursor = self.conexion.cursor()
    
    def cerrar(self):
        self.conexion.close()

class PantallaLogin(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = BaseDatos()

    def iniciar_sesion(self):
        usuario = self.ids.usuario_input.text
        password = self.ids.password_input.text
        if not usuario or not password:
            self.mostrar_mensaje("Todos los campos son obligatorios")
            return
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
        nombre = self.ids.nombre_input.text
        usuario = self.ids.usuario_input.text
        password = self.ids.password_input.text
        email = self.ids.email_input.text
        if not nombre or not usuario or not password:
            self.mostrar_mensaje("Nombre, usuario y contraseña son obligatorios")
            return
        try:
            self.db.cursor.execute("INSERT INTO usuarios (nombre, usuario, password, email) VALUES (?, ?, ?, ?)", (nombre, usuario, password, email))
            self.db.conexion.commit()
            self.mostrar_popup("Registro exitoso", "Usuario creado correctamente")
            self.limpiar_campos()
            self.volver()
        except sqlite3.IntegrityError:
            self.mostrar_mensaje("El usuario ya existe")
        except Exception as e:
            self.mostrar_mensaje(f"Error: {str(e)}")

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

    def mostrar_popup(self, titulo, mensaje):
        layout = BoxLayout(orientation='vertical', padding=10)
        layout.add_widget(Label(text=mensaje, color=(0,0,0,1)))
        btn = Button(text='OK', size_hint_y=0.3, background_color=(0.31, 0.27, 0.9, 1))
        popup = Popup(title=titulo, content=layout, size_hint=(0.5,0.3))
        btn.bind(on_press=popup.dismiss)
        layout.add_widget(btn)
        popup.open()


class MainDashboard(Screen):
    current_tab = StringProperty('dash')
    sidebar_open = BooleanProperty(True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.usuario_actual = None
        self.db = BaseDatos()

    def actualizar_bienvenida(self):
        if self.usuario_actual:
            self.ids.bienvenida_label.text = f'Hola, {self.usuario_actual[3]}'
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
        
        # Cargar data correspondiente al apretar
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

class ProductTableRow(BoxLayout):
    codigo = StringProperty('')
    nombre = StringProperty('')
    categoria = StringProperty('')
    cantidad = NumericProperty(0)
    precio = NumericProperty(0.0)
    
class UserTableRow(BoxLayout):
    usuario = StringProperty('')
    nombre = StringProperty('')
    email = StringProperty('')

class InventarioApp(App):
    def build(self):
        self.db = BaseDatos()
        sm = ScreenManager()
        sm.add_widget(PantallaLogin(name='login'))
        sm.add_widget(PantallaRegistro(name='registro'))
        sm.add_widget(MainDashboard(name='main'))
        sm.current = 'login'
        return sm

    def on_stop(self):
        try:
            self.db.cerrar()
        except:
            pass

    def get_dashboard(self):
        return self.root.get_screen('main')

    def mostrar_popup(self, titulo, mensaje):
        layout = BoxLayout(orientation='vertical', padding=10)
        layout.add_widget(Label(text=mensaje, color=(0,0,0,1)))
        btn = Button(text='OK', size_hint_y=0.4, background_color=(0.31, 0.27, 0.9, 1))
        popup = Popup(title=titulo, content=layout, size_hint=(0.5,0.3))
        btn.bind(on_press=popup.dismiss)
        layout.add_widget(btn)
        popup.open()

    def guardar_producto_handler(self):
        dash = self.get_dashboard()
        p_nuevo = dash.ids.pantalla_listar_interna
        
        codigo = p_nuevo.ids.p_codigo.text
        nombre = p_nuevo.ids.p_nombre.text
        desc = ''
        categoria = p_nuevo.ids.p_categoria.text
        
        if not codigo or not nombre:
            p_nuevo.ids.p_mensaje.text = "Código y nombre son obligatorios"
            Clock.schedule_once(lambda dt: setattr(p_nuevo.ids.p_mensaje, 'text', ''), 3)
            return
            
        try:
            cant = int(p_nuevo.ids.p_cantidad.text) if p_nuevo.ids.p_cantidad.text else 0
            prec = float(p_nuevo.ids.p_precio.text) if p_nuevo.ids.p_precio.text else 0.0
        except:
            p_nuevo.ids.p_mensaje.text = "Cantidad y precio numéricos"
            Clock.schedule_once(lambda dt: setattr(p_nuevo.ids.p_mensaje, 'text', ''), 3)
            return
            
        try:
            self.db.cursor.execute("INSERT INTO productos (codigo, nombre, descripcion, cantidad, precio, categoria) VALUES (?, ?, ?, ?, ?, ?)", (codigo, nombre, desc, cant, prec, categoria))
            self.db.conexion.commit()
            
            p_nuevo.ids.p_codigo.text = ''
            p_nuevo.ids.p_nombre.text = ''
            p_nuevo.ids.p_categoria.text = ''
            p_nuevo.ids.p_cantidad.text = ''
            p_nuevo.ids.p_precio.text = ''
            
            p_nuevo.ids.p_mensaje.text = "Producto añadido"
            p_nuevo.ids.p_mensaje.color = (0.2, 0.8, 0.2, 1) # Green success message
            Clock.schedule_once(lambda dt: setattr(p_nuevo.ids.p_mensaje, 'text', ''), 3)
            Clock.schedule_once(lambda dt: setattr(p_nuevo.ids.p_mensaje, 'color', (1, 0.3, 0.3, 1)), 3)
            
            self.cargar_lista_productos()
        except sqlite3.IntegrityError:
            p_nuevo.ids.p_mensaje.text = "Error: El código ya existe"
            Clock.schedule_once(lambda dt: setattr(p_nuevo.ids.p_mensaje, 'text', ''), 3)
        except Exception as e:
            p_nuevo.ids.p_mensaje.text = f"Error: {e}"
            Clock.schedule_once(lambda dt: setattr(p_nuevo.ids.p_mensaje, 'text', ''), 3)

    def cargar_lista_productos(self):
        dash = self.get_dashboard()
        lista_container = dash.ids.pantalla_listar_interna.ids.p_lista
        lista_container.clear_widgets()
        
        try:
            self.db.cursor.execute("SELECT * FROM productos ORDER BY nombre")
            prods = self.db.cursor.fetchall()
            if not prods:
                lista_container.add_widget(Label(text="No tienes productos en tu inventario.", color=(0.5,0.5,0.5,1), size_hint_y=None, height=50))
                return
            for p in prods:
                card = ProductTableRow(codigo=p[1], nombre=p[2], cantidad=p[4], precio=p[5], categoria=p[6] or 'N/A')
                lista_container.add_widget(card)
        except Exception as e:
            lista_container.add_widget(Label(text=f"Error cargando: {e}", color=(1,0,0,1), size_hint_y=None, height=50))

    def cargar_lista_usuarios(self):
        dash = self.get_dashboard()
        lista_container = dash.ids.pantalla_usuarios_interna.ids.u_lista
        lista_container.clear_widgets()
        
        try:
            self.db.cursor.execute("SELECT * FROM usuarios ORDER BY nombre")
            users = self.db.cursor.fetchall()
            if not users:
                lista_container.add_widget(Label(text="No hay usuarios.", color=(0.5,0.5,0.5,1), size_hint_y=None, height=50))
                return
            for u in users:
                card = UserTableRow(usuario=u[1], nombre=u[3], email=u[4] or 'Sin email')
                lista_container.add_widget(card)
        except Exception as e:
            lista_container.add_widget(Label(text=f"Error cargando: {e}", color=(1,0,0,1), size_hint_y=None, height=50))

    def buscar_producto_handler(self):
        dash = self.get_dashboard()
        texto = dash.ids.pantalla_listar_interna.ids.b_input.text
        resultados = dash.ids.pantalla_listar_interna.ids.p_lista
        resultados.clear_widgets()
        
        if not texto:
            self.cargar_lista_productos()
            return
            
        try:
            self.db.cursor.execute("SELECT * FROM productos WHERE codigo LIKE ? OR nombre LIKE ?", (f'%{texto}%', f'%{texto}%'))
            prods = self.db.cursor.fetchall()
            if not prods:
                resultados.add_widget(Label(text=("No se encontraron resultados para '%s'" % texto), color=(0.5,0.5,0.5,1), size_hint_y=None, height=50))
                return
            for p in prods:
                card = ProductTableRow(codigo=p[1], nombre=p[2], cantidad=p[4], precio=p[5], categoria=p[6] or 'N/A')
                resultados.add_widget(card)
        except Exception as e:
            resultados.add_widget(Label(text=f"Error: {e}", color=(1,0,0,1), size_hint_y=None, height=50))

    def generar_reporte(self):
        dash = self.get_dashboard()
        r_lista = dash.ids.pantalla_reporte_interna.ids.r_lista
        r_lista.clear_widgets()
        
        try:
            LabelSubTitle = lambda txt, col: Label(text=txt, color=col, bold=True, size_hint_y=None, height=40, font_size='18sp', halign='left', text_size=(dash.width-300, 40))
            LabelBody = lambda txt: Label(text=txt, color=(0.2,0.2,0.2,1), size_hint_y=None, height=30, halign='left', text_size=(dash.width-300, 30))
            
            box1 = BoxLayout(orientation='vertical', size_hint_y=None, height=150, padding=10)
            self.db.cursor.execute("SELECT COUNT(*) FROM productos")
            total = self.db.cursor.fetchone()[0]
            self.db.cursor.execute("SELECT SUM(cantidad) FROM productos")
            items = self.db.cursor.fetchone()[0] or 0
            self.db.cursor.execute("SELECT SUM(cantidad * precio) FROM productos")
            valor = self.db.cursor.fetchone()[0] or 0
            
            box1.add_widget(LabelSubTitle("📊 Resumen Financiero", (0.31, 0.27, 0.9, 1)))
            box1.add_widget(LabelBody(f"Total de referencias únicas: {total}"))
            box1.add_widget(LabelBody(f"Total de unidades almacenadas: {items}"))
            box1.add_widget(LabelBody(f"Valorización total: ${valor:,.2f}"))
            r_lista.add_widget(box1)
            
            self.db.cursor.execute("SELECT codigo, nombre, cantidad FROM productos WHERE cantidad < 5")
            bajo = self.db.cursor.fetchall()
            
            box2 = BoxLayout(orientation='vertical', size_hint_y=None, padding=10)
            box2.bind(minimum_height=box2.setter('height'))
            box2.add_widget(LabelSubTitle("Alerta de Bajo Stock", (0.9, 0.3, 0.3, 1)))
            
            if bajo:
                for p in bajo:
                    box2.add_widget(LabelBody(f"• {p[1]} (Cód: {p[0]}) - Stock: {p[2]} unid."))
            else:
                box2.add_widget(LabelBody("Todo en orden. No hay productos con stock menor a 5."))
            
            r_lista.add_widget(box2)
            
        except Exception as e:
            r_lista.add_widget(Label(text=f"Error generando reporte: {e}", color=(1,0,0,1), size_hint_y=None, height=50))

if __name__ == '__main__':
    InventarioApp().run()
