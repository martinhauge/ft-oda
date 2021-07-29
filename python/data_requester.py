from ftplib import FTP
from pathlib import Path
from time import sleep

data_folder = Path('data')

sleep_time = 1

def get_paths(con, path=''):
	return con.nlst(path)

print(f'Saving documents to {data_folder.absolute()}')
# Open connection
url = 'oda.ft.dk'
path = 'ODAXML/Referat/samling'

ftp = FTP(url)
ftp.login()

ftp.cwd(path)

# Find collections

collections = get_paths(ftp)

for collection in collections:

	print(f'Requesting data for {collection}')

	meetings = get_paths(ftp, collection)
	ftp.cwd(collection)


	collection_folder = Path(data_folder, collection)
	collection_folder.mkdir(parents=True, exist_ok=True)

	sleep(sleep_time)

	for meeting in meetings:
		document_path = Path(collection_folder, meeting)

		if not document_path.exists():
			# Save document
			ftp.retrbinary(f'RETR {meeting }', open(document_path, 'wb').write)

			sleep(sleep_time)

	ftp.cwd('..')


# Close connection
ftp.quit()