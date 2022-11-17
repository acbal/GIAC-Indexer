# GIAC Indexer

Written to help create indexes for GIAC certification exams. I wanted to have a tool to create a printable version of the index I made using spreadsheet software. 

The python script requires a "index.tsv" file (Tab Separated Values) spreadsheet (e.g. exported from Microsoft Excel or Google Sheets). The Index should have three columns with field names **Keyword**, **Location**, **Comment**.  

The script has a few options when run.
* Display the index as is  
* Display a sorted index  
* Search for a term in the Keyword or Comment Fields  
* Display duplicate Keywords (great for finding entries in need of more context)  
* Output an HTML file of the sorted index (which can then be converted to PDF or printed directly!)

TODO
- [ ] Create an option to have alphabetical page breaks (i.e. each letter starts on its own page)
- [ ] Option to have no alphabetical breaks 


