PostgreSQL

Será nuestro Data Warehouse.

Persistirá la información transformada.

MinIO

Será nuestro Data Lake.

Aquí guardaremos los archivos originales.


Primer uso

docker compose \
-f docker-compose.yml \
-f docker-compose.bootstrap.yml \
up --build

Uso diario

docker compose up -d

Se agrega Makefile

Primera ejecución

1. make bootstrap

Luego make up 



Vamos a responder preguntas como:

¿Qué representa cada archivo?
¿Qué entidad del negocio modela?
¿Qué relaciones existen?
¿Qué datos llegarían en tiempo real?
¿Qué datos son catálogos estáticos?
¿Qué datos deberían ir al Data Lake?
¿Qué datos deberían terminar en el Data Warehouse?

Eso es exactamente el trabajo que hace un Data Engineer antes de construir un pipeline.


Data Generator

Este componente va a simular el sistema POS (Point of Sale) de una cadena de supermercados. En una empresa, este flujo normalmente vendría de Kafka, RabbitMQ o directamente desde los sistemas de caja. Nosotros lo simularemos leyendo el histórico y publicando pequeños lotes.