Configuración del Entorno Virtual y Ejecución del Proyecto

video de ayuda para la creacion del entorno vitual 

https://www.youtube.com/watch?v=Fo-jkW8rPs8

Instala virtualenv si aún no lo tienes instalado:
Copiar código

-> pip install virtualenv

Crea un entorno virtual en tu directorio de proyecto:
bash
Copiar código
-> virtualenv env


Activación del Entorno Virtual:
Desde la línea de comandos (cmd), activa el entorno virtual:
bash
Copiar código

-> .\env\Scripts\activate

Instalación de Dependencias:
Asegúrate de tener un archivo requirements.txt que liste las dependencias necesarias para tu proyecto. Luego, instálalas con el siguiente comando:
Copiar código

-> pip install -r requirements.txt

Inicio del Proyecto Flask:
Ejecuta el siguiente comando para iniciar tu aplicación Flask:
Copiar código

-> python app.py

Acceso a la Aplicación:

Abre un navegador web y visita http://localhost:5000 para ver tu aplicación Flask en funcionamiento.

Para desactivar el entorno virtual cuando hayas terminado de trabajar en tu proyecto:

Desde la línea de comandos (cmd), simplemente ejecuta el siguiente comando:
Copiar código

-> deactivate

Esto restaurará tu entorno de Python al estado anterior a la activación del entorno virtual