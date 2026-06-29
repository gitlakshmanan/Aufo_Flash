# 📊 Auto Flash KPI Dashboard

A **Streamlit-based KPI Dashboard** that analyzes Excel data and provides interactive visualizations, daily performance metrics, trend analysis, and automatic alerts for significant changes in quantity and revenue.

---

## 🚀 Features

- 📁 Upload Excel files (`.xlsx` / `.xls`)
- 📄 Select worksheets from the uploaded file
- 📅 Filter data by date range
- 🔍 Filter by Service Type
- 📈 Daily KPI metric cards
- 📊 Interactive charts using Plotly
- 🚨 Automatic detection of drastic changes (20%+)
- 🔴 Critical, Warning, and Moderate alert system
- 📉 Revenue trend analysis
- 📦 Quantity trend analysis
- 📊 Weekly, Monthly & Quarterly comparisons
- 💡 Business insights and summary metrics
- 🎨 Modern responsive Streamlit UI

---

## 🛠️ Technologies Used

- Python 3.x
- Streamlit
- Pandas
- NumPy
- Plotly
- OpenPyXL

---

## 📂 Project Structure

```
auto_flash/
│
├── auto_flash.py          # Main Streamlit application
├── requirements.txt
├── README.md
└── sample_data.xlsx
```

---

## 📥 Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/auto_flash.git

cd auto_flash
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
streamlit run auto_flash.py
```

The application will open automatically in your browser.

---

## 📄 Expected Excel Format

The uploaded Excel sheet must contain the following columns:

| Column | Description |
|---------|-------------|
| ServiceType | Name of the service |
| Reportdate | Date of report |
| Total | Quantity processed |
| Amount | Revenue amount |

Example:

| ServiceType | Reportdate | Total | Amount |
|--------------|------------|------:|-------:|
| Fulfillment | 2026-01-01 | 120 | 1500 |
| Clean & Screen | 2026-01-02 | 90 | 980 |

---

## 📊 Dashboard Modules

### KPI Cards

Displays daily:

- Total Quantity
- Revenue
- Difference from previous day
- Percentage change

---

### Revenue Analysis

Interactive charts include:

- Daily Revenue Trend
- Daily Quantity Trend
- Weekly Revenue Analysis
- Monthly Comparison
- Quarterly Distribution
- Week-over-Week Comparison

---

### Smart Alerts

Automatically detects sudden changes.

Severity Levels:

| Change | Status |
|---------|---------|
| ≥20% | Moderate |
| ≥30% | Warning |
| ≥50% | Critical |

Alerts display:

- Quantity change
- Revenue change
- Previous vs Current values
- Percentage difference

---

## 📈 Key Insights

The dashboard automatically calculates:

- Highest Revenue Day
- Average Daily Revenue
- Total Revenue
- Total Quantity
- Weekly Performance Change

---

## 📦 Required Python Packages

```text
streamlit
pandas
numpy
plotly
openpyxl
scikit-learn
```

---

## 📌 Future Improvements

- Database integration
- Automatic Excel refresh
- Email alerts
- PDF report generation
- User authentication
- Export dashboard to PDF
- AI-based revenue forecasting
- Machine Learning anomaly detection

---

## 👨‍💻 Developer

**Lakshmanan Chelliah**

Python Developer | Data Analytics | AI & Machine Learning Enthusiast

---

## 📄 License

This project is licensed under the MIT License.

---

## ⭐ If you like this project

Give it a ⭐ on GitHub and feel free to contribute by submitting issues or pull requests.