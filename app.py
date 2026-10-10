
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Book My Show Orders",
    page_icon="🎟️",
    layout="wide"
)


st.markdown("""
<style>
.stApp {
    background-color: #0b1220;
    color: #e5edf7;
}

/* KPI card background */
[data-testid="stMetric"] {
    background-color: #19263b;
    border: 1px solid #334155;
    padding: 18px;
    border-radius: 14px;
}

/* KPI labels */
[data-testid="stMetricLabel"] {
    color: #cbd5e1 !important;
}

[data-testid="stMetricLabel"] p {
    color: #cbd5e1 !important;
}

/* KPI numbers - bright cyan */
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] * {
    color: #38bdf8 !important;
    font-weight: 800 !important;
}

/* Revenue */
div[data-testid="stMetric"]:has(
    [data-testid="stMetricLabel"]
    :is(p, div):first-child
) {
    border-color: #334155;
}

/* Main headings */
h1, h2, h3 {
    color: #f8fafc !important;
}

/* Sidebar text */
section[data-testid="stSidebar"] {
    color: #0f172a;
}
</style>
""", unsafe_allow_html=True)


DATA = Path(__file__).parent / "data"

@st.cache_data(ttl=60)
def load_data():
    names = [
        "movies", "cinemas", "customers",
        "shows", "orders", "tickets", "payments"
    ]

    tables = {
        name: pd.read_csv(DATA / f"{name}.csv")
        for name in names
    }

    tables["shows"]["show_datetime"] = pd.to_datetime(
        tables["shows"]["show_datetime"]
    )
    tables["orders"]["booking_date"] = pd.to_datetime(
        tables["orders"]["booking_date"]
    )

    sales = (
        tables["orders"]
        .merge(tables["shows"], on="show_id")
        .merge(tables["movies"], on="movie_id")
        .merge(
            tables["cinemas"],
            on="cinema_id",
            suffixes=("", "_cinema")
        )
        .merge(tables["payments"], on="order_id")
    )

    return tables, sales

try:
    tables, all_orders = load_data()
except (FileNotFoundError, ValueError, KeyError) as error:
    st.error(f"Unable to load datasets: {error}")
    st.stop()


st.title("🎟️ Book My Show Orders")
st.caption(
    "Movie Ticketing & Revenue Intelligence | "
    "Synthetic portfolio dataset — not affiliated with BookMyShow"
)

# SIDEBAR FILTERS
st.sidebar.header("Dashboard Filters")

cities = sorted(all_orders["city"].unique())
movies = sorted(all_orders["movie_name"].unique())
industries = sorted(all_orders["industry"].unique())

selected_cities = st.sidebar.multiselect(
    "Cinema Cities", cities, default=cities
)
selected_movies = st.sidebar.multiselect(
    "Movies", movies, default=movies
)
selected_industries = st.sidebar.multiselect(
    "Industries", industries, default=industries
)

min_date = all_orders["show_datetime"].dt.date.min()
max_date = all_orders["show_datetime"].dt.date.max()

dates = st.sidebar.date_input(
    "Show Dates",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if not isinstance(dates, (tuple, list)) or len(dates) != 2:
    st.info("Select both start and end dates.")
    st.stop()

start_date, end_date = dates

filtered = all_orders[
    all_orders["city"].isin(selected_cities)
    & all_orders["movie_name"].isin(selected_movies)
    & all_orders["industry"].isin(selected_industries)
    & all_orders["show_datetime"].dt.date.between(
        start_date, end_date
    )
].copy()

if filtered.empty:
    st.warning("No orders match your filters.")
    st.stop()

confirmed = filtered[
    filtered["status"] == "Confirmed"
].copy()

cancelled = filtered[
    filtered["status"] == "Cancelled"
].copy()

tickets_sold = int(confirmed["ticket_quantity"].sum())
revenue = float(confirmed["order_amount"].sum())
bookings = len(confirmed)
cancellations = len(cancelled)
refunds = float(cancelled["payment_amount"].sum())

# EXECUTIVE KPIS
st.subheader("📊 Executive Overview")

a, b, c, d = st.columns(4)

a.metric("Confirmed Revenue", f"₹{revenue:,.0f}")
b.metric("Tickets Sold", f"{tickets_sold:,}")
c.metric("Confirmed Orders", f"{bookings:,}")
d.metric("Cancelled Orders", f"{cancellations:,}")

e, f, g, h = st.columns(4)

e.metric(
    "Average Order Value",
    f"₹{revenue / bookings:,.0f}" if bookings else "₹0"
)
f.metric(
    "Average Ticket Price",
    f"₹{revenue / tickets_sold:,.0f}"
    if tickets_sold else "₹0"
)
g.metric(
    "Cancellation Rate",
    f"{100 * cancellations / len(filtered):.1f}%"
)
h.metric("Refunded Amount", f"₹{refunds:,.0f}")

st.divider()

# MOVIE PERFORMANCE
st.subheader("🎬 Movie Performance")

movie_sales = (
    confirmed.groupby(
        ["movie_name", "industry"], as_index=False
    )
    .agg(
        tickets_sold=("ticket_quantity", "sum"),
        revenue=("order_amount", "sum"),
        orders=("order_id", "nunique")
    )
    .sort_values("tickets_sold", ascending=False)
)

left, right = st.columns(2)

with left:
    fig = px.bar(
        movie_sales,
        x="tickets_sold",
        y="movie_name",
        color="industry",
        orientation="h",
        title="Top Movies by Tickets Sold",
        labels={
            "movie_name": "Movie",
            "tickets_sold": "Tickets"
        }
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)

with right:
    industry_sales = (
        confirmed.groupby("industry", as_index=False)[
            "ticket_quantity"
        ].sum()
    )
    fig = px.pie(
        industry_sales,
        names="industry",
        values="ticket_quantity",
        hole=0.55,
        title="Bollywood vs Hollywood Ticket Share"
    )
    st.plotly_chart(fig, use_container_width=True)

# CITY-WISE MOVIE SALES
st.subheader("🏙️ Movie Sales by City")

city_movie = (
    confirmed.groupby(
        ["city", "movie_name"], as_index=False
    )
    .agg(
        tickets_sold=("ticket_quantity", "sum"),
        revenue=("order_amount", "sum"),
        orders=("order_id", "nunique")
    )
)

if not city_movie.empty:
    winners = (
        city_movie.sort_values(
            ["city", "tickets_sold", "revenue", "movie_name"],
            ascending=[True, False, False, True]
        )
        .drop_duplicates("city")
    )

    st.markdown("**Best-Selling Movie in Each City**")
    st.dataframe(
        winners,
        use_container_width=True,
        hide_index=True
    )

    fig = px.bar(
        city_movie,
        x="city",
        y="tickets_sold",
        color="movie_name",
        barmode="group",
        title="Movie Ticket Sales Across Cities",
        labels={
            "city": "Cinema City",
            "tickets_sold": "Confirmed Tickets",
            "movie_name": "Movie"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# DAILY TRENDS
st.subheader("📈 Revenue and Ticket Trends")

trend = (
    confirmed.assign(
        show_day=confirmed["show_datetime"].dt.date
    )
    .groupby("show_day", as_index=False)
    .agg(
        revenue=("order_amount", "sum"),
        tickets=("ticket_quantity", "sum")
    )
)

left, right = st.columns(2)

with left:
    st.plotly_chart(
        px.line(
            trend,
            x="show_day",
            y="revenue",
            markers=True,
            title="Daily Revenue",
            labels={
                "show_day": "Show Date",
                "revenue": "Revenue (₹)"
            }
        ),
        use_container_width=True
    )

with right:
    st.plotly_chart(
        px.line(
            trend,
            x="show_day",
            y="tickets",
            markers=True,
            title="Daily Ticket Sales",
            labels={
                "show_day": "Show Date",
                "tickets": "Tickets"
            }
        ),
        use_container_width=True
    )

# CINEMA PERFORMANCE
st.subheader("🏢 Cinema Performance & Occupancy")

cinema_sales = (
    confirmed.groupby(
        ["city", "cinema_name"], as_index=False
    )
    .agg(
        tickets_sold=("ticket_quantity", "sum"),
        revenue=("order_amount", "sum")
    )
)

show_scope = (
    tables["shows"]
    .merge(
        tables["cinemas"][
            ["cinema_id", "cinema_name", "city"]
        ],
        on="cinema_id"
    )
    .merge(
        tables["movies"][
            ["movie_id", "movie_name", "industry"]
        ],
        on="movie_id"
    )
)

show_scope = show_scope[
    show_scope["city"].isin(selected_cities)
    & show_scope["movie_name"].isin(selected_movies)
    & show_scope["industry"].isin(selected_industries)
    & show_scope["show_datetime"].dt.date.between(
        start_date, end_date
    )
]

capacity = (
    show_scope.groupby(
        ["city", "cinema_name"], as_index=False
    )["seat_capacity"].sum()
)

cinema_stats = capacity.merge(
    cinema_sales,
    on=["city", "cinema_name"],
    how="left"
).fillna({
    "tickets_sold": 0,
    "revenue": 0
})

cinema_stats["occupancy_pct"] = (
    100
    * cinema_stats["tickets_sold"]
    / cinema_stats["seat_capacity"]
).round(1)

st.dataframe(
    cinema_stats,
    use_container_width=True,
    hide_index=True
)

# PAYMENTS AND CANCELLATIONS
left, right = st.columns(2)

with left:
    st.subheader("💳 Payment Analysis")
    paid = (
        confirmed.groupby(
            "payment_method", as_index=False
        )["payment_amount"].sum()
    )
    st.plotly_chart(
        px.bar(
            paid,
            x="payment_method",
            y="payment_amount",
            title="Revenue by Payment Method"
        ),
        use_container_width=True
    )

with right:
    st.subheader("🎟️ Order Status")
    status_counts = (
        filtered["status"].value_counts().reset_index()
    )
    status_counts.columns = ["status", "orders"]

    st.plotly_chart(
        px.pie(
            status_counts,
            names="status",
            values="orders",
            hole=0.55,
            title="Confirmed vs Cancelled Orders"
        ),
        use_container_width=True
    )

# DATA EXPLORER
st.divider()
st.subheader("🔎 Booking Data Explorer")

view = filtered[
    [
        "order_id",
        "booking_date",
        "show_datetime",
        "city",
        "cinema_name",
        "movie_name",
        "industry",
        "ticket_quantity",
        "order_amount",
        "status",
        "payment_method"
    ]
].sort_values("booking_date", ascending=False)

st.dataframe(
    view,
    use_container_width=True,
    hide_index=True
)

st.download_button(
    "Download Filtered Orders",
    data=view.to_csv(index=False).encode("utf-8"),
    file_name="book_my_show_filtered_orders.csv",
    mime="text/csv"
)

st.caption(
    "All transactions and performance figures are synthetic. "
    "Movie metadata is illustrative and should be verified."
)
