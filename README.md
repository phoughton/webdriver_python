# webdriver_python a simple Python Webdriver example.

This is a simple example of how to use python to grab some information from a medical data website.
The data is a subset of that grabbed by this [web-scraping script](https://github.com/phoughton/scraping). 

## The Specification

This code was actually assigned to me by a potential employer, a while ago.

The script uses Python and Webdriver to grab a subset of data from a website listing medical company data.

The Specification I was provided was:
```
Using Selenium webdriver, controlled by a language of your choice;

Navigate to https://www.medicines.org.uk/emc/browse-companies
For each page of the company browser
Capture details about the first, the third and the last company on the page.  The details must include the company name, the logo and all contact information.  Do not capture the information about the drugs related to that company
Store the logo as an image in a folder
Add the company details to an internal data structure.  Include the filename of the image file
Output the internal data structure of the company details as a Json file and also as an XML file

Send in a ZIP file containing the images, the json file and the XML file, along with all the source code you created.
```

## Notes:
- The script expects Chrome Driver (for WebDriver) to be in the path.
- The script expects the Selenium package to be installed.

