# GIAC Indexer

Written to help create indexes for GIAC certification exams. I wanted to have a tool to create a printable version of the index I made using spreadsheet software.  

This script takes an unsorted TSV (tab separated values) file and outputs a sorted, HTML page that can be viewed in a browser and printed.


## Usage
The python script requires a "index.tsv" file (e.g. exported from Microsoft Excel or Google Sheets) in the same folder as the script.  
The script works with **two column** (Location and Keyword) or **three column** indexes (Keyword, Location, Comment). The first row of the spreadsheet should have these titles.

The script has a few options when run.
* Display the index as is  
* Display a sorted index  
* Search for a term in the Keyword or Comment Fields (or Both!)  
* Display duplicate Keywords (great for finding entries in need of more context)  
* Output an HTML file of the sorted index (which can then be converted to PDF or printed directly!) 
    * The script can add a background colour to the location based on the book (as of right now colours can be altered by modifying the <style> in the HTML file) 
    * Per book location colours assume the location is in the format n.nnn (book#.page#)
    


