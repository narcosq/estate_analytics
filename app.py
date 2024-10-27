from flask import Flask, request, jsonify, abort
from models import db, Listing
from analytics import calculate_median_price, calculate_listing_growth, prepare_heatmap_data, plot_listing_growth, \
    plot_price_median, calculate_price_decrease, calculate_price_increase, calculate_price_deviation, count_listings

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/real_estate'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

# get median price based on region, city, and district
@app.route("/analytics/median_price", methods=["GET"])
def get_median_price():
    region = request.args.get('region')
    city = request.args.get('city')
    district = request.args.get('district')
    median_price = calculate_median_price(region, city, district)
    return jsonify({"median_price": median_price})

# get the count of listings in a specified date range
@app.route("/analytics/listing_count", methods=["GET"])
def get_listing_count():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    count = count_listings(start_date, end_date)
    return jsonify({"listing_count": count})

# get price deviation based on region, city, and district
@app.route("/analytics/price_deviation", methods=["GET"])
def get_price_deviation():
    region = request.args.get('region')
    city = request.args.get('city')
    district = request.args.get('district')
    deviation = calculate_price_deviation(region, city, district)
    return jsonify({"price_deviation": deviation})

# get the count of price increases in a specified area
@app.route("/analytics/price_increase", methods=["GET"])
def get_price_increase():
    region = request.args.get('region')
    city = request.args.get('city')
    district = request.args.get('district')
    increase_count = calculate_price_increase(region, city, district)
    return jsonify({"price_increase_count": increase_count})

# get the count of price decreases in a specified area
@app.route("/analytics/price_decrease", methods=["GET"])
def get_price_decrease():
    region = request.args.get('region')
    city = request.args.get('city')
    district = request.args.get('district')
    decrease_count = calculate_price_decrease(region, city, district)
    return jsonify({"price_decrease_count": decrease_count})

# plot median price trends
@app.route("/analytics/plot/median_price", methods=["GET"])
def plot_median_price():
    region = request.args.get('region')
    city = request.args.get('city')
    district = request.args.get('district')
    plot_price_median(region, city, district)
    return jsonify({"message": "Plot generated."})

# plot listing growth trends
@app.route("/analytics/plot/listing_growth", methods=["GET"])
def plot_growth():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    plot_listing_growth(start_date, end_date)
    return jsonify({"message": "Growth plot generated."})

# get all listings
@app.route("/listings", methods=["GET"])
def get_listings():
    listings = Listing.query.all()
    result = [listing.to_dict() for listing in listings]
    return jsonify(result)

# add a new listing
@app.route("/listings", methods=["POST"])
def add_listing():
    data = request.get_json()
    listing = Listing(
        price=data.get('price'),
        square_meters=data.get('square_meters'),
        district=data.get('district'),
        city=data.get('city'),
        region=data.get('region')
    )
    db.session.add(listing)
    db.session.commit()
    return jsonify(listing.to_dict()), 201

# update an existing listing (e.g., for deactivation)
@app.route("/listings/<int:id>", methods=["PUT"])
def update_listing(id):
    listing = Listing.query.get(id)
    if not listing:
        abort(404)

    data = request.get_json()
    listing.deactivation_date = data.get('deactivation_date')
    listing.deactivation_reason = data.get('deactivation_reason')
    db.session.commit()
    return jsonify(listing.to_dict())

# get median price data
@app.route("/analytics/median_price", methods=["GET"])
def get_median_price():
    result = calculate_median_price()
    return jsonify(result)

# get listing growth data
@app.route("/analytics/listing_growth", methods=["GET"])
def get_listing_growth():
    result = calculate_listing_growth()
    return jsonify(result)

# get heatmap data
@app.route("/analytics/heatmap", methods=["GET"])
def get_heatmap_data():
    result = prepare_heatmap_data()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)