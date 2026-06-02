# Persevera – Aplicación Web de Gestión de Facturas

Proyecto universitario desarrollado en equipo para el curso de Sistemas de Computación. Se trata de una aplicación web para gestionar compras, ventas, proveedores, clientes e inventario de una empresa comercial. Desarrollada para reemplazar el seguimiento manual en planillas por una interfaz dinámica y filtrable conectada a una base de datos relacional.

El archivo web.py contiene la lógica del servidor y las rutas Flask — cada endpoint consulta la base de datos y renderiza su template HTML correspondiente.

# Instalación 

Usar el gestor de paquetes pip para instalar las dependencias. Ajustar los datos de conexión en web.py si es necesario


```bash
pip install flask pymysql
```

# Uso

```bash
python web.py
```

Abrir http://localhost:3000 en el navegador

# Funciones 

- Registro y consulta de proveedores, clientes y compras
- Búsqueda de facturas por proveedor o cliente con vista de detalle
- Inventario con cálculo de stock en tiempo real
- Cálculo de utilidades entre rangos de fechas

# Stack

- Python, Flask, PyMySQL
- MySQL
- HTML, CSS, JavaScript, Bootstrap
