# 📚 DOCUMENTACIÓN COMPLETA DEL SISTEMA DE INVENTARIO

## 📋 ÍNDICE
1. [Estructura del Proyecto](#estructura-del-proyecto)
2. [Arquitectura General](#arquitectura-general)
3. [Base de Datos](#base-de-datos)
4. [Sistema de Autenticación y Roles](#sistema-de-autenticación-y-roles)
5. [Gestión de Inventario](#gestión-de-inventario)
6. [Gestión de Usuarios](#gestión-de-usuarios)
7. [Sistema de Reportes](#sistema-de-reportes)
8. [Interfaz Gráfica](#interfaz-gráfica)
9. [Flujo Completo de la Aplicación](#flujo-completo-de-la-aplicación)
10. [Seguridad](#seguridad)
11. [Funciones Principales Detalladas](#funciones-principales-detalladas)

---

## 📁 ESTRUCTURA DEL PROYECTO

```
inventario_v1/
│
├── 📄 main.py                    # Aplicación principal y lógica de negocio
├── 📄 pantallas.py              # Clases de pantallas (Login, Registro, Dashboard)
├── 📄 base_datos.py             # Conexión y estructura de base de datos
├── 📄 inventario.kv             # Archivo de diseño de interfaz (Kivy Language)
├── 📄 inventario.db             # Base de datos SQLite (generada automáticamente)
├── 📄 logo.png                  # Logo de la empresa para el PDF
├── 📄 Reporte_Inventario.pdf    # PDF generado (ejemplo)
│
├── 📁 kivy_venv/                # Entorno virtual de Python con Kivy
│   ├── Scripts/                 # Scripts de activación del entorno virtual
│   ├── Lib/                     # Librerías instaladas
│   │   └── site-packages/       # Paquetes Python instalados
│   │       ├── kivy/            # Framework Kivy
│   │       ├── reportlab/       # Librería para generar PDFs
│   │       ├── PIL/             # Procesamiento de imágenes
│   │       └── ...              # Otras dependencias
│   └── share/                   # Recursos compartidos
│
└── 📁 venv/                     # Segundo entorno virtual (alternativo)
```

### 📝 Descripción de Archivos Principales

#### `main.py` (502 líneas)
**Propósito**: Archivo principal de la aplicación que contiene:
- Clase `InventarioApp`: Aplicación principal de Kivy
- Gestión de productos (CRUD completo)
- Gestión de usuarios (solo para administradores)
- Generación de reportes en pantalla y PDF
- Manejo de popups y alertas
- Coordinación entre componentes

**Funciones principales**:
- `build()`: Construye la interfaz inicial
- `guardar_producto_handler()`: Agrega productos
- `eliminar_producto()`: Elimina productos
- `abrir_editar_producto()`: Edita productos
- `cargar_lista_productos()`: Lista productos
- `buscar_producto_handler()`: Busca productos
- `generar_pdf()`: Genera reporte PDF
- `cargar_lista_usuarios()`: Lista usuarios
- `eliminar_usuario()`: Elimina usuarios
- `abrir_editar_usuario()`: Edita usuarios
- `generar_reporte()`: Genera reporte en pantalla

#### `pantallas.py` (266 líneas)
**Propósito**: Define las pantallas de la aplicación y su lógica:
- `PantallaLogin`: Autenticación de usuarios
- `PantallaRegistro`: Registro de nuevos usuarios
- `MainDashboard`: Panel principal con navegación
- Componentes personalizados (botones, filas de tabla)

**Clases principales**:
- `RoundedButton`: Botón con bordes redondeados
- `SidebarButton`: Botón del menú lateral
- `ProductTableRow`: Fila de tabla de productos
- `UserTableRow`: Fila de tabla de usuarios
- `PantallaLogin`: Pantalla de inicio de sesión
- `PantallaRegistro`: Pantalla de registro
- `MainDashboard`: Panel principal

#### `base_datos.py` (35 líneas)
**Propósito**: Manejo de la base de datos SQLite:
- Conexión a la base de datos
- Creación de tablas
- Función de hash para contraseñas

**Clases y funciones**:
- `BaseDatos`: Clase principal para manejo de BD
- `hashear_password()`: Convierte contraseña a SHA-256
- `crear_tablas()`: Crea las tablas si no existen
- `cerrar()`: Cierra la conexión

#### `inventario.kv` (866 líneas)
**Propósito**: Define la interfaz gráfica usando Kivy Language:
- Estilos de componentes (botones, inputs, cards)
- Layout de todas las pantallas
- Diseño responsive
- Temas y colores

**Componentes definidos**:
- `<RoundedButton>`: Estilo de botón redondeado
- `<ModernTextInput>`: Input moderno con fuente grande
- `<CardLayout>`: Contenedor con sombra
- `<SidebarButton>`: Botón del sidebar
- `<PantallaLogin>`: Layout de login
- `<PantallaRegistro>`: Layout de registro
- `<MainDashboard>`: Layout del dashboard
- `<ProductTableRow>`: Layout de fila de producto
- `<UserTableRow>`: Layout de fila de usuario

#### `inventario.db`
**Propósito**: Base de datos SQLite que almacena:
- Tabla `usuarios`: Información de usuarios
- Tabla `productos`: Información de productos

**Nota**: Este archivo se genera automáticamente al ejecutar la aplicación por primera vez.

#### `logo.png`
**Propósito**: Logo de la empresa que se incluye en el PDF del reporte.

---

## 🏗️ ARQUITECTURA GENERAL

### Tecnologías Utilizadas

1. **Python 3.x**: Lenguaje de programación principal
2. **Kivy**: Framework para interfaces gráficas de escritorio
3. **SQLite**: Base de datos relacional embebida
4. **ReportLab**: Librería para generación de PDFs
5. **Tkinter**: Para diálogos de guardar archivo (opcional)

### Patrón de Diseño

La aplicación sigue un patrón **MVC (Modelo-Vista-Controlador)** simplificado:

- **Modelo**: `base_datos.py` - Maneja los datos
- **Vista**: `inventario.kv` - Define la interfaz
- **Controlador**: `main.py` y `pantallas.py` - Maneja la lógica

### Flujo de Datos

```
Usuario → Interfaz (KV) → Pantallas (Python) → Lógica (main.py) → Base de Datos (SQLite)
                                                      ↓
                                              Reportes (PDF/Visual)
```

---

## 💾 BASE DE DATOS

### Esquema de Base de Datos

#### Tabla: `usuarios`

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Identificador único |
| `usuario` | TEXT | UNIQUE, NOT NULL | Nombre de usuario (login) |
| `password` | TEXT | NOT NULL | Hash SHA-256 de la contraseña |
| `nombre` | TEXT | NOT NULL | Nombre completo del usuario |
| `email` | TEXT | | Correo electrónico |
| `rol` | TEXT | DEFAULT 'empleado' | Rol: 'admin' o 'empleado' |

**Ejemplo de registro**:
```sql
INSERT INTO usuarios (usuario, password, nombre, email, rol) 
VALUES ('admin', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Juan Pérez', 'juan@email.com', 'admin');
```

#### Tabla: `productos`

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Identificador único |
| `codigo` | TEXT | UNIQUE, NOT NULL | Código único del producto |
| `nombre` | TEXT | NOT NULL | Nombre del producto |
| `descripcion` | TEXT | | Descripción detallada |
| `cantidad` | INTEGER | DEFAULT 0 | Stock disponible |
| `precio` | REAL | DEFAULT 0.0 | Precio unitario |
| `categoria` | TEXT | | Categoría del producto |

**Ejemplo de registro**:
```sql
INSERT INTO productos (codigo, nombre, descripcion, cantidad, precio, categoria) 
VALUES ('PROD001', 'Lápiz HB', 'Lápiz grafito número 2', 50, 0.50, 'Papelería');
```

### Funciones de Base de Datos

#### `BaseDatos.__init__()`
```python
def __init__(self):
    self.conexion = sqlite3.connect('inventario.db')
    self.cursor = self.conexion.cursor()
    self.crear_tablas()
```
- Establece conexión con SQLite
- Crea cursor para ejecutar consultas
- Llama a `crear_tablas()` para inicializar estructura

#### `crear_tablas()`
```python
def crear_tablas(self):
    # Crea tabla usuarios si no existe
    self.cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (...)''')
    # Crea tabla productos si no existe
    self.cursor.execute('''CREATE TABLE IF NOT EXISTS productos (...)''')
    self.conexion.commit()
```
- Usa `CREATE TABLE IF NOT EXISTS` para evitar errores
- Crea ambas tablas con sus restricciones
- Hace commit de los cambios

#### `hashear_password(password)`
```python
def hashear_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
```
- Convierte contraseña a hash SHA-256
- Ejemplo: "123456" → "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"
- **Nunca se almacenan contraseñas en texto plano**

---

## 🔐 SISTEMA DE AUTENTICACIÓN Y ROLES

### Proceso de Login

#### 1. Pantalla de Login (`PantallaLogin`)

**Flujo detallado**:

```
Usuario ingresa credenciales
    ↓
Validación de campos vacíos
    ↓
Hash de contraseña (SHA-256)
    ↓
Consulta a base de datos
    ↓
¿Usuario encontrado?
    ├─ SÍ → Guardar usuario_actual → Redirigir a Dashboard
    └─ NO → Mostrar error
```

**Código clave**:
```python
def iniciar_sesion(self):
    usuario = self.ids.usuario_input.text.strip()
    password_raw = self.ids.password_input.text.strip()
    
    # Validación
    if not usuario or not password_raw:
        self.mostrar_mensaje("Todos los campos son obligatorios")
        return
    
    # Hash de contraseña
    password = hashear_password(password_raw)
    
    # Consulta
    self.db.cursor.execute(
        "SELECT * FROM usuarios WHERE usuario = ? AND password = ?", 
        (usuario, password)
    )
    usuario_data = self.db.cursor.fetchone()
    
    if usuario_data:
        # Login exitoso
        self.manager.current = 'main'
        self.manager.get_screen('main').usuario_actual = usuario_data
        self.manager.get_screen('main').actualizar_bienvenida()
```

**Datos almacenados en `usuario_actual`**:
```python
usuario_data = (id, usuario, password_hash, nombre, email, rol)
# Ejemplo: (1, 'admin', 'hash...', 'Juan Pérez', 'juan@email.com', 'admin')
```

### Proceso de Registro

#### 2. Pantalla de Registro (`PantallaRegistro`)

**Validaciones implementadas**:

1. **Nombre completo**:
   ```python
   if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
       # Solo letras, espacios y acentos
   ```

2. **Email**:
   ```python
   if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
       # Formato válido de email
   ```

3. **Usuario**:
   ```python
   if len(usuario) < 4 or not usuario.isalnum():
       # Mínimo 4 caracteres, solo alfanuméricos
   ```

4. **Contraseña**:
   ```python
   if len(password_raw) < 6:
       # Mínimo 6 caracteres
   ```

**Asignación automática de rol**:
```python
# Si es el primer usuario → ADMIN
# Si ya hay usuarios → EMPLEADO
self.db.cursor.execute("SELECT COUNT(*) FROM usuarios")
total = self.db.cursor.fetchone()[0]
rol = 'admin' if total == 0 else 'empleado'
```

**Inserción en base de datos**:
```python
password = hashear_password(password_raw)
self.db.cursor.execute(
    "INSERT INTO usuarios (nombre, usuario, password, email, rol) VALUES (?, ?, ?, ?, ?)",
    (nombre, usuario, password, email, rol)
)
self.db.conexion.commit()
```

### Sistema de Roles

#### Roles Disponibles

1. **ADMIN** (`rol = 'admin'`):
   - ✅ Acceso completo a todas las funciones
   - ✅ Puede gestionar usuarios
   - ✅ Puede agregar/editar/eliminar productos
   - ✅ Puede generar reportes y PDFs
   - ✅ Ve todas las opciones del menú

2. **EMPLEADO** (`rol = 'empleado'`):
   - ✅ Puede ver productos
   - ✅ Puede buscar productos
   - ❌ NO puede agregar productos
   - ❌ NO puede editar productos
   - ❌ NO puede eliminar productos
   - ❌ NO puede gestionar usuarios
   - ❌ NO puede generar reportes
   - ❌ NO puede generar PDFs

#### Implementación de Permisos

**Función `actualizar_bienvenida()`**:
```python
def actualizar_bienvenida(self):
    if self.usuario_actual:
        nombre = self.usuario_actual[3]
        rol = self.usuario_actual[5] if len(self.usuario_actual) > 5 else 'empleado'
        
        self.ids.bienvenida_label.text = f'Hola, {nombre} ({rol})'
        
        if rol != 'admin':
            # OCULTAR elementos para empleados
            self.ids.btn_usr.opacity = 0          # Botón Usuarios
            self.ids.btn_usr.disabled = True
            self.ids.btn_rep.opacity = 0          # Botón Reportes
            self.ids.btn_rep.disabled = True
            # Formulario de agregar producto
            self.ids.pantalla_listar_interna.ids.formulario_agregar_producto.opacity = 0
            self.ids.pantalla_listar_interna.ids.formulario_agregar_producto.disabled = True
            # Botón PDF
            self.ids.pantalla_listar_interna.ids.btn_pdf.opacity = 0
            self.ids.pantalla_listar_interna.ids.btn_pdf.disabled = True
        else:
            # MOSTRAR elementos para admin
            # ... código inverso
```

**Control en filas de productos**:
```python
def cargar_lista_productos(self):
    # Verificar rol
    es_admin = False
    if dash.usuario_actual:
        rol = dash.usuario_actual[5] if len(dash.usuario_actual) > 5 else 'empleado'
        es_admin = (rol == 'admin')
    
    # Crear filas con o sin botones
    for p in prods:
        card = ProductTableRow(
            codigo=p[1], 
            nombre=p[2], 
            cantidad=p[4], 
            precio=p[5], 
            categoria=p[6] or 'N/A', 
            mostrar_botones=es_admin  # ← Control de visibilidad
        )
```

---

## 📦 GESTIÓN DE INVENTARIO

### Dashboard Principal

#### Estadísticas en Tiempo Real

El dashboard muestra 3 métricas principales:

1. **Total de Productos**:
   ```python
   self.db.cursor.execute("SELECT COUNT(*) FROM productos")
   total = self.db.cursor.fetchone()[0]
   ```
   - Cuenta todos los productos únicos en el inventario
   - Se actualiza automáticamente al agregar/eliminar productos

2. **Unidades en Stock**:
   ```python
   self.db.cursor.execute("SELECT SUM(cantidad) FROM productos")
   items = self.db.cursor.fetchone()[0] or 0
   ```
   - Suma todas las cantidades de todos los productos
   - Si no hay productos, retorna 0

3. **Valor de Inventario**:
   ```python
   self.db.cursor.execute("SELECT SUM(cantidad * precio) FROM productos")
   valor = self.db.cursor.fetchone()[0] or 0
   ```
   - Calcula: cantidad × precio para cada producto y suma todo
   - Representa el valor total del inventario

**Actualización automática**:
- Se actualiza al cambiar de pestaña al Dashboard
- Se actualiza después de agregar/editar/eliminar productos

### Operaciones CRUD de Productos

#### CREATE - Agregar Producto

**Función**: `guardar_producto_handler()`

**Proceso**:
```python
1. Obtener datos del formulario
   - codigo, nombre, categoria, cantidad, precio

2. Validaciones:
   - Código y nombre son obligatorios
   - Cantidad debe ser numérica (int)
   - Precio debe ser numérico (float)

3. Inserción en BD:
   INSERT INTO productos (codigo, nombre, descripcion, cantidad, precio, categoria)
   VALUES (?, ?, ?, ?, ?, ?)

4. Limpiar formulario

5. Actualizar lista y dashboard
```

**Código completo**:
```python
def guardar_producto_handler(self):
    dash = self.get_dashboard()
    p_nuevo = dash.ids.pantalla_listar_interna
    
    # Obtener datos
    codigo = p_nuevo.ids.p_codigo.text.strip()
    nombre = p_nuevo.ids.p_nombre.text.strip()
    categoria = p_nuevo.ids.p_categoria.text.strip()
    
    # Validar campos obligatorios
    if not codigo or not nombre:
        p_nuevo.ids.p_mensaje.text = "Código y nombre son obligatorios"
        return
    
    # Validar números
    try:
        cant = int(p_nuevo.ids.p_cantidad.text) if p_nuevo.ids.p_cantidad.text else 0
        prec = float(p_nuevo.ids.p_precio.text) if p_nuevo.ids.p_precio.text else 0.0
    except:
        p_nuevo.ids.p_mensaje.text = "Cantidad y precio numéricos"
        return
    
    # Insertar
    try:
        self.db.cursor.execute(
            "INSERT INTO productos (codigo, nombre, descripcion, cantidad, precio, categoria) VALUES (?, ?, ?, ?, ?, ?)",
            (codigo, nombre, '', cant, prec, categoria)
        )
        self.db.conexion.commit()
        
        # Limpiar y actualizar
        # ...
    except sqlite3.IntegrityError:
        # Error si el código ya existe
        p_nuevo.ids.p_mensaje.text = "Error: El código ya existe"
```

#### READ - Listar y Buscar Productos

**Función**: `cargar_lista_productos()`

**Proceso**:
```python
1. Limpiar contenedor de lista
2. Verificar rol del usuario (admin/empleado)
3. Consultar productos ordenados por nombre
4. Crear filas (ProductTableRow) para cada producto
5. Agregar filas al contenedor
```

**Búsqueda**: `buscar_producto_handler()`

```python
# Búsqueda por código O nombre (coincidencias parciales)
self.db.cursor.execute(
    "SELECT * FROM productos WHERE codigo LIKE ? OR nombre LIKE ?",
    (f'%{texto}%', f'%{texto}%')
)
```

**Características**:
- Búsqueda insensible a mayúsculas/minúsculas
- Coincidencias parciales (ej: "lap" encuentra "Lápiz")
- Busca en código y nombre simultáneamente
- Si el campo está vacío, muestra todos los productos

#### UPDATE - Editar Producto

**Función**: `abrir_editar_producto(codigo)`

**Proceso**:
```python
1. Consultar producto por código
2. Abrir popup con formulario prellenado
3. Usuario modifica: nombre, categoría, cantidad, precio
4. Al guardar:
   UPDATE productos 
   SET nombre=?, categoria=?, cantidad=?, precio=? 
   WHERE codigo=?
5. Actualizar lista y dashboard
```

**Nota**: El código NO se puede editar (es la clave única)

#### DELETE - Eliminar Producto

**Función**: `eliminar_producto(codigo)`

**Proceso**:
```python
1. Ejecutar DELETE FROM productos WHERE codigo=?
2. Hacer commit
3. Actualizar lista y dashboard
```

**Sin confirmación**: Se elimina inmediatamente (podría mejorarse)

---

## 👥 GESTIÓN DE USUARIOS (Solo Admin)

### Listar Usuarios

**Función**: `cargar_lista_usuarios()`

```python
def cargar_lista_usuarios(self):
    dash = self.get_dashboard()
    lista_container = dash.ids.pantalla_usuarios_interna.ids.u_lista
    lista_container.clear_widgets()
    
    # Consultar usuarios ordenados por nombre
    self.db.cursor.execute("SELECT * FROM usuarios ORDER BY nombre")
    users = self.db.cursor.fetchall()
    
    # Crear filas para cada usuario
    for u in users:
        card = UserTableRow(
            usuario=u[1],      # usuario
            nombre=u[3],        # nombre
            email=u[4] or 'Sin email',  # email
            rol=u[5] or 'empleado'      # rol
        )
        lista_container.add_widget(card)
```

**Información mostrada**:
- Usuario (nombre de login)
- Nombre completo
- Email
- Rol (admin/empleado)

### Editar Usuario

**Función**: `abrir_editar_usuario(usuario)`

**Restricciones**:
- ❌ No puedes editar tu propio rol
- ✅ Puedes editar nombre y email
- ✅ Puedes cambiar el rol de otros usuarios

**Proceso**:
```python
1. Verificar que no sea el usuario actual
2. Consultar datos del usuario
3. Abrir popup con formulario
4. Al guardar:
   UPDATE usuarios 
   SET nombre=?, email=?, rol=? 
   WHERE usuario=?
```

### Eliminar Usuario

**Función**: `eliminar_usuario(usuario)`

**Restricciones**:
- ❌ No puedes eliminar tu propio usuario
- ✅ Puedes eliminar otros usuarios

**Código**:
```python
def eliminar_usuario(self, usuario):
    dash = self.get_dashboard()
    # Prevenir auto-eliminación
    if dash.usuario_actual[1] == usuario:
        self.mostrar_alerta("Error", "No puedes eliminar tu propio usuario activo.")
        return
    
    # Eliminar
    self.db.cursor.execute("DELETE FROM usuarios WHERE usuario=?", (usuario,))
    self.db.conexion.commit()
    self.cargar_lista_usuarios()
```

---

## 📊 SISTEMA DE REPORTES

### Reporte en Pantalla

**Función**: `generar_reporte()`

**Secciones del reporte**:

#### 1. Resumen Financiero

Muestra 3 estadísticas:

```python
# Total de referencias únicas
self.db.cursor.execute("SELECT COUNT(*) FROM productos")
total = self.db.cursor.fetchone()[0]

# Total de unidades almacenadas
self.db.cursor.execute("SELECT SUM(cantidad) FROM productos")
items = self.db.cursor.fetchone()[0] or 0

# Valorización total
self.db.cursor.execute("SELECT SUM(cantidad * precio) FROM productos")
valor = self.db.cursor.fetchone()[0] or 0
```

**Visualización**:
- Título: "📊 Resumen Financiero" (color morado)
- Lista de 3 items con valores formateados

#### 2. Alerta de Bajo Stock

Identifica productos con stock crítico:

```python
# Productos con cantidad menor a 5
self.db.cursor.execute(
    "SELECT codigo, nombre, cantidad FROM productos WHERE cantidad < 5"
)
bajo = self.db.cursor.fetchall()
```

**Visualización**:
- Título: "Alerta de Bajo Stock" (color rojo)
- Lista de productos con:
  - Nombre del producto
  - Código
  - Cantidad actual
- Si no hay productos con bajo stock, muestra mensaje positivo

### Generación de PDF

**Función**: `generar_pdf()`

#### Proceso Completo

```
1. Abrir diálogo de guardar archivo (tkinter)
   ↓
2. Usuario elige ubicación y nombre
   ↓
3. Consultar todos los productos
   ↓
4. Crear canvas PDF (ReportLab)
   ↓
5. Dibujar membrete con logo
   ↓
6. Dibujar tabla de productos
   ↓
7. Calcular y mostrar totales
   ↓
8. Guardar PDF
   ↓
9. Mostrar mensaje de éxito
```

#### Estructura del PDF

**1. Membrete Superior**:

```
┌─────────────────────────────────────────────────────────┐
│  Emperadora Internet y Mas                    [LOGO]    │
│  RIF: J-29966140-6                                      │
│  Valencia Barrio Monumental III Av principal           │
│  Teléfono: 0241-8480889                                 │
│  Email: laemperadorainternetymas@gmail.com              │
├─────────────────────────────────────────────────────────┤
│  REPORTE OFICIAL DE INVENTARIO    Generado: 11/03/2026  │
└─────────────────────────────────────────────────────────┘
```

**Características**:
- Logo en lado derecho (si existe `logo.png`)
- Datos de empresa en lado izquierdo
- Línea separadora azul
- Título del reporte
- Fecha y hora de generación

**2. Tabla de Productos**:

```
┌────────┬──────────────┬─────────────┬──────┬────────┬────────┐
│ CÓDIGO │    NOMBRE    │  CATEGORÍA  │ CANT │ PRECIO  │ TOTAL  │
├────────┼──────────────┼─────────────┼──────┼────────┼────────┤
│  01    │   blusa      │    ropa     │  5   │ $10.00 │ $50.00 │
│  02    │  cuaderno    │  libreria   │  2   │  $2.00 │  $4.00 │
└────────┴──────────────┴─────────────┴──────┴────────┴────────┘
```

**Características**:
- Encabezado con fondo morado claro
- Filas alternadas (blanco/gris claro)
- Bordes en todas las celdas
- Columna TOTAL calculada (cantidad × precio)
- Texto truncado si es muy largo

**3. Fila de Totales**:

```
┌─────────────────────────────────────────────────────────┐
│ TOTALES:                                   9    $84.00 │
└─────────────────────────────────────────────────────────┘
```

**Cálculos**:
```python
# Total de cantidad
self.db.cursor.execute("SELECT SUM(cantidad) FROM productos")
total_cant = self.db.cursor.fetchone()[0] or 0

# Total de valor
self.db.cursor.execute("SELECT SUM(cantidad * precio) FROM productos")
total_valor = self.db.cursor.fetchone()[0] or 0
```

**4. Paginación Automática**:

Si hay muchos productos:
- Crea nuevas páginas automáticamente
- Repite encabezado en cada página
- Continúa la numeración de filas

#### Código de Generación

**Inicialización**:
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

c = canvas.Canvas(pdf_path, pagesize=letter)
width, height = letter  # 612 x 792 puntos
```

**Dibujar logo**:
```python
logo_path = os.path.join(os.getcwd(), "logo.png")
if os.path.exists(logo_path):
    c.drawImage(
        logo_path, 
        logo_x, logo_y, 
        width=100, height=100, 
        preserveAspectRatio=True
    )
```

**Dibujar texto**:
```python
c.setFont("Helvetica-Bold", 20)
c.setFillColor(colors.HexColor('#4F45E6'))
c.drawString(50, height - 50, "Emperadora Internet y Mas")
```

**Dibujar tabla**:
```python
# Fondo de fila
c.setFillColor(colors.HexColor('#F5F5F5'))
c.rect(x, y, width, height, fill=1, stroke=0)

# Borde de celda
c.setStrokeColor(colors.HexColor('#D0D0D0'))
c.rect(x, y, width, height, fill=0, stroke=1)

# Texto en celda
c.drawString(x, y, texto)
```

---

## 🎨 INTERFAZ GRÁFICA

### Framework Kivy

Kivy es un framework de Python para crear interfaces gráficas multiplataforma.

### Componentes Personalizados

#### 1. `RoundedButton`
Botón con bordes redondeados y color personalizable.

**Propiedades**:
- `bg_color`: Color de fondo (RGBA)
- Cambia de color al presionar (más oscuro)

#### 2. `ModernTextInput`
Input de texto moderno con:
- Fuente grande (18sp)
- Padding aumentado (15, 10)
- Bordes redondeados
- Borde que cambia de color al enfocar

#### 3. `CardLayout`
Contenedor con:
- Fondo blanco
- Bordes redondeados (15px)
- Sombra sutil

#### 4. `SidebarButton`
Botón del menú lateral con:
- Estado activo/inactivo
- Cambio de color según estado
- Icono y texto

### Estructura de Pantallas

#### Pantalla de Login
```
┌─────────────────────────────┐
│   Bienvenido de nuevo       │
│   Inicia sesión...          │
│                             │
│   Usuario: [________]       │
│   Contraseña: [________]   │
│                             │
│   [INICIAR SESIÓN]          │
│                             │
│   ¿No tienes cuenta?        │
│   Regístrate aquí           │
└─────────────────────────────┘
```

#### Dashboard Principal
```
┌──────────┬──────────────────────────────────┐
│ [☰]     │  InventarioApp    Hola, Juan     │
├──────────┼──────────────────────────────────┤
│ MENÚ     │                                   │
│          │  [Contenido según pestaña]       │
│ Dashboard│                                   │
│ Inventario│                                   │
│ Usuarios │                                   │
│ Reportes │                                   │
│          │                                   │
└──────────┴──────────────────────────────────┘
```

### Navegación

**ScreenManager**: Gestiona las pantallas principales
- `login`: Pantalla de inicio de sesión
- `registro`: Pantalla de registro
- `main`: Dashboard principal

**ScreenManager interno**: Gestiona pestañas del dashboard
- `dash`: Dashboard con estadísticas
- `inv`: Inventario con productos
- `usr`: Usuarios (solo admin)
- `rep`: Reportes (solo admin)

---

## 🔄 FLUJO COMPLETO DE LA APLICACIÓN

### 1. Inicio de la Aplicación

```
main.py → InventarioApp.build()
    ↓
Crear ScreenManager
    ↓
Agregar pantallas: Login, Registro, Dashboard
    ↓
Establecer pantalla actual: 'login'
    ↓
Mostrar interfaz
```

### 2. Proceso de Autenticación

```
Usuario en pantalla Login
    ↓
Ingresa usuario y contraseña
    ↓
Clic en "INICIAR SESIÓN"
    ↓
PantallaLogin.iniciar_sesion()
    ↓
Validar campos
    ↓
Hash de contraseña
    ↓
Consulta a BD
    ↓
¿Usuario válido?
    ├─ SÍ → Guardar usuario_actual
    │        Redirigir a 'main'
    │        actualizar_bienvenida()
    │        Configurar permisos según rol
    │
    └─ NO → Mostrar error
```

### 3. Navegación en Dashboard

```
Usuario en Dashboard
    ↓
Clic en pestaña (Dashboard/Inventario/Usuarios/Reportes)
    ↓
MainDashboard.switch_tab()
    ↓
Cambiar ScreenManager interno
    ↓
Cargar contenido según pestaña:
    - 'dash' → cargar_dashboard()
    - 'inv' → cargar_lista_productos()
    - 'usr' → cargar_lista_usuarios()
    - 'rep' → generar_reporte()
```

### 4. Gestión de Productos

#### Agregar Producto
```
Usuario llena formulario
    ↓
Clic en "AÑADIR"
    ↓
guardar_producto_handler()
    ↓
Validar datos
    ↓
INSERT INTO productos
    ↓
Actualizar lista y dashboard
```

#### Buscar Producto
```
Usuario escribe en campo de búsqueda
    ↓
Clic en "BUSCAR"
    ↓
buscar_producto_handler()
    ↓
Consulta con LIKE
    ↓
Mostrar resultados
```

#### Editar Producto
```
Clic en botón "E" de un producto
    ↓
abrir_editar_producto(codigo)
    ↓
Abrir popup con datos actuales
    ↓
Usuario modifica datos
    ↓
Clic en "GUARDAR CAMBIOS"
    ↓
UPDATE productos
    ↓
Actualizar lista y dashboard
```

#### Eliminar Producto
```
Clic en botón "X" de un producto
    ↓
eliminar_producto(codigo)
    ↓
DELETE FROM productos
    ↓
Actualizar lista y dashboard
```

### 5. Generación de Reporte PDF

```
Usuario (admin) en pestaña Inventario
    ↓
Clic en botón "PDF"
    ↓
generar_pdf()
    ↓
Abrir diálogo de guardar archivo
    ↓
Usuario elige ubicación
    ↓
Consultar productos
    ↓
Crear canvas PDF
    ↓
Dibujar membrete
    ↓
Dibujar tabla
    ↓
Calcular totales
    ↓
Guardar PDF
    ↓
Mostrar mensaje de éxito
```

---

## 🔒 SEGURIDAD

### Medidas Implementadas

#### 1. Hash de Contraseñas
- **Algoritmo**: SHA-256
- **Implementación**: `hashlib.sha256()`
- **Resultado**: Hash hexadecimal de 64 caracteres
- **Ventaja**: Aunque alguien acceda a la BD, no puede ver contraseñas

#### 2. Validación de Entrada
- **SQL Injection**: Prevenido con consultas parametrizadas (`?`)
- **XSS**: No aplicable (aplicación de escritorio)
- **Validación de tipos**: Campos numéricos validados antes de insertar

#### 3. Control de Acceso
- **Roles**: Admin y Empleado
- **Permisos**: Verificados en cada acción
- **UI**: Elementos ocultos según rol

#### 4. Restricciones de Usuario
- **Auto-eliminación**: Prevenida
- **Auto-edición de rol**: Prevenida
- **Códigos únicos**: Prevención de duplicados

### Ejemplo de Consulta Segura

```python
# ✅ SEGURO - Consulta parametrizada
self.db.cursor.execute(
    "SELECT * FROM usuarios WHERE usuario = ? AND password = ?",
    (usuario, password)
)

# ❌ INSEGURO - Vulnerable a SQL Injection
self.db.cursor.execute(
    f"SELECT * FROM usuarios WHERE usuario = '{usuario}' AND password = '{password}'"
)
```

---

## 📋 FUNCIONES PRINCIPALES DETALLADAS

### main.py

#### `InventarioApp.build()`
**Propósito**: Construye la aplicación inicial

**Código**:
```python
def build(self):
    self.db = BaseDatos()  # Crear conexión a BD
    
    sm = ScreenManager()  # Gestor de pantallas
    sm.add_widget(PantallaLogin(name='login'))
    sm.add_widget(PantallaRegistro(name='registro'))
    sm.add_widget(MainDashboard(name='main'))
    sm.current = 'login'  # Pantalla inicial
    
    return sm
```

#### `guardar_producto_handler()`
**Propósito**: Agrega un nuevo producto al inventario

**Parámetros**: Ninguno (obtiene datos de la UI)

**Retorno**: None

**Proceso**:
1. Obtener valores de inputs
2. Validar campos obligatorios
3. Validar tipos numéricos
4. Insertar en BD
5. Limpiar formulario
6. Actualizar UI

**Errores manejados**:
- Campos vacíos
- Tipos incorrectos
- Código duplicado (IntegrityError)

#### `cargar_lista_productos()`
**Propósito**: Carga y muestra todos los productos

**Parámetros**: Ninguno

**Retorno**: None

**Proceso**:
1. Limpiar contenedor
2. Verificar rol del usuario
3. Consultar productos
4. Crear filas para cada producto
5. Agregar filas al contenedor

**Características**:
- Ordena por nombre
- Controla visibilidad de botones según rol

#### `generar_pdf()`
**Propósito**: Genera un PDF con el reporte de inventario

**Parámetros**: Ninguno

**Retorno**: None

**Dependencias**:
- `reportlab`: Para generar PDF
- `tkinter`: Para diálogo de guardar (opcional)

**Proceso**:
1. Abrir diálogo de guardar
2. Consultar productos
3. Crear canvas PDF
4. Dibujar membrete
5. Dibujar tabla
6. Calcular totales
7. Guardar archivo

**Características**:
- Membrete personalizado
- Tabla formateada
- Paginación automática
- Logo opcional

### pantallas.py

#### `PantallaLogin.iniciar_sesion()`
**Propósito**: Autentica un usuario

**Validaciones**:
- Campos no vacíos
- Usuario existe en BD
- Contraseña correcta

**Acciones**:
- Hash de contraseña
- Consulta a BD
- Guarda usuario_actual
- Redirige a dashboard

#### `PantallaRegistro.registrar_usuario()`
**Propósito**: Registra un nuevo usuario

**Validaciones**:
- Todos los campos llenos
- Nombre solo letras
- Email válido
- Usuario alfanumérico, mínimo 4 caracteres
- Contraseña mínimo 6 caracteres

**Lógica especial**:
- Primer usuario → admin
- Usuarios siguientes → empleado

#### `MainDashboard.actualizar_bienvenida()`
**Propósito**: Configura la interfaz según el rol del usuario

**Acciones**:
- Muestra nombre y rol
- Oculta/muestra elementos según rol
- Configura permisos de UI

#### `MainDashboard.cargar_dashboard()`
**Propósito**: Calcula y muestra estadísticas

**Consultas**:
- COUNT de productos
- SUM de cantidades
- SUM de (cantidad × precio)

**Actualización**:
- Se ejecuta al cambiar a pestaña Dashboard
- Se ejecuta después de cambios en productos

### base_datos.py

#### `BaseDatos.__init__()`
**Propósito**: Inicializa la conexión a la base de datos

**Acciones**:
- Conecta a `inventario.db`
- Crea cursor
- Llama a `crear_tablas()`

#### `crear_tablas()`
**Propósito**: Crea las tablas si no existen

**Tablas creadas**:
- `usuarios`
- `productos`

**Características**:
- Usa `CREATE TABLE IF NOT EXISTS`
- Define restricciones (UNIQUE, PRIMARY KEY, etc.)

#### `hashear_password()`
**Propósito**: Convierte contraseña a hash SHA-256

**Entrada**: String con contraseña en texto plano

**Salida**: String hexadecimal de 64 caracteres

**Ejemplo**:
```python
hashear_password("123456")
# → "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"
```

---

## 🎯 RESUMEN EJECUTIVO

### Funcionalidades Principales

✅ **Autenticación de usuarios** con roles (admin/empleado)
✅ **Gestión completa de productos** (CRUD)
✅ **Búsqueda de productos** en tiempo real
✅ **Dashboard con estadísticas** en tiempo real
✅ **Gestión de usuarios** (solo admin)
✅ **Reportes visuales** con alertas
✅ **Generación de PDFs** profesionales con membrete
✅ **Control de permisos** basado en roles
✅ **Interfaz moderna** y responsive

### Tecnologías Clave

- **Python 3.x**: Lenguaje principal
- **Kivy**: Framework GUI
- **SQLite**: Base de datos
- **ReportLab**: Generación de PDFs
- **Tkinter**: Diálogos de archivo

### Características de Seguridad

- Contraseñas hasheadas (SHA-256)
- Consultas parametrizadas (prevención SQL Injection)
- Control de acceso basado en roles
- Validación de entrada de datos

### Estructura de Datos

- **2 tablas principales**: usuarios, productos
- **Relaciones**: Ninguna (tablas independientes)
- **Índices**: PRIMARY KEY en ambas tablas, UNIQUE en usuario y código

---

## 📞 INFORMACIÓN ADICIONAL

### Requisitos del Sistema

- Python 3.7 o superior
- Kivy 2.0 o superior
- ReportLab (para PDFs)
- SQLite3 (incluido en Python)

### Instalación de Dependencias

```bash
pip install kivy reportlab
```

### Ejecución

```bash
python main.py
```

### Base de Datos

- **Tipo**: SQLite
- **Archivo**: `inventario.db`
- **Ubicación**: Misma carpeta que `main.py`
- **Creación**: Automática al ejecutar por primera vez

---

**Documentación generada el**: 2026
**Versión del sistema**: 1.0
**Autor**: Sistema de Inventario - Emperadora Internet y Mas






