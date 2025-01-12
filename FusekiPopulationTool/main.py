from URL_fetcher import URLFetcher
from fuseki_client import FusekiClient
from link_processor import LinkProcessor
from local_file_processor import LocalFileProcessor

if __name__ == "__main__":
    # Configuration
    FUSEKI_URL = "http://localhost:3030/watr-dataset/data"
    LINKS_FILE = "WDC_files/sample-urls.txt"
    HOSPITAL_FILE = "WDC_files/Hospital_sample.txt"

    # Instantiate objects
    fuseki_client = FusekiClient(FUSEKI_URL)
    url_fetcher = URLFetcher()
    link_processor = LinkProcessor(LINKS_FILE, fuseki_client, url_fetcher)
    local_file_processor = LocalFileProcessor(fuseki_client)

    # Process data
    link_processor.process_links()
    local_file_processor.process_local_file(HOSPITAL_FILE)