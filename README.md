# Test de Back-End para Enviame.

### Descripción

Proyecto de dos microservicios comunicados desarrollado en Python con Flask, SQL Alchemy y Docker.

En el proyecto he utlizado el template proporcionado por Enviame, basado en principios fundamentales del libro Arquitectura Limpia.

Cada servicio cuenta con su propia base de datos.

En el proyecto, contamos con dos microservicios, el de "ecommerce-service" y el de "delivery-service".

### Construcción 🛠️
* **Lenguaje:** Python 3
* **Framework:** Flask, SQL Alchemy

## Requisitos
- Docker instalado.

## Instalación y ejecución:

- Clone o descargue el proyecto.
- Copiar **.env.example** a **.env**. Se utilizará como fuente de variables de entorno.
- Dentro de las carpetas Docker/app de ecommerce-service y delivery-services:
* Copie **.env.example** a **.env**. Se utilizará como fuente de variables de entorno.

Ejecute el comando ```docker-compose``` dentro de la carpeta **docker-python**.

* Construir los contenedores: ```docker-compose build```

* Inicializar los servicios: ```docker-compose up -d```

* Detener los servicios: ```docker-compose stop```

De forma predeterminada, los microservicios se ejecutarán en los siguientes puertos:
- ecommerce-service: 8000
- delivery-service: 8001

#### Nota:
La aplicación Flask probablemente lanzará una excepción la primera vez, porque intentará conectarse al servicio MySQL que aún se está inicializando por primera vez; en este caso, espere a que MySQL se inicialice por completo primero y luego ejecute los comandos: 
`docker-compose restart ecommerce-app` y `docker-compose restart delivery-app` en otra terminal para reiniciar los servicios bloqueados.

### Probar la aplicación:
Para probar los endpoints basta con entrar al archivo req.http dentro de cada carpeta de los servicios, para ello debe tener instalado en su editor de código un cliente REST(por ejemplo **REST Client**, para Visual Studio Code).

### Endpoints creados:
- Creación de usuarios(administrador, vendedor, usuario del mercado).
- CRUD de las empresas.
- CRUD de los vendedores.
- CRUD de los productos.
- CRUD de las órdenes de compras.
- CRUD de las entregas.

### Observaciones:
1. He utilizado autenticación por JWT(JSON Web Tokens) para el login. 
2. He creado decoradores para identificar qué tipos de usuarios son los autorizados para utilizar los endpoints.
3. Si el estado de una órden de compra es cambiado a "confirmado", se resta automáticamente la cantidad del producto introducida en la orden de compra, de la base de datos.
4. La orden de compra solo se puede cancelar(borrar) si el estado de la misma es "creado" o "confirmado".
5. Al cancelar una orden de compra se incrementa automaticamente el producto que había sido disminuido en la base de datos.
6. Si el estado de una orden se cambia a "enviado", el microservicio de ecommerce se comunica con el microservicio de delivery creando el objeto de entrega con los respectivos datos de la orden de compra.
4. Para completar la aplicación me faltó implementar la relación entre una empresa y sus vendedores, así también la relación entre una empresa y los productos de la misma. Por el lado del microservicio de entregas me faltó implementar la función de cambio de estado de las entregas, tengo entendido que lo podría realizar como un task hecho con Celery para correr la función cada 30 segundos y así cambiar el estado, y por último realizar la notificación al microservicio de ecommerce de que el pedido ya fue entregado, pero por falta de tiempo ya no lo pude realizar.

### Testing ⚙️
En esta ocación por falta de tiempo no pude implementar los test unitarios para el proyecto.
