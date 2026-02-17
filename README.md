# 🛒 Amazon Price Tracker

A simple Python script that monitors the price of a product on Amazon and sends an email notification when the price drops below a specified threshold.

---

## 📌 Features

- Scrapes:
  - Product Title
  - Current Price
  - Product Rating
- Logs price data to a CSV file
- Sends an email alert when the price falls below your target price
- Runs automatically once per day (configurable)

---

## 🛠 Technologies Used

- Python 3.14
- requests
- BeautifulSoup (bs4)
- smtplib
- csv
- datetime
- time
- pathlib

---

## 📂 Project Structure

amazon-price-tracker/
│
├── price_tracker.py
├── AmazonWebScraperDataset.csv
└── README.md