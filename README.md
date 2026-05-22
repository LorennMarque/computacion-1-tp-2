# Monitor de CPU con Redis

Prueba en clase para practicar **Redis**. Se pidió un tablero de monitoreo en tiempo real de CPU con una ventana de **1 minuto** (los datos en Redis expiran a los 60 segundos).

![Demo de tablero de CPU](https://github.com/user-attachments/assets/73b38cb7-0679-45e5-ab9c-04813183c270.gif)

## Qué hace

- **Colector**: lee el uso de CPU con `psutil` y lo guarda en Redis.
- **Tablero**: servidor web (Flask) que lee Redis y muestra el estado actual e historial de la última ventana.
- **Alerta**: si el CPU supera un umbral, el tablero entra en modo alerta. Por defecto está en **50%** (`ALERT_THRESHOLD` en `templates/dashboard.html`); se puede cambiar.

## Arquitectura

Con **multiprocessing** se levantan dos procesos:

1. **Colector** (`app/collector.py`) — script en loop que obtiene métricas y las persiste en Redis.
2. **Web** (`app/web.py`) — sirve el tablero HTML y las APIs que consultan Redis.

El punto de entrada es `run.py`, que arranca ambos procesos.

## Alerta al superar treshold
Demostración del estado de alerta. Para exigir el CPU se ocuparon al 100% 15 cores del dispositivo haciendo calculos pesados genéricos.

![Superación del umbral de alerta](https://github.com/user-attachments/assets/6b9a0de5-db3c-44ab-9915-2fea12ddbf19)

## Requisitos

- Python 3
- Redis en `localhost:6379`
- Dependencias: `pip install -r requirements.txt`

## Ejecutar

```bash
redis-server   # si no está corriendo
python run.py
```

Abrir: `http://localhost:5003`
