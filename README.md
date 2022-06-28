# Recommendations Microservice for a Commerce website

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

This system is designed for an **eCommerce store**.

## Overview

The recommendations resource is a representation a product recommendation based on another product. In essence it is just a relationship between two products that "go
together" (e.g., radio and batteries, printers and ink, shirts and pants, etc.). It could also recommend based on what other customers have purchased like "customers who bought item A usually buy item B". Recommendations should have a recommendation type like cross-sell, up- sell, accessory, etc. This way a product page could request all of the up-sells for a product. (Hint: an up-sell is a more full featured and expensive product that you recommend instead of the one they initially want to buy, cross-sells are other items just like this one with similar features and price.)

The `/service` folder contains `models.py` file for the model and a `routes.py` file for the service. The `/tests` folder has test cases for testing the model and the service separately.

## Attributes

id : non-information bearing key

product_id : id of the source product

product_name : name of the source product

rec_id : id of the recommended product

rec_name : name of the recommended product

rec_type : the type of recommendation (CROSS_SELL = 0, UP_SELL = 1, ACCESSORY = 2, BUY_WITH = 3)

## Functionalities

### 1. Create a new recommendation

POST: `/recommendations`

fields: product_id, product_name, rec_id, rec_name, rec_type

### 2. Read a recommendation

GET: `/recommendations/<int:id>`

fields: product_id, product_name, rec_id, rec_name, rec_type

### 3. Update a recommendation

PUT: `/recommendations/<int:id>`

### 4. Delete a recommendation

DELETE: `/recommendations/<int:id>`

### 5. List recommendations

GET: `/recommendations`

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
```

## Recommendation Squad Members
Huang, Brady;
Kankanala, Meghana;
Li, Sixian;
Chiu, Pin-Yi;
Wang, Qiheng

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** taught by John Rofrano, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
