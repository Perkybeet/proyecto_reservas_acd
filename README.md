# Proyecto Reservas ACD

Esta aplicación gestionará la base de datos de un restaurante, permitiendo el acceso exclusivo a los empleados. La aplicación se centra en tres aspectos principales:

- **Clientes**
- **Mesas**
- **Reservas**

## Funcionalidades Clave

- **Gestión de Clientes:** Permite registrar, actualizar y consultar información de clientes.
- **Gestión de Mesas:** Administra el estado y la disponibilidad de las mesas del restaurante.
- **Gestión de Reservas:** Facilita la creación, modificación y cancelación de reservas, asignando mesas y gestionando horarios.

## Seguridad y Acceso

El acceso a la aplicación está restringido únicamente a los empleados del restaurante. Para ingresar, se deben utilizar las siguientes credenciales:

- **Usuario:** `admin`
- **Contraseña:** `admin`

## Flujo de Inicio de Sesión

1. Al iniciar la aplicación, se presenta una pantalla de login.
2. El usuario ingresa sus credenciales (usuario y contraseña).
3. Si las credenciales son correctas, se redirige al usuario al **Main View** de la aplicación, donde puede gestionar clientes, mesas y reservas.
4. Si las credenciales son incorrectas, se muestra un aviso al usuario indicando que el acceso no fue autorizado.

## Arquitectura General

La aplicación está desarrollada utilizando **Flet**, lo que permite crear interfaces gráficas para la gestión de datos en tiempo real. La arquitectura se compone de vistas modulares para cada sección de la aplicación (por ejemplo, `main_view` para la vista principal) y utiliza un diccionario para la validación de credenciales en el inicio de sesión.

## Tecnologías Utilizadas

- **Python:** Lenguaje de programación principal.
- **Flet:** Framework para construir aplicaciones de escritorio con interfaces de usuario modernas.
- **Base de Datos:** Se usa un gestor "mongodb" para almacenar la información de clientes, mesas y reservas.

## Dependencias

- **Pymongo:**
- **Flet**
- **Pydantic**
