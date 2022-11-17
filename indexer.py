"""
indexer.py
Author: Allan Balanda allan.balanda@ryerson.ca

This program takes a GIAC index in tsv format (e.g. exported from google sheets or excel)
and can be used to generated a sorted file ready to print (with page breaks between letters)
"""

import csv

def start_program():
    """ Loads the tsv file and calls prompt function """
    
    index_tsv = load_file()
    user_prompt(index_tsv)


def load_file():
    """ Open TSV file and create a list where each entry in a dict """

    index_tsv = []

    with open("index.tsv", "r") as index_file:
        tsv_reader = csv.DictReader(index_file, delimiter="\t")
        for entry in tsv_reader:
            index_tsv.append({'Keyword':entry['Keyword'], 'Location':entry['Location'], 'Comment':entry['Comment']})

    return index_tsv
        
        
def user_prompt(index_tsv):
    """ Get input from user for what the program is to do """

    
    options = ['show', 'sort', 'search', 'duplicates', 'output']
    user_input = ""
    
    while user_input != "exit":
        print("\n\n\t\t===GIAC INDEX HELPER SCRIPT===")
        print("Please Choose an Option: show sort search duplicates output ('exit' to quit)")
        user_input = input("Enter Choice: ").lower()
        if user_input == "exit":
            break
        elif user_input in options:
            option_handler(user_input, index_tsv)
        else:
            print("Please enter a valid option")

def option_handler(user_input, index_tsv):
    """ Helper function to call appropriate function based on user input """

    if user_input == "show":
        show_index(index_tsv)
    elif user_input == "sort":
        sort_index(index_tsv, display=True)
    elif user_input == "search":
        search_index(index_tsv)
    elif user_input == "duplicates":
        find_duplicates(index_tsv)
    elif user_input == "output":
        output_index(index_tsv)

def show_index(index_tsv):
    """ Displays the index as is """

    for entry in index_tsv:
        print(f"{entry['Keyword']} - [{entry['Location']}] - {entry['Comment']}")

def sort_index(index_tsv, display=False):
    """ Sorts the index by keyword and optionally prints to screen """

    # Sort by key, use lambda to return the 'keyword' element of each dict entry
    index_tsv.sort(key=lambda dict_entry: dict_entry['Keyword'].lower())

    if display:
        show_index(index_tsv)
        
def search_index(index_tsv):
    """ Searches the index and returns results containing the query """

    query = input("Search term: ").lower()
    option_input = input("Search **K**eyword, **C**omment, or **B**oth: ").lower()

    # Just test first 3 chars, should work even with some minor typos
    if option_input == "k" or option_input[:3] == "key":
        for entry in index_tsv:
            if query in entry['Keyword'].lower():
                print(f"{entry['Keyword']} - [{entry['Location']}] - {entry['Comment']}")
    elif option_input == "c" or option_input[:3] == "com":
        for entry in index_tsv:
            if query in entry['Comment'].lower():
                print(f"{entry['Keyword']} - [{entry['Location']}] - {entry['Comment']}")
    elif option_input == "b" or option_input[:3] == "bot":
        for entry in index_tsv:
            if query in entry['Keyword'].lower() or query in entry['Comment'].lower():
                print(f"{entry['Keyword']} - [{entry['Location']}] - {entry['Comment']}")
    else:
        print("Invalid option")

def find_duplicates(index_tsv):
    """ Find entries with a duplicate keyword (great for identifying terms in need of more context """

    # First sort the index
    sort_index(index_tsv)

    duplicates = [] 
    # Iterate through index, if entries i, i+1 equal, append them if not already in duplicates
    # Must stop iteration at len-1 to prevent out of bounds
    for i in range(len(index_tsv) - 1):
        j = i + 1
        if index_tsv[i]['Keyword'].lower() == index_tsv[j]['Keyword'].lower():
            if index_tsv[i]['Keyword'] not in duplicates:
                duplicates.append(index_tsv[i])
            if index_tsv[j]['Keyword'] not in duplicates:
                duplicates.append(index_tsv[j])
        else: # They don't match so print 'duplicates' and clear the list

            for entry in duplicates:
                print(f"{entry['Keyword']} - [{entry['Location']}] - {entry['Comment']}")

            duplicates = []

def alphabetical_breaks(index_tsv):
    """ Inserts alphabetical breaks in a sorted index """

    sort_index(index_tsv)

    # If the first char of the next entry is not the same, insert a string "Letter: <<next char>>"
    # 'i' is current index; 'j' is next index in the list
    stop_index = len(index_tsv) - 1
    i = 0
    while i < stop_index:
        j = i + 1

        # Check that the keyword starts with a letter (ignore numbers, '.' etc.)
        if not index_tsv[i]['Keyword'][0].isalpha():
            print(index_tsv[i]['Keyword'])
            i += 1
            continue

        # if next letter different, insert a row, then increment i to skip over the new empty row!
        if index_tsv[i]['Keyword'][0].lower() != index_tsv[j]['Keyword'][0].lower():
                index_tsv.insert(j, f"Letter {index_tsv[j]['Keyword'].upper()}")
                i += 1
                stop_index += 1 # List is now longer, add another iteration to for loop

        # Increment counter
        i += 1
    
    show_index(index_tsv)

def write_file(index_html):
    """ Writes the file to disk """

    with open("index.html", "w") as fo_write:
        fo_write.write(index_html)
    print("Index Written as index.html")

def escape_ang_brackets(entry):
    """ For HTML Export, replace < > with &lt; and &gt; """

    entry['Keyword'] = entry['Keyword'].replace('<', '&lt;')
    entry['Keyword'] = entry['Keyword'].replace('>', '&gt;')
    entry['Comment'] = entry['Comment'].replace('<', '&lt;')
    entry['Comment'] = entry['Comment'].replace('>', '&gt;')
        

def output_index(index_tsv):
    """ Outputs the index in HTML format """

    # Prep the file first
    sort_index(index_tsv)
    
    index_html = """<html><body><table>
                <head>
                <style>

                :root {
                    --border-radius: 5px;
                    --box-shadow: 2px 2px 10px;
                    --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
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
                
                @media print {
                    @page {
                      margin: 1.5cm;   
                    }
                    section.table > div:nth-of-type(odd) {
                        background: #e0e0e0;
                    }
                    div.row > div {
                      display: inline-block;  
                      margin: 0.1cm;
                      overflow-x: auto;
                      padding: 0;
                    }
                    div.row {
                      display: block;
                    }
                    .thead {
                        text-align: center;
                        font-weight: bold;
                    }
                    .keyword {
                        width: 30%;
                    }
                    .location {
                        width: 10%;
                        text-align: center;
                    }
                    .comment {
                        width:50%;
                    }
                }

                
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
                    border-spacing: 2px;
                }
                .row {
                    display: table-row;
                }
                .row > div {
                    display: table-cell;
                    padding: 2px;
                }
                .thead {
                    text-align: center;
                    font-weight: bold;
                }
                .location {
                    text-align: center;
                }

                </style>
                </head>
                <section class="table">
                <div class="row">
                <div class="keyword thead">Keyword</div><div class="location thead">Location</div><div class="thead">Comment</div>
                </div>
                """

    # Iterate through index, adding each row
    # Check for new letters, add Letter breaks!
    current_char = ''
    for entry in index_tsv:

        # Change angle brackets for HTML codes
        escape_ang_brackets(entry)

        # Check if new Letter
        if entry['Keyword'][0].upper().isalpha():
            if entry['Keyword'][0].upper() != current_char:
                current_char = entry['Keyword'][0].upper()
                index_html += f"<div class=\"row\"><div></div><div class=\"alphabet\"><h1>{current_char}</h1></div><div></div></div>"
        
        index_html += f"<div class=\"row\"><div class=\"keyword\">{entry['Keyword']}</div><div class=\"location\">{entry['Location']}</div><div class=\"comment\">{entry['Comment']}</div></div>"

    # Finalise the html page and write it
    index_html += "</section></body></html>"
    write_file(index_html)
    

if __name__ == "__main__":

    start_program()
