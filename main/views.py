import json
import ast
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Compras, Product, produtosCompras, transbank
from django.contrib import messages
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProductForm
from django.http import JsonResponse
from uuid import uuid4  # Para generar IDs únicos de compra
from datetime import datetime
from django.db import models
from transbank.webpay.webpay_plus.transaction import Transaction



# importar dabases compras

# Create your views here.

cart_data = []

def index(request):
    return render(request, 'index.html')

def logros(request):
    return render(request, 'logros.html')

def contacto(request):
    return render(request, 'contacto.html')

def nosotros(request):
    return render(request, 'nosotros.html')

def carrito(request):
    return render(request, 'carrito.html')

def pago(request):
    if request.method == 'POST':
        total = request.POST.get('total', '0.00')  # Recibe el total desde el formulario
    else:
        total = '0.00'  # Valor predeterminado si el método no es POST

    return render(request, 'pago.html', {'total': total})

def seguimiento(request):
    return render(request, 'seguimiento.html')

def exit(request):
    logout(request)
    return redirect('login')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Asunto del correo
            subject = "Nuevo Mensaje de Contacto"
            # Contenido del correo
            message = f"{form.cleaned_data['first_name']} {form.cleaned_data['last_name']} escribió:\n\n{form.cleaned_data['message']}"
            # Correo del remitente (quien envió el mensaje)
            sender = form.cleaned_data['email']
            # Tu correo de destino
            recipients = ['rodrigorios007@gmail.com']  # Cambia esto por tu correo

            try:
                send_mail(subject, message, sender, recipients)
                messages.success(request, "Tu mensaje ha sido enviado correctamente.")
                return redirect('contacto')
            except BadHeaderError:
                messages.error(request, "Se produjo un error al intentar enviar el correo.")
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = ContactForm()

    return render(request, 'contacto.html', {'form': form})

@login_required
def crud(request):
    products = Product.objects.all()  # Obtener todos los productos
    return render(request, 'crud.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            print("Datos válidos:", form.cleaned_data)  # Debug
            form.save()
            messages.success(request, 'Producto agregado exitosamente')
            return redirect('crud')
        else:
            print("Errores del formulario:", form.errors)  # Debug
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente')
            return redirect('crud')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form})

def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Producto eliminado exitosamente')
    return redirect('crud')

def product_list(request):
    products = Product.objects.all()  # Obtén todos los productos de la base de datos
    return render(request, 'productos.html', {'products': products})

def carrito(request):
    # Manejar el carrito exclusivamente desde la sesión
    if request.method == 'POST':
        import json
        # Guardar los datos del carrito en la sesión
        request.session['carrito'] = json.loads(request.body)
        return JsonResponse({'message': 'Carrito recibido correctamente'})

    # Obtener los datos del carrito desde la sesión
    cart_data = request.session.get('carrito', {})
    return render(request, 'carrito.html', {'cart_items': cart_data})

    
def desc_product_front(data):
    cleaned_data = data.strip('"')
    list = ast.literal_eval(cleaned_data)
    return list

def iniciar_pago(request):
    # return 'pipo'
    # if request.method == 'POST':
    # return JsonResponse({'foo':'bar'})
    data = json.loads(request.body)
    # PASAR TODAS LAS VARIABLES DEL FORMULARIO
    nombre = data['nombre']
    rut = data['rut']
    telefono = data['telefono']
    correo = data['correo']
    zona = data['zona']
    direccion = data['direccion']
    total = data['total']
    productos_list = desc_product_front(data['productos'])
    #telefono = data['phone']
    #total = request.GET.get("total", 0)  # Capturar el monto del carrito
    #total = int(total)  # Convertir a entero
    
    
    url_retorno = request.build_absolute_uri('/confirmar_pago/')
    url_final = request.build_absolute_uri('/resultado_pago/')

    # insert data in compras
    
    compra = Compras(
        nombre=nombre,
        rut=rut,
        telefono=telefono,
        correo=correo,
        direccion=direccion,
        costo_envio = 0,
        total=total
    )
    compra.save()
    request.session['compra_id'] = compra.id
    request.session['totalFinal'] = compra.total


    # productos
   
    for item in productos_list:
        product = produtosCompras(
            id_compra = compra.id,
            id_product = item['id'],
            cantidad = item['quantity'],
            precio = item['price'],
            oferta = 0,
            precio_final = item['price'] * item['quantity']
        )
        product.save()
    
    session_id = str(uuid4())[:26]  # O usar datetime.now().strftime('%Y%m%d%H%M%S%f')[:26]

    respuesta = Transaction().create(
        buy_order = str(compra.id),
        session_id = session_id,
        amount = int(total),
        return_url = url_retorno,
    )
    url = respuesta['url'] + '?token_ws=' + respuesta['token']
    
    # INSERTAR EN TBK
    transaccion = transbank(

            fecha = datetime.now(),
            session_id = session_id,
            token = respuesta['token'],
            id_compras = compra.id,
             response_code = '',  
            authorization_code = '',  
            payment_type_code = '',  
            installments_number = 0,  
            installments_amount = 0,  
            card_number = '', 
            total=total,
        )
    transaccion.save()
    return JsonResponse({'mensaje':'success', 'data' :url  })

def confirmar_pago(request):
    # Obtener el token desde los parámetros GET
    token = request.GET.get("token_ws")

    if not token:
        return render(request, 'error.html', {'mensaje': "No se recibió un token válido desde Transbank."})

    try:
        # Confirmar la transacción con Webpay Plus
        respuesta = Transaction().commit(token)
        print(respuesta)
        if respuesta['status'] == 'AUTHORIZED':
            # Si el pago es exitoso, generar un ID de compra único
            
            compra_id = request.session.get('compra_id')
            if not compra_id:
                return render(request, 'error.html', {'mensaje': "No se pudo recuperar el ID de la compra desde la sesión."})
            
            # Actualizar los datos de la transacción
            transaccion = transbank.objects.filter(token=token).first() 
            if transaccion:
                transaccion.response_code = respuesta.get('response_code', '-1')
                transaccion.authorization_code = respuesta.get('authorization_code', '0')
                transaccion.payment_type_code = respuesta.get('payment_type_code', '0')
                transaccion.installments_number = respuesta.get('installments_number', 0)
                transaccion.installments_amount = respuesta.get('installments_amount', 0)
                transaccion.card_number = respuesta.get('card_detail', {}).get('card_number', '0')
                transaccion.save()

            # Obtener datos del carrito y envío desde la sesión
            carrito = request.session.get('carrito', {})

            # Guardar la información de la compra en la sesión para `resultado_pago`
            request.session['compra_exitosa'] = {
                'compra_id': compra_id,
                'carrito': carrito,
                'total': respuesta['amount'],
            }

            # Vaciar el carrito de la sesión después de guardar los datos
            
            return redirect('/resultado_pago/?success=true')
        else:
            return redirect('/resultado_pago/?success=false')
    except Exception as e:
        return render(request, 'error.html', {'mensaje': f"Error al procesar el pago: {str(e)}"})

def resultado_pago(request):
    # Verificar si el pago fue exitoso
    success = request.GET.get('success', 'false') == 'true'

    # Recuperar información de la compra desde la sesión
    compra_exitosa = request.session.pop('compra_exitosa', None)
    if compra_exitosa:
        compra_id = compra_exitosa.get('compra_id')
        print(f"Valor de compra_id recuperado: {compra_id}")  # Bandera para imprimir el valor de compra_id
    else:
        print("No se encontró 'compra_exitosa' en la sesión")
    

    mensaje = "Pago realizado con éxito" if success else "Hubo un error en el pago"
    
    id_compra = compra_exitosa.get('compra_id')
    productos = produtosCompras.objects.filter(id_compra=id_compra)
    cart_items = []
    for producto in productos:
        cart_items.append({
            'name': f"Producto {producto.id_product}",  # Puedes reemplazar con un nombre real si tienes una relación con `Product`
            'quantity': producto.cantidad,
            'price': producto.precio,
            'subtotal': producto.precio * producto.cantidad,
            'total': producto.precio_final
        })
    print(f"Cart items construidos: {cart_items}") 
    total = sum(item['subtotal'] for item in cart_items)
    total_final = request.session.get('totalFinal', None)  # Valor predeterminado si no está definido

    
    return render(request, 'resultado.html', {
        'mensaje': "Pago realizado con éxito" if success else "Hubo un error en el pago",
        'cart_items': cart_items,
        'total': total,
        'vaciar_carrito': True,
        'totalFinal': total_final,
    })


def carrito_view(request):
    # Obtén los productos del carrito desde la sesión
    cart_items = obtener_items_carrito(request)
    
    # Calcula el total asegurándote de que los valores son correctos
    total = sum(item['quantity'] * item['price'] for item in cart_items if item['price'] and item['quantity'])
    
    # Renderiza el template
    return render(request, 'carrito.html', {
        'cart_items': cart_items,
        'total': round(total, 2)  # Redondea a 2 decimales si es necesario
    })

def obtener_items_carrito(request):
    carrito = request.session.get('carrito', {})
    items = []
    for item_id, detalles in carrito.items():
        # Asegúrate de que el precio y la cantidad sean números válidos
        price = float(detalles.get('price', 0))  # Convierte a float, predeterminado a 0 si está vacío
        quantity = int(detalles.get('quantity', 0))  # Convierte a entero
        items.append({
            'id': item_id,
            'name': detalles.get('name', 'Producto desconocido'),
            'price': price,
            'quantity': quantity,
        })
    return items

def tipo_pagos(request):
    payment_types = {
       'VD': 'Venta Débito',
        'VN': 'Venta Norma',
        'VC': 'Venta en cuotas',
        'SI': '3 cuotas sin interés',
        'S2': '2 cuotas sin interés',
        'NC': 'Cuotas sin interés',
        'VP': 'Venta Prepago',
        'NO': 'Cuotas sin interés',  
    }
    return JsonResponse(payment_types)