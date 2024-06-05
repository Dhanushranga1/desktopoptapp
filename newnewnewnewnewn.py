from matplotlib.widgets import Button
import matplotlib.pyplot as plt
import matplotlib.table as mtable

# Define the fabric dimensions
width = 1.5  # meters
length = 75.8  # meters

# Define the defect points
defects = [
    {"from": 2, "to": 2, "points": 4},
    {"from": 5, "to": 5, "points": 4},
    {"from": 10, "to": 10, "points": 1},
    {"from": 22, "to": 22, "points": 4},
    {"from": 23, "to": 28, "points": 10},
    {"from": 35, "to": 35, "points": 2},
    {"from": 39, "to": 39, "points": 4},
    {"from": 46, "to": 46, "points": 2},
    {"from": 70, "to": 70, "points": 2}
]

# Calculate the total points
total_points = sum(defect["points"] for defect in defects)

# Initialize lists to store the defect density for each interval
defect_densities = []
interval_points = []
interval_points_sum = []  # New list to store the sum of points

intervals=[5,10,15,20]
# Calculate the defect density for each 10-meter interval
for interval in intervals:
    for i in range(0, int(length), interval):
        interval_points.append(i)
        interval_defects = [defect for defect in defects if i <= defect["from"] < i + interval]
        interval_points_sum.append(sum(defect["points"] for defect in interval_defects))  # Use the new list here
        defect_densities.append(interval_points_sum[-1] / interval)  # Use the last element of the new list here

        # Find the interval with the highest defect density
        max_density_index = defect_densities.index(max(defect_densities))

        # Print the from and to points of the interval where the defect density is high
        # print(f"Interval with highest defect density: {interval_points[max_density_index]}-{interval_points[max_density_index] + interval}")

        # Plot the defect density for each interval
        plt.plot(interval_points, defect_densities)
        plt.xlabel("Interval (meters)")
        plt.ylabel("Defect Density")
        plt.title("Defect Density by Interval")
        # plt.show()

        # Create a table using matplotlib
        fig, ax = plt.subplots()
        ax.axis('off')

        table_data = [["Interval", "Defect Density"]]
        table_data.extend([[f"{interval_points[i]}-{interval_points[i] + interval}", f"{defect_densities[i]:.2f}"] for i in range(len(interval_points))])
        # for i in range(len(interval_points)):
        #     table_data.append([f"{interval_points[i]}-{interval_points[i] + interval}", f"{defect_densities[i]:.2f}"])

        table = ax.table(cellText=table_data, loc='center')
        ax.add_table(table)
        ax.set_title("Defect Density by Interval")

        # Add interactive features to the table
        def sort_table(column):
            table_data.sort(key=lambda x: x[column])
            cells = table.get_celld()
            for i in range(len(table_data)):
                for j in range(len(table_data[i])):
                    cells[i, j].get_text().set_text(table_data[i][j])
            fig.canvas.draw_idle()

        # Add a sort function to the table
        sort_table(0)

        # Add a button to sort the table
        button_ax = plt.axes([0.7, 0.05, 0.2, 0.075])   # type: ignore
        button = Button(button_ax, 'Sort')
        button.on_clicked(lambda event: sort_table(1))

        # plt.show()

        # Find the interval with the highest defect density
max_density = max(defect_densities)
max_density_index = defect_densities.index(max_density)
highest_interval = f"{interval_points[max_density_index]}-{interval_points[max_density_index] + intervals[max_density_index // len(intervals)]}"

print(f"Interval with the highest defect density: {highest_interval}")
# Count the occurrences of each interval
interval_counts = {}
for i in range(len(interval_points)):
    interval = f"{interval_points[i]}-{interval_points[i] + intervals[i // len(intervals)]}"
    if interval in interval_counts:
        interval_counts[interval] += 1
    else:
        interval_counts[interval] = 1

# Find the interval with the highest frequency
highest_frequency_interval = max(interval_counts, key=lambda k : interval_counts[k])
print(f"Interval with the highest frequency: {highest_frequency_interval}")

print(f"this displays the interval points: {interval_points}")  # This displays the interval_points:
