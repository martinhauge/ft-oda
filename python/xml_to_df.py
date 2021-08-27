from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd

def xml_to_str(xml_path):
	'''Open XML-file and return it as a string.
	'''
	with open(xml_path) as f:
		xml_str = f.read()
	return xml_str

def xml_str_to_rows(xml_str):
	'''Convert XML text string to a list of dictionaries
	with selected data fields extracted from markup.
	'''
	xml_rows = list()
	xml_soup = BeautifulSoup(xml_str, 'lxml')

	for item in xml_soup.select('Tale'):
		xml_rows.append(xml_to_dict(item))

	return xml_rows

def xml_to_dict(item):
	'''Extract data from XML and return as a dictionary.
	'''

	# Error handling in case of missing data for each data field.
	first_name = item.select_one('OratorFirstName')
	first_name = first_name.text if first_name else ''
	
	last_name = item.select_one('OratorLastName')
	last_name = last_name.text if last_name else ''

	group_name = item.select_one('GroupNameShort')
	group_name = group_name.text if group_name else ''

	role = item.select_one('OratorRole')
	role = role.text if role else ''

	start_time = item.select_one('StartDateTime')
	start_time = start_time.text if start_time else ''

	# End time defaults to last available entry in case of consecutive segments.
	end_time = item.select('EndDateTime')
	end_time = end_time[-1].text if end_time else ''

	# Consecutive segments by the same speaker are joined together.
	text_segments = item.select('TaleSegment')
	text = ' '.join([' '.join([i.text for i in segment.select('char')]) for segment in text_segments]) if text_segments else ''

	# Collect and return extracted data in a dictionary
	xml_dict = {
	'first_name': first_name,
	'last_name': last_name,
	'group_name': group_name,
	'role': role,
	'start_time': start_time,
	'end_time': end_time,
	'text': text
	}

	return xml_dict

if __name__ == '__main__':
	# Define path to XML files to be converted.
	data_folder = ''

	csv_file = 'file_name.csv'

	# Get list of paths to files in data folder.
	file_paths = [Path(f) for f in Path(data_folder).iterdir()]	

	# List for appending data rows before export.
	rows = list()

	for path in file_paths:
		xml_str = xml_to_str(path)
		rows.extend(xml_str_to_rows(xml_str))

	# Convert data to pandas DataFrame, sort rows by time and export as csv.
	pd.DataFrame(rows, columns=rows[0].keys()).sort_values('start_time').to_csv(csv_file, index=False)
