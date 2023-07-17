#!/bin/bash
function usage () {
  cat <<HELP_USAGE
  Usage:
  $0 [-h] [-p PORT]

  -h, --help   Display this help message
  -p, --port   Deploy port, default 8081
HELP_USAGE
  exit 0
}
# default values
PORT=8081

# args parse
POSITIONAL_ARGS=()
while [[ $# -gt 0 ]]; do
  case $1 in
    -h|--help)
      usage
      ;;
    -p|--port)
      PORT="$2"
      shift # past argument
      shift # past value
      ;;
    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;
    *)
      POSITIONAL_ARGS+=("$1") # save positional arg
      shift # past argument
      ;;
  esac
done

set -- "${POSITIONAL_ARGS[@]}" # restore positional parameters

# # Activate virual environment
# python -m venv .venv
# source .venv/bin/activate

# # Install all dependencies
# pip install --upgrade pip
# pip install -r requirements.txt

# Start the Kafka Producer process
gunicorn producer:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --timeout 300
