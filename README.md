# GitHub Advanced Security (GHAS) - DefectDojo Integration

<div align="center">

[![YouTube Channel Subscribers](https://img.shields.io/youtube/channel/subscribers/UC140iBrEZbOtvxWsJ-Tb0lQ?style=for-the-badge&logo=youtube&logoColor=white&color=red)](https://www.youtube.com/c/GiselaTorres?sub_confirmation=1) [![GitHub followers](https://img.shields.io/github/followers/0GiS0?style=for-the-badge&logo=github&logoColor=white)](https://github.com/0GiS0) [![LinkedIn Follow](https://img.shields.io/badge/LinkedIn-Follow-blue?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/giselatorresbuitrago/) [![X Follow](https://img.shields.io/badge/X-Follow-black?style=for-the-badge&logo=x&logoColor=white)](https://twitter.com/0GiS0)

</div>

---

Hi developer 👋🏻! This repository is a **Proof of Concept (PoC)** to integrate **GitHub Advanced Security (GHAS)** with **DefectDojo**. I tried to make it as simple as possible, so you can easily adapt it to your needs.

## 📑 Table of Contents

- [GitHub Advanced Security (GHAS) - DefectDojo Integration](#github-advanced-security-ghas---defectdojo-integration)
  - [📑 Table of Contents](#-table-of-contents)
  - [✨ Features](#-features)
  - [🛠️ Technologies](#️-technologies)
  - [📋 Prerequisites](#-prerequisites)
  - [🚀 Installation](#-installation)
    - [Step 1: Clone this repository](#step-1-clone-this-repository)
    - [Step 2: Set up DefectDojo](#step-2-set-up-defectdojo)
    - [Step 3: Create Product and Engagement in DefectDojo](#step-3-create-product-and-engagement-in-defectdojo)
    - [Step 4: Expose DefectDojo with a tunnel](#step-4-expose-defectdojo-with-a-tunnel)
    - [Step 5: Configure GitHub Secrets](#step-5-configure-github-secrets)
    - [Step 6: Create a GitHub App (Optional)](#step-6-create-a-github-app-optional)
  - [💻 Usage](#-usage)
    - [Import Dependabot Alerts](#import-dependabot-alerts)
    - [Import Code Scanning Alerts](#import-code-scanning-alerts)
    - [Import Secret Scanning Alerts](#import-secret-scanning-alerts)
  - [📁 Project Structure](#-project-structure)
  - [🌐 Follow Me](#-follow-me)

## ✨ Features

- **Full GHAS Integration**: Import all three types of GitHub Advanced Security alerts into DefectDojo
- **Automated Workflows**: GitHub Actions workflows ready to use
- **Dependabot Alerts**: Import using `GitHub Vulnerability Scan` format
- **Code Scanning Alerts**: Import CodeQL results using `SARIF` format
- **Secret Scanning Alerts**: Create findings directly via DefectDojo API
- **Sample Flask App**: Includes a vulnerable Flask application for testing

## 🛠️ Technologies

- **Python 3.8+** - Main programming language
- **Flask** - Web framework for the sample vulnerable app
- **GitHub Actions** - CI/CD automation
- **GitHub Advanced Security** - Security scanning (Dependabot, CodeQL, Secret Scanning)
- **DefectDojo** - Vulnerability management platform
- **Docker** - Container support

## 📋 Prerequisites

- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/) & Docker Compose
- [GitHub CLI](https://cli.github.com/) (optional)
- A GitHub repository with GHAS enabled
- A GitHub App with `read:security_events` permission (for secrets and dependabot alerts)

## 🚀 Installation

### Step 1: Clone this repository

```bash
git clone https://github.com/0GiS0/import-ghas-to-defectdojo.git
cd import-ghas-to-defectdojo
```

### Step 2: Set up DefectDojo

Clone and run DefectDojo locally:

```bash
git clone https://github.com/DefectDojo/django-DefectDojo.git
cd django-DefectDojo
docker compose up -d
docker compose logs initializer | grep "Admin password:"
```

Then you can log in to DefectDojo at `http://localhost:8080` with username `admin` and the password from the logs.

### Step 3: Create Product and Engagement in DefectDojo

You need a **Product** and an **Engagement** created in DefectDojo. You can create them using the API. Check the file `requests/create_defectDojo_artifacts.http` for examples.

### Step 4: Expose DefectDojo with a tunnel

Use a tunneling service like [pinggy.io](https://pinggy.io/) or [ngrok](https://ngrok.com/):

```bash
# Using pinggy.io
ssh -p 443 -R0:localhost:8080 qr@a.pinggy.io

# Using ngrok
ngrok http 8080
```

### Step 5: Configure GitHub Secrets

Add the following secrets to your GitHub repository:

| Secret | Description |
|--------|-------------|
| `DEFECTDOJO_URL` | The URL exposed by the tunnel |
| `DEFECTDOJO_TOKEN` | DefectDojo API token (create it in your user profile) |

### Step 6: Create a GitHub App (Optional)

To get secrets and dependabot alerts, create a GitHub App with the `read:security_events` permission. Follow the [official documentation](https://docs.github.com/en/developers/apps/building-github-apps/creating-a-github-app).

🎉 **Congratulations! You are ready to go!**

## 💻 Usage

### Import Dependabot Alerts

Dependabot alerts are imported using the `GitHub Vulnerability Scan` format (available since DefectDojo 2.4.0).

The workflow `.github/workflows/send_dependabot_security_alerts.yml` retrieves alerts via GraphQL API and sends them to DefectDojo:

```bash
curl -X POST "$DEFECTDOJO_URL/import-scan/" \
  -H "Authorization: Token $DEFECTDOJO_TOKEN" \
  -F 'product_name=YOUR_PRODUCT_NAME' \
  -F 'engagement=ENGAGEMENT_ID' \
  -F 'scan_type=Github Vulnerability Scan' \
  -F 'file=@dependabot-security-alerts.json'
```

### Import Code Scanning Alerts

Code Scanning alerts (CodeQL) are imported using the `SARIF` format.

The workflow `.github/workflows/codeql_and_defectdojo.yml` runs CodeQL analysis and uploads results:

```bash
curl -X POST "$DEFECTDOJO_URL/import-scan/" \
  -H "Authorization: Token $DEFECTDOJO_TOKEN" \
  -F 'product_name=YOUR_PRODUCT_NAME' \
  -F 'engagement=ENGAGEMENT_ID' \
  -F 'scan_type=SARIF' \
  -F 'file=@results/python.sarif'
```

### Import Secret Scanning Alerts

Secret Scanning alerts are created directly as findings via the DefectDojo API.

The workflow `.github/workflows/send_secrets_to_defectdojo.yml`:

1. **Fetches secrets** from GitHub REST API
2. **Transforms** the data to DefectDojo format using `jq`
3. **Creates findings** via POST to `/api/v2/findings/`

```bash
# Get secrets from GitHub
curl -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/OWNER/REPO/secret-scanning/alerts > secrets.json

# Transform and send to DefectDojo
curl -X POST "$DEFECTDOJO_URL/findings/" \
  -H "Authorization: Token $DEFECTDOJO_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$FINDING_DATA"
```

## 📁 Project Structure

```
import-ghas-to-defectdojo/
├── .github/
│   ├── dependabot.yml
│   └── workflows/
│       ├── codeql_and_defectdojo.yml      # CodeQL + SARIF upload
│       ├── get_alerts.yml                  # Get GHAS alerts
│       ├── send_dependabot_security_alerts.yml
│       └── send_secrets_to_defectdojo.yml
├── flask_webgoat/                          # Sample vulnerable Flask app
│   ├── actions.py
│   ├── auth.py
│   ├── status.py
│   ├── ui.py
│   ├── users.py
│   └── templates/
├── requests/                               # HTTP request examples
│   ├── create_defectDojo_artifacts.http
│   ├── defectDojo.http
│   ├── ghas_alerts_requests.http
│   └── send_*.http
├── app.py
├── Dockerfile
├── requirements.txt
└── README.md
```

## 🌐 Follow Me

If you found this project useful, don't forget to follow me on my social networks:

<div align="center">

[![YouTube Channel Subscribers](https://img.shields.io/youtube/channel/subscribers/UC140iBrEZbOtvxWsJ-Tb0lQ?style=for-the-badge&logo=youtube&logoColor=white&color=red)](https://www.youtube.com/c/GiselaTorres?sub_confirmation=1) [![GitHub followers](https://img.shields.io/github/followers/0GiS0?style=for-the-badge&logo=github&logoColor=white)](https://github.com/0GiS0) [![LinkedIn Follow](https://img.shields.io/badge/LinkedIn-Follow-blue?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/giselatorresbuitrago/) [![X Follow](https://img.shields.io/badge/X-Follow-black?style=for-the-badge&logo=x&logoColor=white)](https://twitter.com/0GiS0)

</div>

---

Happy hacking! 🐱‍👤
