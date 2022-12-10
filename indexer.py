"""
indexer.py
Author: Allan Balanda allan.balanda@ryerson.ca

This program is designed to help output a printable index for a GIAC exam.
The input is a plain text file with markdown inspired formatting. 

The index input should be in the format:
(Keyword) (Location) (optional comment)
Linux 1.234 An operating system
Windows 2.101 *italic* **bold** ;;blue Blue text;;

Note: asterisks in the file must be escaped! \*

Currently Lines starting with "#" are skipped (use for comments etc!)
Can use \n for a linebreak, Must escape with \\n
"""

import sys
import re
import string
import csv


### Define the Index class

class Index():
    
    def __init__(self):
        """ Instantiates the Index""" 
        
        self.columns = 0
        self.entries = []
        self.count = 0
    
    def add_entry(self, keyword, location, comment=''):
        """ Add an entry to the index """
        
        self.entries.append({"Keyword":keyword, "Location":location, "Comment":comment})
        self.count += 1


### TSV Specific Functions

def load_file_tsv(file_name):
    """ Open TSV file and create the index object """

    index = Index()

    with open(file_name, "r") as index_file:
        tsv_reader = csv.DictReader(index_file, delimiter="\t")
        
        # Determine if 3 or 2 column index
        try:
            for entry in tsv_reader:
                index.add_entry(entry['Keyword'], entry['Location'], entry['Comment'])
        except KeyError:
            print("Comment Column Not Detected")
        else:
            print("Loaded TSV File: Three Column Index Detected")
            index.columns = 3
            return index
        
    # Load 2 column index
    with open(file_name, "r") as index_file:
        tsv_reader = csv.DictReader(index_file, delimiter="\t")

        # Catch error if no headings
        try:
            for entry in tsv_reader:
                index.add_entry(entry['Keyword'], entry['Location'])
        except KeyError:
            print("Error: No Headings detected, does the TSV file have Keyword/Location/Comment titles in the first row?")
            return index
        else:
            index.columns = 2
            print("Loaded TSV File: Two Column Index Detected")
            return index

### Markdown Specific Functions

def parse_line(index, line):
    """ Searches the line for the keyword, location, comment and populates index entry"""
    # TODO throw an error message for each line parse failure!!! (print the line in question)

    # Get location first
    location_re = re.search('\d+\.\d+', line)
    location = line[location_re.start():location_re.end()]
    
    # Get remaining text
    line_text = re.split('\d+\.\d+', line)

    # Strip whitespace and eliminate empty strings
    line_text_clean = []
    for item in line_text:
        if item != '':
            line_text_clean.append(item.strip())

    # if len 'line_text_clean' is 1 then it's a two column index
    if len(line_text_clean) == 1:
        index.add_entry(line_text_clean[0], location)
    else: # 3 columns
        index.add_entry(line_text_clean[0], location, line_text_clean[1])


def parse_file(file_name):
    """ Parses the file, determine # of columns, returns populated index """
    # TODO Try catch filenotfound error

    # Catch if file might be TSV?
    tsv_file = False
    
    # Index will be a list of dicts (keys of keyword,location,comment)
    index = Index()
    # Default 2 column
    index.columns = 2
    
    # Identify where is the keyword, location, comment (skip lines with #)
    with open(file_name, "r") as fo:
        for line in fo:

            # TSV Check
            if "\t" in line:
                tsv_file = True
            
            if len(line) > 1 and not line.startswith('#'):
                parse_line(index, line.rstrip())

                # Check if any entries use 3 columns
                if index.entries[-1]['Comment'] != '':
                    index.columns = 3
                    
    if tsv_file:
        print("Warning: This might be a TSV file without Headings, did you use the right flag?\nOutput not guaranteed")
    else:
        print(f"Input was a markdown file with {index.columns} columns.")   
    return index

def strip_formatting(keyword):
    """ Strips markdown formatting and colour formatting from entries to make sort key """

    # First we have to strip colour formatting e.g. ;;blue before stripping punctuation e.g. ;;
            
    while ';;' in keyword:
        # Catch edge case: single ;; remains
        if keyword.count(';;') == 1:
            keyword = keyword.replace(';;', '', 1)
            break
        # Clear terminal ';;' (prevent indexing error)
        if keyword.endswith(';;'):
            keyword = keyword[:-2]
        # find something like ";;xxx"
        start = keyword.index(';;')
        stop = keyword.index(' ', start) + 1 # First 'space' after the ';;____' (+1 removes that space)
        # Add that color to the stripped colors list
        keyword = keyword[:start] + keyword[stop:]

    # Remove remaining markdown punctuation
    keyword = keyword.translate(str.maketrans('', '', "*"))

    return keyword


### Generic Code

def find_duplicates(index):
    """ Find entries with a duplicate keyword (great to find terms in need of more context) """

    duplicates = Index()
    duplicates.columns = index.columns
    
    # Iterate through index, compare entries i and i+1
    for i in range(0, index.count - 1): #Skip entry 1 (meta data, stop at len-1 for out of bounds)
        j = i + 1
        if index.entries[i]['Keyword'].lower() == index.entries[j]['Keyword'].lower():
            duplicates.entries.append(index.entries[i])
            if index.entries[j]['Keyword'].lower() not in duplicates.entries:
                duplicates.entries.append(index.entries[j])

    return duplicates

def search_index(index):
    """ Searches the index and returns results containing the query """

    columns = index.columns
    query = input("Search term: ").lower()

    # Determine if 3 or 2 column index
    if columns == 3:
        option_input = input("Search **K**eyword, **C**omment, or **B**oth: ").lower()

        # Just test first 3 chars, should work even with some minor typos
        if option_input == "k" or option_input[:3] == "key":
            for entry in index.entries:
                if query in entry['Keyword'].lower():
                    print(f"{entry['Keyword']} - [{entry['Location']}] - {entry['Comment']}")
        elif option_input == "c" or option_input[:3] == "com":
            for entry in index.entries:
                if query in entry['Comment'].lower():
                    print(f"{entry['Keyword']} - [{entry['Location']}] - {entry['Comment']}")
        elif option_input == "b" or option_input[:3] == "bot":
            for entry in index.entries:
                if query in entry['Keyword'].lower() or query in entry['Comment'].lower():
                    print(f"{entry['Keyword']} - [{entry['Location']}] - {entry['Comment']}")
        else:
            print("Invalid option")
            
    # Two Column Index
    elif columns == 2:
        for entry in index.entries:
            if query in entry['Keyword'].lower():
                print(f"{entry['Location']} \t- {entry['Keyword']}")

### Functions related to Creating a report

def report_count(index):
    """ Iterates through index and determines entries per book/per letter """

    book_entries = {}
    alphabet_entries = {}

    for entry in index.entries:

        # Book count
        current_book = entry['Location'][:entry['Location'].index('.')] # Get str before the decimal
        if current_book not in book_entries:
            book_entries[current_book] = 1
        else:
            book_entries[current_book] += 1

        # Letter count
        current_letter = get_first_letter(entry['Keyword']).upper()
        # handle non alphabet chars
        if not current_letter.isalpha():
            current_letter = "#"   
        if current_letter not in alphabet_entries:
            alphabet_entries[current_letter] = 1
        else:
            alphabet_entries[current_letter] += 1

    return book_entries, alphabet_entries

def create_report(index, tsv):
    """ Ouputs a report with information about the number of entries """

    # Get data
    book_entries, alphabet_entries = report_count(index)
    
    output = "<html><body><h1>Index Summary</h1>"
    # Type of Input
    if tsv:
        output += f"<b>The input was a TSV file with {index.columns} columns.</b>"
    else:
        output += f"<b>The input was a MD file with {index.columns} columns.</b>"
    # Total Length
    output += f"<p>Total Length: {index.count} entries</p>"

    # Per Book Entries
    output += "<h3>Entries per Book Number</h3>"
    ## Must print sorted book entries
    for book in sorted(book_entries.keys()):
        output += f"<b>Book {book}</b> --- {book_entries[book]}<br>"

    # Per Letter Entries
    output += "<h3>Entries per Letter</h3>"
    for letter, value in alphabet_entries.items():
        output += f"<b>{letter}</b> --- {value}<br>"

    output += "</body></html>"


    # Write the file
    write_file(output, "report.html")

### Functions for HTML Output

def format_to_html(text):
    """ Replaces markdown formatting and special chars with html equivalents """

    # First escape angle brackets
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    # Add in line breaks -- catching escaped ones
    text = text.replace('\\\\n', '!NEWLINE!')
    text = text.replace('\\n', '<br>')
    text = text.replace('!NEWLINE!', '\\n')

    #Color characters
    while ';;' in text:
        tag_index = text.index(";;") + 2
        tag_stop_index = text.index(" ", tag_index)
        color = text[tag_index:tag_stop_index]
        
        text = text.replace(";;"+color, f"<span style=\"color:{color}\">", 1)
        text = text.replace(";;", "</span>", 1)

    # Bold
    while '**' in text:
        text = text.replace("**", "<span class=\"bold\">", 1)
        text = text.replace("**", "</span>", 1)
        
    # Italic while saving '*' characters
    if not text.count('*') == 1: # Single asterisk? Might be in tsv file or not escaped
        if '\*' in text:
            text = text.replace('\*', "!AST!")
        while '*' in text:
            text = text.replace("*", "<span class=\"italic\">", 1)
            text = text.replace("*", "</span>", 1)
        if '!AST!' in text:
            text = text.replace('!AST!', '*')
            
    return text

def create_html_head():
    """ Creates start of html file """

    html = """<html><body><table>
                <head>
                <style>

                :root {
                    --border-radius: 5px;
                    --box-shadow: 2px 2px 10px;
                    --font-family: Calibri, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
                    --justify-normal: left;
                    --line-height: 1.5;
                }

                body {
                    background: var(--color-bg);
                    color: var(--color-text);
                    font-family: var(--font-family);
                    line-height: var(--line-height);
                    margin: 0;
                    padding: 0;
                }

                .bold {
                    font-weight: bold;
                }
                .italic {
                    font-style: italic;
                }
                """
    return html

def add_print_css(columns):
    """ Adds the proper stylesheet depending on the number of columns """

    print_css = ""

    if columns == 3:
        print_css += """             
                @media print {
                    @page {
                      margin: 1.5cm;   
                    }
                    section.table > div:nth-of-type(odd) {
                        background: #e0e0e0;
                    }
                    .table {
                        page-break-after: always;
                        width:20cm;
                    }
                    div.row > div {
                      display: inline-block;  
                      overflow-x: auto;
                      padding: 0;
                      vertical-align: top;
                    }
                    div.row {
                      display: block;
                    }
                    h1 {
                        page-break-before: always;
                        margin-left: 10em;
                    }
                    .thead {
                        text-align: center;
                        font-weight: bold;
                        }
                    .keyword {
                        width: 30%;
                        margin-left: 0.1cm;
                        /*margin: 0.1cm; /* Can be removed, good for readability when using colour output */
                    }
                    .location {
                        width: 10%;
                        text-align: center;
                    }
                    .comment {
                        width:50%;
                        margin-left: 0.5cm;
                    }
                }
                """
    elif columns == 2:
        print_css += """             
                @media print {
                    @page {
                      margin: 0.5cm;   
                    }
                    section.table {
                        align-items: center;
                        width: 20cm;
                    }
                    section.table > div:nth-of-type(odd) {
                        background: #e0e0e0;
                    }
                    .table {
                        page-break-after: always;
                    }
                    div.row > div {
                      display: inline-block;  
                      overflow-x: auto;
                      padding: 0;
                      margin-right: 0.25cm;
                      vertical-align: top;
                    }
                    div.row {
                      display: block;
                      width:100%;
                    }
                    h1 {
                        page-break-before: always;
                        margin-left: 10em;
                    }
                    .thead {
                        text-align: center;
                        font-weight: bold;
                        }
                    .keyword {
                        margin-left: 0.5cm;
                    }
                    .location {
                        width: 15%;
                        text-align: center;
                    }
                }"""
    return print_css

def add_print_css2():
    """ Holds the rest of the non specific css """

    return """
                section.table > div:nth-of-type(odd) {
                    background: #e0e0e0;
                }
                .alphabet
                {
                    text-align: center;
                    page-break-before:auto;
                }
                .table {
                    display: table;
                    border-spacing: 1px;
                }
                .row {
                    display: table-row;
                }
                .row > div {
                    display: table-cell;
                    padding: 4px; 
                }
                .thead {
                    text-align: center;
                    font-weight: bold;
                }
                .location {
                    text-align: center;
                }

                .colour1 {
                background: #b7e1cd;
                }
                .colour2 {
                background: #e1c8b7;
                }
                .colour3 {
                background: #b7c5e1;
                }
                .colour4 {
                background: #e0e1b7;

                }
                .colour5 {
                background: #e1bcb7;

                }
                .colour6 {
                background: #b7dde1
                }
                

                </style>
                </head>
                <section class="table">"""

def pick_colour(location):
    """ Returns the proper colour code depending on which book the location references """

    # Assume location in the form n.nnn
    book = location.split('.')[0]

    return f" colour{book}"

def create_html_line(entry, columns, book_colours):
    """ Converts each individual index entry to html """

    if book_colours:
        colour = pick_colour(entry['Location'])
    else:
        colour = ''

    entry['Keyword'] = format_to_html(entry['Keyword'])
    if columns == 2:
        return f"<div class=\"row\"><div class=\"location{colour}\">{entry['Location']}</div><div class=\"keyword\">{entry['Keyword']}</div></div>\n\n"
    if columns == 3:
        entry['Comment'] = format_to_html(entry['Comment'])
        return f"<div class=\"row\"><div class=\"keyword\">{entry['Keyword']}</div><div class=\"location{colour}\">{entry['Location']}</div><div class=\"comment\">{entry['Comment']}</div></div>\n\n"

def get_first_letter(keyword):
    """ Get the first character that is actually part of the keyword (i.e. not punctuation!) """

    char_i = 0
    while char_i < len(keyword):
        if keyword[char_i] == ';':
            char_i = keyword.index(' ', char_i) + 1 # First space after this char
            continue
        elif keyword[char_i] == "*":
            char_i += 1
            continue
        else:
            return keyword[char_i]
        

def create_html(index, book_colours, columns, page_breaks, header):
    """ Creates the HTML file """

    html_file = create_html_head()
    html_file += add_print_css(columns)
    html_file += add_print_css2()
    
    # Add title if desired
    if header:
        html_file += f"<h1>{header}</h1>"

    # Add each index entry, checking for new start letters
    current_char = ''
    non_alpha_char = False
    for entry in index.entries:
        test_letter = get_first_letter(entry['Keyword']).upper()

        # We haven't seen a non alphabetical character
        if not non_alpha_char and not test_letter.isalpha(): 
            non_alpha_char = True
            # Page Breaks
            if page_breaks:
                if columns == 2:
                    html_file += f"""<div class=\"row\"><div class=\"alphabet\"><h1>#./!</h1></div><div></div></div>"""
                else:
                    html_file += f"""<div class=\"row\"><div></div><div class=\"alphabet\"><h1>#./!</h1></div><div></div></div>"""
            else:
                if columns == 2:
                    html_file += f"""<div class=\"row\"><div class=\"alphabet\"><h1>#./!</h1></div><div></div></div>"""
                else:
                    html_file += f"""<div class=\"row\"><div></div><div class=\"alphabet\"><h1>#./!</h1></div><div></div></div>"""

        if test_letter.isalpha() and not non_alpha_char: # Didn't have non alpha char
            non_alpha_char = True # Don't go through this path second time
            if test_letter != current_char:
                current_char = test_letter

                if columns == 2:
                    html_file += f"""<div class=\"row\"><div class=\"alphabet\"><h1>{current_char}</h1></div><div></div></div>"""
                else:
                    html_file += f"""<div class=\"row\"><div></div><div class=\"alphabet\"><h1>{current_char}</h1></div><div></div></div>"""


        # The rest of the Alphabetical entries 
        elif test_letter.isalpha(): 
            if test_letter != current_char:
                current_char = test_letter

                # Page Breaks
                if page_breaks:
                    if columns == 2:
                        html_file += f"""</section><section class="table"><div class=\"row\"><div class=\"alphabet\"><h1>{current_char}</h1></div><div></div></div>"""
                    else:
                        html_file += f"""</section><section class="table"><div class=\"row\"><div></div><div class=\"alphabet\"><h1>{current_char}</h1></div><div></div></div>"""
                else:
                    if columns == 2:
                        html_file += f"""<div class=\"row\"><div class=\"alphabet\"><h1>{current_char}</h1></div><div></div></div>"""
                    else:
                        html_file += f"""<div class=\"row\"><div></div><div class=\"alphabet\"><h1>{current_char}</h1></div><div></div></div>"""
                    
        html_file += create_html_line(entry, columns, book_colours)

    return html_file

def print_html(index, book_colours, file_name, page_breaks, header=''):
    """ Outputs a HTML File """

    columns = index.columns
    html_file = ""
    html_file += create_html(index, book_colours, columns, page_breaks, header)
    html_file += "</section></body></html>"

    #Write the file
    write_file(html_file, file_name)
    

def write_file(index_html, file_name):
    """ Writes the file to disk """

    with open(file_name, "w") as fo_write:
        fo_write.write(index_html)
    print(f"{file_name[:file_name.index('.')].title()} written as {file_name}")

def start_program(arg_list):
    """ Calls appropriate functions based on cli args """

    book_colours = False
    tsv = False
    duplicates = False
    report = False
    search = False
    page_breaks = False
    header = ''
    
    # Check for header flag and get the title
    if '-h' in arg_list[:-1]:
        header = ' '.join(arg_list[arg_list.index('-h')+1:-1])
        
    # Check args, -h flag must come last
    flags = ''.join(arg_list[:arg_list.index('-h')])
    if '-' in flags:
        if 'c' in flags:
            book_colours = True
        if 't' in flags:
            tsv = True
        if 'd' in flags:
            duplicates = True
        if 'r' in flags:
            report = True
        if 's' in flags:
            search = True
        if 'p' in flags:
            page_breaks = True

    ### Load the file into memory        
    # Markdown File
    if not tsv:
        # Failsafe to check if user forgot TSV flag
        try:
            # Load index from file and sort it
            index = parse_file(arg_list[-1])
        except AttributeError:
            tsv = True
            print("Warning: -t TSV flag not used but input appears to be TSV file")
        else:
            # Sort key is 'Keyword' (need to remove formatting and color formatting)
            index.entries.sort(key=lambda dict_entry: strip_formatting(dict_entry['Keyword'].lower()))

    # TSV File
    if tsv:
        index = load_file_tsv(arg_list[-1])
        # If len(index)==0 then error in loading TSV file
        if len(index.entries) == 0:
            return True
        index.entries.sort(key=lambda dict_entry: dict_entry['Keyword'].lower())

    ### File in memory as 'index' and is sorted

    # Run search if requested
    if search:
        search_index(index)
        return True
    # Output Desired results
    if report:
        create_report(index, tsv)
    if duplicates:
        duplicates = find_duplicates(index)
        print_html(duplicates, book_colours, "duplicates.html", False)

    # Ouput Index to HTML
    print_html(index, book_colours, "index.html", page_breaks, header)
    

if __name__ == "__main__":

    # Usage python3 indexer_md.py <flags> <-h "title"> <filename>
    
    if len(sys.argv) > 1:
        start_program(sys.argv[1:])
    else:
        print("Index Helper script\nUsage: $ python3 indexer.py <flags> <-h \"page title\"> <filename>\nFlags:")
        print("\t-c\t colour output for book locations")
        print("\t-t\t Tab separated values file import")
        print("\t-d\t Show duplicate keyword entries")
        print("\t-h\t \"text\" Add a title at the start of the page")
        print("\t-r\t Generate a report about your index (entries per book/per letter)")
        print("\t-p\t Have page breaks at each letter")
        print("\t-s\t Search your index, do not output any file")

