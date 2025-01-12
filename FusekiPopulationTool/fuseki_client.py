import requests

class FusekiClient:
    """
    This class interacts with the Fuseki server
    """
    def __init__(self, fuseki_endpoint):
        self.fuseki_endpoint = fuseki_endpoint

    def add_nquads(self, text_response):
        """
        Function that adds N-Quads data to the Fuseki server
        """
        headers = {"Content-Type": "application/n-quads"}
        try:
            response = requests.post(self.fuseki_endpoint, data=text_response, headers=headers)
            if response.status_code in (200, 201):
                print("N-Quads data successfully added to Fuseki.")
            else:
                print(f"Failed to add N-Quads to Fuseki. Status: {response.status_code}, Error: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Fuseki: {e}")