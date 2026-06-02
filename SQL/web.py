from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
import pymysql as ps 
import secrets



def conexion():
    return ps.connect(host='127.0.0.1',
                      port=4306,
                      user='root',
                      password='',
                      db='persevera')


app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

@app.route('/')
def Index():
    return render_template('Index.html')

################################################# CONSULTAS ########################################################################

@app.route('/Proveedores_consulta')
def proveedoresc():
    conn = conexion()
    cursor = conn.cursor()
    # Consulta SQL para obtener los nombres de los proveedores
    cursor.execute("SELECT Nombre FROM proveedor")
    proveedores = cursor.fetchall()
    conn.close()
    return render_template('Proveedores_consulta.html', proveedores=proveedores)

@app.route('/get_invoices')
def get_invoices():
    proveedor = request.args.get('proveedor')

    conn = conexion()
    cursor = conn.cursor()
    # Consulta SQL para obtener los números de factura asociados al proveedor seleccionado
    cursor.execute("SELECT factura_de_compra.Número_Factura_Compra FROM factura_de_compra,proveedor WHERE factura_de_compra.RUT_Proveedor = proveedor.RUT_Proveedor AND proveedor.Nombre=%s", (proveedor,))
    invoices = cursor.fetchall()
    conn.close()
    # Devolver los números de factura como una lista JSON
    return jsonify({'invoices': [invoice[0] for invoice in invoices]})
@app.route('/get_invoice_info')
def get_invoice_info():
    numero_factura = request.args.get('numero_factura')

    conn = conexion()
    cursor = conn.cursor()
    # Consulta SQL para obtener los detalles de la factura según el número de factura
    cursor.execute("SELECT proveedor.Nombre,factura_de_compra.Fecha_Factura_Compra,factura_de_compra.Total_Factura_Compra FROM proveedor,factura_de_compra WHERE Número_Factura_Compra = %s AND proveedor.RUT_proveedor=factura_de_compra.RUT_proveedor", (numero_factura,))
    factura_info = cursor.fetchone()
    conn.close()

    # Devolver los detalles de la factura como un objeto JSON
    return jsonify({
        'proveedor': factura_info[0],
        'fecha': factura_info[1],
        'monto': factura_info[2],
    })
@app.route('/get_invoice_products')
def get_invoice_products():
    numero_factura = request.args.get('numero_factura')
    conn = conexion()
    cursor = conn.cursor()
    # Consulta SQL para obtener los productos comprados según el número de factura
    cursor.execute("SELECT Nombre_Producto,Precio_Compra,Cantidad FROM producto WHERE Número_Factura_Compra = %s", (numero_factura,))
    products = cursor.fetchall()
    conn.close()
    # Devolver los productos como una lista JSON
    return jsonify({'products': [{'nombre': product[0], 'precio': product[1], 'cantidad': product[2]} for product in products]})

@app.route('/redireccionar_proveedoresc')
def redireccionar_proveedoresc():
    return redirect('/Proveedores_consulta')

@app.route('/Clientes_consulta')
def clientesc():
    conn = conexion()
    cursor = conn.cursor()
    # Consulta SQL para obtener los nombres de los proveedores
    cursor.execute("SELECT Nombre_Cliente FROM cliente")
    clientes = cursor.fetchall()
    conn.close()
    return render_template('Clientes_consulta.html', clientes=clientes)
@app.route('/clientes_facturas')
def clientes_facturas():
    cliente = request.args.get('cliente')
    conn = conexion()
    cursor = conn.cursor()
    # Consulta SQL para obtener los números de factura asociados al proveedor seleccionado
    cursor.execute("SELECT factura_de_venta.Número_Factura_Venta FROM factura_de_venta,cliente WHERE factura_de_venta.RUT_Cliente = cliente.RUT_Cliente AND cliente.Nombre_Cliente=%s", (cliente,))
    facturascl = cursor.fetchall()
    conn.close()
    # Devolver los números de factura como una lista JSON
    return jsonify({'invoices': [facturacl[0] for facturacl in facturascl]})
@app.route('/clientes_facturas_info')
def clientes_facturas_info():
    numero_factura = request.args.get('numero_factura')

    conn = conexion()
    cursor = conn.cursor()
    # Consulta SQL para obtener los detalles de la factura según el número de factura
    cursor.execute("SELECT cliente.Nombre_Cliente,factura_de_venta.Fecha_Venta,factura_de_venta.Utilidades FROM cliente,factura_de_venta WHERE Número_Factura_Venta = %s AND cliente.RUT_Cliente=factura_de_venta.RUT_Cliente", (numero_factura,))
    factura_info = cursor.fetchone()
    conn.close()

    # Devolver los detalles de la factura como un objeto JSON
    return jsonify({
        'cliente': factura_info[0],
        'fecha': factura_info[1],
        'utilidad': factura_info[2],
    })

@app.route('/redireccionar_clientesc')
def redireccionar_clientesc():
    return redirect('/Clientes_consulta')

@app.route('/Compras_consulta')
def comprasc():
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT Nombre_Producto FROM producto")
    productos = cursor.fetchall()
    conn.close()

    return render_template('Compras_consulta.html', productos=productos)

@app.route('/search_products')
def search_products():
    query = request.args.get('query')

    conn = conexion()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT producto.Nombre_Producto,proveedor.Nombre,producto.Precio_Compra, factura_de_compra.Fecha_Factura_Compra,factura_de_compra.Número_Factura_Compra, producto.Cantidad FROM producto,proveedor,factura_de_compra WHERE producto.Nombre_Producto LIKE %s AND proveedor.RUT_Proveedor=factura_de_compra.RUT_Proveedor AND producto.Número_Factura_Compra=factura_de_compra.Número_Factura_Compra",
        ('%' + query + '%',)
    )
    products = cursor.fetchall()
    conn.close()

    return jsonify({
        'products': [
            {
                'nombre': product[0],
                'proveedor': product[1],
                'precio_compra': product[2],
                'fecha_compra': product[3],
                'Numero_factura': product[4],    
                'Cantidad': product[5]
            }
            for product in products
        ]
    })
@app.route('/redireccionar_comprasc')
def redireccionar_comprasc():
    return redirect('/Compras_consulta')

@app.route('/Utilidades_consulta')
def utilidad() -> None: 
    return render_template('Utilidad_consulta.html')

@app.route('/calcular_utilidades')
def calculo_utilidades():
    fecha_inicio = request.args.get('fechaInicio')
    fecha_termino = request.args.get('fechaTermino')
    conn = conexion()
    cursor = conn.cursor()
    # Consulta SQL para calcular las utilidades totales entre las fechas especificadas
    cursor.execute("SELECT SUM(Utilidades) FROM factura_de_venta WHERE Fecha_Venta BETWEEN %s AND %s", (fecha_inicio, fecha_termino))
    utilidades = cursor.fetchone()[0]
    utilidades_str=str(utilidades)
    print(utilidades_str)
    conn.close()

    return jsonify({'utilidades': utilidades_str})

@app.route('/inventario')
def inventario():
    conn = conexion()
    cursor = conn.cursor()

    # Consulta SQL para obtener el inventario de productos con la cantidad actual
    cursor.execute("""
        SELECT
            p.Nombre_Producto,
            COALESCE(p.Cantidad, 0) - COALESCE(v.Cantidad_Vendida, 0) AS Cantidad_Actual,
            MAX(p.Precio_Venta) AS Precio_Venta_Maximo
        FROM
            (SELECT Nombre_Producto, SUM(Cantidad) AS Cantidad, MAX(Precio_Venta) AS Precio_Venta
             FROM producto GROUP BY Nombre_Producto) p
            LEFT JOIN
            (SELECT Nombre_Producto, SUM(Unidades) AS Cantidad_Vendida
             FROM aparece_en_venta GROUP BY Nombre_Producto) v
            ON p.Nombre_Producto = v.Nombre_Producto
        GROUP BY
            p.Nombre_Producto
    """)
    inventario = cursor.fetchall()
    conn.close()

    return render_template('inventario.html', inventario=inventario)

@app.route('/buscar_productos')
def buscar_productos():
    nombre_producto = request.args.get('nombre_producto')

    conn = conexion()
    cursor = conn.cursor()

    # Consulta SQL para obtener los nombres de productos que coinciden con la búsqueda
    cursor.execute("SELECT Nombre_Producto FROM producto WHERE Nombre_Producto LIKE %s", (f'%{nombre_producto}%',))
    productos = cursor.fetchall()
    conn.close()

    # Extraer los nombres de productos de la lista de resultados
    nombres_productos = [producto[0] for producto in productos]

    return jsonify({'productos': nombres_productos})


###########################################################################################################################################

@app.route('/registroproveedor')
def muestraregistroproveedor():
    return render_template('registroproveedor.html')

@app.route('/anadir_proveedor', methods=['POST'])
def anadir_proveedor():
    if request.method == 'POST':
        RUTProveedor = request.form['RUTProveedor']
        Nombre = request.form['Nombre']
        direccion = request.form['direccion']
        correoelectronico = request.form['correoelectronico']
        telefono = request.form['telefono']
        cunn=conexion()
        cur = cunn.cursor() 
        cur.execute('INSERT INTO proveedor (RUT_Proveedor, Nombre, dirección, Correo_Electrónico, teléfono) VALUES (%s, %s, %s, %s, %s)', (RUTProveedor, Nombre, direccion, correoelectronico, telefono)) 
        cunn.commit() 
        flash('Contacto añadido satisfactoriamente.')
        return redirect('/registroproveedor')



@app.route('/registrocompra')
def muestraregistrocompra():
    conn = conexion()
    cursor = conn.cursor()
    # Consulta SQL para obtener los nombres de los proveedores
    cursor.execute("SELECT Nombre FROM proveedor")
    proveedores = cursor.fetchall()
    conn.close()
    return render_template('registrarcompra.html',proveedores=proveedores)

@app.route('/add_compra', methods=['POST'])
def add_compras():
    numero_factura = request.form['numero_factura']
    fecha_compra = request.form['fecha_compra']
    proveedor = request.form['proveedor'].replace("('", "").replace("',)", "")
    cantidad_productos = int(request.form['cantidad_productos'])

    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT RUT_Proveedor FROM proveedor WHERE Nombre = %s", (proveedor,))
    rut_proveedor = cursor.fetchone()[0]
    # Insertar la factura en la tabla 'factura_de_compra'
    cursor.execute("INSERT INTO factura_de_compra (Número_Factura_Compra, RUT_Proveedor, Fecha_Factura_Compra)    VALUES (%s, %s, %s)",
                   (numero_factura, rut_proveedor, fecha_compra))
    
    # Insertar los productos en la tabla 'producto'
    for i in range(1, cantidad_productos + 1):
        nombre_producto = request.form['nombre_producto_' + str(i)]
        precio_compra = float(request.form['precio_compra_' + str(i)])
        precio_venta = float(request.form['precio_venta_' + str(i)])
        cantidad = int(request.form['cantidad_' + str(i)])
        
        cursor.execute("INSERT INTO producto (Nombre_Producto, Número_Factura_Compra, Precio_Compra, Precio_Venta, Cantidad) VALUES (%s, %s, %s, %s, %s)",
                       (nombre_producto, numero_factura, precio_compra, precio_venta, cantidad))
    
    conn.commit()
    conn.close()
    
    return redirect('/')

@app.route('/registrocliente')
def muestraregistrocliente():
    return render_template('registrarcliente.html')

@app.route('/anadir_cliente', methods=['POST'])
def anadir_cliente():
    if request.method == 'POST':
        RUT_Cliente = request.form['RUT_Cliente']
        Nombre_Cliente = request.form['Nombre_Cliente']
        Dirección_Cliente = request.form['Dirección_Cliente']
        Teléfono_Cliente = request.form['Teléfono_Cliente']
        cunn=conexion()
        cur = cunn.cursor() 
        cur.execute('INSERT INTO cliente (RUT_Cliente, Nombre_Cliente, Dirección_Cliente, Teléfono_Cliente) VALUES (%s, %s, %s, %s)', (RUT_Cliente, Nombre_Cliente, Dirección_Cliente, Teléfono_Cliente)) 
        cunn.commit() 
        flash('Cliente añadido correctamente.')
        return redirect('/registrocliente')
        
if __name__ == '__main__':
    app.run(port = 3000, debug = True)