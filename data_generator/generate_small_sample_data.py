import json
import random
import string


def generate_random_data_2columns(rows):
    data = []
    for _ in range(rows):
        random_string = ''.join(random.choices(string.ascii_letters, k=5))
        random_number = random.randint(1, 100)
        data.append({"name": random_string, "age": random_number})
    return data


def generate_json_file_2columns(filename, rows):
    data = generate_random_data_2columns(rows)
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


if __name__ == '__main__':
    # 2 Columns data generator
    generate_json_file_2columns('name_age_10k.json', 10000)
