#!/bin/bash

# turn on bash's job control
set -m

# Start the Kafka Producer process
gunicorn producer:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8081
