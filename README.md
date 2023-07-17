# kafka

Learning Kafka

## 1. Producer Setting

### 1.1 Environment Setup

- Create virtual environment

```
cd producer
python -m venv <environment-name>
```

- Activate virtual environemtn

```
source <environment-name>/bin/activate
```

- Install all dependencies

```
pip install -r requirements.txt
```

### 1.2 Run producer

```
cd producer
./run.sh
```

## 2. Consumer

### 1.1 Environment Setup

- Create virtual environment

```
cd consumer
python -m venv <environment-name>
```

- Activate virtual environemtn

```
source <environment-name>/bin/activate
```

- Install all dependencies

```
pip install -r requirements.txt
```

### 1.2 Run Consumer

```
cd consumer
chmod +x run.sh
./run.sh
```
