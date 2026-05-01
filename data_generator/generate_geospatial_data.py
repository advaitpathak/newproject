import json
import random
import string
from datetime import datetime


def generate_random_string(length):
    letters = string.ascii_letters + string.digits + " " * 5
    return ''.join(random.choice(letters) for _ in range(length))


def generate_sample_record_20columns():
    record = {
        "id": random.randint(1, 10000),
        "latitude": random.uniform(-90, 90),
        "longitude": random.uniform(-180, 180),
        "name": generate_random_string(10),
        "address": generate_random_string(20),
        "city": generate_random_string(10),
        "state": generate_random_string(10),
        "country": generate_random_string(10),
        "zipcode": generate_random_string(6),
        "category": generate_random_string(10),
        "description": generate_random_string(50),
        "website": "https://example.com",
        "phone": "+1-123-456-7890",
        "email": "example@example.com",
        "rating": round(random.uniform(0, 5), 1),
        "opening_hours": generate_random_string(15),
        "created_at": datetime.utcnow().strftime('%Y-%m-%d'),
        "updated_at": datetime.utcnow().strftime('%Y-%m-%d'),
        "tags": [generate_random_string(5) for _ in range(random.randint(1, 5))]
    }
    return record


if __name__ == '__main__':
    # 20 Columns data generator
    rows = 10000
    records = [generate_sample_record_20columns() for _ in range(rows)]
    with open("geospatial_data_10k.json", "w") as file:
        json.dump(records, file, indent=4)
    print("Sample records saved to 'sample_records.json'")