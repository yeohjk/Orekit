# Imports packages
import openpyxl 
from datetime import datetime

# Sets up lists
dict_sheets = {"pos_x":"0x80070000 - Data Order 1",\
               "pos_y":"0x80080000 - Data Order 1",\
               "pos_z":"0x80090000 - Data Order 1",\
               "vel_x":"0x800A0000 - Data Order 1",\
               "vel_y":"0x800B0000 - Data Order 1",\
               "vel_z":"0x800C0000 - Data Order 1"}

# Loads workbook
wb = openpyxl.load_workbook('../../Data/TELEOS_1/WOD/WOD_SID_10_20May.xlsx')

# Loops through sheets
for field in dict_sheets:
    ws = wb[dict_sheets[field]]
    print('Total number of rows: '+str(ws.max_row)+'. And total number of columns: '+str(ws.max_column))
    print(ws.cell(row=11,column=8).value)
    print(type(ws.cell(row=11,column=8).value))