import matplotlib.pyplot as plt

# Define the fabric dimensions
width = 1.5  # meters
length = 75.8  # meters

# Define the defect points
defects = [
    {"from": 9, "to": 9, "defect": "SLUB YARN", "type": "MAJOR", "points": 4},
    {"from": 21, "to": 21, "defect": "MISSING END", "type": "MAJOR", "points": 4},
    {"from": 33, "to": 33, "defect": "MISSING END", "type": "MAJOR", "points": 5},
    {"from": 35, "to": 35, "defect": "RUST STAIN", "type": "MAJOR", "points": 4},
    {"from": 38, "to": 38, "defect": "RUST STAIN", "type": "MINOR", "points": 1},
    {"from": 42, "to": 42, "defect": "SLUB YARN", "type": "MAJOR", "points": 4},
    {"from": 47, "to": 47, "defect": "RUST STAIN", "type": "MAJOR", "points": 4},
    {"from": 49, "to": 49, "defect": "LOOSE WARP", "type": "MINOR", "points": 2},
    {"from": 59, "to": 59, "defect": "SLUB YARN", "type": "MAJOR", "points": 4}
]

# Calculate the total points
total_points = sum(defect["points"] for defect in defects)

# # Initialize lists to store the defect density for each interval
# defect_densities = []
# interval_points = []

# # Calculate the defect density for each 10-meter interval
# for i in range(0, int(length), 10):
#     interval_points.append(i)
#     interval_defects = [defect for defect in defects if i <= defect["from"] < i + 10]
#     interval_points = sum(defect["points"] for defect in interval_defects)
#     defect_densities.append(interval_points / 10)
# Initialize lists to store the defect density for each interval
defect_densities = []
interval_points = []
interval_points_sum = []  # New list to store the sum of points

# Calculate the defect density for each 10-meter interval
for i in range(0, int(length), 10):
    interval_points.append(i)
    interval_defects = [defect for defect in defects if i <= defect["from"] < i + 10]
    interval_points_sum.append(sum(defect["points"] for defect in interval_defects))  # Use the new list here
    defect_densities.append(interval_points_sum[-1] / 10)  # Use the last element of the new list here

# Plot the defect density for each interval
plt.plot(interval_points, defect_densities)
plt.xlabel("Interval (meters)")
plt.ylabel("Defect Density")
plt.title("Defect Density by Interval")
plt.show()

# Plot the defect density for each interval
plt.plot(interval_points, defect_densities)
plt.xlabel("Interval (meters)")
plt.ylabel("Defect Density")
plt.title("Defect Density by Interval")
plt.show()