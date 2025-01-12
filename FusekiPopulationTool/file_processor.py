import re

class FileProcessor:
    """
    This class handles file preprocessing tasks
    """
    @staticmethod
    def preprocess_nquads(file_path):
        """
        This function reads and preprocesses a local N-Quads file
        """
        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = f.read()
            fixed_lines = []
            for line in raw_data.splitlines():
                # Match lines with JSON-like objects
                match = re.match(r'(<[^>]+>) (<[^>]+>) <\[(.+)\]> (<[^>]+>)', line)
                if match:
                    subject, predicate, json_object, graph = match.groups()
                    urls = json_object.split(",")
                    for url in urls:
                        # Clean up URL
                        url = url.strip().strip('\\"').replace('%20', '').replace('\\', '')
                        if url:
                            fixed_lines.append(f"{subject} {predicate} <{url}> {graph} .")
                else:
                    fixed_lines.append(line)
        return "\n".join(fixed_lines)