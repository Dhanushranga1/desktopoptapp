defects = [
    {"from": 5, "to": 5, "points": 4},
    {"from": 7, "to": 7, "points": 1},
    {"from": 15, "to": 15, "points": 1},
    {"from": 15.3, "to": 18.5, "points": contionous defect},
    {"from": 23, "to": 23, "points": 4},
    {"from": 25, "to": 25, "points": 1},
    {"from": 28, "to": 28, "points": 4},
    {"from": 30, "to": 30, "points": 1},
    {"from": 41, "to": 41, "points": 4},
    {"from": 50, "to": 52, "points": 1},
    {"from": 66, "to": 66, "points": 4},
    {"from": 68, "to": 68, "points": 4},
    {"from": 71, "to": 71, "points": 1},
    {"from": 76, "to": 76, "points": 4},
    {"from": 78, "to": 78, "points": 4},
    {"from": 79, "to": 79, "points": 4}
]

# Calculate the total defect points per meter square
total_defect_points = sum(defect["points"] for defect in defects)
total_length = 103
total_width = 1.5
defect_points_per_meter_square = (total_defect_points * 100) / (total_length * total_width)

# Define the industrial standard
industrial_standard = 23

# Initialize the result list
result = []

# Initialize the current section
current_section = {"from": 0, "to": 0, "points": 0}

# Iterate over the defects
for defect in defects:
    if defect["from"] > current_section["to"]:
        # Add the current section to the result
        result.append(current_section)
        current_section = {"from": defect["from"], "to": defect["from"], "points": defect["points"]}
    else:
        # Update the current section
        current_section["to"] = defect["to"]
        current_section["points"] += defect["points"]

# Add the last section to the result
result.append(current_section)

# Initialize the joined sections
joined_sections = []

# Initialize the current joined section
current_joined_section = {"from": 0, "to": 0, "points": 0}

# Iterate over the result
for i in range(len(result) - 1):
    if result[i]["to"] + 0.1 < result[i + 1]["from"]:
        # Add the current section to the joined sections
        joined_sections.append(current_joined_section)
        current_joined_section = {"from": result[i]["to"], "to": result[i]["to"], "points": 0}
    else:
        # Update the current joined section
        current_joined_section["to"] = result[i + 1]["to"]
        current_joined_section["points"] += result[i + 1]["points"]

# Add the last section to the joined sections
joined_sections.append(current_joined_section)

# Initialize the final result
final_result = []

# Initialize the current final section
current_final_section = {"from": 0, "to": 0, "points": 0}

# Iterate over the joined sections
for i in range(len(joined_sections) - 1):
    if joined_sections[i]["to"] + 0.1 < joined_sections[i + 1]["from"]:
        # Add the current section to the final result
        final_result.append(current_final_section)
        current_final_section = {"from": joined_sections[i]["to"], "to": joined_sections[i]["to"], "points": 0}
    else:
        # Update the current final section
        current_final_section["to"] = joined_sections[i + 1]["to"]
        current_final_section["points"] += joined_sections[i + 1]["points"]

# Add the last section to the final result
final_result.append(current_final_section)

# Add the good fabric sections
final_result.append({"from": 0, "to": 15, "points": 0})
final_result.append({"from": 28, "to": 71, "points": 0})
final_result.append({"from": 79, "to": 103, "points": 0})

# Join the final sections
for i in range(len(final_result) - 1):
    if final_result[i]["to"] + 0.1 < final_result[i + 1]["from"]:
        # Add the current section to the final result
        final_result[i]["to"] = final_result[i]["to"]
        final_result[i]["points"] += 4
    else:
        # Update the current final section
        final_result[i]["to"] = final_result[i + 1]["to"]
        final_result[i]["points"] += final_result[i + 1]["points"]

# Print the final result
for i, section in enumerate(final_result):
    if i > 0:
        print(f"Joined fabric from {section['from']} to {section['to']} with {section['points']} defects")
    else:
        print(f"Good fabric from {section['from']} to {section['to']} with 0 defects")

# Print the total defect points per meter square
print(f"Total defect points per meter square: {defect_points_per_meter_square}")