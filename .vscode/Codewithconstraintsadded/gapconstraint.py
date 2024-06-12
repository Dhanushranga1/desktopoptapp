import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns

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

# Function to remove combined sections from the fabric
def remove_sections(defects, length, width, sections, min_usable_length):
    new_defects = defects[:]
    total_cut_length = 0
    removed_sections = []
    
    for start, end in sections:
        new_defects = [d for d in new_defects if d['from'] > end or d['to'] < start]
        removed_sections.append((start, end))
        total_cut_length += (end - start + 1)
    
    new_length = length - total_cut_length

    # Check if the remaining parts are less than min_usable_length
    remaining_starts = [0] + [end + 1 for start, end in sections]
    remaining_ends = [start - 1 for start, end in sections] + [length - 1]
    remaining_sections = [(start, end) for start, end in zip(remaining_starts, remaining_ends) if end - start + 1 >= min_usable_length]

    if remaining_sections:
        new_defects = [d for d in new_defects if any(start <= d['from'] <= end for start, end in remaining_sections)]
        new_length = sum(end - start + 1 for start, end in remaining_sections)
        removed_sections.extend([(start, end) for start, end in zip(remaining_starts, remaining_ends) if end - start + 1 < min_usable_length])
    
    return new_defects, new_length, total_cut_length, removed_sections

# Function to plot the original, remaining, and removed fabric sections
def plot_fabric_sections(original_length, remaining_length, removed_sections, width):
    fig, ax = plt.subplots(figsize=(14, 8))
    
    sns.set(style="whitegrid")

    # Plot original fabric
    ax.add_patch(patches.Rectangle((0, 2), original_length, width, edgecolor='black', facecolor='lightgrey', label='Original Fabric'))
    ax.text(original_length / 2, 2.5, f'Original Fabric\n{original_length} meters', horizontalalignment='center', verticalalignment='center', fontsize=12, color='black')

    # Plot remaining fabric
    remaining_start = 0
    for start, end in removed_sections:
        if start > remaining_start:
            ax.add_patch(patches.Rectangle((remaining_start, 1), start - remaining_start, width, edgecolor='black', facecolor='lightgreen', label='Remaining Fabric'))
            ax.text((remaining_start + start) / 2, 1.5, f'{start - remaining_start} meters', horizontalalignment='center', verticalalignment='center', fontsize=12, color='black')
        remaining_start = end + 1
    if remaining_start < original_length:
        ax.add_patch(patches.Rectangle((remaining_start, 1), original_length - remaining_start, width, edgecolor='black', facecolor='lightgreen'))
        ax.text((remaining_start + original_length) / 2, 1.5, f'{original_length - remaining_start} meters', horizontalalignment='center', verticalalignment='center', fontsize=12, color='black')

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
        new_defects, new_length, total_cut_length, removed_sections = remove_sections(defects, length, width, sections, min_usable_length)
        new_ppms = calculate_ppms(new_defects, new_length, width)
        
        print(f"New PPMS after removing sections {sections}: {new_ppms}")
        print(f"Total Length of cut parts: {total_cut_length} meters")
        print(f"Remaining Length: {new_length} meters")
        
        plot_ppms(original_ppms, new_ppms, length, new_length, total_cut_length)
        plot_fabric_sections(length, new_length, removed_sections, width)
    else:
        print("PPMS is within acceptable limits. No need to cut the fabric.")

# Example usage
defects = [
    {"from": 7, "to": 7, "points": 1},
    # {"from": 5, "to": 5, "points": 4},
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
width = 1.5     # Example width in meters
THRESHOLD_PPMS = 23  # Threshold PPMS
NUM_SECTIONS = 5  # Number of sections to remove
MIN_USABLE_LENGTH = 0  # Minimum usable length in meters
MAX_GAP = 4  # Maximum gap between sections to be considered for combining

main(defects, length, width, THRESHOLD_PPMS, NUM_SECTIONS, MIN_USABLE_LENGTH, MAX_GAP)
