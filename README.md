# widgetweb_hogares_etb

**Autor:** Ramón Dario Rozo Torres 09 de Enero de 2025
**Última Modificación:** Ramón Dario Rozo Torres 09 de Enero de 2025  
**Versión:** 1.0.0

## Descripción

Widget con chat web para la atención del segmento hogares de ETB (Pruebas).

## Instalación

```bash
    1.  Clonar repositorio (https://repo.groupcos.com/rpa/widgetweb_hogares_etb).

    2.  Entrar a la carpeta raiz del proyecto.

    3.  Instalar dependencias del proyecto de la siguiente manera:
        
        •   cd ChatWeb/Autenticacion
                npm i o  npm install
        •   cd ChatWeb
                npm i o  npm install
        •   cd ChatWeb/python
            *   Crear entorno virtual de python:
                    python3 -m venv venv
            *   Activar entorno virtual de python:
                    source venv/bin/activate
            *   Instalar las dependencias del proyecto:
                    pip3 install -r requirements.txt

            *   Para instalar paquetes necesarios que no estan en el archivo requirements.txt
                    pip3 install paquete1
                    pip3 install paquete2
                    ...
            
                Nota: Genere el archivo requirements.txt con el comando pip3 freeze > requirements.txt

    4.  Configurar variables de entorno:
        •   Backend
            *   Copiar el archivo .env.example y dejarlo como .env (cp .env.example .env).
                -   Digitar los datos solicitados en la estructura del archivo
                -   Guardar el archivo .env

        •   Frontend
            *   Ubicarse en la ruta cd ChatWeb/src/public/js
                -   Copiar el archivo env.js.example y dejarlo como env.js (cp env.js.example env.js).
                -   Digitar los datos solicitados en la estructura del archivo
                -   Guardar el archivo env.js

        •   Widget
            *   Ubicarse en la ruta cd ChatWeb/src/public/dist/js
                - En el archivo widget-chat.js configurar las variables globales para alcance externo.

    5.  Levantar base de datos ejecutando el codigo que se encuentran en la carpeta migrations.
        •   Ubicarse en la ruta cd ChatWeb/migrations
            *    Defina en el archivo 2024_12_12_create_database.sql la base de datos sobre la que se va a trabajar.

        •   Ejectuar los siguientes archivos:
            *   Primero ejecute el codigo del archivo en la ruta migrations/chat/2024_12_12_create_tbl_chat.sql
            *   Segundo ejecute el codigo del archivo en la ruta migrations/mensaje/2024_07_21_create_tbl_mensaje.sql

    6.  Cargar la data inicial de la base de datos que se encuentra en la carpeta seeds.
        •   Ubicarse en la ruta cd ChatWeb/seeds
            *  Por ahora no hay data que se deba tener en cuenta para inicializar el proyecto.

    *   Nota: La carpeta (cd ChatWeb/docs) docs debe tener permisos totales ya que en esta se guardan los archivos adjuntos desde el chat.

```

## Uso

```bash
1.  Iniciar servicios y aplicaciones ambiente de desarrollo.

    •   cd ChatWeb/Autenticacion
        npm run dev

    •   cd ChatWeb
        npm run dev

    •   cd ChatWeb/python
        Activar entorno virtual de python:
            source venv/bin/activate
        Ejecutar el archivo ChatWebHook.py:
            python3 ChatWebHook.py


2.  Iniciar servicios y aplicaciones ambiente de producción.

    •   cd ChatWeb/Autenticacion
        npm run prod

    •   cd ChatWeb
        npm run prod

    •   cd ChatWeb/python
        Activar entorno virtual de python:
            source venv/bin/activate
        Ejecutar el archivo ChatWebHook.py:
            python3 ChatWebHook.py

Nota: Para iniciar el widget debes primero levantar estos servicios y luego abrir el archivo widget.html en un navegador garantizando que se vinculen tanto el css (url_chat_web/dist/css/widget-chat.css) como el js (url_chat_web/dist/js/widget-chat.js).

```

## Acceso

```bash
    1.  Ambiente de pruebas
            https://XXXXXXXXX

    2.  Ambiente de produccion
            https://XXXXXXXXX

    3.  Autenticacion
            *   No aplica

```

## Modulos - permisos

```bash
    1.  WIDGET CHAT WEB TIEMPO REAL
        •   Arbol de atencion.

```

## Contribuyendo

Si deseas contribuir al proyecto, por favor sigue los siguientes pasos:

1. Desde la rama master, crea una rama nombre_tu_rama.
2. Clone el proyecto desde el repositorio oficial y rama master.
3. Crea una rama para tu funcionalidad (`git checkout -b nombre_tu_rama`).
4. Realiza un commit de tus cambios (`git commit -m 'Mensaje de commit...'`).
5. Sube los cambios al repositorio (`git push origin nombre_tu_rama`)
6. Solicita un merge a la rama quality.
7. Si el merge es exitoso, solicita un merge a la rama master desde la rama quality.
8. Solicita el deploy de la rama master.

## Licencia

Todos los derechos reservados a Montechelo.