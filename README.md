Real Estate Analytics API


The Real Estate Analytics API is designed to provide real estate agents with valuable insights into property listings. It aggregates and analyzes data from a real estate classified database, enabling users to make informed decisions based on metrics such as median prices, listing growth, and price trends.

Technologies Used
Python: Primary programming language for the backend.
Flask: Web framework for building the API.
SQLAlchemy: ORM for database interaction.
PostgreSQL: Relational database for storing property listings.
Pandas: Library for data manipulation and analysis.
Matplotlib & Seaborn: Libraries for data visualization.
Git: Version control system.
Installation
Clone the repository:
git clone https://github.com/narcosq/estate_analytics.git

Navigate to the project directory:
cd repo-name

Create a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install the required dependencies:
pip install -r requirements.txt

Set up the database and configure the connection in config.py.


API Endpoints
Analytics Endpoints


Get Median Price
GET /analytics/median_price

Query Parameters:
region: Filter by region.
city: Filter by city.
district: Filter by district.
Response: JSON object with the median price.

Get Listing Count

GET /analytics/listing_count

Query Parameters:
start_date: Start date for the analysis.
end_date: End date for the analysis.
Response: JSON object with the listing count.

Get Price Deviation

GET /analytics/price_deviation

Query Parameters:
region: Filter by region.
city: Filter by city.
district: Filter by district.
Response: JSON object with the price deviation.

Get Price Increase Count

GET /analytics/price_increase

Query Parameters:
region: Filter by region.
city: Filter by city.
district: Filter by district.
Response: JSON object with the count of price increases.

Get Price Decrease Count

GET /analytics/price_decrease

Query Parameters:
region: Filter by region.
city: Filter by city.
district: Filter by district.
Response: JSON object with the count of price decreases.
Listings Endpoints

Get All Listings

GET /listings
Response: JSON array of all listings.
Add New Listing

POST /listings
Request Body: JSON object containing price, square_meters, district, city, region.
Response: JSON object of the newly created listing.
Update Listing

PUT /listings/<int:id>
Request Body: JSON object containing deactivation_date, deactivation_reason.
Response: JSON object of the updated listing.

Running the Project
To run the project, use the following command:
python app.py
The API will be available at http://localhost:5000.

Usage Examples
Get Median Price
curl "http://localhost:5000/analytics/median_price?region=RegionName&city=CityName&district=DistrictName"

Get Listing Count
curl "http://localhost:5000/analytics/listing_count?start_date=2023-01-01&end_date=2023-01-31"

