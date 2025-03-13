import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv(
    "/home/tjselevani/PycharmProjects/PythonProject/data/last-3-months-transactions.csv"
)

# Define global variables
VEHICLE_BOOKED = "SM944"
TRANSACTION_TYPE = "CREDIT"

# Filter data
vehicle_data = data[
    (data["vehicle_booked"] == VEHICLE_BOOKED)
    & (data["transaction_type"] == TRANSACTION_TYPE)
].copy()

# Convert 'created_at' to datetime
vehicle_data["created_at"] = pd.to_datetime(vehicle_data["created_at"])

# Option 1: Group by Day
vehicle_data["day"] = vehicle_data[
    "created_at"
].dt.date  # Extracts only the date (YYYY-MM-DD)

# Option 2: Group by Week
vehicle_data["week"] = (
    vehicle_data["created_at"].dt.to_period("W").astype(str)
)  # Group into weeks

# Option 3: Group by Month
vehicle_data["month"] = (
    vehicle_data["created_at"].dt.to_period("M").astype(str)
)  # Group into months

# Option 4: Group by Year
vehicle_data["year"] = vehicle_data["created_at"].dt.year  # Extract year

# Choose one grouping (change 'day' to 'week', 'month', or 'year' as needed)
group_by = "month"  # Change to 'day', 'week', or 'year' as required
aggregated_data = vehicle_data.groupby(group_by)["amount"].sum().reset_index()

# Plot
plt.figure(figsize=(12, 6))
sns.lineplot(x=group_by, y="amount", data=aggregated_data, marker="o")

# Customize graph
plt.title(
    f"Total Fare Charges Over Time for {VEHICLE_BOOKED} ({TRANSACTION_TYPE} Transactions)"
)
plt.xlabel(group_by.capitalize())  # Dynamic label
plt.ylabel("Total Fare Amount")
plt.xticks(rotation=45)
plt.grid(True)

# Show plot
plt.show()







?








