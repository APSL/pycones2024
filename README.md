# README.md


## Al acabar este taller habrás aprendido...

* A levatar una API RESTful con django-rest-framework.
* La importancia de aplicar un sistema de auteticación a tú API y las diferencias entre el nativo de drf y knox.
* Generar tests de tus edpoints con pytest.
* Cómo generar documentación para tú API co OpenAPI.
* Aplicar técnicas de versionado de API.


## Requisitos previos

* Conocer las bases de la programación.
* Disponer de un IDE.
* Python 3.9+

## Diapositivas del taller

[link a las diapositivas del taller](https://docs.google.com/presentation/d/1NUa9EKM1aPK_KSGx1ESXvX1K_5BZ9SCVoFV7NXkpZsI/edit?usp=sharing)


## Instalación

1. Descargamos el proyecto del repositorio.
    ```bash
    mkdir pycon_workspace
    cd pycon_workspace
    git clone git@github.com:APSL/pycones2024.git
    ```

2. Instalamos dependencias. Tenemos formas de hacerlo.
    ```bash
    pip install -r requirements.txt
    ```

    ```bash
    pipenv install --dev
    ```

3. Creamos y poblamos la base de datos.
    ```bash
    cd src
    python manage.py migrate
    python manage.py syncdata initial_data.json
    ```

4. Verificar que el proyecto se puede ejecutar.
    ```bash
    python manage.py runserver 
    ```
  
5. Visita tú web! Dispones de los usuarios `admin`, `Clerk` y `Courier`, todos con el password `superseguro`.

* http://localhost:8000/admin
* http://localhost:8000/schema/
