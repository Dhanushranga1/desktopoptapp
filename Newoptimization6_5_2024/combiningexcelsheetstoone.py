import os
import pandas as pd
import openpyxl
print("Copying sheets from multiple files to one file")
cwd = os.path.abspath('C:\\Myfiles')
files = os.listdir(cwd)  

df_total = pd.DataFrame()
df_total.to_excel('Combined/combined_file.xlsx') #create a new file
workbook=openpyxl.load_workbook('Combined/combined_file.xlsx')
ss_sheet = workbook['Sheet1']
ss_sheet.title = 'TempExcelSheetForDeleting'
workbook.save('Combined/combined_file.xlsx')


for file in files:                         # loop through Excel files
    if file.endswith('.xls') or file.endswith('.xlsx'):
        excel_file = pd.ExcelFile(file)
        sheets = excel_file.sheet_names
        for sheet in sheets:               # loop through sheets inside an Excel file
            print (file, sheet)
            df = excel_file.parse(sheet_name = sheet)
            with pd.ExcelWriter("Combined/combined_file.xlsx",mode='a') as writer:  
                df.to_excel(writer, sheet_name=f"{sheet}", index=False)
            #df.to_excel("Combined/combined_file.xlsx", sheet_name=f"{sheet}")

workbook=openpyxl.load_workbook('Combined/combined_file.xlsx')
std=workbook["TempExcelSheetForDeleting"]
workbook.remove(std)
workbook.save('Combined/combined_file.xlsx')
print("Loaded, press ENTER to end")
dali=input()
#df_total.to_excel('Combined/combined_file.xlsx')
print("Done")
dali=input()