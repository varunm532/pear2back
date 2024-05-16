
# Define maintenance activities and costs for different car tiers
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

maintenance_costs = {
    "Economy": [30, 20, 100, 15, 25, 120, 80, 50, 90, 20, 80, 40, 15, 30, 150],
    "Premium": [100, 50, 300, 50, 50, 200, 150, 100, 150, 50, 150, 100, 30, 50, 300],
    "Luxury": [300, 100, 800, 100, 100, 500, 400, 300, 500, 100, 400, 200, 50, 100, 1000]
}

# Function to collect car tier from the user
def collect_car_tier():
    tier = input("Enter your car tier (Economy, Premium, or Luxury): ")
    while tier not in maintenance_costs:
        print("Invalid tier. Please choose from Economy, Premium, or Luxury.")
        tier = input("Enter your car tier: ")
    return tier

# Function to select maintenance activity and display its cost
def select_maintenance_activity():
    print("Select Maintenance Activity:")
    for i, activity in enumerate(maintenance_activities, start=1):
        print(f"{i}. {activity}")
    choice = int(input("Enter the number corresponding to the maintenance activity: "))
    while choice < 1 or choice > len(maintenance_activities):
        print("Invalid choice. Please enter a number within the range.")
        choice = int(input("Enter the number corresponding to the maintenance activity: "))
    return maintenance_activities[choice - 1]

# Main function
def main():
    # Collect car tier from the user
    tier = collect_car_tier()
    
    total_cost = 0
    while True:
        # Select maintenance activity and display its cost
        activity = select_maintenance_activity()
        cost = maintenance_costs[tier][maintenance_activities.index(activity)]
        total_cost += cost
        
        print(f"\nCost of {activity} for {tier} tier: ${cost}")
        
        done = input("Are you done? (yes/no): ").lower()
        if done == "yes":
            break

    print(f"\nTotal Maintenance Cost for {tier} tier: ${total_cost}")

# Call the main function
if __name__ == "__main__":
    main()