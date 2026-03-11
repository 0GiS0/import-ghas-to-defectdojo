# GitHub Advanced Security (GHAS) - Integración con DefectDojo

<div align="center">

[![YouTube Channel Subscribers](https://img.shields.io/youtube/channel/subscribers/UC140iBrEZbOtvxWsJ-Tb0lQ?style=for-the-badge&logo=youtube&logoColor=white&color=red)](https://www.youtube.com/c/GiselaTorres?sub_confirmation=1) [![GitHub followers](https://img.shields.io/github/followers/0GiS0?style=for-the-badge&logo=github&logoColor=white)](https://github.com/0GiS0) [![LinkedIn Follow](https://img.shields.io/badge/LinkedIn-S%C3%ADgueme-blue?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/giselatorresbuitrago/) [![X Follow](https://img.shields.io/badge/X-S%C3%ADgueme-black?style=for-the-badge&logo=x&logoColor=white)](https://twitter.com/0GiS0)

</div>

---

¡Hola developer 👋🏻! Este repositorio es una **Prueba de Concepto (PoC)** para integrar **GitHub Advanced Security (GHAS)** con **DefectDojo**. He intentado hacerlo lo más simple posible para que puedas adaptarlo fácilmente a tus necesidades.

## 📑 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#️-tecnologías)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Uso](#-uso)
  - [Importar Alertas de Dependabot](#importar-alertas-de-dependabot)
  - [Importar Alertas de Code Scanning](#importar-alertas-de-code-scanning)
  - [Importar Alertas de Secret Scanning](#importar-alertas-de-secret-scanning)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Sígueme](#-sígueme-en-mis-redes-sociales)

## ✨ Características

- **Integración completa con GHAS**: Importa los tres tipos de alertas de GitHub Advanced Security a DefectDojo
- **Workflows automatizados**: GitHub Actions listos para usar
- **Alertas de Dependabot**: Importación usando el formato `GitHub Vulnerability Scan`
- **Alertas de Code Scanning**: Importación de resultados de CodeQL usando formato `SARIF`
- **Alertas de Secret Scanning**: Creación de hallazgos directamente vía API de DefectDojo
- **Aplicación Flask de ejemplo**: Incluye una aplicación Flask vulnerable para pruebas

## 🛠️ Tecnologías

- **Python 3.8+** - Lenguaje de programación principal
- **Flask** - Framework web para la aplicación vulnerable de ejemplo
- **GitHub Actions** - Automatización CI/CD
- **GitHub Advanced Security** - Escaneo de seguridad (Dependabot, CodeQL, Secret Scanning)
- **DefectDojo** - Plataforma de gestión de vulnerabilidades
- **Docker** - Soporte de contenedores

## 📋 Requisitos Previos

- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/) y Docker Compose
- [GitHub CLI](https://cli.github.com/) (opcional)
- Un repositorio de GitHub con GHAS habilitado
- Una GitHub App con permiso `read:security_events` (para alertas de secrets y dependabot)

## 🚀 Instalación

### Paso 1: Clonar este repositorio

```bash
git clone https://github.com/0GiS0/import-ghas-to-defectdojo.git
cd import-ghas-to-defectdojo
```

### Paso 2: Configurar DefectDojo

Clona y ejecuta DefectDojo localmente:

```bash
git clone https://github.com/DefectDojo/django-DefectDojo.git
cd django-DefectDojo
docker compose up
```

### Paso 3: Crear Producto y Engagement en DefectDojo

Necesitas un **Product** y un **Engagement** creados en DefectDojo. Puedes crearlos usando la API. Consulta el archivo `requests/create_defectDojo_artifacts.http` para ver ejemplos.

### Paso 4: Exponer DefectDojo con un túnel

Usa un servicio de túneles como [pinggy.io](https://pinggy.io/) o [ngrok](https://ngrok.com/):

```bash
# Usando pinggy.io
ssh -p 443 -R0:localhost:8080 qr@a.pinggy.io

# Usando ngrok
ngrok http 8080
```

### Paso 5: Configurar Secrets en GitHub

Añade los siguientes secrets a tu repositorio de GitHub:

| Secret | Descripción |
|--------|-------------|
| `DEFECTDOJO_URL` | La URL expuesta por el túnel |
| `DEFECTDOJO_TOKEN` | Token de API de DefectDojo (créalo en tu perfil de usuario) |

### Paso 6: Crear una GitHub App (Opcional)

Para obtener alertas de secrets y dependabot, crea una GitHub App con el permiso `read:security_events`. Sigue la [documentación oficial](https://docs.github.com/en/developers/apps/building-github-apps/creating-a-github-app).

🎉 **¡Felicidades! ¡Ya estás listo para empezar!**

## 💻 Uso

### Importar Alertas de Dependabot

Las alertas de Dependabot se importan usando el formato `GitHub Vulnerability Scan` (disponible desde DefectDojo 2.4.0).

El workflow `.github/workflows/send_dependabot_security_alerts.yml` obtiene las alertas vía API GraphQL y las envía a DefectDojo:

```bash
curl -X POST "$DEFECTDOJO_URL/import-scan/" \
  -H "Authorization: Token $DEFECTDOJO_TOKEN" \
  -F 'product_name=TU_NOMBRE_DE_PRODUCTO' \
  -F 'engagement=ID_DEL_ENGAGEMENT' \
  -F 'scan_type=Github Vulnerability Scan' \
  -F 'file=@dependabot-security-alerts.json'
```

### Importar Alertas de Code Scanning

Las alertas de Code Scanning (CodeQL) se importan usando el formato `SARIF`.

El workflow `.github/workflows/codeql_and_defectdojo.yml` ejecuta el análisis de CodeQL y sube los resultados:

```bash
curl -X POST "$DEFECTDOJO_URL/import-scan/" \
  -H "Authorization: Token $DEFECTDOJO_TOKEN" \
  -F 'product_name=TU_NOMBRE_DE_PRODUCTO' \
  -F 'engagement=ID_DEL_ENGAGEMENT' \
  -F 'scan_type=SARIF' \
  -F 'file=@results/python.sarif'
```

### Importar Alertas de Secret Scanning

Las alertas de Secret Scanning se crean directamente como hallazgos (findings) vía la API de DefectDojo.

El workflow `.github/workflows/send_secrets_to_defectdojo.yml`:

1. **Obtiene los secrets** desde la API REST de GitHub
2. **Transforma** los datos al formato de DefectDojo usando `jq`
3. **Crea los hallazgos** vía POST a `/api/v2/findings/`

```bash
# Obtener secrets desde GitHub
curl -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/OWNER/REPO/secret-scanning/alerts > secrets.json

# Transformar y enviar a DefectDojo
curl -X POST "$DEFECTDOJO_URL/findings/" \
  -H "Authorization: Token $DEFECTDOJO_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$FINDING_DATA"
```

## 📁 Estructura del Proyecto

```
import-ghas-to-defectdojo/
├── .github/
│   ├── dependabot.yml
│   └── workflows/
│       ├── codeql_and_defectdojo.yml      # CodeQL + subida SARIF
│       ├── get_alerts.yml                  # Obtener alertas GHAS
│       ├── send_dependabot_security_alerts.yml
│       └── send_secrets_to_defectdojo.yml
├── flask_webgoat/                          # App Flask vulnerable de ejemplo
│   ├── actions.py
│   ├── auth.py
│   ├── status.py
│   ├── ui.py
│   ├── users.py
│   └── templates/
├── requests/                               # Ejemplos de peticiones HTTP
│   ├── create_defectDojo_artifacts.http
│   ├── defectDojo.http
│   ├── ghas_alerts_requests.http
│   └── send_*.http
├── app.py
├── Dockerfile
├── requirements.txt
└── README.md
```

## 🌐 Sígueme en Mis Redes Sociales

Si te ha resultado útil este proyecto, no olvides seguirme en mis redes sociales:

<div align="center">

[![YouTube Channel Subscribers](https://img.shields.io/youtube/channel/subscribers/UC140iBrEZbOtvxWsJ-Tb0lQ?style=for-the-badge&logo=youtube&logoColor=white&color=red)](https://www.youtube.com/c/GiselaTorres?sub_confirmation=1) [![GitHub followers](https://img.shields.io/github/followers/0GiS0?style=for-the-badge&logo=github&logoColor=white)](https://github.com/0GiS0) [![LinkedIn Follow](https://img.shields.io/badge/LinkedIn-S%C3%ADgueme-blue?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/giselatorresbuitrago/) [![X Follow](https://img.shields.io/badge/X-S%C3%ADgueme-black?style=for-the-badge&logo=x&logoColor=white)](https://twitter.com/0GiS0)

</div>

---

¡Happy hacking! 🐱‍👤
