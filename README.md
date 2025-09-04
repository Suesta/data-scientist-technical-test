# 🧪 Data Scientist Technical Test

This repository contains the full solution to a **technical test for a Junior Data Scientist position**, covering email classification, data analysis, visualization, and flexible rule-based systems.  
The project is divided into four main parts, each tackling a different challenge while maintaining reproducibility, clarity, and modular design.

---

## 📂 Repository Structure

```text
.
├── PART_1/   # Email classification API with FastAPI + MySQL
├── PART_2/   # Analysis and visualization of categorized emails
├── PART_3/   # Draft generation of customer responses with GPT
├── PART_4/   # Flexible rule-based email classification system
├── LICENSE
└── Problem Statement.docx  # Original technical test description
````

---

## 🔎 Part Overview

### **PART 1 – Email Classification API**

* REST service built with **FastAPI** to classify customer emails into 8 business categories.
* Integrates with a **MySQL database** (customers, debts, emails).
* Automatically excludes customers with outstanding payments.
* Includes **unit tests** and Docker setup (`Dockerfile` + `docker-compose.yml`).
* **Deliverable:** `emails_categorizados.csv`.

---

### **PART 2 – Analysis & Visualization**

* Analytical module that processes the classified emails (`emails_categorizados.csv`).
* Produces insights and visualizations:

  * Volume of emails per category.
  * Email distribution by month and day of the week.
* Outputs charts as `.png` files and a results report (`INFORME_RESULTADOS.md`).

---

### **PART 3 – Automated Response Drafting**

* Consumes the classification API from **Part 1**.
* Uses **OpenAI GPT** (`gpt-4o-mini`) to generate **tailored draft responses**.
* Handles both normal customers and debtors (impagos) with appropriate messaging.
* Configurable via `.env` (`OPENAI_API_KEY`, `CLASSIFY_URL`).

---

### **PART 4 – Flexible Classification System**

* Natural Language (NL) configurable rule-based classifier.
* Rules can be written in Spanish or English, converted to JSON, and evaluated sequentially.
* If no rule applies, falls back to the **Part 1 API** for classification.
* Fully tested with unit tests (`pytest`).

---

## 🛠️ Technologies Used

* **Languages & Frameworks:** Python 3.9+, FastAPI, SQL (MySQL), PyTorch (for text processing in extensions).
* **Data & Analysis:** Pandas, Matplotlib, Regex.
* **Infra & Tools:** Docker, Docker Compose, `.env` environment variables.
* **AI/ML:** OpenAI GPT (for response generation).
* **Testing:** Pytest (unit tests included).

---

## 🚀 Quick Start

Clone the repository:

```bash
git clone https://github.com/Suesta/data-scientist-technical-test.git
cd data-scientist-technical-test
```

Follow the setup instructions in each part:

* **Part 1:** Launch FastAPI + MySQL using Docker Compose.
* **Part 2:** Run the analysis script once `emails_categorizados.csv` is available.
* **Part 3:** Configure `.env` with OpenAI API key and run `main.py`.
* **Part 4:** Run tests (`pytest -q`) to validate the flexible classification system.

---

## 📌 Notes

* Sensitive information (API keys, credentials) is excluded from the repo (`.env` files not uploaded).
* All data is **synthetic or anonymized** for the purpose of the technical test.
* The repo is designed to showcase **end-to-end problem solving** for a Data Scientist role: from API development to analysis and response automation.

---
