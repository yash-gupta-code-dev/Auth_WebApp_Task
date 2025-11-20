from faker import Faker
import csv

fake = Faker()

with open("users.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["username", "email", "phone", "first_name", "last_name"])

    for _ in range(10000):
        first = fake.first_name()
        last = fake.last_name()
        writer.writerow([
            (first + last).lower(),
            fake.email(),
            fake.phone_number(),
            first,
            last
        ])
