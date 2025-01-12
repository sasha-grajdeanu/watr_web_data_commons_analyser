import requests

class LinkProcessor:
    """
    Class that processes a file containing links to N-Quads files
    """
    def __init__(self, links_file, fuseki_client, url_fetcher):
        self.links_file = links_file
        self.fuseki_client = fuseki_client
        self.url_fetcher = url_fetcher

    def process_links(self):
        """
        Function that reads the links file, fetches N-Quads from each link, and adds them to Fuseki
        """
        with open(self.links_file, "r") as file:
            links = file.readlines()

        with requests.Session() as session:
            for link in links:
                link = link.strip()
                if not link:
                    continue

                print(f"Fetching N-Quads from: {link}")
                nquads_data = self.url_fetcher.fetch_with_retries(session, link)
                if nquads_data:
                    print(f"Successfully fetched N-Quads from: {link}")
                    self.fuseki_client.add_nquads(nquads_data)
                else:
                    print(f"Skipping {link} due to repeated failures.")
