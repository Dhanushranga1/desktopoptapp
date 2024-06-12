import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns

# Function to calculate PPMS
def calculate_ppms(defects, length, width):
    total_defect_points = sum(defect['points'] for defect in defects)
    if length != 0 and width != 0:
        ppms = (total_defect_points * 100) / (length * width)
    elif length == 0 and width == 0:
        ppms = 0
    else:
        ppms = float('inf')
    return ppms

# Function to calculate the defect density for a given section
def calculate_section_ppms(defects, start, end, width):
    section_length = end - start + 1
    section_points = sum(defect['points'] for defect in defects if defect['from'] >= start and defect['to'] <= end)
    section_ppms = (section_points * 100) / (section_length * width)
    return section_ppms

# Function to find multiple high-density sections and combine them
def find_combined_highest_density_sections(defects, width, num_sections, max_gap):
    sections = []
    remaining_defects = defects[:]
    
    for _ in range(num_sections):
        max_density = 0
        best_section = (0, 0)
        
        for i in range(len(remaining_defects)):
            for j in range(i, len(remaining_defects)):
                start = remaining_defects[i]['from']
                end = remaining_defects[j]['to']
                if end - start <= max_gap:
                    density = calculate_section_ppms(remaining_defects, start, end, width)
                    if density > max_density:
                        max_density = density
                        best_section = (start, end)
        
        if best_section != (0, 0):
            sections.append(best_section)
            # Remove the found section from the list of defects
            remaining_defects = [d for d in remaining_defects if d['from'] > best_section[1] or d['to'] < best_section[0]]
    
    if sections:
        combined_start = min(start for start, end in sections)
        combined_end = max(end for start, end in sections)
        return [(combined_start, combined_end)]
    else:
        return []

# Function to remove sections from the fabric, considering usable sub-sections
def remove_sections(defects, length, width, sections, min_usable_length, max_gap):
    new_defects = defects[:]
    total_cut_length = 0
    removed_sections = []
    kept_sections = []
    
    for start, end in sections:
        # Check if the section can be split
        sub_start = start
        while sub_start <= end:
            sub_end = min(sub_start + max_gap, end)
            section_ppms = calculate_section_ppms(new_defects, sub_start, sub_end, width)
            if section_ppms > THRESHOLD_PPMS:
                removed_sections.append((sub_start, sub_end))
                total_cut_length += (sub_end - sub_start + 1)
            else:
                if (sub_end - sub_start + 1) >= min_usable_length:
                    kept_sections.append((sub_start, sub_end))
            sub_start = sub_end + 1

        # Add 4 points defect to the density calculation after sections are joined
        if sub_end < length:
            next_section = [d for d in new_defects if d['from'] >= sub_end + 1]
            if next_section:
                next_start = next_section[0]['from']
                next_end = next_section[0]['to']
                if next_start - sub_end <= max_gap:
                    new_defects.append({"from": sub_end, "to": sub_end, "points": 4})

    # Re-calculate new defects and length
    new_defects = [d for d in new_defects if not any(start <= d['from'] <= end for start, end in removed_sections)]
    new_length = sum(end - start + 1 for start, end in kept_sections)
    
    return new_defects, new_length, total_cut_length, removed_sections, kept_sections

# Function to plot the original, remaining, and removed fabric sections
def plot_fabric_sections(original_length, remaining_length, removed_sections, kept_sections, width):
    fig, ax = plt.subplots(figsize=(14, 8))
    
    sns.set(style="whitegrid")

    # Plot original fabric
    ax.add_patch(patches.Rectangle((0, 2), original_length, width, edgecolor='black', facecolor='lightgrey', label='Original Fabric'))
    ax.text(original_length / 2, 2.5, f'Original Fabric\n{original_length} meters', horizontalalignment='center', verticalalignment='center', fontsize=12, color='black')

    # Plot remaining fabric
    for start, end in kept_sections:
        ax.add_patch(patches.Rectangle((start, 1), end - start + 1, width, edgecolor='black', facecolor='lightgreen', label='Remaining Fabric'))
        ax.text((start + end) / 2, 1.5, f'{end - start + 1} meters', horizontalalignment='center', verticalalignment='center', fontsize=12, color='black')

    # Plot removed sections
    y_offset = 0
    for start, end in removed_sections:
        ax.add_patch(patches.Rectangle((start, y_offset), end - start + 1, width, edgecolor='black', facecolor='red', label='Removed Section'))
        ax.text((start + end) / 2, y_offset + 0.5, f'Removed: {start}-{end}\n{end - start + 1} meters', horizontalalignment='center', verticalalignment='center', fontsize=12, color='black')
        y_offset -= 1
    
    ax.set_xlim(0, original_length)
    ax.set_ylim(y_offset - 1, 3)
    ax.set_xlabel('Meters', fontsize=14)
    ax.set_yticks([])
    ax.legend(loc='upper right')
    plt.title('Fabric Sections Visualization', fontsize=16)
    plt.show()

# Function to plot PPMS and lengths
def plot_ppms(before_ppms, after_ppms, original_length, new_length, cut_length):
    fig, ax1 = plt.subplots(figsize=(10, 6))

    sns.set(style="whitegrid")

    ax1.set_xlabel('Fabric Roll', fontsize=14)
    ax1.set_ylabel('PPMS', fontsize=14)
    bars = ax1.bar(['Before', 'After'], [before_ppms, after_ppms], color=['#4c72b0', '#55a868'], edgecolor='black')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Length (meters)', fontsize=14)
    ax2.plot(['Before', 'After'], [original_length, new_length], color='#c44e52', marker='o', markersize=8, linewidth=2, label='Length')

    plt.title(f'Fabric Roll Optimization (Total Cut Length: {cut_length}m)', fontsize=16)

    # Adding data labels
    for bar in bars:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, yval + 1, round(yval, 2), ha='center', va='bottom', fontsize=12, color='black')

    ax2.text(1, new_length, f'{new_length}m', ha='center', va='bottom', fontsize=12, color='#c44e52')

    fig.tight_layout()
    plt.show()

# Main function
def main(defects, length, width, threshold_ppms, num_sections, min_usable_length, max_gap):
    original_ppms = calculate_ppms(defects, length, width)
    print(f"Original PPMS: {original_ppms}")
    print(f"Original Length: {length} meters")
    
    if original_ppms > threshold_ppms:
        sections = find_combined_highest_density_sections(defects, width, num_sections, max_gap)
        new_defects, new_length, total_cut_length, removed_sections, kept_sections = remove_sections(defects, length, width, sections, min_usable_length, max_gap)
        new_ppms = calculate_ppms(new_defects, new_length, width)
        
        print(f"New PPMS after removing sections {sections}: {new_ppms}")
        print(f"Total Length of cut parts: {total_cut_length} meters")
        print(f"Remaining Length: {new_length} meters")
        
        plot_ppms(original_ppms, new_ppms, length, new_length, total_cut_length)
        plot_fabric_sections(length, new_length, removed_sections, kept_sections, width)
    else:
        print("PPMS is within acceptable limits. No need to cut the fabric.")

# Example usage
defects = [
    {"from": 7, "to": 7, "points": 1},
    {"from": 15, "to": 15, "points": 1},
    {"from": 15.3, "to": 18.5, "points": 25},
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

length = 103  # Example length in meters
width = 1.5  # Example width in meters
THRESHOLD_PPMS = 23  # Threshold PPMS
NUM_SECTIONS = 6  # Number of sections to remove
MIN_USABLE_LENGTH = 20  # Minimum usable length in meters
MAX_GAP = 5  # Maximum gap between sections to be considered for combining

main(defects, length, width, THRESHOLD_PPMS, NUM_SECTIONS, MIN_USABLE_LENGTH, MAX_GAP)
