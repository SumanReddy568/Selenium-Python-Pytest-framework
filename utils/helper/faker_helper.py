from faker import Faker

fake = Faker()

def generate_fake_data(field):
    """Generate fake data based on the specified field."""
    if field == "first_name":
        return fake.first_name()
    elif field == "last_name":
        return fake.last_name()
    elif field == "zip_code":
        return fake.zipcode()
    elif field == "postal_code":
        return fake.postalcode()
    else:
        raise ValueError("Invalid field name. Please choose from: first_name, last_name, zip_code, postal_code")
