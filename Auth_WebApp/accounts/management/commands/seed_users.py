import csv
import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class Command(BaseCommand):
    help = 'Generates 10,000 fake users and saves credentials to a CSV file'

    def handle(self, *args, **kwargs):
        fake = Faker()
        users_to_create = []
        total_users = 10000
        plain_password = 'password123' # The password we will write to the file
        
        # Pre-hash the password for the Database (Speed optimization)
        hashed_password = make_password(plain_password)

        self.stdout.write(self.style.WARNING(f'Generating {total_users} users and writing to CSV...'))

        #Open a CSV file to write the credentials
        filename = 'users_credentials.csv'
        
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            writer.writerow(['Username', 'Email', 'Phone Number', 'First Name', 'Last Name', 'Password'])

            for i in range(total_users):
                # Generate Data
                email = fake.unique.email()
                # Ensure username is unique enough
                username = email.split('@')[0] + f"_{i}_{random.randint(100,999)}"
                
                # Generate unique phone: +15550000000 to +15550009999
                phone = f"+1555{i:07d}" 
                
                first_name = fake.first_name()
                last_name = fake.last_name()

                # A. Write to CSV (Plain Text)
                writer.writerow([username, email, phone, first_name, last_name, plain_password])

                # B. Create User Object (Hashed Password)
                user = User(
                    username=username,
                    email=email,
                    phone_number=phone,
                    first_name=first_name,
                    last_name=last_name,
                    password=hashed_password,
                    is_active=True,
                    is_staff=False,
                    is_superuser=False
                )
                users_to_create.append(user)

                if (i + 1) % 1000 == 0:
                    self.stdout.write(f'Processed {i + 1} users...')

        # Bulk Insert into Database
        self.stdout.write(self.style.WARNING('Inserting users into the database...'))
        User.objects.bulk_create(users_to_create, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS(f'Done! {total_users} users created.'))
        self.stdout.write(self.style.SUCCESS(f'Credentials saved to: {filename}'))