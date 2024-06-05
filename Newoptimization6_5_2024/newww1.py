
import matplotlib.pyplot as plt

def calculate_ppms(defects, length, width):
    total_defect_points = sum(defect['points'] for defect in defects)
    ppms = (total_defect_points * 100) / (length * width)
    return ppms

def find_and_remove_high_defect_section(defects, length, width):
    max_density = 0
    cut_section = None
    for i in range(len(defects)):
        for j in range(i, len(defects)):
            section_length = defects[j]['to'] - defects[i]['from'] + 1
            section_points = sum(defect['points'] for defect in defects[i:j+1])
            density = section_points / section_length
            if density > max_density:
                max_density = density
                cut_section = (defects[i]['from'], defects[j]['to'])

    new_defects = [d for d in defects if d['from'] < cut_section[0] or d['to'] > cut_section[1]] if cut_section is not None else defects
    cut_length = cut_section[1] - cut_section[0] + 1 if cut_section is not None else 0
    new_length = length - cut_length

    return new_defects, new_length, cut_section

def plot_ppms(before_ppms, after_ppms, original_length, new_length):
    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Fabric Roll')
    ax1.set_ylabel('PPMS')
    ax1.bar(['Before', 'After'], [before_ppms, after_ppms], color=['blue', 'green'])

    ax2 = ax1.twinx()
    ax2.set_ylabel('Length (meters)')
    ax2.plot(['Before', 'After'], [original_length, new_length], color='red', marker='o')

    plt.title('Fabric Roll Optimization')
    plt.show()

def main(defects, length, width, threshold_ppms):
    original_ppms = calculate_ppms(defects, length, width)
    if original_ppms > threshold_ppms:
        new_defects, new_length, cut_section = find_and_remove_high_defect_section(defects, length, width)
        new_ppms = calculate_ppms(new_defects, new_length, width)
        print(f"Original PPMS: {original_ppms}")
        print(f"New PPMS after removing section {cut_section}: {new_ppms}")
        plot_ppms(original_ppms, new_ppms, length, new_length)
    else:
        print(f"PPMS is within acceptable limits: {original_ppms}")

# Example usage
defects = [
    {"from": 2, "to": 4, "points": 4},
    {"from": 5, "to": 8, "points": 4},
    {"from": 10, "to": 12, "points": 1},
    # {"from": 20, "to": 21, "points": 4},
    {"from": 22, "to": 32, "points": 34},
    {"from": 33, "to": 36, "points": 9},
    {"from": 39, "to": 42, "points": 8},
    {"from": 46, "to": 48, "points": 3},
    {"from": 70, "to": 72, "points": 4}
]

length = 75.8  # Example length in meters
width = 1.5    # Example width in meters
THRESHOLD_PPMS=23

main(defects, length, width, THRESHOLD_PPMS)
