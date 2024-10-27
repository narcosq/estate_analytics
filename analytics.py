import pandas as pd
from datetime import datetime, timedelta
from models import db, Listing
import matplotlib.pyplot as plt

# calculating median prices for a given region, city and neighborhood for the last month
def calculate_median_price(region=None, city=None, district=None):
    last_month = datetime.utcnow() - timedelta(days=30)
    query = db.session.query(Listing).filter(
        Listing.submission_date >= last_month
    )
    if region:
        query = query.filter(Listing.region == region)
    if city:
        query = query.filter(Listing.city == city)
    if district:
        query = query.filter(Listing.district == district)

    df = pd.read_sql(query.statement, db.session.bind)
    median_price = df['price'].median()
    return median_price

# get the number of ads for a specified period
def count_listings(start_date, end_date):
    query = db.session.query(Listing).filter(
        Listing.submission_date.between(start_date, end_date)
    )
    count = query.count()
    return count

# calculation of deviation from the average price for the month
def calculate_price_deviation(region=None, city=None, district=None):
    last_month = datetime.utcnow() - timedelta(days=30)
    query = db.session.query(Listing).filter(
        Listing.submission_date >= last_month
    )
    if region:
        query = query.filter(Listing.region == region)
    if city:
        query = query.filter(Listing.city == city)
    if district:
        query = query.filter(Listing.district == district)

    df = pd.read_sql(query.statement, db.session.bind)
    mean_price = df['price'].mean()
    current_price = df['price'].iloc[-1] if not df.empty else None
    deviation = current_price - mean_price if current_price is not None else None
    return deviation

# monthly price increases
def calculate_price_increase(region=None, city=None, district=None):
    last_month = datetime.utcnow() - timedelta(days=30)
    query = db.session.query(Listing).filter(
        Listing.submission_date >= last_month
    )
    if region:
        query = query.filter(Listing.region == region)
    if city:
        query = query.filter(Listing.city == city)
    if district:
        query = query.filter(Listing.district == district)

    df = pd.read_sql(query.statement, db.session.bind)
    increases = df[df['price'].diff() > 0]
    return increases.shape[0]

# monthly price reductions
def calculate_price_decrease(region=None, city=None, district=None):
    last_month = datetime.utcnow() - timedelta(days=30)
    query = db.session.query(Listing).filter(
        Listing.submission_date >= last_month
    )
    if region:
        query = query.filter(Listing.region == region)
    if city:
        query = query.filter(Listing.city == city)
    if district:
        query = query.filter(Listing.district == district)

    df = pd.read_sql(query.statement, db.session.bind)
    decreases = df[df['price'].diff() < 0]
    return decreases.shape[0]


# build graph
def plot_price_median(region=None, city=None, district=None):
    last_month = datetime.utcnow() - timedelta(days=30)
    query = db.session.query(Listing).filter(
        Listing.submission_date >= last_month
    )
    if region:
        query = query.filter(Listing.region == region)
    if city:
        query = query.filter(Listing.city == city)
    if district:
        query = query.filter(Listing.district == district)

    df = pd.read_sql(query.statement, db.session.bind)

    plt.figure(figsize=(10, 6))
    df['submission_date'] = pd.to_datetime(df['submission_date'])
    df.set_index('submission_date', inplace=True)

    median_prices = df['price'].resample('D').median()
    median_prices.plot(label='Median Price', color='blue')

    plt.title('Median Price Over the Last Month')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()
    plt.show()

# heatmap
def prepare_heatmap_data():
    query = db.session.query(Listing.district, Listing.city, Listing.region)
    df = pd.read_sql(query.statement, db.session.bind)
    heatmap_data = df.groupby(['region', 'city', 'district']).size().reset_index(name='count')
    return heatmap_data.to_dict('records')

# analyzing the growth in the number of announcements by date
def calculate_listing_growth():
    query = db.session.query(Listing.submission_date)
    df = pd.read_sql(query.statement, db.session.bind)
    df['submission_date'] = pd.to_datetime(df['submission_date'])
    growth = df['submission_date'].resample('M').count()
    return growth.to_dict()

def plot_listing_growth(start_date, end_date):
    query = db.session.query(Listing).filter(
        Listing.submission_date.between(start_date, end_date)
    )
    df = pd.read_sql(query.statement, db.session.bind)

    df['submission_date'] = pd.to_datetime(df['submission_date'])
    df.set_index('submission_date', inplace=True)

    listings_count = df.resample('D').count()['id']

    plt.figure(figsize=(10, 6))
    listings_count.plot(label='Listings Count', color='green')

    plt.title('Number of Listings Over the Period')
    plt.xlabel('Date')
    plt.ylabel('Count of Listings')
    plt.legend()
    plt.grid()
    plt.show()