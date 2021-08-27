# Folketinget Open Data
Various scripts for working with Folketinget's open data API.


### `data_requester`
Download all parliamentary proceedings (2009-) in XML-format from Folketinget's FTP-server.

### `xml_to_df`
Extract specific data fields from XML and convert to CSV/DataFrame.

Extracted data:
- Speaker name
- Group affiliation
- Role
- Time of speech
- Content of speech

At the moment Python-only.