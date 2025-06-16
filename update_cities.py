from database import Database

if __name__ == "__main__":
    db = Database()
    new_cities = ["Multan", "Peshawar", "Quetta", "Hyderabad", "Sialkot"]
    db.add_cities(new_cities)