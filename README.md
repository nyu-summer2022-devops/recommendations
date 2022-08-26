# Recommendations Microservice for a Commerce website

[![Build Status](https://github.com/nyu-summer2022-devops/recommendations/actions/workflows/ci.yml/badge.svg)](https://github.com/nyu-summer2022-devops/recommendations/actions)
[![codecov](https://codecov.io/gh/nyu-summer2022-devops/recommendations/branch/master/graph/badge.svg?token=2QOVHKZ67W)](https://codecov.io/gh/nyu-summer2022-devops/recommendations)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

This system is designed for an **eCommerce store**.

## Overview

The recommendations resource is a representation a product recommendation based on another product. In essence it is just a relationship between two products that "go
together" (e.g., radio and batteries, printers and ink, shirts and pants, etc.). It could also recommend based on what other customers have purchased like "customers who bought item A usually buy item B". Recommendations should have a recommendation type like cross-sell, up- sell, accessory, etc. This way a product page could request all of the up-sells for a product. (Hint: an up-sell is a more full featured and expensive product that you recommend instead of the one they initially want to buy, cross-sells are other items just like this one with similar features and price.)

The `/service` folder contains `models.py` file for the model and a `routes.py` file for the service. The `/tests` folder has test cases for testing the model and the service separately.

The application is currently deployed to a Kubernetes cluster on IBM cloud. 

## Attributes

id : non-information bearing key

product_id : id of the source product

product_name : name of the source product

rec_id : id of the recommended product

rec_name : name of the recommended product

rec_type : the type of recommendation (CROSS_SELL = 0, UP_SELL = 1, ACCESSORY = 2, BUY_WITH = 3)

## Functionalities

We built a [**RESTful API**](http://159.122.175.152:31001/) and a [**Swagger API Documentation**](http://159.122.175.152:31001/apidocs). Main routes are listed below in the chart: 
| Endpoint                                  | Method    | Description |
|-------------------------------------------|-----------|-------------|
|`/api/recommendations `                    | **POST**  | Creates a new recommendation |
|`/api/recommendations/<int:id>> `          | **GET**   | Read a recommendation |
|`/api/recommendations/<int:id> `           | **PUT**   | Update a recommendation |
|`/api/recommendations/<int:id> `           | **DELETE**   | Delete a recommendation |
|`/api/recommendations `                    | **GET**   | List all recommendations |
|`/api/recommendations/<int:id>/like `      | **PUT**   | Like a recommendation |
|`/api/recommendations/<int:id>/unlike `    | **PUT**   | Unlike a recommendation |
|`/api/recommendations ` | **GET** | Query recommendations |

The **GET** method with endpoint : `/api/recommendations` suports **Query** Strings with multiple constraints. 
For instance : `/api/recommendations?product_id=1` will return the list of all recommdedations for the profuct with product id equals to 1;
`/api/recommendations?product_id=1&rec_type=accessory` will return the list of all recommendatons for the accessories of the profuct with product id equals to 1.

## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters

service/                   - service python package
├── __init__.py            - package initializer
├── models.py              - module with business models
├── routes.py              - module with service routes
└── utils                  - utility package
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/              - test cases package
├── __init__.py     - package initializer
├── test_models.py  - test suite for business models
└── test_routes.py  - test suite for service routes

features/           - for bdd testing
├── environment.py
├── recs.feature
└── steps
     ├── recs_steps.py
     └── webs_steps.py
```

## Services
### Bring up development environment
To bring up the development environment, please clone this repo, change into the repo directory, and then open Visual Studio Code using the code . command. VS Code will prompt to reopen in a container. Please select it. It will take a while the first time as it builds the Docker image and creates a container from it to develop in.

```bash
git clone git@github.com:nyu-summer2022-devops/recommendations.git
cd recommendations
code .
```
### Run TDD tests
Run the tests in a ```bash``` terminal using the following command: 
```bash
make test
```
Run the test suite and report the code coverage. 

### Run BDD tests
First run the REST service in a ```bash``` terminal using the following command: 
(a web page can be opened on a local browser)
```bash
make run
```
Then start another ```bash``` terminal and run the ```behave``` test:
```bash
behave
```



## Recommendation Squad Members

Huang, Brady;
Kankanala, Meghana;
Li, Sixian;
Chiu, Pin-Yi;
Wang, Qiheng

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** taught by John Rofrano, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.

