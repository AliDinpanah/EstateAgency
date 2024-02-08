import mysql.connector
from mysql.connector import Error
import db
import yaml
from hashlib import sha256
import os
import random

config = yaml.safe_load(open("./data/config.yaml"))


# Queries to create tables
create_agencies_table = """
CREATE TABLE IF NOT EXISTS agencies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    phone VARCHAR(15) UNIQUE,
    city VARCHAR(30) NOT NULL,
    employees_count TINYINT,
    admin_firstname VARCHAR(45) NOT NULL,
    admin_lastname VARCHAR(45) NOT NULL,
    admin_phone VARCHAR(15) UNIQUE NOT NULL,
    admin_password VARCHAR(256) NOT NULL
);
"""

create_ads_table = """
CREATE TABLE IF NOT EXISTS ads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(30) NOT NULL,
    district VARCHAR(40) NOT NULL,
    title VARCHAR(128) NOT NULL,
    description VARCHAR(512),
    rooms_count TINYINT UNSIGNED,
    price INT,
    rent INT,
    mortgage INT,
    metrage INT UNSIGNED NOT NULL,
    property_type ENUM("residential", "commercial", "office", "industrial") NOT NULL,
    uid DECIMAL(7) UNIQUE,
    agency_id INT,
    primary_image VARCHAR(255) NOT NULL,
    FOREIGN KEY (agency_id) REFERENCES agencies(id)
);
"""

create_facilities_table = """
CREATE TABLE IF NOT EXISTS facilities (
    id TINYINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30) NOT NULL
);
"""

create_conditions_table = """
CREATE TABLE IF NOT EXISTS conditions (
    id TINYINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30) NOT NULL
);
"""

create_ads_conditions_table = """
CREATE TABLE IF NOT EXISTS ads_conditions (
    ad_id INT NOT NULL,
    condition_id TINYINT NOT NULL,
    FOREIGN KEY (ad_id) REFERENCES ads(id),
    FOREIGN KEY (condition_id) REFERENCES conditions(id),
    PRIMARY KEY (ad_id, condition_id)
);
"""

create_ads_facilities_table = """
CREATE TABLE IF NOT EXISTS ads_facilities (
    ad_id INT NOT NULL,
    facility_id TINYINT NOT NULL,
    FOREIGN KEY (ad_id) REFERENCES ads(id),
    FOREIGN KEY (facility_id) REFERENCES facilities(id),
    PRIMARY KEY (ad_id, facility_id)
);
"""

create_ads_images_table = """
CREATE TABLE IF NOT EXISTS ads_images (
    ad_id INT NOT NULL,
    image_filename VARCHAR(255) NOT NULL,
    FOREIGN KEY (ad_id) REFERENCES ads(id),
    PRIMARY KEY (ad_id, image_filename)
);
"""

create_users_table = """
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    phone VARCHAR(15) NOT NULL,
    email VARCHAR(255),
    first_name VARCHAR(45),
    last_name VARCHAR(45),
    password VARCHAR(256)
);
"""

create_verification_codes_table = """
CREATE TABLE IF NOT EXISTS verification_codes (
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    phone VARCHAR(15) PRIMARY KEY NOT NULL,
    code DECIMAL(6) NOT NULL
);
""" # phone should not be set as foregin key becuase the user may not be registered yet

for table in ["ads_conditions", "ads_facilities", "conditions", "facilities", "ads_images", "verification_codes", "users", "ads", "agencies"]:
    db.execute_query( f"DROP TABLE IF EXISTS {table}")
    db.connection.commit()

# Execute the queries
db.execute_query(create_conditions_table)
db.execute_query(create_facilities_table)
db.execute_query(create_agencies_table)
db.execute_query(create_ads_table)
db.execute_query(create_ads_conditions_table)
db.execute_query(create_ads_facilities_table)
db.execute_query(create_ads_images_table)
db.execute_query(create_users_table)
db.execute_query(create_verification_codes_table)

# Insert some data
for key, val in config["facilities"].items():
    db.execute_query("INSERT INTO facilities (id, name) VALUES (%s, %s)", (key, val))

for key, val in config["conditions"].items():
    db.execute_query("INSERT INTO conditions (id, name) VALUES (%s, %s)", (key, val))


def password_hash(password: str) -> str:
    return sha256(password.encode()).hexdigest()

db.execute_query("INSERT INTO users (phone, email, first_name, last_name, password) VALUES (%s, %s, %s, %s, %s)", ("09383009302", "bagheri.810907@gmail.com", "Amir", "Bagheri", password_hash("1234")))
db.execute_query("INSERT INTO agencies (name, phone, city, employees_count, admin_firstname, admin_lastname, admin_phone, admin_password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", ("Agency 1", "021111111", "Tehran", 10, "Asghar", "Akbari", "09120000000", password_hash("1234")))
db.connection.commit()

# Insert some ads
images_list = os.listdir("./uploads/")
images_list = [image for image in images_list if image.endswith(".jpg") or image.endswith(".png") or image.endswith(".jpeg")]

min_facility_id = db.fetch_one("SELECT MIN(id) FROM facilities")[0]
max_facility_id = db.fetch_one("SELECT MAX(id) FROM facilities")[0]
min_condition_id = db.fetch_one("SELECT MIN(id) FROM conditions")[0]
max_condition_id = db.fetch_one("SELECT MAX(id) FROM conditions")[0]
agencies_ids = db.fetch_all("SELECT id FROM agencies")
agencies_ids = [agency[0] for agency in agencies_ids]

# Random ads

titles = [
    "Spacious Family Home in Quiet Neighborhood",
    "Modern Office Space in Central Business District",
    "Large Industrial Facility with Easy Access to Transport",
    "Prime Location Commercial Storefront",
    "Cozy and Affordable Studio Apartment Near Downtown",
    "Charming Studio Apartment in Central Tehran",
    "Luxury Villa with Private Garden in Saadat Abad",
    "Cozy Downtown Flat - Great for Singles",
    "Spacious Family Home Near Tajrish Square",
    "Modern Office Space in Vanak - Ideal for Startups",
    "Rustic Cabin in the Heart of Alborz Mountains",
    "Elegant Penthouse with Panoramic City Views",
    "Affordable Student Housing Close to University",
    "Fully Furnished Apartment - Short Term Lease Available",
    "High-Traffic Retail Space in Popular Shopping District",
    "Contemporary Art Studio in Cultural Hub",
    "Large Industrial Warehouse with Easy Highway Access",
    "Quiet Suburban House Perfect for Families",
    "Renovated Historical Building in Tehran's Old Town",
    "Boutique Bed and Breakfast in Scenic Location",
    "State-of-the-Art Gym Facility in a Busy Neighborhood",
    "Peaceful Countryside Retreat - A Nature Lover's Dream",
    "Small Office Building Suitable for Local Businesses",
    "Luxurious High-Rise Condo with Exclusive Amenities",
    "Budget-Friendly Studio in Up-and-Coming Area",
    "Contemporary Loft in Trendy Neighborhood",
    "Spacious and Bright Two-Bedroom Apartment",
    "Elegant Studio in Historic Downtown",
    "Family Home with Large Garden and Pool",
    "Sleek Minimalist Apartment with City Views",
    "Charming Countryside Cottage with Modern Amenities",
    "Luxury Penthouse with Rooftop Terrace",
    "Cozy Bungalow Near the Beach",
    "Stylish Townhouse in Gated Community",
    "Renovated Loft in Converted Warehouse",
    "Secluded Mountain Cabin with Stunning Views",
    "Impressive Estate with Private Vineyard",
    "Modern Eco-Friendly Home with Solar Panels",
    "Quaint Victorian House with Original Features",
    "Expansive Ranch with Horse Stables",
    "Beachfront Villa with Private Dock",
    "Urban Apartment Close to Nightlife and Shops",
    "Tranquil Lakeside Retreat in Natural Setting",
    "Chic Studio Perfect for City Living",
    "Grand Manor with Sweeping Lawns",
    "Functional Studio in Central Business District",
    "Historic Farmhouse with Rustic Charm",
    "Luxurious Apartment in High-Rise Complex",
    "Boutique City Center Flat with Balcony",
    "Contemporary Home with Smart Technology",
    "Spacious Suburban House with Home Office",
    "Charming Bed and Breakfast in Scenic Locale",
    "Sophisticated Condo with State-of-the-Art Gym",
    "Compact and Efficient Micro-Apartment",
    "Traditional Villa with Mediterranean Garden"
]

descriptions = [
    "This family home offers a serene living space with a large backyard, perfect for families seeking peace and quiet.",
    "Located in the heart of the city, this office space features modern amenities and open-plan working areas.",
    "Ideal for manufacturing or warehousing, this industrial site provides ample space and is well-connected to major transport routes.",
    "A high-traffic commercial space suitable for retail or dining, located in one of the city's most bustling areas.",
    "A compact and efficient studio apartment, ideal for singles or couples, featuring easy access to the city's amenities.",
    "This studio apartment offers a compact yet stylish living space, ideal for singles or couples, featuring a modern kitchenette and a well-appointed bathroom.",
    "Discover luxury living in this expansive villa, boasting a lush private garden, multiple bedrooms, a state-of-the-art kitchen, and a spacious living area perfect for entertaining.",
    "Ideal for students or young professionals, this cozy flat provides a comfortable living space with convenient access to city amenities and public transport.",
    "A family-friendly home in a serene neighborhood, featuring a large backyard, multiple bedrooms, a modern kitchen, and proximity to schools and parks.",
    "Offering a contemporary open-plan workspace, this office is perfect for startups or small businesses, located in a bustling commercial area with great connectivity.",
    "Escape to this rustic cabin surrounded by nature, offering a unique living experience with breathtaking mountain views and ample outdoor activities.",
    "This penthouse stands out with its elegant design, luxurious amenities, and a stunning panoramic view of the city, ideal for those seeking a high-end urban lifestyle.",
    "Affordable and convenient, this housing option is perfect for students, providing basic amenities and a community atmosphere close to major universities.",
    "Fully furnished and ready to move in, this apartment is perfect for short-term stays, featuring all necessary appliances and a comfortable living area.",
    "Positioned in a high-traffic shopping district, this retail space offers excellent visibility and footfall, ideal for businesses looking to attract a wide customer base.",
    "A creative space for artists and designers, this studio is situated in a vibrant cultural area, offering ample natural light and inspiration.",
    "This industrial warehouse provides vast storage space, easy access for large vehicles, and proximity to major highways, ideal for logistics and manufacturing operations.",
    "Located in a quiet suburban area, this house is perfect for families seeking a peaceful environment, with a spacious garden and friendly neighborhood.",
    "Rich in history, this renovated building combines classic architecture with modern amenities, located in the charming old town area of Tehran.",
    "Experience the beauty of the countryside in our boutique bed and breakfast, offering personalized service and a tranquil setting for a perfect getaway.",
    "A fully equipped gym facility in a prime location, attracting a steady clientele and offering various fitness classes and state-of-the-art equipment.",
    "Nestled in the countryside, this retreat is a haven for nature enthusiasts, featuring hiking trails, wildlife watching, and a peaceful atmosphere.",
    "Suitable for local businesses or startups, this small office building offers a professional environment with flexible workspace options and basic amenities.",
    "Experience high-rise living in this luxurious condo, featuring exclusive amenities such as a swimming pool, fitness center, and 24-hour security services.",
    "An affordable option for those looking to live in an up-and-coming area, this studio offers basic amenities and a community feel, with easy access to local attractions."
]

city_district_pairs = {
    "Tehran": ["Tajrish", "Shoosh", "Tehran Pars", "Vanak", "Azadi", "Enghelab", "Gisha", "Saadat Abad", "Shahrak-e Gharb", "Niavaran"],
    "Isfahan": ["Jolfa", "Kooshk", "Rehnan", "Shahin Shahr", "Baharestan"],
    "Shiraz": ["Zargari", "Afif-Abad", "Eram", "Sa'adi", "Darvazeh Qoran"],
    "Tabriz": ["El Goli", "Valiasr", "Khiyavan", "Sheshgelan", "Baghmishe"],
    "Mashhad": ["Ahmadabad", "Sajjad", "Tabarsi", "Ghasem Abad", "Navab Safavi"],
    "Qom": ["Salman Farsi", "Payaneh", "Bajak", "Markazi", "Panjeh Ali"]
}

property_types = ["residential", "commercial", "office", "industrial"]

def create_random_ad():
    city = random.choice(list(city_district_pairs.keys()))
    district = random.choice(city_district_pairs[city])
    title = random.choice(titles)
    description = random.choice(descriptions)
    rooms_count = random.randint(0, 5)
    price = random.randint(50000, 1000000) if random.random() > 0.3 else -1
    rent = random.randint(500, 5000) if random.random() > 0.3 else -1
    mortgage = random.randint(10000, 50000) if random.choice([True, False]) else -1
    if random.random() > 0.5:
        price = None
    else:
        rent = None
        mortgage = None
    metrage = random.randint(50, 500)
    property_type = random.choice(property_types)
    uid = random.uniform(1000000, 9999999)
    agency_id = random.choice(agencies_ids)
    primary_image = random.choice(images_list)

    cursor = db.execute_query("""
    INSERT INTO ads (city, district, title, description, rooms_count, price, rent, mortgage, metrage, property_type, uid, agency_id, primary_image)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (city, district, title, description, rooms_count, price, rent, mortgage, metrage, property_type, uid, agency_id, primary_image))

    ad_id = cursor.lastrowid

    # Randomly assign facilities and conditions
    facilities_count = random.randint(1, max_facility_id - min_facility_id + 1)
    conditions_count = random.randint(1, max_condition_id - min_condition_id + 1)

    selected_facilities = random.sample(range(min_facility_id, max_facility_id + 1), facilities_count)
    selected_conditions = random.sample(range(min_condition_id, max_condition_id + 1), conditions_count)

    for facility_id in selected_facilities:
        db.execute_query("INSERT INTO ads_facilities (ad_id, facility_id) VALUES (%s, %s)", (ad_id, facility_id))

    for condition_id in selected_conditions:
        db.execute_query("INSERT INTO ads_conditions (ad_id, condition_id) VALUES (%s, %s)", (ad_id, condition_id))
    
    # Randomly assign images
    images_count = random.randint(0, 4)
    selected_images = random.sample(images_list, images_count)
    db.execute_query("INSERT INTO ads_images (ad_id, image_filename) VALUES (%s, %s)", (ad_id, primary_image))
    for image in selected_images:
        if image == primary_image:
            continue
        db.execute_query("INSERT INTO ads_images (ad_id, image_filename) VALUES (%s, %s)", (ad_id, image))

# Insert 100 random ads
for _ in range(100):
    create_random_ad()

db.connection.commit()
