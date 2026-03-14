import sqlite3
import os
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock
try:
    from tkinter import filedialog
    import tkinter as tk
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

# Importamos desde nuestros otros archivos
from base_datos import BaseDatos
from pantallas import PantallaLogin, PantallaRegistro, MainDashboard, ProductTableRow, UserTableRow

Window.clearcolor = (0.96, 0.97, 0.98, 1) 
Window.size = (1000, 700)

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

    # ================= FUNCIONES DE POPUPS GENÉRICOS =================
    def mostrar_alerta(self, titulo, mensaje):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        lbl = Label(text=mensaje, color=(1, 1, 1, 1), font_size='14sp', halign='center', valign='middle')
        lbl.bind(size=lbl.setter('text_size'))
        layout.add_widget(lbl)
        btn = Button(text='CERRAR', size_hint_y=None, height=45, background_color=(0.31, 0.27, 0.9, 1))
        popup = Popup(title=titulo, content=layout, size_hint=(0.6, 0.4), background_color=(0.1, 0.1, 0.1, 1))
        btn.bind(on_release=popup.dismiss)
        layout.add_widget(btn)
        popup.open()

    # ================= GESTIÓN DE PRODUCTOS =================
    def guardar_producto_handler(self):
        dash = self.get_dashboard()
        p_nuevo = dash.ids.pantalla_listar_interna
        
        codigo = p_nuevo.ids.p_codigo.text.strip()
        nombre = p_nuevo.ids.p_nombre.text.strip()
        desc = ''
        categoria = p_nuevo.ids.p_categoria.text.strip()
        
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
            
            self.cargar_lista_productos()
            self.get_dashboard().cargar_dashboard()
        except sqlite3.IntegrityError:
            p_nuevo.ids.p_mensaje.text = "Error: El código ya existe"
            Clock.schedule_once(lambda dt: setattr(p_nuevo.ids.p_mensaje, 'text', ''), 3)
        except Exception as e:
            p_nuevo.ids.p_mensaje.text = f"Error: {e}"
            Clock.schedule_once(lambda dt: setattr(p_nuevo.ids.p_mensaje, 'text', ''), 3)

    def eliminar_producto(self, codigo):
        self.db.cursor.execute("DELETE FROM productos WHERE codigo=?", (codigo,))
        self.db.conexion.commit()
        self.cargar_lista_productos()
        self.get_dashboard().cargar_dashboard()

    def abrir_editar_producto(self, codigo):
        self.db.cursor.execute("SELECT * FROM productos WHERE codigo=?", (codigo,))
        prod = self.db.cursor.fetchone()
        if not prod: return
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        n_input = TextInput(text=prod[2], multiline=False)
        c_input = TextInput(text=prod[6] if prod[6] else '', multiline=False)
        cant_input = TextInput(text=str(prod[4]), multiline=False)
        p_input = TextInput(text=str(prod[5]), multiline=False)
        
        layout.add_widget(Label(text="Nombre:"))
        layout.add_widget(n_input)
        layout.add_widget(Label(text="Categoría:"))
        layout.add_widget(c_input)
        layout.add_widget(Label(text="Cantidad:"))
        layout.add_widget(cant_input)
        layout.add_widget(Label(text="Precio:"))
        layout.add_widget(p_input)
        
        btn = Button(text="GUARDAR CAMBIOS", size_hint_y=None, height=40, background_color=(0.2, 0.8, 0.2, 1))
        layout.add_widget(btn)
        
        popup = Popup(title=f"Editar Producto: {codigo}", content=layout, size_hint=(0.5, 0.7), background_color=(0.1, 0.1, 0.1, 1))
        
        def guardar_cambios(instance):
            try:
                self.db.cursor.execute("UPDATE productos SET nombre=?, categoria=?, cantidad=?, precio=? WHERE codigo=?",
                                       (n_input.text.strip(), c_input.text.strip(), int(cant_input.text), float(p_input.text), codigo))
                self.db.conexion.commit()
                self.cargar_lista_productos()
                self.get_dashboard().cargar_dashboard()
                popup.dismiss()
            except Exception as e:
                print(e)
                
        btn.bind(on_release=guardar_cambios)
        popup.open()

    def cargar_lista_productos(self):
        dash = self.get_dashboard()
        lista_container = dash.ids.pantalla_listar_interna.ids.p_lista
        lista_container.clear_widgets()
        try:
            # Verificar si el usuario es admin
            es_admin = False
            if dash.usuario_actual:
                rol = dash.usuario_actual[5] if len(dash.usuario_actual) > 5 else 'empleado'
                es_admin = (rol == 'admin')
            
            self.db.cursor.execute("SELECT * FROM productos ORDER BY codigo")
            prods = self.db.cursor.fetchall()
            if not prods: return
            for p in prods:
                card = ProductTableRow(codigo=p[1], nombre=p[2], cantidad=p[4], precio=p[5], categoria=p[6] or 'N/A', mostrar_botones=es_admin)
                lista_container.add_widget(card)
        except Exception as e: print(e)

    def buscar_producto_handler(self):
        dash = self.get_dashboard()
        texto = dash.ids.pantalla_listar_interna.ids.b_input.text.strip()
        resultados = dash.ids.pantalla_listar_interna.ids.p_lista
        resultados.clear_widgets()
        if not texto:
            self.cargar_lista_productos()
            return
        try:
            # Verificar si el usuario es admin
            es_admin = False
            if dash.usuario_actual:
                rol = dash.usuario_actual[5] if len(dash.usuario_actual) > 5 else 'empleado'
                es_admin = (rol == 'admin')
            
            self.db.cursor.execute("SELECT * FROM productos WHERE codigo LIKE ? OR nombre LIKE ?", (f'%{texto}%', f'%{texto}%'))
            prods = self.db.cursor.fetchall()
            for p in prods:
                card = ProductTableRow(codigo=p[1], nombre=p[2], cantidad=p[4], precio=p[5], categoria=p[6] or 'N/A', mostrar_botones=es_admin)
                resultados.add_widget(card)
        except Exception as e: print(e)

    def generar_pdf(self):
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            from reportlab.lib import colors
            from reportlab.lib.units import inch
            from datetime import datetime
            
            # Abrir diálogo para guardar el archivo
            if TKINTER_AVAILABLE:
                root = tk.Tk()
                root.withdraw()  # Ocultar la ventana principal de tkinter
                root.attributes('-topmost', True)  # Traer al frente
                
                # Abrir diálogo de guardar archivo
                pdf_path = filedialog.asksaveasfilename(
                    defaultextension=".pdf",
                    filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                    title="Guardar Reporte de Inventario",
                    initialfile="Reporte_Inventario.pdf"
                )
                root.destroy()
                
                # Si el usuario canceló el diálogo
                if not pdf_path:
                    return
            else:
                # Si tkinter no está disponible, usar la ruta por defecto
                pdf_path = os.path.join(os.getcwd(), "Reporte_Inventario.pdf")
            
            self.db.cursor.execute("SELECT codigo, nombre, categoria, cantidad, precio FROM productos ORDER BY nombre")
            prods = self.db.cursor.fetchall()
            
            c = canvas.Canvas(pdf_path, pagesize=letter)
            width, height = letter
            
            # ========== MEMBRETE DE LA EMPRESA ==========
            # Logo en el lado derecho, por encima de la línea azul
            logo_path = os.path.join(os.getcwd(), "logo.png")
            if os.path.exists(logo_path):
                try:
                    # Logo en el lado derecho, por encima de la línea azul
                    logo_width = 100
                    logo_height = 100
                    logo_x = width - 50 - logo_width  # 50px del margen derecho
                    logo_y = height - 20 - logo_height  # Más arriba, por encima de la línea azul
                    c.drawImage(logo_path, logo_x, logo_y, width=logo_width, height=logo_height, preserveAspectRatio=True)
                except Exception as e:
                    print(f"Error al cargar el logo: {e}")
            
            # Datos de la empresa (lado izquierdo)
            c.setFont("Helvetica-Bold", 20)
            c.setFillColor(colors.HexColor('#4F45E6'))  # Color morado similar al tema
            c.drawString(50, height - 50, "Emperadora Internet y Mas")
            
            c.setFont("Helvetica", 11)
            c.setFillColor(colors.black)
            c.drawString(50, height - 70, "RIF: J-29966140-6")
            c.drawString(50, height - 85, "Valencia Barrio Monumental III Av principal")
            c.drawString(50, height - 100, "Teléfono: 0241-8480889")
            c.drawString(50, height - 115, "Email: laemperadorainternetymas@gmail.com")
            
            # Línea separadora
            c.setStrokeColor(colors.HexColor('#4F45E6'))
            c.setLineWidth(2)
            c.line(50, height - 130, width - 50, height - 130)
            
            # Título del reporte
            c.setFont("Helvetica-Bold", 16)
            c.setFillColor(colors.black)
            c.drawString(50, height - 155, "REPORTE OFICIAL DE INVENTARIO")
            
            # Fecha de generación
            fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            c.setFont("Helvetica", 10)
            c.setFillColor(colors.grey)
            c.drawString(width - 200, height - 155, f"Generado: {fecha}")
            
            # ========== TABLA DE PRODUCTOS ==========
            y_start = height - 200
            y_current = y_start
            
            # Ancho de la tabla expandida (márgenes más pequeños para llegar al borde)
            table_x_start = 40
            table_x_end = width - 40
            table_width = table_x_end - table_x_start
            
            # Posiciones de las columnas (redistribuidas para llegar al borde)
            # Calculamos para que TOTAL llegue cerca del borde derecho
            col_codigo = table_x_start + 5
            col_nombre = table_x_start + 70  # Reducido para dar más espacio
            col_categoria = table_x_start + 240
            col_cantidad = table_x_start + 370
            col_precio = table_x_start + 430
            col_total = width - 90  # Cerca del borde derecho, dejando espacio para el contenido
            
            # Encabezados de la tabla con fondo
            header_height = 30
            c.setFillColor(colors.HexColor('#E8E7F5'))
            c.rect(table_x_start, y_current - header_height, table_width, header_height, fill=1, stroke=0)
            
            c.setFont("Helvetica-Bold", 11)
            c.setFillColor(colors.HexColor('#4F45E6'))
            c.drawString(col_codigo, y_current - 20, "CÓDIGO")
            c.drawString(col_nombre, y_current - 20, "NOMBRE")
            c.drawString(col_categoria, y_current - 20, "CATEGORÍA")
            c.drawString(col_cantidad, y_current - 20, "CANT.")
            c.drawString(col_precio, y_current - 20, "PRECIO")
            c.drawString(col_total, y_current - 20, "TOTAL")
            
            # Línea debajo del encabezado
            c.setStrokeColor(colors.HexColor('#4F45E6'))
            c.setLineWidth(1.5)
            c.line(table_x_start, y_current - header_height, table_x_end, y_current - header_height)
            
            # Datos de productos
            y_current -= header_height + 5
            c.setFont("Helvetica", 10)
            c.setFillColor(colors.black)
            
            row_height = 25
            alternate = False
            
            for idx, p in enumerate(prods):
                # Color alternado para filas
                if alternate:
                    c.setFillColor(colors.HexColor('#F5F5F5'))
                    c.rect(table_x_start, y_current - row_height, table_width, row_height, fill=1, stroke=0)
                else:
                    c.setFillColor(colors.white)
                    c.rect(table_x_start, y_current - row_height, table_width, row_height, fill=1, stroke=0)
                
                # Bordes de la celda
                c.setStrokeColor(colors.HexColor('#D0D0D0'))
                c.setLineWidth(0.5)
                c.rect(table_x_start, y_current - row_height, table_width, row_height, fill=0, stroke=1)
                
                # Contenido de las celdas
                c.setFillColor(colors.black)
                codigo = str(p[0])[:12] if len(str(p[0])) > 12 else str(p[0])
                nombre = str(p[1])[:28] if len(str(p[1])) > 28 else str(p[1])  # Reducido de 35
                categoria = str(p[2])[:18] if p[2] and len(str(p[2])) > 18 else (str(p[2]) if p[2] else 'N/A')
                cantidad = str(p[3])
                precio = f"${p[4]:.2f}"
                total = f"${p[3] * p[4]:.2f}"
                
                c.drawString(col_codigo, y_current - 18, codigo)
                c.drawString(col_nombre, y_current - 18, nombre)
                c.drawString(col_categoria, y_current - 18, categoria)
                c.drawString(col_cantidad, y_current - 18, cantidad)
                c.drawString(col_precio, y_current - 18, precio)
                c.drawString(col_total, y_current - 18, total)
                
                y_current -= row_height
                alternate = not alternate
                
                # Nueva página si es necesario
                if y_current < 100:
                    c.showPage()
                    # Redibujar encabezado en nueva página
                    y_current = height - 50
                    c.setFillColor(colors.HexColor('#E8E7F5'))
                    c.rect(table_x_start, y_current - header_height, table_width, header_height, fill=1, stroke=0)
                    c.setFont("Helvetica-Bold", 11)
                    c.setFillColor(colors.HexColor('#4F45E6'))
                    c.drawString(col_codigo, y_current - 20, "CÓDIGO")
                    c.drawString(col_nombre, y_current - 20, "NOMBRE")
                    c.drawString(col_categoria, y_current - 20, "CATEGORÍA")
                    c.drawString(col_cantidad, y_current - 20, "CANT.")
                    c.drawString(col_precio, y_current - 20, "PRECIO")
                    c.drawString(col_total, y_current - 20, "TOTAL")
                    c.setStrokeColor(colors.HexColor('#4F45E6'))
                    c.setLineWidth(1.5)
                    c.line(table_x_start, y_current - header_height, table_x_end, y_current - header_height)
                    y_current -= header_height + 5
                    alternate = False
            
            # Totales al final
            y_current -= 10
            c.setFillColor(colors.HexColor('#E8E7F5'))
            c.rect(table_x_start, y_current - row_height, table_width, row_height, fill=1, stroke=0)
            c.setStrokeColor(colors.HexColor('#4F45E6'))
            c.setLineWidth(1.5)
            c.rect(table_x_start, y_current - row_height, table_width, row_height, fill=0, stroke=1)
            
            self.db.cursor.execute("SELECT SUM(cantidad) FROM productos")
            total_cant = self.db.cursor.fetchone()[0] or 0
            self.db.cursor.execute("SELECT SUM(cantidad * precio) FROM productos")
            total_valor = self.db.cursor.fetchone()[0] or 0
            
            c.setFont("Helvetica-Bold", 11)
            c.setFillColor(colors.HexColor('#4F45E6'))
            c.drawString(col_codigo, y_current - 18, "TOTALES:")
            c.drawString(col_cantidad, y_current - 18, str(int(total_cant)))
            c.drawString(col_total, y_current - 18, f"${total_valor:,.2f}")
            
            c.save()
            self.mostrar_alerta("Éxito", f"PDF generado correctamente en:\n{pdf_path}")
            
        except ImportError:
            self.mostrar_alerta("Error", "Falta la librería ReportLab.\nEjecuta en la terminal: pip install reportlab")
        except Exception as e:
            self.mostrar_alerta("Error", f"No se pudo generar: {str(e)}")

    # ================= GESTIÓN DE USUARIOS =================
    def cargar_lista_usuarios(self):
        dash = self.get_dashboard()
        lista_container = dash.ids.pantalla_usuarios_interna.ids.u_lista
        lista_container.clear_widgets()
        try:
            self.db.cursor.execute("SELECT * FROM usuarios ORDER BY nombre")
            users = self.db.cursor.fetchall()
            if not users: return
            for u in users:
                # AQUÍ PASAMOS EL ROL AL DISEÑO
                card = UserTableRow(usuario=u[1], nombre=u[3], email=u[4] or 'Sin email', rol=u[5] or 'empleado')
                lista_container.add_widget(card)
        except Exception as e: print(e)

    def eliminar_usuario(self, usuario):
        dash = self.get_dashboard()
        if dash.usuario_actual[1] == usuario:
            self.mostrar_alerta("Error", "No puedes eliminar tu propio usuario activo.")
            return
        self.db.cursor.execute("DELETE FROM usuarios WHERE usuario=?", (usuario,))
        self.db.conexion.commit()
        self.cargar_lista_usuarios()

    def abrir_editar_usuario(self, usuario):
        dash = self.get_dashboard()
        if dash.usuario_actual[1] == usuario:
            self.mostrar_alerta("Error", "No puedes editar tu propio rol desde aquí.")
            return

        self.db.cursor.execute("SELECT * FROM usuarios WHERE usuario=?", (usuario,))
        usr = self.db.cursor.fetchone()
        if not usr: return
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        n_input = TextInput(text=usr[3], multiline=False)
        e_input = TextInput(text=usr[4], multiline=False)
        r_input = TextInput(text=usr[5] if usr[5] else 'empleado', multiline=False)
        
        layout.add_widget(Label(text="Nombre:"))
        layout.add_widget(n_input)
        layout.add_widget(Label(text="Email:"))
        layout.add_widget(e_input)
        layout.add_widget(Label(text="Rol (escribe 'admin' o 'empleado'):"))
        layout.add_widget(r_input)
        
        btn = Button(text="GUARDAR CAMBIOS", size_hint_y=None, height=40, background_color=(0.2, 0.8, 0.2, 1))
        layout.add_widget(btn)
        
        popup = Popup(title=f"Editar Usuario: {usuario}", content=layout, size_hint=(0.5, 0.6), background_color=(0.1, 0.1, 0.1, 1))
        
        def guardar_cambios(instance):
            try:
                self.db.cursor.execute("UPDATE usuarios SET nombre=?, email=?, rol=? WHERE usuario=?",
                                       (n_input.text.strip(), e_input.text.strip(), r_input.text.strip().lower(), usuario))
                self.db.conexion.commit()
                self.cargar_lista_usuarios()
                popup.dismiss()
            except Exception as e:
                print(e)
                
        btn.bind(on_release=guardar_cambios)
        popup.open()

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
            
            box1.add_widget(LabelSubTitle("Resumen Financiero", (0.31, 0.27, 0.9, 1)))
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
            print(e)

if __name__ == '__main__':
    
    app = InventarioApp()
    app.title = "Sistema de Inventario"
    app.run()