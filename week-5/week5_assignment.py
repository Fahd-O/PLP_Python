# Week Five Assignment: OOP in Python

# -------------------------------
# Assignment 1: Design Your Own Class! 🏗️
# -------------------------------

class Smartphone:
    def __init__(self, brand, model, storage, battery):
        self.brand = brand
        self.model = model
        self.storage = storage
        self.battery = battery

    def call(self, number):
        print(f"📞 Calling {number} from {self.brand} {self.model}...")

    def charge(self, amount):
        self.battery += amount
        if self.battery > 100:
            self.battery = 100
        print(f"🔋 Battery charged to {self.battery}%")

    def __str__(self):
        return f"{self.brand} {self.model} | Storage: {self.storage}GB | Battery: {self.battery}%"


# Inheritance Example (Encapsulation & Polymorphism)
class Smartwatch(Smartphone):  # Inherits from Smartphone
    def __init__(self, brand, model, battery, fitness_tracking=True):
        super().__init__(brand, model, storage=8, battery=battery)  # Smartwatches usually have low storage
        self.fitness_tracking = fitness_tracking

    def track_steps(self, steps):
        if self.fitness_tracking:
            print(f"Tracking {steps} steps on {self.brand} {self.model}!")
        else:
            print("⚠️ Fitness tracking is disabled.")

    # Polymorphism (overriding call method)
    def call(self, number):
        print(f"⌚ Voice call to {number} from {self.brand} {self.model} Smartwatch.")


# -------------------------------
# Activity 2: Polymorphism Challenge! 🐾
# -------------------------------

class Vehicle:
    def move(self):
        print("This vehicle moves...")

class Car(Vehicle):
    def move(self):
        print("🚗 Driving on the road...")

class Plane(Vehicle):
    def move(self):
        print("✈️ Flying in the sky...")

class Boat(Vehicle):
    def move(self):
        print("⛵ Sailing on water...")


# -------------------------------
# Demo Section
# -------------------------------
if __name__ == "__main__":
    # Assignment 1 Demo
    phone = Smartphone("Samsung", "Galaxy S22", 128, 75)
    watch = Smartwatch("Apple", "Watch Series 7", 60)

    print(phone)
    phone.call("+2348012345678")
    phone.charge(20)

    print("\n" + str(watch))
    watch.call("+2348098765432")  # Polymorphism: different call() method
    watch.track_steps(5000)

    # Activity 2 Demo
    print("\n--- Vehicle Polymorphism Demo ---")
    vehicles = [Car(), Plane(), Boat()]

    for v in vehicles:
        v.move()
