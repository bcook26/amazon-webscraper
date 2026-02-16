import requests
import os
from bs4 import BeautifulSoup
import csv
import smtplib
import time
from datetime import date
from pathlib import Path

# ---------------------------
# Configuration
# ---------------------------
TEST = False
URL = "https://www.amazon.com/dp/B07FNW9FGJ"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}

CSV_FILE = "AmazonWebScraperDataset.csv"
MIN_BUY_PRICE = 14.00

EMAIL_ADDRESS = "user_email@email.com" if TEST else os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = "xxxxxxxxxxxx" if TEST else os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465


# ---------------------------
# Scraping Logic
# ---------------------------

def get_product_info(url: str) -> dict:
    """Fetch product title, price, and rating from Amazon."""
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    title = soup.find(id="productTitle")
    price = soup.find("span", class_="a-offscreen")
    rating = soup.find("span", class_="a-icon-alt")

    if not title or not price:
        raise ValueError("Could not find product title or price on page.")

    title_text = title.get_text(strip=True)
    price_value = float(price.get_text(strip=True).replace("$", ""))
    rating_text = rating.get_text(strip=True) if rating else "N/A"

    return {
        "title": title_text,
        "price": price_value,
        "rating": rating_text,
        "date": date.today(),
    }


# ---------------------------
# CSV Handling
# ---------------------------

def save_to_csv(data: dict):
    """Append product data to CSV file."""
    file_exists = Path(CSV_FILE).exists()

    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["ProductTitle", "Price", "Rating", "Date"])

        writer.writerow([data["title"], data["price"], data["rating"], data["date"]])


# ---------------------------
# Email Notification
# ---------------------------

def send_email(product_title: str, current_price: float):
    """Send email alert if price drops below threshold."""
    subject = f"Price Alert: {product_title}"
    body = (
        f"The product '{product_title}' is now ${current_price:.2f}.\n\n"
        f"It has dropped below your target price of ${MIN_BUY_PRICE:.2f}."
    )

    message = f"Subject: {subject}\n\n{body}"

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)


# ---------------------------
# Main Price Check
# ---------------------------

def check_price():
    try:
        product = get_product_info(URL)
        print(product)

        save_to_csv(product)

        if product["price"] < MIN_BUY_PRICE:
            send_email(product["title"], product["price"])

    except Exception as e:
        print(f"Error checking price: {e}")


# ---------------------------
# Scheduler (Daily Check)
# ---------------------------

if __name__ == "__main__":
    while True:
        check_price()
        time.sleep(86400)  # 24 hours
