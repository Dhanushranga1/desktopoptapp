def optimize_fabric_rolls(roll_a, roll_b, width, standard):
    # Calculate the total area of the fabric rolls
    area_a = roll_a['length'] * width
    area_b = roll_b['length'] * width
    total_area = area_a + area_b
    
    # Calculate the initial defect point density
    initial_points = sum(roll_a['points']) + sum(roll_b['points'])
    initial_density = (initial_points * 100) / total_area
    
    # Optimize Fabric Roll A
    optimized_a = roll_a.copy()
    for i in range(len(roll_a['from'])-1, -1, -1):
        if roll_a['type'][i] == 'MAJOR':
            del optimized_a['from'][i]
            del optimized_a['to'][i]
            del optimized_a['name'][i]
            del optimized_a['type'][i]
            del optimized_a['points'][i]
            if sum(optimized_a['points']) * 100 / (optimized_a['length'] * width) <= standard:
                break
    roll_a_length = optimized_a['length']
    
    # Combine the optimized fabric rolls
    combined_length = roll_a_length + roll_b['length']
    if combined_length < 80:
        return None
    
    # Calculate the optimized defect point density
    optimized_points = sum(optimized_a['points']) + sum(roll_b['points'])
    optimized_density = (optimized_points * 100) / (combined_length * width)
    
    return optimized_density

# Example usage
roll_a = {
    'from': [7, 15, 23, 25, 28, 30, 41, 41, 52, 66, 68, 71, 76],
    'to': [7, 15, 23, 25, 28, 30, 41, 41, 52, 66, 68, 71, 76],
    'name': ['HOLE', 'MISSING END', 'MISSING END', 'RUST STAIN', 'HANDLING STAIN', 'LOOSE WARP', 'MISSING END', 'SLUB', 'RUST STAIN', 'HANDLING STAIN', 'HANDLING STAIN', 'MISSING END', 'WRONG END'],
    'type': ['MAJOR', 'MINOR', 'MAJOR', 'MINOR', 'MINOR', 'MINOR', 'MINOR', 'MAJOR', 'MINOR', 'MAJOR', 'MAJOR', 'MINOR', 'MAJOR'],
    'points': [4, 1, 5, 1, 4, 1, 4, 4, 1, 4, 4, 1, 4],
    'length': 88.7
}

roll_b = {
    'from': [3, 27, 37, 46, 48, 54, 58, 67, 75, 76],
    'to': [3, 27, 37, 46, 48, 54, 58, 67, 75, 76],
    'name': ['CONTOMINATION', 'WRONG END', 'SLUB YARN', 'SLUB YARN', 'SLUB YARN', 'CONTOMINATION', 'MISSING END', 'BROKEN PICK', 'SLUB YARN', 'SLUB YARN'],
    'type': ['MINOR', 'MAJOR', 'MAJOR', 'MAJOR', 'MAJOR', 'MAJOR', 'MINOR', 'MAJOR', 'MAJOR', 'MAJOR'],
    'points': [2, 4, 4, 4, 4, 4, 1, 4, 4, 4],
    'length': 81.1
}

width = 1.5
standard = 23

optimized_density = optimize_fabric_rolls(roll_a, roll_b, width, standard)
if optimized_density is not None:
    print(f"Optimized defect point density: {optimized_density:.2f} points per 100 square meters")
else:
    print("Optimization failed to meet the minimum length requirement.")