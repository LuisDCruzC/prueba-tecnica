## Requisitos previos
- **Tener instalador `Docker` y `python`**

## Configuracion inicial
- Abrir terminal de powershell en la raiz del proyecto.
- Ejecutar `docker-compose up -d` para iniciar el contenedor de PostgreSQL.
- Crear un entorno virutal (opcional) con: `python -m venv venv`
- Activar el entorno virtual en windows: `.\venv\Scripts\Activate`
                     o en macOS / linux: `source venv/bin/activate`

- Instalar las dependencias: `pip install -r requirements.txt`

## Seccion 1
-  Cuenta con 5 carpetas dentro de la seccion y cada una cuenta con un README para responder adecuadamente a lo que se solicito en el archivo word. De igual forma cuenta con los pasos para ejecutar cada uno de los scripts.

- [Carga de información](seccion1/1_carga_informacion/README.md)
- [Extracción de información](seccion1/2_extraccion/README.md)
- [Transformación de información](seccion1/3_transformacion/README.md)
- [Dispersión de información](seccion1/4_dispersion_informacion/README.md)
- [SQL](seccion1/5_sql/README.md)

## Seccion 2
- Cuenta con el api integrada y de igual manera cuenta con su propio README para conocer los pasos para correr el API.

- [API](seccion2/README.md)