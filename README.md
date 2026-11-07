# Real-Time ETL Pipeline & Business Intelligence Analytics

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![SQLite](https://img.shields.io/badge/SQLite-3.0+-003B57?style=for-the-badge&logo=sqlite)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas)

Un pipeline automatizado de arquitectura end-to-end diseñado para extraer datos desde una API REST en tiempo real, modelar una base de datos relacional normalizada (3FN) e ingerir transacciones para su análisis de Business Intelligence.

---

## 🏗️ Arquitectura del Sistema

```text
[ API REST Externa ] ──(Extract)──> [ Python / Pandas Pipeline ]
                                            │
                                      (Transform & Load)
                                            ▼
[ Base de Datos Relacional SQLite ] <──(3FN Schema & Foreign Keys)
        │
        ├──> [ Vistas SQL Analíticas ] (Rendimiento, KPIs, Métricas de Clientes)
        └──> [ Dashboards & Conexión BI ] (Power BI / Excel)