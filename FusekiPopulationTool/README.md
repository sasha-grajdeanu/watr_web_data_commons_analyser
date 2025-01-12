# Fuseki N-Quads Processor
This tool allows you to fetch, preprocess, and upload N-Quads data to Apache Jena Fuseki server.

## Configuration
Follow these steps to set up and access the Apache Jena Fuseki server:
1. **Download Apache Jena Fuseki Server**   
[Apache Jena Fuseki Server](https://dlcdn.apache.org/jena/binaries/apache-jena-fuseki-5.2.0.zip)

2. **Extract the `.zip` File**    
Extract the downloaded `.zip` file to C: directory (e.g., `C:\apache-jena-fuseki-5.2.0`)

3. **Start the Server**   
Open a Command Prompt, navigate to the extracted directory, and run the following command to start the server:    
```bash
fuseki-server --update
```

4. **Access the Server**    
Open your web browser and go to http://localhost:3030

5. **Create a Dataset**
   - Go to the "Manage" page
   - Under the "New Dataset", create a dataset with the following settings:
       - **Name**: `watr-dataset`
       - **Dataset Type**: Persistent

## Usage
This tool processes sample files from the [Web Data Commons Schema.org Subsets](https://webdatacommons.org/structureddata/2023-12/stats/schema_org_subsets.html)

### File Overview
- `sample-urls.txt`: Contains URLs to sample files with N-Quads
- `Hospital_sample.txt`: Contains a sample file for the Hospital subset

The `Hospital_sample.txt` file is processed separately because the original file contains a JSON-like object that must be cleaned before being added to Fuseki.

### Run the Tool
To run the tool, execute the `main.py` file using Python:  
```python main.py```