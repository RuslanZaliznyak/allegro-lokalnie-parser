# Program Description

## Overview

This program is designed to scrape data from the website "https://allegrolokalnie.pl" and store the extracted information in a CSV file. It uses web scraping techniques to retrieve product details such as title, price, URL, and offer type from the website's search results.

## Features

- Web scraping: The program utilizes the BeautifulSoup library to parse the HTML content of the website and extract relevant data.

- Pagination: It automatically handles pagination to retrieve data from multiple pages of search results.

- Data Processing: The program processes the scraped data and cleans it by removing unnecessary characters and whitespace.

- CSV Export: The extracted data is saved in a CSV (Comma-Separated Values) file format, allowing easy import and analysis in spreadsheet applications.

## Usage

To use the program, follow these steps:

1. Ensure you have Python 3.x installed on your system.

2. Install the required packages by running the following command:

`pip install requests bs4 typing`


3. Clone or download the program files from the GitHub repository.

4. Open the command line or terminal and navigate to the directory where the program files are located.

5. Modify the `item_name` and `file_name` variables in the `Parser` class constructor to specify the desired item name and output file name.

6. Run the program by executing the following command:

`python your_code_file.py`


7. The program will scrape the website, retrieve the data, and save it to a CSV file with the specified file name.

## Contribution

Contributions to the program are welcome. If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request on the GitHub repository.

## License

This program is licensed under the [MIT License](LICENSE).

