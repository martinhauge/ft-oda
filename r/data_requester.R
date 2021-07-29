# R script for downloading XML documents
# from Danish Parliament FTP-server.
# ---

library(tidyverse)
library(curl)

# Initial setup.
# Path to destination for downloaded documents:
data_folder <- "data"

# Sleep time between requests in seconds
sleep_time = 1

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
if (!dir.exists(data_folder)) {
  dir.create(data_folder)
}

# Absolute data destination
print(str_c("Saving documents to ", file.path(getwd(), data_folder)))

# Loop through collections and prepare download of meeting data.
for (collection in collection_urls) {
  
  # Make directory for data files.
  dir_name <- file.path(data_folder, str_extract(collection, "\\d{5}"))
  if (!dir.exists(dir_name)) {
    dir.create(dir_name)
  }

  # Get meeting URLs.
  meeting_urls <- get_meeting_urls(collection)
  print(str_c("Requesting documents from ", collection))
  
  # Wait between requests.
  Sys.sleep(sleep_time)
  
  # Download meeting documents.
  for (meeting_url in meeting_urls) {
    file_name <- file.path(data_folder, str_extract(meeting_url, "\\d{5}/\\d{5}.*"))
    
    if (!file.exists(file_name)) {
      curl_download(meeting_url, file_name)
      
      # Wait between requests.
      Sys.sleep(sleep_time)
    }
  }
}
