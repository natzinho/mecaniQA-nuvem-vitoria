"""Simulador IoT da equipe Vitoria para a atividade OAT 2.

Gera dados sinteticos de equipamentos; nao representa telemetria real.
"""

import logging
import math
import os
import random
import signal
import threading
import time

from prometheus_client import Counter, Gauge, start_http_server


TEMPERATURE = Gauge(
    "iot_engine_temperature_celsius", "Temperatura simulada do motor em Celsius", ["sensor_id"]
)
OIL_PRESSURE = Gauge(
    "iot_oil_pressure_bar", "Pressao simulada do oleo em bar", ["sensor_id"]
)
VIBRATION = Gauge(
    "iot_vibration_meters_per_second_squared",
    "Aceleracao simulada de vibracao em metros por segundo ao quadrado",
    ["sensor_id"],
)
READINGS = Counter(
    "iot_sensor_readings_total", "Quantidade de leituras individuais geradas", ["sensor_id"]
)
LAST_UPDATE = Gauge(
    "iot_sensor_last_update_timestamp_seconds",
    "Horario Unix da ultima atualizacao do sensor",
    ["sensor_id"],
)


def read_config():
    """Falha antes de iniciar se a configuracao for invalida."""
    port = int(os.getenv("METRICS_PORT", "8000"))
    interval = float(os.getenv("SIMULATION_INTERVAL_SECONDS", "5"))
    sensor_count = int(os.getenv("SENSOR_COUNT", "3"))
    if not 1 <= port <= 65535:
        raise ValueError("METRICS_PORT deve estar entre 1 e 65535")
    if not math.isfinite(interval) or interval <= 0:
        raise ValueError("SIMULATION_INTERVAL_SECONDS deve ser finito e positivo")
    if not 1 <= sensor_count <= 100:
        raise ValueError("SENSOR_COUNT deve estar entre 1 e 100")
    return port, interval, sensor_count


def sample_sensors(sensor_ids):
    for sensor_id in sensor_ids:
        TEMPERATURE.labels(sensor_id).set(round(random.uniform(70, 110), 2))
        OIL_PRESSURE.labels(sensor_id).set(round(random.uniform(1.5, 5.5), 2))
        VIBRATION.labels(sensor_id).set(round(random.uniform(0.1, 4.0), 3))
        READINGS.labels(sensor_id).inc(3)
        LAST_UPDATE.labels(sensor_id).set(time.time())


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    port, interval, sensor_count = read_config()
    sensor_ids = [f"sensor-{number:02d}" for number in range(1, sensor_count + 1)]
    stop = threading.Event()

    def request_shutdown(signum, frame):
        stop.set()

    signal.signal(signal.SIGTERM, request_shutdown)
    signal.signal(signal.SIGINT, request_shutdown)
    sample_sensors(sensor_ids)
    server, thread = start_http_server(port, addr="0.0.0.0")
    logging.info("%s sensores; intervalo %ss; metricas em :%s/metrics", sensor_count, interval, port)
    try:
        while not stop.wait(interval):
            sample_sensors(sensor_ids)
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
        logging.info("Simulador encerrado")


if __name__ == "__main__":
    main()
