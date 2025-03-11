# HBNB Project - Part 3

## Description
This is the third part of the HBNB (Holberton Airbnb Clone) project. The HBNB project is a complete web application that mimics the core functionality of Airbnb. This phase builds upon the previous components to create a more robust application.

## Features
- RESTful API for CRUD operations on all models
- Web dynamic content using JavaScript
- User authentication
- Database storage
- Front-end integration with back-end API

## Installation

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- Node.js (for front-end dependencies)

### Setup
```bash
# Clone the repository
git clone https://github.com/mansiluca/holbertonschool-hbnb.git

# Navigate to project directory
cd holbertonschool-hbnb/part3

# Install Python dependencies
pip install -r requirements.txt

# Setup database
mysql -u root -p < setup_mysql_dev.sql
```

## Usage
```bash
# Start the Flask API server
python3 -m api.v1.app

# In a separate terminal, serve the front-end (if applicable)
python3 -m web_dynamic.app
```

## Directory Structure
```
part3/
├── api/               # RESTful API implementation
├── models/            # Data models
├── tests/             # Unit tests
├── web_dynamic/       # Dynamic web content
├── README.md          # This file
└── requirements.txt   # Python dependencies
```

## Testing
```bash
# Run all tests
python3 -m unittest discover tests
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Authors
- Mansi Luca - [GitHub Profile](https://github.com/mansiluca)
- Jungling Jonas - [GitHub Profile](https://github.com/Jonas-Jungling)