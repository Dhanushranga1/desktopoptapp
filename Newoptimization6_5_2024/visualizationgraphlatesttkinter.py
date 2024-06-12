import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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
def find_combined_highest_density_sections(defects, width, num_sections):
    sections = []
    remaining_defects = defects[:]
    
    for _ in range(num_sections):
        max_density = 0
        best_section = (0, 0)
        
        for i in range(len(remaining_defects)):
            for j in range(i, len(remaining_defects)):
                start = remaining_defects[i]['from']
                end = remaining_defects[j]['to']
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
def remove_sections(defects, length, width, sections):
    new_defects = defects[:]
    total_cut_length = 0
    removed_sections = []
    
    for start, end in sections:
        new_defects = [d for d in new_defects if d['from'] > end or d['to'] < start]
        removed_sections.append((start, end))
        total_cut_length += (end - start + 1)
    
    new_length = length - total_cut_length

    # Check if the remaining parts are less than 20 meters
    remaining_starts = [0] + [end + 1 for start, end in sections]
    remaining_ends = [start - 1 for start, end in sections] + [length - 1]
    remaining_sections = [(start, end) for start, end in zip(remaining_starts, remaining_ends) if end - start + 1 >= 20]

    if remaining_sections:
        new_defects = [d for d in new_defects if any(start <= d['from'] <= end for start, end in remaining_sections)]
        new_length = sum(end - start + 1 for start, end in remaining_sections)
        removed_sections.extend([(start, end) for start, end in zip(remaining_starts, remaining_ends) if end - start + 1 < 20])
    
    return new_defects, new_length, total_cut_length, removed_sections

# Function to plot the original, remaining, and removed fabric sections
def plot_fabric_sections(canvas_frame, original_length, remaining_length, removed_sections, width):
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

    # Display the plot in the tkinter canvas
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Function to plot PPMS and lengths
def plot_ppms(canvas_frame, before_ppms, after_ppms, original_length, new_length, cut_length):
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

    # Display the plot in the tkinter canvas
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Main function
def main(defects, length, width, threshold_ppms, num_sections, canvas_frame1, canvas_frame2, result_text, info_frame):
    original_ppms = calculate_ppms(defects, length, width)
    result_text.insert(tk.END, f"Original PPMS: {original_ppms}\n")
    result_text.insert(tk.END, f"Original Length: {length} meters\n")
    
    if original_ppms > threshold_ppms:
        sections = find_combined_highest_density_sections(defects, width, num_sections)
        new_defects, new_length, total_cut_length, removed_sections = remove_sections(defects, length, width, sections)
        new_ppms = calculate_ppms(new_defects, new_length, width)
        
        result_text.insert(tk.END, f"New PPMS after removing sections {sections}: {new_ppms}\n")
        result_text.insert(tk.END, f"Total Length of cut parts: {total_cut_length} meters\n")
        result_text.insert(tk.END, f"Remaining Length: {new_length} meters\n")
        
        plot_ppms(canvas_frame1, original_ppms, new_ppms, length, new_length, total_cut_length)
        plot_fabric_sections(canvas_frame2, length, new_length, removed_sections, width)
        
        # Displaying the lengths and meter counts in info_frame
        for widget in info_frame.winfo_children():
            widget.destroy()
        info_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        ttk.Label(info_frame, text=f"Original Fabric: {length} meters", font=('Helvetica', 12)).pack(pady=5)
        ttk.Label(info_frame, text=f"Cut Fabric: {total_cut_length} meters", font=('Helvetica', 12)).pack(pady=5)
        ttk.Label(info_frame, text=f"Remaining Fabric: {new_length} meters", font=('Helvetica', 12)).pack(pady=5)
    else:
        result_text.insert(tk.END, "PPMS is within acceptable limits. No need to cut the fabric.\n")

# GUI Application
class FabricOptimizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fabric Optimizer")
        
        # Defects data
        self.defects = [
            {"from": 2, "to": 5, "points": 12},
            {"from": 10, "to": 10, "points": 1},
            {"from": 22, "to": 22, "points": 4},
            {"from": 23, "to": 28, "points": 20},
            {"from": 35, "to": 35, "points": 2},
            {"from": 39, "to": 39, "points": 4},
            {"from": 46, "to": 46, "points": 2},
            {"from": 70, "to": 70, "points": 2}
        ]
        
        # Input fields
        self.length_var = tk.DoubleVar(value=69.6)
        self.width_var = tk.DoubleVar(value=1.5)
        self.threshold_ppms_var = tk.DoubleVar(value=23)
        self.num_sections_var = tk.IntVar(value=2)
        
        input_frame = tk.Frame(self)
        input_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        tk.Label(input_frame, text="Fabric Length (meters):").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(input_frame, textvariable=self.length_var).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Fabric Width (meters):").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(input_frame, textvariable=self.width_var).grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Threshold PPMS:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(input_frame, textvariable=self.threshold_ppms_var).grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Number of Sections to Remove:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(input_frame, textvariable=self.num_sections_var).grid(row=3, column=1, padx=5, pady=5)
        
        self.result_text = tk.Text(input_frame, height=10, width=50)
        self.result_text.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        
        self.canvas_frame1 = tk.Frame(self)
        self.canvas_frame1.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.canvas_frame2 = tk.Frame(self)
        self.canvas_frame2.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.info_frame = tk.Frame(self)
        self.info_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        tk.Button(input_frame, text="Optimize Fabric", command=self.optimize_fabric).grid(row=5, column=0, columnspan=2, pady=10)
    
    def optimize_fabric(self):
        length = self.length_var.get()
        width = self.width_var.get()
        threshold_ppms = self.threshold_ppms_var.get()
        num_sections = self.num_sections_var.get()
        
        self.result_text.delete("1.0", tk.END)
        main(self.defects, length, width, threshold_ppms, num_sections, self.canvas_frame1, self.canvas_frame2, self.result_text, self.info_frame)

if __name__ == "__main__":
    app = FabricOptimizerApp()
    app.mainloop()
