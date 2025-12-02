# IKEA Dirigera Exporter

[![Docker Image Size](https://img.shields.io/docker/image-size/theobarrague/ikea_exporter/latest)](https://hub.docker.com/r/theobarrague/ikea_exporter)
[![Python Version](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Un exporteur Prometheus pour les capteurs environnementaux IKEA Dirigera (Vindriktning, etc.) qui expose les métriques de température, humidité, PM2.5 et VOC.

## ✨ Fonctionnalités

- **Collecte en temps réel** des données des capteurs IKEA
- **Exposition des métriques** au format Prometheus :
  - Température (°C)
  - Humidité (%)
  - PM2.5 (µg/m³)
  - VOC (indice)
  - Dernière mise à jour (timestamp)
- **Conteneurisé** avec Docker pour un déploiement facile
- **Configuration par variables d'environnement**

## 📦 Prérequis

- Une passerelle **IKEA Dirigera** configurée
- Un **token d'API Dirigera** valide
- Docker (pour l'exécution conteneurisée) ou Python 3.14+

## 🚀 Installation

### Avec Docker (recommandé)

1. Lancez le conteneur avec les variables d'environnement requises :
   ```bash
   docker run -d \
     --name ikea_exporter \
     -p 9850:9850 \
     -e DIRIGERA_TOKEN="votre_token_api" \
     -e DIRIGERA_IP="192.168.x.x" \
     theobarrague/ikea_exporter
   ```

### Sans Docker (Python pur)

1. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

2. Lancez l'exporteur :
   ```bash
   DIRIGERA_TOKEN="votre_token" DIRIGERA_IP="192.168.x.x" python ikea_exporter.py
   ```

## 🛠 Configuration

| Variable d'environnement | Description                     | Valeur par défaut |
|--------------------------|---------------------------------|-------------------|
| `DIRIGERA_TOKEN`         | Token d'API Dirigera            | *Requise*         |
| `DIRIGERA_IP`            | Adresse IP de la passerelle    | *Requise*         |
| `EXPORTER_PORT`          | Port du serveur de métriques    | `9850`            |
| `SCRAPE_INTERVAL`        | Intervalle de rafraîchissement (s) | `60`          |

## 📊 Métriques Prometheus

Les métriques sont exposées sur `http://<IP>:9850/metrics` au format Prometheus. Exemple :

```
# HELP ikea_sensor_temperature_celsius Temperature in Celsius for <sensor_name>
# TYPE ikea_sensor_temperature_celsius gauge
ikea_sensor_temperature_celsius{sensor_name="salon"} 23.5

# HELP ikea_sensor_humidity_percent Humidity percentage for <sensor_name>
# TYPE ikea_sensor_humidity_percent gauge
ikea_sensor_humidity_percent{sensor_name="salon"} 45.0
```

## 🔧 Développement

### Dépendances

- [`dirigera`](https://pypi.org/project/dirigera/) : Bibliothèque Python pour l'API Dirigera
- [`prometheus_client`](https://github.com/prometheus/client_python) : Bibliothèque d'export Prometheus

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez votre branche de fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Commitez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Poussez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📄 Licence

Distribué sous la licence MIT. Voir `LICENSE` pour plus d'informations.

## 📬 Contact

Théo Barrague - [@theobarrague](https://github.com/theobarrague)

Lien du projet : [https://github.com/theobarrague/ikea_exporter](https://github.com/theobarrague/ikea_exporter)
