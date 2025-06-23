# Imports packages
import openpyxl 
from datetime import datetime

# Sets up dictionaries and lists
dict_sheets = {"pos_x":"0x80070000 - Data Order 1",\
               "pos_y":"0x80080000 - Data Order 1",\
               "pos_z":"0x80090000 - Data Order 1",\
               "vel_x":"0x800A0000 - Data Order 1",\
               "vel_y":"0x800B0000 - Data Order 1",\
               "vel_z":"0x800C0000 - Data Order 1"}
dict_lists = {"datetime":[],\
                "pos_x":[],\
               "pos_y":[],\
               "pos_z":[],\
               "vel_x":[],\
               "vel_y":[],\
               "vel_z":[]}

# Loads workbook
wb = openpyxl.load_workbook('../../Data/TELEOS_1/WOD/WOD_SID_10_20May.xlsx')

# Loops through sheets
for field in dict_sheets:
    ws = wb[dict_sheets[field]]
    print(f"For {field}")
    print('Total number of rows: '+str(ws.max_row)+'. And total number of columns: '+str(ws.max_column))
    for row_num in range(11,ws.max_row+1):
        dict_lists[field].append(ws.cell(row=row_num,column=1).value)
    print(dict_lists[field])