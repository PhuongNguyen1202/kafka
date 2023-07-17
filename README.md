# kafka

Learning Kafka

## 1. Environment Setup

- Create virtual environment

```
cd producer
python -m venv <environment-name>
```

```
cd consumer
python -m venv <environment-name>
```

- Activate virtual environemtn

```
cd producer
source <environment-name>/bin/activate
```

```
cd consumer
source <environment-name>/bin/activate
```

- Install all dependencies

```
cd producer
pip install -r requirements.txt
```

```
cd consumer
pip install -r requirements.txt
```

## Usage

### 1. Development Mode

- Acitvate all crucial services including kafka, kafka-ui, zookeeper

```
docker compose -f dev.docker-compose.yml up
```

- Run producer

```
cd producer
chmod +x run.sh
./run.sh
```

- Run 3 consumers in three different command pannels

```
cd consumer
python consumer

```

```
cd consumer
python consumer

```

```
cd consumer
python consumer

```

- Send message

```
URL: http://localhost:8081/send-message
Method: POST
Body:
{
    "value": "testing-value"
    // "partition": 2
}
```

### 2. Production Mode

```
update later
```
