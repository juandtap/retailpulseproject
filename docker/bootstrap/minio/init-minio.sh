#!/bin/sh

set -e

echo "========================================="
echo "RetailPulse - MinIO Initialization"
echo "========================================="

echo "Waiting for MinIO..."

until mc alias set retailpulse http://minio:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"
do
    echo "MinIO is not ready yet..."
    sleep 2
done

echo "MinIO is ready."

echo "Creating bucket: $MINIO_BUCKET"

mc mb retailpulse/"$MINIO_BUCKET" --ignore-existing

echo "Bucket ready."

echo "MinIO initialization completed successfully."