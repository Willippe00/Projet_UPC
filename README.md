Python Project: Barcode Lookup Automation on UPCBarcodeLookup
Project Overview
This project was undertaken during my personal time with the primary goal of automating a recurring task at work: the search for barcodes on the UPCBarcodeLookup website.

Features
Automated Navigation on UPCBarcodeLookup: Uses Selenium for automated web page navigation and interaction to extract relevant data.

Data Storage: The fetched information is subsequently stored in a PostgreSQL database for efficient management and easy retrieval.

Image Processing: The project includes image processing capabilities to prepare data for analysis.

Dictionary Comparison: To process the results, a dictionary comparison system has been implemented to evaluate matches.

Final Report: Upon processing, an automated report is generated in Excel format. This report displays match percentages based on different metrics.

Prerequisites
Python 3.x
Python Modules: selenium, psycopg2, openpyxl, PIL (or Pillow), among others.
PostgreSQL set up and configured
Compatible driver for Selenium (e.g., ChromeDriver for Chrome)
Installation
Clone this repository to your local environment.
Install the required Python dependencies using pip install -r requirements.txt (ensure you have a virtual environment activated if needed).
Set up your PostgreSQL database and update the connection information in the project's configuration file.
Ensure the driver for Selenium is accessible in your PATH or specify its location within the code.
Usage
Run the main script: python main.py.
Follow on-screen instructions if any.
Once processing completes, check the generated Excel report in the specified output directory.
Contributions and Support
Given that this project was developed during my personal time, I'm open to any contributions or suggestions. Please feel free to open an issue or a pull request.
