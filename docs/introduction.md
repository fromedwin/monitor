# Overview

## What is Status From Edwin ?

This project provide a **plug and play** docker instance to **quickly** run monitoring tools without much configuration. This is possible by making **opinionated decision** with **no possible configuration**. Main idea is to have a **fast to deploy** and **full set of tools** to use when bootstraping a new project.

## Features

- Monitor **http code** of your application/website.
- Publish a **public status page** with history of experienced outrages. 
- **Alert on outrage** using [PagerDuty](https://pagerduty.com).
- Login using a **[Github account](https://github.com)**.

## Architecture

Each feature is powered by an **third party open-source project**. This project is architectured around a **django application** running a unified web interface orchestring all APIs.  

- **Availability** is powered by **[Prometheus](https://prometheus.io/)** *(Prometheus, AlertManager, and blackbox_exporter)*
- **Web interface** is using **[django framework](https://www.djangoproject.com/)**