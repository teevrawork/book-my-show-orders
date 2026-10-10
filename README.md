# 🎟️ Book My Show Orders — Movie Ticket Analytics Dashboard

**An interactive movie ticket booking and revenue analytics project built with Python, Pandas, Plotly, and Streamlit.**

🔗 **[Live Dashboard](https://book-my-show-orders.streamlit.app/)**

> This is an independent portfolio project using synthetic data. It is not affiliated with BookMyShow. Movie titles and release information are illustrative and should not be treated as verified release records.

## 📌 Business Problem

Movie ticketing businesses need to understand booking trends, revenue performance, customer demand, cinema occupancy, and cancellations.

This project demonstrates how transactional booking data can be transformed into interactive business intelligence dashboards.

## 📊 Dashboard Features

- Executive KPIs: revenue, ticket sales, confirmed orders, cancellations, and average order value
- Interactive filters for cities, movies, industries, and show dates
- Movie performance and city-level sales analysis
- Cinema occupancy analysis
- Payment and cancellation analysis
- Dynamic business insights and actionable recommendations

## 💡 Business Insights

The dashboard automatically identifies:

1. **Top Revenue City:** The city contributing the highest confirmed revenue.
2. **Best-Selling Movie:** The movie with the most confirmed ticket sales.
3. **Cancellation Analysis:** The proportion of cancelled orders and whether it exceeds an illustrative 10% review threshold.

Business recommendations help users identify areas for further investigation.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Data generation and application logic |
| Pandas | Data cleaning, joining, and aggregation |
| Plotly | Interactive data visualization |
| Streamlit | Dashboard interface and deployment |
| GitHub | Version control and project hosting |

## 🗂️ Dataset

The project uses seven related synthetic CSV datasets:

- `movies.csv`
- `cinemas.csv`
- `customers.csv`
- `shows.csv`
- `orders.csv`
- `tickets.csv`
- `payments.csv`

The current show dataset covers **October 2–10, 2026**.

## 🚀 Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the dashboard:

```bash
streamlit run app.py
```

## 🎯 Project Outcomes

This project demonstrates:

- Working with relational datasets
- Creating business KPIs
- Building interactive analytical dashboards
- Translating data into business insights
- Deploying a Python application using GitHub and Streamlit

## 🔗 Live Project

**Dashboard:** https://book-my-show-orders.streamlit.app/

**Repository:** https://github.com/teevrawork/book-my-show-orders

---

*Built as a hands-on Data Analytics and Business Intelligence portfolio project.*
