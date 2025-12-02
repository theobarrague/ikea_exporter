import os
import time
from dirigera import Hub
from prometheus_client import start_http_server, Gauge

DIRIGERA_TOKEN = os.getenv("DIRIGERA_TOKEN")
DIRIGERA_IP = os.getenv("DIRIGERA_IP")
EXPORTER_PORT = int(os.getenv("EXPORTER_PORT", "9850"))
SCRAPE_INTERVAL = int(os.getenv("SCRAPE_INTERVAL", "60"))

SENSOR_METRICS = {}

def init_prometheus_metrics(sensors):
    for sensor in sensors:
        sensor_name = sensor.attributes.custom_name.replace(" ", "_").lower()
        if sensor_name not in SENSOR_METRICS:
            SENSOR_METRICS[sensor_name] = {
                'temperature': Gauge(
                    f'ikea_sensor_temperature_celsius',
                    f'Temperature in Celsius for {sensor_name}',
                    ['sensor_name']
                ),
                'humidity': Gauge(
                    f'ikea_sensor_humidity_percent',
                    f'Humidity percentage for {sensor_name}',
                    ['sensor_name']
                ),
                'pm25': Gauge(
                    f'ikea_sensor_pm25_ugm3',
                    f'PM2.5 concentration in µg/m³ for {sensor_name}',
                    ['sensor_name']
                ),
                'voc': Gauge(
                    f'ikea_sensor_voc_index',
                    f'VOC index for {sensor_name}',
                    ['sensor_name']
                ),
                'last_seen': Gauge(
                    f'ikea_sensor_last_seen_timestamp',
                    f'Last seen timestamp for {sensor_name}',
                    ['sensor_name']
                )
            }

def update_prometheus_metrics(sensors):
    for sensor in sensors:
        sensor_name = sensor.attributes.custom_name.replace(" ", "_").lower()
        current_time = time.time()

        if sensor_name in SENSOR_METRICS:
            metrics = SENSOR_METRICS[sensor_name]

            metrics['temperature'].labels(sensor_name).set(
                sensor.attributes.current_temperature
            )
            metrics['humidity'].labels(sensor_name).set(
                sensor.attributes.current_r_h
            )
            metrics['pm25'].labels(sensor_name).set(
                sensor.attributes.current_p_m25
            )
            metrics['voc'].labels(sensor_name).set(
                sensor.attributes.voc_index
            )
            metrics['last_seen'].labels(sensor_name).set(
                current_time
            )

            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Updated metrics for {sensor.attributes.custom_name}: "
                  f"Temp={sensor.attributes.current_temperature}°C, "
                  f"RH={sensor.attributes.current_r_h}%, "
                  f"PM2.5={sensor.attributes.current_p_m25}, "
                  f"VOC={sensor.attributes.voc_index}")

def main():
    print(f"Starting IKEA Dirigera Exporter on port {EXPORTER_PORT}")
    print(f"Connecting to Dirigera Hub at {DIRIGERA_IP}")
    print(f"Scrape interval set to {SCRAPE_INTERVAL} seconds")

    hub = Hub(token=DIRIGERA_TOKEN, ip_address=DIRIGERA_IP)

    start_http_server(EXPORTER_PORT)
    print(f"Prometheus metrics server started on port {EXPORTER_PORT}")

    while True:
        try:
            sensors = hub.get_environment_sensors()

            if not sensors:
                print("No IKEA sensors found.")
                time.sleep(SCRAPE_INTERVAL)
                continue

            if not SENSOR_METRICS:
                init_prometheus_metrics(sensors)

            update_prometheus_metrics(sensors)

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(SCRAPE_INTERVAL)

if __name__ == "__main__":
    main()

