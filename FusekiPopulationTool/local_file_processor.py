from file_processor import FileProcessor

class LocalFileProcessor:
    """
    This class processes local N-Quads files and uploads them to Fuseki
    """
    def __init__(self, fuseki_client):
        self.fuseki_client = fuseki_client

    def process_local_file(self, file_path):
        """
        Function that processes a local N-Quads file.
        """
        print(f"Processing local file: {file_path}")
        preprocessed_data = FileProcessor.preprocess_nquads(file_path)
        self.fuseki_client.add_nquads(preprocessed_data)