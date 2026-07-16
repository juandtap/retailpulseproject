### PostgreSQL

Será nuestro Data Warehouse.

Persistirá la información transformada.

### MinIO

Será nuestro Data Lake.

Aquí guardaremos los archivos originales.

### Ejecución 

Primer uso

``` 
docker compose \
-f docker-compose.yml \
-f docker-compose.bootstrap.yml \
up --build
 ```

Uso diario

```
docker compose up -d

```

Se agrega Makefile

Primera ejecución

1. make bootstrap

2. Luego make up 



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

Notas:

El estado solo debe actualizarse cuando la operación fue exitosa.

En producción nunca se guardan credenciales en un .env del repositorio.

Se usan:

Kubernetes Secrets
HashiCorp Vault
AWS Secrets Manager
Azure Key Vault
Google Secret Manager

Nosotros simularemos ese escenario más adelante.

- Migrar Logs a carpeta general 
- Cambiar nombre de rama de MASTER a "OTRONOMBRE" y crear otra rama SPARK cuando pasemos a implementar con Spark.
- mejorar stados de carga de batch usando archivos temporales (tempfile)
- Cambiar temporalmente la variable MINIO_ENDPOINT a localhost:9000, cuando se dockerize el servicio de python se coloca como estaba antes
- orque el índice es un detalle interno del BatchGenerator.

    Si algún día cambiamos:

    Pandas → Spark
    CSV → Kafka
    Batch fijo → Streaming

    ese índice dejaría de tener sentido.

    En una buena arquitectura, el estado no debería depender de la implementación interna.

    Que pasa si el archivo pesa demasiado se sigue usando pd.readcsv() ? -> usar polaris

    considerar en un futuro dos ramas una para pandas y otra para spark o usar un .env con

    ```
    PROCESSING_ENGINE=pandas

    o

    PROCESSING_ENGINE=spark
    
    ```

    en 

    ``` 
    reader = DataReaderFactory.create(
        engine=settings.processing_engine
    )
    ```