# GestionAPP
## Que es?
GestionApp es una aplicación desarrollada en Python bajo el enfoque de programación orientada a objetos, diseñada para facilitar la gestión de negocios pequeños y medianos. Su objetivo es facilitar la administración de tiendas, productos y ventas en una herramienta sencilla y eficaz.
## Funcionalidades
### 🏪 Gestión de tiendas

El usuario puede agregar, editar o eliminar tiendas, permitiendo organizar distintos negocios dentro de la misma aplicación.

### 📦 Gestión de productos

Dentro de cada tienda es posible administrar productos: imagen, nombre, precio, stock y ubicación. Esto permite mantener un control actualizado del inventario.

### 🧾 Facturación y registro de ventas

Incluye un módulo de facturación que permite generar ventas y consultar el historial completo de transacciones realizadas, facilitando el seguimiento financiero del negocio.

### 🤖 Chatbot integrado

La aplicación cuenta con un chatbot asistente capaz de responder preguntas sobre el estado del negocio, como productos con bajo stock, cantidad de ventas generadas, información sobre tiendas y más, ayudando al usuario a tomar decisiones rápidas.

## 📥 Instalación

Requisitos previos:

Tener instalado Python 3.9 o superior (se recomienda 3.13).

Abrir una ventana de terminal o CMD para ejecutar los siguientes comandos.

Ejecuta estos comandos en tu terminal:

    python -m ensurepip --upgrade
    pip install firebase-admin
    pip install supabase
    pip install customtkinter
    pip install PySDL2 pysdl2-dll==2.26.5
    pip install openai
    pip install Pillow


Nota:

Igualmente declarar la variable de entorno que viene en el archivo Manual De Backend.pdf

Tkinter ya viene incluido con la instalación estándar de Python, no requiere instalación adicional.

Se recomienda usar un entorno virtual para evitar conflictos con otras librerías.

Ejecutar la aplicación

    python main.py

## Uso

Tras ejecutar la aplicacion saldra una pantalla de carga que durara unos segundos, posteriormente se abrira una ventana donde podra seleccionar crear una cuenta nueva.
Entonces se le pedira que llene los campos para poder crear su cuenta.

<img width="750" alt="image" src="https://github.com/user-attachments/assets/0fb43aa1-e14b-4caf-ba87-96d0555dc016" />

Tras el registro sera redirigido otra vez a la ventana de inicio de sesion, donde tendra que ingresar su correo y contraseña.

Una vez hecho, pasara a la ventana principal de la aplicacion, utilice la barra lateral para desplazarse a travez de la app.

<img width="750" alt="image" src="https://github.com/user-attachments/assets/8e998a73-e13f-4aa4-9e04-55ff26164d8e" />

En el apartado de tiendas, podra gestionar sus tiendas, tras registrar una usando el boton de "Nueva Tienda", podria usar el boton de 3 puntos lateral, para interactuar con la misma.
Tras esto podria modificarla o visualizar sus productos

<img width="750" height="637" alt="image" src="https://github.com/user-attachments/assets/9148bc1a-6994-459c-9ce1-87e7a4db19f9" />

El apartado de productos sigue la misma logica, podra agregar y luego gestionar sus prodcutos, e igualmente se hara uso del menu emergente al presionar el boton de los 3 puntos.



En el apartado de 'Facturar' encontrara la opcion de "Nueva Factura", se le pedira que seleccion ua tienda, un producto y la cantidad a facturar. Tras seleccionar oprima el boton de "Agregar".

Si desea cambiar lo que puso, oprima "Quitar" y agregue el producto nuevamente

Si eso es todo oprima el boton de "Facturar"

Tras esto (Si hay Stock) se resgitrara la venta y podra ver la factura en el apartado de facturas. La cual se guardara en su respectiva tienda y vera su nombre asociado a la fecha, podra visulizar la factura donde vera que fue lo que se vendio exactamente, el momento y un codigo de venta

<img width="554" height="663" alt="image" src="https://github.com/user-attachments/assets/620f3787-5457-4bd2-afc6-2615b7f73b84" />


<img width="567" height="696" alt="image" src="https://github.com/user-attachments/assets/92a6c12f-168f-4758-aa1e-7d5b3546de4a" />


En el apartado de chatbot vera una caja de texto y una entrada de texto, a travez de las cuales se comunicara con el bot para las cosas que necesite.






  
