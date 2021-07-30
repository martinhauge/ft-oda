from ftplib import FTP
from pathlib import Path
from time import sleep


def get_paths(con, path=''):
	return con.nlst(path)

def connect(url, path):
	ftp = FTP(url)
	ftp.login()
	ftp.cwd(path)
	return ftp

def main():

	# Destination of downloaded documents.
	data_folder = Path('data')

	# Rest between requests.
	sleep_time = 1

	print(f'Saving documents to {data_folder.absolute()}')
	

	# Open connection
	
	url = 'oda.ft.dk'
	path = 'ODAXML/Referat/samling'

	ftp = connect(url, path)

	# Find collections
	collections = get_paths(ftp)

	# Loop through collections and prepare download of meeting data.
	for collection in collections:

		print(f'Requesting data for {collection}')

		meetings = get_paths(ftp, collection)

		# Navigate to collection
		ftp.cwd(collection)

		# Prepare destination folder
		collection_folder = Path(data_folder, collection)
		collection_folder.mkdir(parents=True, exist_ok=True)


		for meeting in meetings:
			document_path = Path(collection_folder, meeting)

			if not document_path.exists():
				
				# Save document
				ftp.retrbinary(f'RETR {meeting }', open(document_path, 'wb').write)

				# Wait between downloads.
				sleep(sleep_time)

		# Return to parent folder.
		ftp.cwd('..')


	# Finally close connection.
	ftp.quit()

if __name__ == '__main__':
	main()