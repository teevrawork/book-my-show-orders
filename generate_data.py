
import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

# 1. MOVIES
# Release dates and durations are illustrative
# and should be verified before presenting as facts.

movies = pd.DataFrame([
    [101, "Drishyam: The Conclusion", "Thriller", "Hindi", "Bollywood", "2026-10-02", 150],
    [102, "Pooja Meri Jaan", "Drama", "Hindi", "Bollywood", "2026-10-02", 130],
    [103, "Prem Keetanu", "Romance", "Hindi", "Bollywood", "2026-10-02", 138],
    [104, "Reporting Live", "Thriller", "Hindi", "Bollywood", "2026-10-09", 135],
    [105, "Digger", "Comedy", "English", "Hollywood", "2026-10-02", 130],
    [106, "Verity", "Thriller", "English", "Hollywood", "2026-10-02", 125],
    [107, "The Social Reckoning", "Drama", "English", "Hollywood", "2026-10-09", 135],
    [108, "Animals", "Crime Thriller", "English", "Hollywood", "2026-10-09", 130]
], columns=[
    "movie_id", "movie_name", "genre",
    "language", "industry", "release_date",
    "duration_minutes"
])

# 2. CINEMAS
cinemas = pd.DataFrame([
    [201, "PVR Delhi Demo", "Delhi", 180],
    [202, "INOX Gurugram Demo", "Gurugram", 160],
    [203, "Cinepolis Mumbai Demo", "Mumbai", 200],
    [204, "PVR Pune Demo", "Pune", 175],
    [205, "INOX Bengaluru Demo", "Bengaluru", 190]
], columns=[
    "cinema_id", "cinema_name", "city",
    "seat_capacity"
])

# 3. CUSTOMERS
cities = cinemas["city"].tolist()

customers = pd.DataFrame([
    [
        customer_id,
        random.choice(["18-24", "25-34", "35-44", "45+"]),
        random.choice(cities)
    ]
    for customer_id in range(1001, 1501)
], columns=["customer_id", "age_group", "city"])

# 4. SHOWTIMES
shows_data = []
start_date = datetime(2026, 10, 10)

for show_id in range(3001, 3401):
    movie = movies.iloc[random.randrange(len(movies))]
    cinema = cinemas.iloc[random.randrange(len(cinemas))]

    show_date = start_date + timedelta(
        days=random.randint(0, 29)
    )

    show_datetime = show_date + timedelta(
        hours=random.choice([10, 13, 16, 19, 22])
    )

    shows_data.append([
        show_id,
        int(movie["movie_id"]),
        int(cinema["cinema_id"]),
        show_datetime,
        random.choice([150, 200, 250, 300, 350]),
        int(cinema["seat_capacity"])
    ])

shows = pd.DataFrame(shows_data, columns=[
    "show_id", "movie_id", "cinema_id",
    "show_datetime", "ticket_price", "seat_capacity"
])

# 5. ORDERS, TICKETS AND PAYMENTS
orders_data = []
tickets_data = []
payments_data = []

remaining_seats = dict(
    zip(shows["show_id"], shows["seat_capacity"])
)

for order_id in range(5001, 9001):
    available_shows = [
        show_id for show_id, remaining
        in remaining_seats.items()
        if remaining > 0
    ]

    if not available_shows:
        break

    show_id = random.choice(available_shows)
    show = shows.loc[shows["show_id"] == show_id].iloc[0]

    quantity = random.randint(
        1, min(5, remaining_seats[show_id])
    )

    status = random.choices(
        ["Confirmed", "Cancelled"],
        weights=[92, 8]
    )[0]

    ticket_price = int(show["ticket_price"])
    amount = quantity * ticket_price

    booking_date = show["show_datetime"] - timedelta(
        days=random.randint(1, 10)
    )

    customer_id = random.choice(
        customers["customer_id"].tolist()
    )

    orders_data.append([
        order_id, customer_id, show_id,
        booking_date, quantity, status, amount
    ])

    for seat_number in range(1, quantity + 1):
        tickets_data.append([
            f"T{order_id}-{seat_number}",
            order_id,
            random.choice(["Regular", "Premium", "Recliner"]),
            ticket_price
        ])

    payments_data.append([
        f"P{order_id}",
        order_id,
        random.choice([
            "UPI", "Credit Card", "Debit Card", "Wallet"
        ]),
        amount,
        "Paid" if status == "Confirmed" else "Refunded"
    ])

    if status == "Confirmed":
        remaining_seats[show_id] -= quantity

orders = pd.DataFrame(orders_data, columns=[
    "order_id", "customer_id", "show_id",
    "booking_date", "ticket_quantity",
    "status", "order_amount"
])

tickets = pd.DataFrame(tickets_data, columns=[
    "ticket_id", "order_id",
    "seat_category", "ticket_price"
])

payments = pd.DataFrame(payments_data, columns=[
    "payment_id", "order_id",
    "payment_method", "payment_amount",
    "payment_status"
])

# 6. EXPORT DATASETS
datasets = {
    "movies": movies,
    "cinemas": cinemas,
    "customers": customers,
    "shows": shows,
    "orders": orders,
    "tickets": tickets,
    "payments": payments
}

for name, dataframe in datasets.items():
    dataframe.to_csv(f"{name}.csv", index=False)
    print(f"{name}.csv: {len(dataframe)} rows")

print("All seven datasets generated successfully!")
