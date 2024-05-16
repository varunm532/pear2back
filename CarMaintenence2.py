
maintenance_activities = [
    "Oil Change",
    "Tire Rotation",
    "Brake Inspection and Replacement",
    "Air Filter Replacement",
    "Fluid Checks and Top-ups",
    "Battery Inspection and Replacement",
    "Spark Plug Replacement",
    "Alignment and Suspension Inspection",
    "Fuel System Cleaning",
    "Cabin Air Filter Replacement",
    "Cooling System Maintenance",
    "Exhaust System Inspection",
    "Wiper Blade Replacement",
    "Headlight and Taillight Bulb Replacement",
    "Scheduled Inspections"
]

def Economy(ID):
    prices = {
        1: 30,
        2: 20,
        3: 100,
        4: 15,
        5: 25,
        6: 120,
        7.: 80,
        8: 50, 
        9: 90,
        10: 20,
        11: 80,
        12: 40,
        13: 15,
        14: 30,
        15: 150
    }
    for key, value in prices.items():
        if ID == key:
            return value
        
def Premium(ID):
    prices = {
        1: 100,
        2: 50,
        3: 300,
        4: 50,
        5: 50,
        6: 200,
        7.: 150,
        8: 100, 
        9: 150,
        10: 50,
        11: 150,
        12: 100,
        13: 30,
        14: 50,
        15: 300
    }
    for key, value in prices.items():
        if ID == key:
            return value
        
def Luxury(ID):
    prices = {
        1: 300,
        2: 100,
        3: 800,
        4: 100,
        5: 100,
        6: 500,
        7: 400,
        8: 300,
        9: 500,
        10: 100,
        11: 400,
        12: 200,
        13: 50,
        14: 100,
        15: 1000
    }
    for key, value in prices.items():
        if ID == key:
            return value

print("Welcome to your car maintenance tracker!")
Class = input("Enter your car tier:")

for count, value in enumerate(maintenance_activities, start=1):
    print(str(count)+". "+str(value))
    
if Class == "Economy":
    cost = []
    while True:
        print("Pick numbers that correspond with your maintenance activity: ")
        ID = int(input())
        cost.append(Economy(ID)) 
        bool = input("Done? y/n")  
        if bool == "y":
            break
    print("Your total is:", sum(cost))  
        
if Class == "Premium":
    cost = []
    while True:
        print("Pick numbers that correspond with your maintenance activity: ")

        ID = int(input())
        cost.append(Premium(ID)) 
        bool = input("Done? y/n")  
        if bool == "y":
            break
    print("Your total is:", sum(cost)) 
        
if Class == "Luxury":
    cost = []
    while True:
        print("Pick numbers that correspond with your maintenance activity: ")

        ID = int(input())
        cost.append(Luxury(ID)) 
        bool = input("Done? y/n") 
        if bool == "y":
            break 
    print("Your total is:", sum(cost))  
    
