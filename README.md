# Expense Tracker

Este archivo presenta una guía completa para el proyecto Expense Tracker, una API construida sobre FastAPI para rastrear y gestionar finanzas personales. Ofrece funcionalidades para la gestión de cuentas, transacciones, categorías y autenticación de usuarios.

## Características principales

- **Gestión de cuentas**: Creación y gestión de cuentas financieras.
- **Gestión de categorías**: Creación y organización de ingresos y gastos en categorías personalizables.
- **Transacciones**: Registro y seguimiento de transacciones bajo cuentas y categorías específicas.
- **Autenticación**: Soporte para la autenticación de usuarios y administración de acceso seguro.

## Tecnologías utilizadas

Este proyecto utiliza las siguientes tecnologías y bibliotecas:

- [FastAPI](https://fastapi.tiangolo.com/): Para construir una API rápida y con documentación interactiva.
- [SQLAlchemy](https://www.sqlalchemy.org/): Como ORM para interactuar de manera eficiente con bases de datos.
- [Alembic](https://alembic.sqlalchemy.org/): Para la migración de bases de datos.
- [Pytest](https://pytest.org/): Utilizado para las pruebas unitarias y de integración.

## Estructura del proyecto

El proyecto está estructurado de la siguiente manera:

- `./app`: Contiene todo el código fuente, incluidos modelos, rutas y servicios.
- `./tests`: Almacena pruebas unitarias y de integración para garantizar la robustez del proyecto.
- `requirements.txt`: Lista de todas las dependencias necesarias para el proyecto.
- `.env`: Archivo para definir variables de entorno (se proporciona como ejemplo).

## Cómo empezar

Asegúrate de tener Python 3.8 o superior instalado en tu sistema. Para instalar el proyecto y sus dependencias, sigue estos pasos:

1. Clona el repositorio del proyecto.
2. Crea un entorno virtual:

```bash
python -m venv venv
```

3. Activa el entorno virtual:

- En Windows:

```cmd
venv\Scripts\activate
```

- En UNIX o MacOS:

```bash
source venv/bin/activate
```

4. Instala las dependencias:

```bash
pip install -r requirements.txt
```

5. Inicia el servidor:

```bash
uvicorn run:server --reload
```

Visita `http://127.0.0.1:8000/docs` en tu navegador para acceder a la documentación y probar la API.

## Contribuir

Si deseas contribuir a este proyecto, por favor sigue las siguientes recomendaciones:

- Haz fork y clona el repositorio.
- Crea una rama nueva para tu característica o corrección de errores.
- Efectúa tus cambios de manera limpia y asegúrate de agregar pruebas si es necesario.
- Envía un pull request con tus cambios.

## Licencia

Este proyecto está bajo la licencia MIT. Para más detalles, consulta el archivo `LICENSE` en el repositorio.