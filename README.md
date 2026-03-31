# Smart Injection - Full-Stack OEE System

A comprehensive industrial IoT solution for monitoring **Overall Equipment Effectiveness (OEE)** in real-time. This project bridges the gap between shop-floor data collection and executive-level decision-making.

<p align="center">
  <img src="./dashboard_images/seu_gif_principal.gif" width="800" alt="Dashboard Demo">
</p>

<p align="center">
  <a href="https://oee-dashboard-iqk9lse8jpgyrp5eey8rqq.streamlit.app/">
    <img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" alt="Streamlit App">
  </a>
  <img src="https://img.shields.io/badge/Database-PostgreSQL-blue?style=flat&logo=postgresql" alt="Postgres">
  <img src="https://img.shields.io/badge/Backend-PHP-777BB4?style=flat&logo=php" alt="PHP">
  <img src="https://img.shields.io/badge/Data%20Science-Python-3776AB?style=flat&logo=python" alt="Python">
</p>

| Component | Tech | Description |
| :--- | :--- | :--- |
| **[Frontend]** | <img src="https://img.shields.io/badge/-PHP-777BB4?style=flat-square&logo=php&logoColor=white" /> | Interface de apontamento para os operadores. |
| **[Processing]** | <img src="https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white" /> | Engine de cálculo de OEE com Numpy/Pandas. |
| **[Database]** | <img src="https://img.shields.io/badge/-PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white" /> | Armazenamento relacional via Docker. |
| **[Dashboard]** | <img src="https://img.shields.io/badge/-Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" /> | Visualização de KPIs e análise de qualidade. |

---

![Dashboard Preview](./dashboard_images/dashboard.gif)

🎯 The Challenge: Digital Transformation in Injection Molding
In high-volume plastic injection environments, performance tracking is often fragmented, manual, and prone to data silos. This project was engineered to solve three critical operational bottlenecks:

Complex OEE Calculation: Traditional methods struggle with "Fair OEE" when machines switch molds mid-shift. I implemented logic to dynamically recalculate availability and performance based on specific mold/machine cycle times.

Data Modernization (Legacy to Cloud): Transitioning from error-prone paper logs and isolated spreadsheets to a centralized, Cloud-backed SQL architecture (Supabase), ensuring a "single source of truth."

Granular Traceability: Establishing a relational link between downtime events and specific mold/machine pairs to identify hidden patterns in equipment failure or mold wear.

## 🛠️ Tech Stack
- **Frontend:** PHP (Data Entry Forms for Operators).
- **Database:** PostgreSQL (Relational storage via Docker).
- **Processing:** Python (Pandas/NumPy for OEE math and data engineering).
- **Visualization:** Streamlit (Business Intelligence Dashboard).
- **Infrastructure:** Docker & Docker-Compose.

## 🚀 Project Structure
- `/app_php`: PHP forms for registering production and downtime.
- `/scripts_python`: The "brain" of the project—handles OEE calculations and data processing.
- `/dashboard`: The interactive Streamlit dashboard.
- `/database`: SQL initialization scripts.
- `/dashboard_images`: Visual assets and performance screenshots.

## 📸 Screenshots
<p align="center">
  <img src="./dashboard_images/main.png" width="45%" />
  <img src="./dashboard_images/main1.png" width="45%" />
  <img src="./dashboard_images/main2.png" width="45%" />
  <img src="./dashboard_images/main3.png" width="45%" />
</p>

## ⚙️ How to Run
1. **Infrastructure:** Run `docker-compose up -d` to start the Database and PHP forms.
2. **Install Dependencies:** `pip install -r requirements.txt`
3. **Run Processing:** `python scripts_python/compute_oee.py`
4. **Launch Dashboard:** `streamlit run dashboard/dashboard.py`

---
**Author:** Ricardo Serenato Junior (https://www.linkedin.com/in/ricardoserenatojr/) 