# Imports packages
import openpyxl 

# Loads workbook
wb = openpyxl.load_workbook('../../Data/TELEOS_1/WOD/WOD_SID_10_20May.xlsx')
ws = wb['0x80070000 - Data Order 1']
print('Total number of rows: '+str(ws.max_row)+'. And total number of columns: '+str(ws.max_column))