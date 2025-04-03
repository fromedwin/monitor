# Architecture

User interface run as a **django project**. Data are stored in dev mode within **sqlite**, but should be stored on **postgresql** in production.

**Django** create tasks using **celery** and dispatch them using **rabbitMQ**. It runs a **scheduler** to trigger tasks at regular interval. It also run multiple **workers** based on django code base.

A **typescript worker** run multipel replicas to trigger **lighthouse** reports.

Django generate a **prometheus** config file to trigger monitoring using **blackbox** plugin. **Alertmanager** is connected to prometheus and calling back webhooks to django.

**InfluxDB** store time serie metrics, using **telegraf** to read prometheus metrics. Django can query InfluxDB directly to display metrics.

```{mermaid}
graph TD
    %% Define styles
    classDef infrastructure fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef worker fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    classDef monitoring fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef scheduler fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    classDef external fill:#f5f5f5,stroke:#616161,stroke-width:1px

    %% Infrastructure Layer
    RabbitMQ[RabbitMQ<br>Message Broker]
    InfluxDB[InfluxDB<br>Time Series DB]
    Telegraf[Telegraf<br>Metrics Collector]

    %% Worker Layer
    Celery[Celery Workers<br>Task Processing]
    Lighthouse[Lighthouse Workers<br>Web Performance]
    Heartbeats[Heartbeats Service<br>Health Monitoring]

    %% Monitoring Layer
    Prometheus[Prometheus<br>Metrics & Alerting]
    Alertmanager[Alertmanager<br>Alert Handling]
    Blackbox[Blackbox Exporter<br>Endpoint Monitoring]

    %% Scheduler Layer
    Scheduler[Scheduler<br>Task Scheduling]

    %% External Systems
    Backend[Backend API<br>External System]:::external
    Websites[Monitored Websites<br>External Systems]:::external

    %% Connections - Infrastructure
    RabbitMQ -->|Tasks| Celery
    RabbitMQ -->|Tasks| Lighthouse
    InfluxDB <-->|Store Metrics| Telegraf
    
    %% Connections - Workers
    Celery -->|Results| Backend
    Lighthouse -->|Performance Data| Backend
    Lighthouse -->|Analyzes| Websites
    Heartbeats -->|Health Status| Backend
    
    %% Connections - Monitoring
    Prometheus -->|Alerts| Alertmanager
    Prometheus -.->|Scrapes Metrics| RabbitMQ
    Prometheus -.->|Scrapes Metrics| Blackbox
    Blackbox -.->|Probes| Websites
    Telegraf -.->|Collects Metrics| RabbitMQ
    Telegraf -.->|Collects Metrics| Celery
    
    %% Connections - Scheduler
    Scheduler -->|Schedules Tasks| RabbitMQ
    
    %% Apply styles
    RabbitMQ:::infrastructure
    InfluxDB:::infrastructure
    Telegraf:::infrastructure
    
    Celery:::worker
    Lighthouse:::worker
    Heartbeats:::worker
    
    Prometheus:::monitoring
    Alertmanager:::monitoring
    Blackbox:::monitoring
    
    Scheduler:::scheduler
```




```{toctree}
:maxdepth: 1
:caption: Contents:

architecture/backend
architecture/tasks
architecture/availability
architecture/performances
architecture/metrics