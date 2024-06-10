# import pandas as pd

# # The path to your Excel file
# # excel_file_path = '"C:\Myfiles\New folder\BLENKINGEWHITEC.xlsx"'
# excel_file_path = "C:\\Myfiles\\New folder\\BLENKINGEWHITEC.xlsx"
# # Load the Excel file
# xls = pd.ExcelFile(excel_file_path)

# # List to hold data from all sheets
# all_data = []

# # Iterate through all the sheets in the Excel file
# for sheet_name in xls.sheet_names:
#     # Read the current sheet
#     sheet_data = pd.read_excel(xls, sheet_name=sheet_name)
    
#     # Select only the columns we are interested in
#     selected_columns = sheet_data[['GROSS METER', 'FROM MTR', 'TO MTR', 'POINTS']]
    
#     # Append the selected columns to the list
#     all_data.append(selected_columns)

# # Combine all the data into a single DataFrame
# combined_data = pd.concat(all_data)

# # Save the combined data to a new Excel file
# combined_data.to_excel('combined_fabric_data.xlsx', index=False)

# print('Combined Excel file created successfully!')


import pandas as pd

# The path to your Excel file
excel_file_path = 'fabric_data.xlsx'

# Load the Excel file
xls = pd.ExcelFile(excel_file_path)

# List to hold data from all sheets
all_data = []

# Iterate through all the sheets in the Excel file
for sheet_name in xls.sheet_names:
    # Read the current sheet
    sheet_data = pd.read_excel(xls, sheet_name=sheet_name)
    
    # Select only the columns we are interested in
    selected_columns = sheet_data[['GROSS METER', 'FROM MTR', 'TO MTR', 'POINTS']]
    
    # Append the selected columns to the list
    all_data.append(selected_columns)

# Combine all the data into a single DataFrame
combined_data = pd.concat(all_data)

# Assuming 'GROSS METER' is in the first column, set the value of cell D3
# Note: 'iloc[0, 0]' refers to the first row and first column of the combined data
combined_data.at[2, 'D'] = combined_data.iloc[0, 0]  # Set the value of cell D3

# Save the combined data to a new Excel file
combined_data.to_excel('combined_fabric_data.xlsx', index=False)

print('Combined Excel file created successfully with GROSS METER value in D3!')

