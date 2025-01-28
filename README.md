
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
  * [Running Tests](#test_tube-running-tests)
  * [Run Locally](#running-run-locally)
  * [Deployment](#triangular_flag_on_post-deployment)
- [Usage](#eyes-usage)
- [Contributing](#wave-contributing)
- [License](#warning-license)
- [Contact](#handshake-contact)

  

<!-- About the Project -->
## :star2: About the Project


<!-- Screenshots -->
### :camera: Screenshots

<div align="center"> 
  <img src="https://placehold.co/600x400?text=Your+Screenshot+here" alt="screenshot" />
</div>


<!-- TechStack -->
### :space_invader: Tech Stack

<details>
  <summary>Client</summary>
  <ul>
    <li><a href="https://www.typescriptlang.org/">Typescript</a></li>
    <li><a href="https://reactjs.org/">React.js</a></li>
  </ul>
</details>

<details>
  <summary>Server</summary>
  <ul>
    <li><a href="https://flask.palletsprojects.com/">Flask</a></li>
    <li><a href="https://github.com/AgreementMakerLight/AML-Project">Agreement Maker Light (AML)</a> </li>
  </ul>
</details>

<details>
<summary>Database</summary>
  <ul>
    <li><a href="https://jena.apache.org/documentation/fuseki2/">Apache Jena Fuseki</a></li>
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
| Primary Color | ![#222831](https://via.placeholder.com/10/222831?text=+) #222831 |
| Secondary Color | ![#393E46](https://via.placeholder.com/10/393E46?text=+) #393E46 |
| Accent Color | ![#00ADB5](https://via.placeholder.com/10/00ADB5?text=+) #00ADB5 |
| Text Color | ![#EEEEEE](https://via.placeholder.com/10/EEEEEE?text=+) #EEEEEE |


<!-- Env Variables -->
### :key: Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`FUSEKI_URL="http://localhost:3030/watr-dataset/sparql"`

`AML_PATH=C:\\AML_v3.2\\AgreementMakerLight.jar` (Windows)    
`AML_PATH=/home/user/AML_v3.2/AgreementMakerLight.jar` (Linux/maxOS)

> **⚠️ Note:** If you installed AML in different location, make sure to update the path accordingly in the `.env` file.


<!-- Getting Started -->
## 	:toolbox: Getting Started

<!-- Prerequisites -->
### :bangbang: Prerequisites

- Install Alignment Maker Light (AML): [Download AML v3.2](https://github.com/AgreementMakerLight/AML-Project/releases/download/v3.2/AML_v3.2.zip)
  - After downloading, unzip the file in a directory of your choice (e.g., `C:\` for Windows or `/home/user/` for Linux/macOS). Ensure that you update the path in your `.env` file accordingly.
- Install Apache Jena Fuseki server: [Download Fuseki v5.3.0](https://dlcdn.apache.org/jena/binaries/apache-jena-fuseki-5.3.0.zip)
  - Extract the Fuseki server in a directory such as `C:\` (Windows) or `/home/user/` (Linux/macOS).


<!-- Installation -->
### :gear: Installation

Install my-project with npm

```bash
  yarn install my-project
  cd my-project
```
   
<!-- Running Tests -->
### :test_tube: Running Tests

To run tests, run the following command

```bash
  yarn test test
```

<!-- Run Locally -->
### :running: Run Locally

Clone the project

```bash
  git clone https://github.com/sasha-grajdeanu/watr_web_data_commons_analyser.git
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
  yarn install
```

Start the server

```bash
  yarn start
```
> **⚠️ Note:** For the backend API to work, you need to have Apache Jena Fuseki running on `http://localhost:3030`

<!-- Deployment -->
### :triangular_flag_on_post: Deployment

To deploy this project run

```bash
  yarn deploy
```


<!-- Usage -->
## :eyes: Usage

Use this space to tell a little more about your project and how it can be used. Show additional screenshots, code samples, demos or link to other resources.


```javascript
import Component from 'my-project'

function App() {
  return <Component />
}
```


<!-- Contributing -->
## :wave: Contributing

<a href="https://github.com/sasha-grajdeanu/watr_web_data_commons_analyser/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=sasha-grajdeanu/watr_web_data_commons_analyser" />
</a>


<!-- License -->
## :warning: License

Distributed under the no License. See LICENSE.txt for more information.


<!-- Contact -->
## :handshake: Contact

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email@email_client.com

Project Link: [https://github.com/Louis3797/awesome-readme-template](https://github.com/Louis3797/awesome-readme-template)

