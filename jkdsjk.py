def remove_defects(defects, total_length, threshold):
    # Sort defects by defect density in descending order
    defects.sort(key=lambda x: x[2] / x[1], reverse=True)

    # Initialize variables to track total points and length removed
    total_points = 0
    total_length_removed = 0
    removed_sections = []

    # Iterate over the sorted defects
    for defect in defects:
        # Calculate points and length of fabric to be removed
        points = defect[2]
        length = defect[1]

        # Add these values to the total points and length removed
        total_points += points
        total_length_removed += length

        # If the total points removed exceed the threshold, stop
        if total_points > threshold:
            break

        # Record the section to be removed
        removed_sections.append((defect[0], defect[1]))

    return total_points, total_length_removed, removed_sections

# Defect data for fabric rolls A and B
fabric_roll_a_defects = [
        (7, 7, 4), (15, 15, 1), (23, 23, 5), (25, 25, 1), (28, 28, 4),
    (30, 30, 1), (41, 41, 4), (41, 41, 4), (52, 52, 1), (66, 66, 4),
    (68, 68, 4), (71, 71, 1), (76, 76, 4)
]

fabric_roll_b_defects = [
        (3, 3, 2), (27, 27, 4), (37, 37, 4), (46, 46, 4), (48, 48, 4),
    (54, 54, 4), (58, 58, 1), (67, 67, 4), (75, 75, 4), (76, 76, 4)

]

# Combine defect data from both fabric rolls
all_defects = fabric_roll_a_defects + fabric_roll_b_defects

# Total length of fabric rolls A and B
total_length_a = 88.7
total_length_b = 81.1
total_length = total_length_a + total_length_b

threshold = 20  # points

# Remove defects until threshold is reached
total_points_removed, total_length_removed, removed_sections = remove_defects(all_defects, total_length, threshold)

print(f"Total points removed: {total_points_removed}")
print(f"Total length removed: {total_length_removed}m")
print("Sections to be removed:")
for section in removed_sections:
    print(f"From meter {section[0]} to meter {section[0] + section[1]}")