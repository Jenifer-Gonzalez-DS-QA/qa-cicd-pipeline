# 🔄 QA CI/CD Pipeline — Automation Suite

Suite de pruebas con 3 niveles (smoke, regresión, performance) integrada con *GitHub Actions*.
Las pruebas corren automáticamente en cada push, pull request y de lunes a viernes a las 8am.

> *API usada:* [JSONPlaceholder](https://jsonplaceholder.typicode.com) — gratuita, sin registro, sin API key, disponible 24/7.

> 💡 Este proyecto demuestra mentalidad *DevOps aplicada al QA*: las pruebas no se ejecutan manualmente, sino que forman parte del ciclo de desarrollo y corren solas.

-----

## 📌 Tabla de Contenidos

- [¿Qué hace este proyecto?](#qué-hace-este-proyecto)
- [Arquitectura del Pipeline](#arquitectura-del-pipeline)
- [Tecnologías](#tecnologías)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Cómo Ejecutar las Pruebas](#cómo-ejecutar-las-pruebas)
- [Marcadores y Ejecución Selectiva](#marcadores-y-ejecución-selectiva)
- [Pipelines de GitHub Actions](#pipelines-de-github-actions)
- [Cómo leer los Reportes](#cómo-leer-los-reportes)
- [Autora](#autora)

-----

## ¿Qué hace este proyecto?

Organiza las pruebas en 3 niveles con marcadores de pytest y las ejecuta automáticamente en GitHub Actions con un pipeline de 4 jobs:

- *Smoke* → 17 pruebas críticas que verifican que la API responde
- *Regression* → 28 pruebas exhaustivas del comportamiento de cada endpoint
- *Performance* → 6 pruebas que validan que cada endpoint responde en menos de 3 segundos
- *Consolidar* → agrupa todos los reportes HTML como artifacts descargables

-----

## 🏗️ Arquitectura del Pipeline


Push / PR / Cron (8am L-V)
          │
          ▼
  ┌───────────────┐
  │ 🔥 Smoke      │  ← Corre siempre primero (~30s)
  └──────┬────────┘
         │ (solo si pasa)
    ┌────┴──────────────────────┐
    │                           │
    ▼                           ▼
┌──────────────┐     ┌──────────────────────┐
│ 🔄 Regression│     │ ⚡ Performance Tests  │
│  (~2 min)    │     │  (~30s)               │
└──────┬───────┘     └──────────┬────────────┘
       │                        │
       └──────────┬─────────────┘
                  ▼
        ┌──────────────────┐
        │ 📊 Consolidar    │  ← Artifacts por 30 días
        └──────────────────┘


-----

## 🛠 Tecnologías

|Herramienta   |Versión|Uso                    |
|--------------|-------|-----------------------|
|Python        |3.11+  |Lenguaje base          |
|pytest        |7.4.3  |Framework de pruebas   |
|requests      |2.31.0 |Cliente HTTP           |
|pytest-html   |4.1.1  |Reportes HTML por nivel|
|GitHub Actions|-      |CI/CD automatizado     |

-----

## 📁 Estructura del Proyecto


qa-cicd-pipeline/
│
├── tests/
│   ├── __init__.py
│   └── test_suite.py         # Suite completa con 4 clases y 3 niveles de marcadores
│
├── .github/
│   └── workflows/
│       ├── qa-pipeline.yml   # Pipeline principal: 4 jobs
│       └── pr-check.yml      # Smoke rápido en cada Pull Request
│
├── reports/                  # Reportes generados (ignorados en git)
│   ├── smoke-report.html
│   ├── regression-report.html
│   ├── performance-report.html
│   └── results.csv           # CSV acumulativo por prueba
│
├── conftest.py               # Fixtures, marcadores y hook de CSV
├── pytest.ini                # Configuración de pytest
├── requirements.txt
├── .gitignore
└── README.md


-----

## ⚙️ Instalación

bash
# 1. Clonar el repositorio
git clone https://github.com/Jenifer-Gonzalez-DS-QA/qa-cicd-pipeline.git
cd qa-cicd-pipeline

# 2. Crear entorno virtual
python -m venv venv

# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt


-----

## ▶️ Cómo Ejecutar las Pruebas

bash
# Toda la suite (los 3 niveles juntos)
pytest

# Solo smoke — rápido, pruebas críticas (~30 segundos)
pytest -m smoke

# Solo regresión — suite completa
pytest -m regression

# Solo performance — tiempos de respuesta
pytest -m performance

# Smoke + reporte HTML
pytest -m smoke --html=reports/smoke-report.html --self-contained-html

# Ver resumen sin verbosidad
pytest -m smoke -q


> Los reportes HTML se generan en la carpeta reports/.
> Ábrelos en cualquier navegador haciendo doble clic.

-----

## 🏷️ Marcadores y Ejecución Selectiva

|Marcador                  |Cuántas pruebas|Cuándo usarlo                                  |
|--------------------------|---------------|-----------------------------------------------|
|@pytest.mark.smoke      |17             |Antes de cualquier deploy — verifica lo crítico|
|@pytest.mark.regression |28             |En cada PR y después de cambios — verifica todo|
|@pytest.mark.performance|6              |Después de cambios de infraestructura          |

*¿Cómo funcionan?*

En el código, cada prueba tiene un decorador:

python
@pytest.mark.smoke
def test_get_posts_returns_200(self, api):
    ...

@pytest.mark.regression
def test_get_post_not_found(self, api):
    ...

@pytest.mark.performance
def test_response_time_under_3s(self, api, endpoint):
    ...


Cuando corres pytest -m smoke, solo ejecuta las que tienen @pytest.mark.smoke.

-----

## 🔄 Pipelines de GitHub Actions

### qa-pipeline.yml — Pipeline principal

Se activa en:

- push a las ramas main o develop
- pull_request a main
- Todos los días hábiles a las 8am UTC (automático)
- Manualmente: en GitHub → pestaña *Actions* → botón *Run workflow*

*Cómo ver los resultados en GitHub:*

1. Ir a tu repositorio en GitHub
1. Hacer clic en la pestaña *Actions*
1. Hacer clic en la ejecución más reciente
1. Verás los 4 jobs con ✅ o ❌
1. Hacer clic en cualquier job para ver el log detallado
1. Al final de la página en *Artifacts* → descargar el reporte HTML

### pr-check.yml — Check de Pull Requests

Se activa automáticamente cuando creas un Pull Request.
Corre solo los smoke tests (~30 segundos).
Si fallan, GitHub bloquea el merge del PR automáticamente.

-----

## 📊 Cómo leer los Reportes

Tienes 3 reportes HTML separados según el nivel. Ábrelos en tu navegador.

### smoke-report.html

Las pruebas más importantes. Si alguna falla aquí, el pipeline detiene todo.
Busca: ¿todas dicen PASSED? Si hay alguna FAILED, haz clic en ella para ver el error exacto.

### regression-report.html

La suite completa. Aquí verás el comportamiento detallado de cada endpoint.

- PASSED = el endpoint responde exactamente como se espera
- FAILED = algo cambió o hay un bug — el error te dice exactamente qué

*Ejemplo de error típico:*


AssertionError: assert 500 == 200
E  + where 500 = <Response [500]>.status_code


Significa: esperabas 200, el servidor devolvió 500 (error interno).

### performance-report.html

Pruebas de tiempo de respuesta. Cada prueba verifica que el endpoint responde en menos de 3 segundos.

*Ejemplo de fallo de performance:*


AssertionError: Respuesta lenta: 4.231s para /posts


Significa: ese endpoint tardó más de 3 segundos — posible problema de red o carga del servidor.

### results.csv

Archivo generado por el hook de conftest.py. Contiene una fila por cada prueba ejecutada con: timestamp, nombre, resultado y duración. Puedes abrirlo en Excel para analizarlo.

-----

## 🔗 Relación con los otros proyectos del portafolio

|Proyecto                   |Rol                                    |
|---------------------------|---------------------------------------|
|api-testing-framework    |Base: estructura y cliente HTTP        |
|qa-dashboard             |Análisis: métricas y visualización     |
|qa-cicd-pipeline ← este|Automatización: corre solo en cada push|

Los 3 juntos forman un ecosistema QA completo de nivel profesional.

-----

## 👩‍💻 Autora

*Jenifer Gonzalez*

QA Engineer | Data Science | Scrum Master

[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin)](https://linkedin.com/in/jenifer-paola-gonzalez-peñuela)
[![GitHub](https://img.shields.io/badge/GitHub-black?style=flat&logo=github)](https://github.com/Jenifer-Gonzalez-DS-QA/)

-----

> 💡 *Este proyecto es parte de un portafolio de 3 proyectos de automatización QA.
> Ver también: [API Testing Framework](https://github.com/Jenifer-Gonzalez-DS-QA/api-testing-framework) y [QA Dashboard](https://github.com/Jenifer-Gonzalez-DS-QA/qa-dashboard)*
