import matplotlib.pyplot as plt

# Function to calculate PPMS
def calculate_ppms(defects, length, width):
    total_defect_points = sum(defect['points'] for defect in defects)
    ppms = (total_defect_points * 100) / (length * width)
    return ppms

# Function to calculate the defect density for a given section
def calculate_section_ppms(defects, start, end, width):
    section_length = end - start + 1
    section_points = sum(defect['points'] for defect in defects if defect['from'] >= start and defect['to'] <= end)
    section_ppms = (section_points * 100) / (section_length * width)
    return section_ppms

# Function to find the section with the highest defect density
def find_highest_density_section(defects, width):
    max_density = 0
    cut_section = (0, 0)
    for i in range(len(defects)):
        for j in range(i, len(defects)):
            start = defects[i]['from']
            end = defects[j]['to']
            density = calculate_section_ppms(defects, start, end, width)
            if density > max_density:
                max_density = density
                cut_section = (start, end)
    return cut_section

# Function to remove a specified section from the fabric
def remove_section(defects, length, width, start, end):
    new_defects = [d for d in defects if d['from'] > end or d['to'] < start]
    cut_length = end - start + 1
    new_length = length - cut_length

    return new_defects, new_length, (start, end)

# Function to plot PPMS and lengths
def plot_ppms(before_ppms, after_ppms, original_length, new_length, cut_length):
    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Fabric Roll')
    ax1.set_ylabel('PPMS')
    ax1.bar(['Before', 'After'], [before_ppms, after_ppms], color=['blue', 'green'])

    ax2 = ax1.twinx()
    ax2.set_ylabel('Length (meters)')
    ax2.plot(['Before', 'After'], [original_length, new_length], color='red', marker='o')

    plt.title(f'Fabric Roll Optimization (Cut Length: {cut_length}m)')
    plt.show()

# Main function
def main(defects, length, width, threshold_ppms):
    original_ppms = calculate_ppms(defects, length, width)
    print(f"Original PPMS: {original_ppms}")
    print(f"Original Length: {length} meters")
    
    if original_ppms > threshold_ppms:
        cut_start, cut_end = find_highest_density_section(defects, width)
        new_defects, new_length, cut_section = remove_section(defects, length, width, cut_start, cut_end)
        cut_length = cut_section[1] - cut_section[0] + 1
        new_ppms = calculate_ppms(new_defects, new_length, width)
        
        print(f"New PPMS after removing section {cut_section}: {new_ppms}")
        print(f"Length of cut part: {cut_length} meters")
        print(f"Remaining Length: {new_length} meters")
        
        plot_ppms(original_ppms, new_ppms, length, new_length, cut_length)
    else:
        print("PPMS is within acceptable limits. No need to cut the fabric.")

# Example usage
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

length = 75.8  # Example length in meters
width = 1.5     # Example width in meters
THRESHOLD_PPMS = 26  # Threshold PPMS

main(defects, length, width, THRESHOLD_PPMS)
