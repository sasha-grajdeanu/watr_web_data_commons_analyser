
<div align="center">

  <h1>WATR - Web Data Commons Analyzer</h1>
  
  
  
<!-- Badges -->
<p>
  <a href="https://github.com/sasha-grajdeanu/watr_web_data_commons_analyser/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/sasha-grajdeanu/watr_web_data_commons_analyser" alt="contributors" />
  </a>
  <a href="">
    <img src="https://img.shields.io/github/last-commit/sasha-grajdeanu/watr_web_data_commons_analyser" alt="last update" />
  </a>
  <a href="https://github.com/sasha-grajdeanu/watr_web_data_commons_analyser/network/members">
    <img src="https://img.shields.io/github/forks/sasha-grajdeanu/watr_web_data_commons_analyser" alt="forks" />
  </a>
  <a href="https://github.com/sasha-grajdeanu/watr_web_data_commons_analyser/stargazers">
    <img src="https://img.shields.io/github/stars/sasha-grajdeanu/watr_web_data_commons_analyser" alt="stars" />
  </a>
  <a href="https://github.com/sasha-grajdeanu/watr_web_data_commons_analyser/issues/">
    <img src="https://img.shields.io/github/issues/sasha-grajdeanu/watr_web_data_commons_analyser" alt="open issues" />
  </a>
  <a href="https://github.com/sasha-grajdeanu/watr_web_data_commons_analyser/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/sasha-grajdeanu/watr_web_data_commons_analyser.svg" alt="license" />
  </a>
</p>
   
<h4>
    <a href="https://github.com/sasha-grajdeanu/watr_web_data_commons_analyser/">View Demo</a>
  <span> · </span>
    <a href="https://github.com/sasha-grajdeanu/watr_web_data_commons_analyser">Documentation</a>
  <span> · </span>
    <a href="https://github.com/sasha-grajdeanu/watr_web_data_commons_analyser/issues/">Report Bug</a>
  <span> · </span>
    <a href="https://github.com/sasha-grajdeanu/watr_web_data_commons_analyser/issues/">Request Feature</a>
  </h4>
</div>

<br />

<!-- Table of Contents -->
# :notebook_with_decorative_cover: Table of Contents

- [About the Project](#star2-about-the-project)
  * [Screenshots](#camera-screenshots)
  * [Tech Stack](#space_invader-tech-stack)
  * [Features](#dart-features)
  * [Color Reference](#art-color-reference)
  * [Environment Variables](#key-environment-variables)
- [Getting Started](#toolbox-getting-started)
  * [Prerequisites](#bangbang-prerequisites)
  * [Installation](#gear-installation)
  * [Run Locally](#running-run-locally)
- [Usage](#eyes-usage)
- [Contributing](#wave-contributing)

  

<!-- About the Project -->
## :star2: About the Project


<!-- Screenshots -->
### :camera: Screenshots

<div align="center"> 
  <img src="https://github.com/sasha-grajdeanu/watr_web_data_commons_analyser/blob/main/docs/scholarly-html-documentation/images/Compare.png" alt="screenshot" />
</div>


<!-- TechStack -->
### :space_invader: Tech Stack

<details>
  <summary>Client</summary>
  <ul>
    <li><a href="https://reactjs.org/">React.js</a></li>
    <li><a href="https://vite.dev/">Vite</a></li>
    <li><a href="https://tailwindcss.com/">TailwindCSS</a></li>
  </ul>
</details>

<details>
  <summary>Server</summary>
  <ul>
    <li><a href="https://flask.palletsprojects.com/">Flask</a></li>
  </ul>
</details>

<details>
<summary>Database/Triple Store</summary>
  <ul>
    <li><a href="https://jena.apache.org/documentation/fuseki2/">Apache Jena Fuseki</a></li>
  </ul>
</details>

<details>
  <summary>Ontology Matching</summary>
  <ul>
    <li><a href="https://github.com/AgreementMakerLight/AML-Project">Agreement Maker Light (AML)</a> </li>
  </ul>
</details>


<!-- Features -->
### :dart: Features

- Visualize data from Fuseki
- Classify data based on subject and predicate
- Compare data from Fuseki
- Align the ontology extracted from Fuseki to other ontologies

<!-- Color Reference -->
### :art: Color Reference

| Color             | Hex                                                                |
| ----------------- | ------------------------------------------------------------------ |
| WATR-100 | ![#1a4078](https://via.placeholder.com/10/1a4078?text=+) #1a4078 |
| WATR_200 | ![#686ea7](https://via.placeholder.com/10/686ea7?text=+) #686ea7 |
| WATR-300 | ![#aea8d6](https://via.placeholder.com/10/aea8d6?text=+) #aea8d6 |
| WATR-400 | ![#ebdded](https://via.placeholder.com/10/ebdded?text=+) #ebdded |


<!-- Env Variables -->
### :key: Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SPARQL_ENDPOINT="http://localhost:3030/watr-dataset/sparql"`

> **⚠️ Note:** It is important to create a dataset named "/watr-dataset" in Fuseki to work.

`AML_PATH=C:\\AML_v3.2\\AgreementMakerLight.jar` (Windows)    
`AML_PATH=/home/user/AML_v3.2/AgreementMakerLight.jar` (Linux/maxOS)

> **⚠️ Note:** If you installed AML in different location, make sure to update the path accordingly in the `.env` file.


<!-- Getting Started -->
## 	:toolbox: Getting Started

<!-- Prerequisites -->
### :bangbang: Prerequisites


<!-- Installation -->
### :gear: Installation

Install the necessary tools for the project:
1. [Node.js](https://nodejs.org/) (required)
2. [Python](https://www.python.org/) (required)
3. [Apache Jena Fuseki](https://dlcdn.apache.org/jena/binaries/apache-jena-fuseki-5.3.0.zip) (required)
4. [AgreementMakerLight](https://github.com/AgreementMakerLight/AML-Project/releases/download/v3.2/AML_v3.2.zip) (required)


<!-- Run Locally -->
### :running: Run Locally

Clone the project

```bash
  git clone https://github.com/sasha-grajdeanu/watr_web_data_commons_analyser.git
```

Go to the project directory

```bash
  cd watr_web_data_commons_analyser
```

Install dependencies

- to install all libraries for back-end component, run
  
```bash
  pip install -r requirements.txt
```

- to install the front-end component, run:
  
```bash
  npm install
```

Start the server

```bash
# Start the frontend
cd watr_front_refactor ; npm run dev

# Start the backend
cd watr_back ; python app.py

# Start the Fuseki server
cd /path/to/fuseki ; fuseki-server --update
```

> **⚠️ Note:** For the backend API to work, you need to have Apache Jena Fuseki running on `http://localhost:3030` 
> with a dataset named `watr-dataset`


<!-- Usage -->
## :eyes: Usage

The Web Data Commons Analyzer (WATR) is a web-based application designed to process and analyze metadata extracted from the Web Data Commons. Through this platform, users can perform complex tasks such as visualizing the structure and relationships within the data, classifying it according to predefined categories, comparing data, and aligning the data with existing ontologies. The system uses SPARQL queries to a Apache Jena Fuseki server to retrieve the data, and results are available in HTML, JSON-LD and JSON formats. Various statistics for each operation are provided using the RDF Data Cube vocabulary. 

When opening the web application, the user will see the home page, where information about the project is displayed.

From the navigation bar, they can select the following pages:
### Visualisation

This page is dedicated to viewing data provided by Web Data Commons. The user will fill out a form to select the class from which they want to view data, then choose whether they want to see all data related to the class or only a portion of it. If they select “true”, they must specify the desired number of records. If any form field is left empty, the user will be warned before submission.

After submitting the form, a panel will appear on the right side, displaying a graph generated using the selected class's data, along with various statistics about the data (number of unique entities, properties, and their usage frequency, etc.).

The user can download data files in various formats (HTML, JSON-LD) as well as a file with the generated statistics, modeled using the RDF Data Cube vocabulary.
### Comparison

This page is dedicated to comparing two classes from the dataset provided by Web Data Commons. The user will fill out a form to select two different classes for comparison. If any field is left empty or the user selects the same class twice, they will be warned before submitting the form.

After submission, a panel will appear on the right side displaying a table showing the properties used by each class, their frequency, and various statistics about the comparison (common properties, unique properties for each class, the most used and least used properties).

The user can download data files in various formats (HTML, JSON-LD) as well as a file with the generated statistics, modeled using the RDF Data Cube vocabulary.
### Classification

This page allows the classification of data provided by Web Data Commons based on class and property. The user will fill out a form to select a class and a property for classification. If any field is left empty, the user will be warned before submitting the form.

After submission, a panel will appear on the right side, displaying a graph generated using the provided data, along with various statistics about the data. The user can download data files in various formats (HTML, JSON-LD) as well as files with the generated statistics, modeled using the RDF Data Cube vocabulary.
### Alignment

This page is dedicated to aligning the data provided by Web Data Commons to an existing ontology. The user will fill out a form to select the ontology based on which the alignment will be performed. If any field is left empty, the user will be warned before submitting the form.

After submission, a panel will appear on the right side displaying a table with the alignment results and an average of the aligned data. The user can download data files in various formats (HTML, JSON-LD) as well as a file with the generated statistics, modeled using the RDF Data Cube vocabulary.



<!-- Contributing -->
## :wave: Contributing

<a href="https://github.com/sasha-grajdeanu/watr_web_data_commons_analyser/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=sasha-grajdeanu/watr_web_data_commons_analyser" />
</a>



