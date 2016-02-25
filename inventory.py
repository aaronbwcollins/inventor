#! python2

import os
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials


print('Starting Up, please wait for promnt...')
# For Testing purposes 
#scan = ''

exec_path = os.path.dirname(os.path.realpath(__file__))
# Configuration
json_key = json.load(open("%s/inventory-06b3cba18fd9.json" % exec_path))


# Variables (Do Not Edit!)
scope = ['https://spreadsheets.google.com/feeds']
creds = SignedJwtAssertionCredentials(
	json_key['client_email'], json_key['private_key'].encode(), scope)
gc = gspread.authorize(creds)
wks = gc.open("Test Inventory")

# Set Sheet Location
location = "Sheet1"
#TODO location via Pashu if user based
current_wks = wks.worksheet(location)


#TODO Read Barcode via Pashu
#TODO Ask for QTY. via Pashu

def normal_reduction(barcode, wks):
	# Reduces QTY by 1
	Qty_to_update = -(int('1'))
	try:
		cell = wks.find(barcode)
		cellRow = int(cell.row)
		cellCol = int(cell.col)
		values_list = wks.row_values(cellRow)
		cellCol = cellCol + 1
		current_Qty = int(values_list[1]) + Qty_to_update
		wks.update_cell(cellRow, cellCol, current_Qty)
		print('Item successfully reduced by ' + str(-Qty_to_update))
	except Exception:
		print('Barcode not found!')

def add_inventory(wks):
	# Adds Inventory
	print('*(Add Mode)*')	
	print('Please Scan Barcode:')
	barcode = raw_input()
	try:
		cell = wks.find(barcode)
		print('Please Enter QTY.')
		Qty_to_update = (int(raw_input()))
		cellRow = int(cell.row)
		cellCol = int(cell.col)
		values_list = wks.row_values(cellRow)
		cellCol = cellCol + 1
		current_Qty = int(values_list[1]) + Qty_to_update
		wks.update_cell(cellRow, cellCol, current_Qty)
		print('Item successfully increased by ' + str(Qty_to_update))
	except Exception:
		print('Barcode not found! Resetting...')

def subtract_inventory(wks):
	# Subtracts Inventory
	print('*(Subtract Mode)*')
	print('Please Scan Barcode:')
	barcode = raw_input()
	try:
		cell = wks.find(barcode)
		print('')
		print('Please Enter QTY.')
		Qty_to_update = -(int(raw_input()))
		cellRow = int(cell.row)
		cellCol = int(cell.col)
		values_list = wks.row_values(cellRow)
		cellCol = cellCol + 1
		current_Qty = int(values_list[1]) + Qty_to_update
		wks.update_cell(cellRow, cellCol, current_Qty)
		print('Item successfully reduced by ' + str(-Qty_to_update))
	except Exception:
		print('Barcode not found! Resetting...')

def audit_inventory(wks):
	# Audits Inventory
	for i in range(2,10):
		values_list = wks.row_values(i)
		if values_list[0] != '':
			print('Please wait for promnt...')
			barcode = values_list[0]
			print('*(Audit Mode)*')
			cell = wks.find(barcode)
			cellRow = int(cell.row)
			cellCol = int(cell.col)
			cellCol = cellCol + 1
			print('Current Item:')
			print(values_list[0])
			print('Recorded Stock:')
			print(values_list[1])
			print('Please enter current stock:')
			Qty_to_update = int(raw_input())
			current_Qty = Qty_to_update
			wks.update_cell(cellRow, cellCol, current_Qty)
	print('Audit Complete')


while True:
	print('Please Scan barcode:')
	scan = raw_input()	

	if scan == 'Add':
		add_inventory(current_wks)
	elif scan == 'Subtract':
		subtract_inventory(current_wks)
	elif scan == 'Audit':
		audit_inventory(current_wks)
	elif scan == 'exit':
		break
	else:
		normal_reduction(scan, current_wks)
