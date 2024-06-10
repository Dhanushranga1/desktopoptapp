import pandas as pd
import pyodbc

# Create a connection to the SQLite database
conn = pyodbc.connect(r'DRIVER={SQL Server};'
                      r'SERVER=DHANUSH\\SQLEXPRESS;'
                      r'DATABASE=DB1;'
                      r'Trusted_Connection=yes;')
cursor = conn.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS fabric_info (
        id INTEGER PRIMARY KEY,
        sort_number TEXT,
        fabric_type TEXT,
        shade TEXT,
        roll_number TEXT,
        lot_number TEXT,
        shade_group TEXT,
        gross_meter REAL,
        allowance REAL,
        net_meter REAL,
        gross_weight REAL,
        net_weight REAL,
        grade TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS defects (
        id INTEGER PRIMARY KEY,
        fabric_id INTEGER,
        from_mtr INTEGER,
        to_mtr INTEGER,
        defect_name TEXT,
        defect_type TEXT,
        points INTEGER,
        FOREIGN KEY (fabric_id) REFERENCES fabric_info (id)
    )
''')

# Load the Excel workbook
file_path = '/mnt/data/your_excel_file.xlsx'
excel_data = pd.ExcelFile(file_path)

for sheet_name in excel_data.sheet_names:
    df = excel_data.parse(sheet_name)

    # Extract fabric information
    fabric_info = {
        'sort_number': df.iloc[0, 1],
        'fabric_type': df.iloc[1, 1],
        'shade': df.iloc[2, 1],
        'roll_number': df.iloc[3, 1],
        'lot_number': df.iloc[4, 1],
        'shade_group': df.iloc[5, 1],
        'gross_meter': df.iloc[0, 3],
        'allowance': df.iloc[1, 3],
        'net_meter': df.iloc[2, 3],
        'gross_weight': df.iloc[3, 3],
        'net_weight': df.iloc[4, 3],
        'grade': df.iloc[5, 3],
    }

    # Insert fabric info into the database
    cursor.execute('''
        INSERT INTO fabric_info (sort_number, fabric_type, shade, roll_number, lot_number, shade_group, gross_meter, allowance, net_meter, gross_weight, net_weight, grade)
        VALUES (:sort_number, :fabric_type, :shade, :roll_number, :lot_number, :shade_group, :gross_meter, :allowance, :net_meter, :gross_weight, :net_weight, :grade)
    ''', fabric_info)
    cursor.execute("SELECT SCOPE_IDENTITY()")
    fabric_id = cursor.fetchone()[0]

    # Extract and insert defect details
    defect_rows = df.iloc[11:, [0, 1, 2, 3, 4]].dropna()
    for _, row in defect_rows.iterrows():
        defect = {
            'fabric_id': fabric_id,
            'from_mtr': row[0],
            'to_mtr': row[1],
            'defect_name': row[2],
            'defect_type': row[3],
            'points': row[4]
        }
        cursor.execute('''
            INSERT INTO defects (fabric_id, from_mtr, to_mtr, defect_name, defect_type, points)
            VALUES (:fabric_id, :from_mtr, :to_mtr, :defect_name, :defect_type, :points)
        ''', defect)

# Commit and close the connection
conn.commit()
conn.close()
