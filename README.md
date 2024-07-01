First object was to extract data from each url given in input file and save it with their respective url_id name
For extracting data from the url  Beautifulsoup is used for each file. Extracted the title and content of the article using their html tag and classes and saved all the files with their respective url_id in the article folder.
Code for this is in “data_extract.py” file and all the extracted articles are in “Article” folder

For the second objective text analysis 
As instructed all the data are found for each article and after finding the data, merge all the data with input.xlsx file on url_id. Then save it into an “output.xlsx” file. Code is in the “text_analysis.py” file

The libraries that are used are
Request, 
pandas, 
os, 
beautifulsoup (bs4), 
Openpyxl
