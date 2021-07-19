# R script for downloading XML documents
# from Danish Parliament FTP-server.
# ---

library(tidyverse)
library(curl)

# Define requester functions.
get_collection_urls <- function(base_url){
  
  # Connect to FTP-server. 
  con <- curl(base_url)
  
  # Extract collection IDs
  con %>% 
    read_lines() %>% 
    str_extract("\\d{5}") -> collection_ids
  
  # Build and return URLs for collections.
  str_c(base_url, collection_ids, "/")
}

get_meeting_urls <- function(col_url) {
  
  # Connect to FTP-server. 
  con <- curl(col_url)
  
  # Extract meeting IDs.
  con %>% 
    read_lines() %>% 
    str_extract("\\d{5}_M.*") -> meeting_ids
  
  # Build and return URLs for meeting documents.
  str_c(col_url, meeting_ids)
}


# Base URL for collections on FTP-server.
request_url <- "ftp://oda.ft.dk/ODAXML/Referat/samling/"

# Get collection URLs.
collection_urls <- get_collection_urls(request_url)

# Make sure data folder exists.
if (!dir.exists("data")) {
  dir.create("data")
}

# Loop through collections and prepare download of meeting data.
for (collection in collection_urls) {
  
  # Make directory for data files.
  dir_name <- str_c("data/", str_extract(collection, "\\d{5}"))
  if (!dir.exists(dir_name)) {
    dir.create(dir_name)
  }

  # Get meeting URLs.
  meeting_urls <- get_meeting_urls(collection)
  
  # Download meeting documents.
  for (meeting_url in meeting_urls) {
    file_name <- str_c("data/", str_extract(meeting_url, "\\d{5}/\\d{5}.*"))
    
    curl_download(meeting_url, file_name)
    
    # Wait between requests.
    Sys.sleep(1)
  }
  
  # Wait between requests.
  Sys.sleep(1)
}
