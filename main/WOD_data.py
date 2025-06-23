# Imports packages
import openpyxl 

# Sets up lists
list_sheets = ["0x80070000 - Data Order 1",\
               "0x80080000 - Data Order 1",\
               "0x80090000 - Data Order 1",\
               "0x800A0000 - Data Order 1",\
               "0x800B0000 - Data Order 1",\
               "0x800C0000 - Data Order 1",]

# Loads workbook
wb = openpyxl.load_workbook('../../Data/TELEOS_1/WOD/WOD_SID_10_20May.xlsx')
ws = wb['0x80070000 - Data Order 1']
print('Total number of rows: '+str(ws.max_row)+'. And total number of columns: '+str(ws.max_column))

print(ws.cell(row=11,column=1).value)
print(type(ws.cell(row=11,column=1).value))