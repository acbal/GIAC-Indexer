# GIAC Indexer

Written to help create printable indexes for GIAC certification exams. This script takes an unsorted TSV or markdown file file and outputs a sorted HTML page that can be viewed in a browser (or printed/printed to PDF).

This script can run on two types of input files: **Tab Separated Values** or **markdown inspired**. TSV files can be exported from spreadsheet software such as Microsoft Excel or Google Sheets.

## TSV Files (Tab Separated Values)

TSV files can be **2** or **3** columns. The first row must contain column titles **Keyword** and **Location** (format *n.nnn* e.g. *1.101*) for two column indexes. Three column indexes can also have the field **Comment**.

## Markdown Files

Markdown files use a subset of markdown but with the addition of color! (e.g. for separating red team vs blue team). Acceptable formatting includes: `*italic*`, `**bold**`, and `;;color Text goes here;;` where `color` is the name of the color you desire. Asterisks (\*) must be escaped as so `\*`. Newlines can be included as `\n`. Newlines can be escaped as `\\n`.

The markdown can also be either two columns or three colums. Each line denotes a new entry:

### Two Column Markdown

> Linux 1.103  
> Windows 1.105  

or 

> 1.103 Linux  
> 1.105 Windows Operating system  

### Three column Markdown

> Linux 1.103 A free operating system  
> Windows 1.105 Dominant desktop OS  

# Usage

```$ python3 indexer.py <flags> <-h "Optional title"> <filename>```

By Default the script takes a markdown file and outputs an HTML based index. However, optional flags can be used to modify functionality:

## Flags

`-c` add a background colour to the location based on the book (as of right now colours can be altered by modifying the <style> in the HTML file)  
`-t` Allow the input of a TSV File  
`-d` Output a file with duplicate keywords (great for identifying entries in need of more context)  
`-r` Output a report file showing how many entries per book and per letter of the alphabet  
`-p` When printing the index, force page breaks after each letter.  
`-s` Search: Search you index and print results to the terminal (This flag can only be combined with -t for TSV input)  
`-h` Add an optional title to the output file, this argument must come last.  

Flags can be combined, for example:

```python3 indexer.py -tcdr index.tsv``` The above will take a TSV file and output a report, a list of duplicates, and the output index will have color coded locations.

```python3 indexer.py -p -r -d index.md``` The above will take a markdown file and output a report, a list of duplicates, and the output index will not be color coded but will have page breaks after each letter.
    


