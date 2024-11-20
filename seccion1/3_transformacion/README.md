# Prueba tecnica Seccion 1: Transformacion de la informacion

## Pasos 
- Ejecutar el script. `python .\seccion1\3_transformacion\transform_data.py`

## Comentarios
**Transformaciones que se tuvieron que realizar**:
- Se tuvieron que renombrar las columnas `name` y `paid_at`
- Se transformaron los tipos de datos de todas las columnas al igual que el tipo de caracteres maximos permitidos.
- Se validaron los valores de `amount` que no exedieran de los 16 digitos.


**Algunos de los retos que obtuve al realizar las transformaciones fueron**:
- La columna `created_at` contenia valores nulos y en el ejercicio se pedia que fuera NOT NULL, por lo que necesite agregar la fecha y hora actual de los registros vacios.
- Al agregar los valores de la columna amount algunos datos excedian el limite permitido que se habia asignado, por lo que se implemento una validacion para asegurar que esos valores no excedieran el limite permitido.
- Al intentar cambiar los campos `updated_at, created_at` con uso de pandas los valores NaT causaban error al insertar en la base de datos porque se reemplazaron a None.
- Cuando se intento insertar los datos a la tabla creada al principio se utilizo un metodo llamado `to_sql` pero se quedaba trabajo el script al momento de ejecutarse, por lo que se opto por utilizar `psycopg2` y `execute_values` para optimizar la insercion de los mismos.
