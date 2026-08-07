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


Un concepto que después podemos introducir en RetailPulse:

    -Data Contract


NIVEL 1 — GENÉRICO
──────────────────
MinIOUploader
ParquetSerializer
StateManager
Logging
Retry
Config

NIVEL 2 — CONFIGURABLE
──────────────────────
CsvDatasetReader
Schema validation
Partition builder

NIVEL 3 — ESPECÍFICO DEL NEGOCIO
────────────────────────────────
Sales transformations
Holiday logic
Promotion features
Payday features
Demand forecasting

## Diseño de capas del Data Lake

```
retailpulse-dev/
│
├── raw/
├── bronze/
├── standard/
├── silver/
├── gold/
├── consumption/
└── ml/
```

### RAW - Fuente original
Aquí queremos conservar los datos prácticamente como fueron recibidos.

```
raw/
├── sales/
├── stores/
├── transactions/
├── holidays/
└── oil/
```

### 2 BRONZE - Datos tipados y estructurados

Aquí ya procesamos Raw.

Bronze tendrá:

    -esquema definido;
    -tipos correctos;
    -fechas convertidas;
    -datos corruptos detectados;
    -metadata de ingestión;
    -posiblemente deduplicación técnica mínima.

Por ejemplo:
```bronze/sales/ ```

Aquí sí podemos particionar por:
```
year=2013/
month=01/
day=01/
```
porque Spark puede abrir un batch Raw y separar las filas según su fecha real.

### standard - Estandarización



En Standard podríamos establecer nuestro propio contrato:

store_id
product_family
items_on_promotion

Además:

date

podría convertirse en:

sale_date

Entonces:
```
Bronze
──────────────
store_nbr
family
sales
onpromotion

↓

Standard
──────────────────
store_id
product_family
units_sold
items_on_promotion
sale_date
```
¿Por qué es útil?

Porque RetailPulse deja de depender completamente del naming de Favorita.

Si mañana incorporamos otro retailer cuyos campos sean:

shop_id
category
quantity
promotion_qty

podemos convertir ambos al mismo contrato estándar:

store_id
product_family
units_sold
items_on_promotion

Eso hace que RetailPulse pueda evolucionar hacia una plataforma multi-source sin intentar crear un ETL mágico completamente genérico.

### 4. SILVER Datos de negocio

Aquí combinamos dominios.

```
standard/sales
        +
standard/stores
        +
standard/holidays
        +
standard/oil
        +
standard/transactions
             │
             ▼
          silver
```
Podemos crear un dataset enriquecido:

```
sale_date
store_id
city
state
store_type
cluster
product_family
sales
on_promotion
transactions
oil_price
is_holiday
holiday_type
is_payday
```

 ### 5. GOLD - Productos analíticos

Gold ya no representa registros individuales necesariamente.

Representa métricas preparadas.

```gold/
├── daily_store_sales/
├── sales_by_family/
├── promotion_performance/
├── city_performance/
└── executive_kpis/
```

Por ejemplo:

```daily_store_sales
─────────────────
date
store_id
total_sales
transactions
avg_sales_per_transaction
promotion_sales
```

### 6. consumption — Datos preparados para consumidores

Esta capa responde una pregunta diferente:

¿Quién va a utilizar estos datos?

```
consumption/
├── dashboard/
├── api/
├── reporting/
└── exports/

```

Gold es un producto de datos.

Consumption es una presentación del producto para un consumidor específico.

### 7. ML - Machine Learning

Como RetailPulse terminará llegando a ML/MLOps, separaría esa responsabilidad.

```ml/
├── features/
├── training/
├── predictions/
└── monitoring/
```

```ml/predictions/demand_forecast/
    prediction_date
    store_id
    family
    predicted_sales
    model_version
    prediction_created_at

```

RESUMEN FLUJO

```
                FUENTES
                   │
       ┌───────────┼────────────┐
       │           │            │
      CSV         APIs        Kafka
       │           │            │
       └───────────┼────────────┘
                   ▼
                  RAW
          Datos tal como llegan
                   │
                   ▼
                BRONZE
            Tipado + esquema
                   │
                   ▼
               STANDARD
          Contrato RetailPulse
                   │
                   ▼
                SILVER
         Datos enriquecidos
                   │
           ┌───────┴────────┐
           ▼                ▼
         GOLD              ML
     Analytics           Features
           │                │
           ▼                ▼
     CONSUMPTION         MLflow
           │                │
     ┌─────┴─────┐          ▼
     ▼           ▼      Predictions
Dashboard      API
```
No reemplazaremos Pandas. Cada tecnología tendrá un trabajo diferente:
    data-generator
    Pandas
    Fuente → RAW

    spark-processor
    Spark
    RAW → BRONZE → posteriormente SILVER