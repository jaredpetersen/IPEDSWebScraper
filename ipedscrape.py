from bs4 import BeautifulSoup
import urllib2
import string
from time import sleep

# Base URL to be scraped
base_url = 'http://nces.ed.gov/ipeds/glossary/?charindex='

# File to be written to
html_file = open('wordpressipedtable.html', 'w')

# List of pages that have data on them
successful_pages = []

# List of strings to write to the file
# Used so the link navigation can be added at the top after all of the pages have been checked out
write_list = []

def make_soup(page):
     """Set up Beautiful Soup for scraping

        Keyword argument:
        page -- the IPED page character (ex. "A", "B", etc.)
     """
     html = urllib2.urlopen(base_url + page).read()
     return BeautifulSoup(html, 'lxml')

def get_data(page, page_header):
     """Get the terms and defintions from the table at a specific page

        Keyword arguments:
        page -- the IPED page character (ex. "A", "B", etc.)
        page_header -- the header for the page used in the table html
     """
     soup = make_soup(page)
     # Check to make sure the page isn't empty
     if soup.find('table', 'ipdGlsSearch') is None:

          # Mark the page as having data
          successful_pages.append(page_header)

          # Create the HTML table
          write_list.append('<h1 id="' + page_header + '" style="margin-bottom: 0px;">' + page_header + '</h1>\n<table class="table_border1px" width="100%" cellspacing="0" cellpadding="5">\n<tbody>\n<tr bgcolor="maroon">\n<th class="table_head_2_reverse" style="color: white" align="left">Term</th>\n<th class="table_head_2_reverse" style="color: white" align="left">Definition</th>\n</tr>\n')

          # Used to color the table rows
          counter = 0

          # [1:] used to skip the header row
          for tr in soup.find_all('tr')[1:]:
               tds = tr.find_all('td')
               write_data(tds[0].text.encode('utf-8'), tds[1].text.encode('utf-8'), counter)
               counter += 1

          # Close the table
          write_list.append('</tbody>\n</table>\n<br />\n')

def write_data(term, definition, counter):
     """Write the input terms to the write_list with the proper row coloration

        Keyword arguments:
        term -- the IPED term
        defintion -- the definition of the IPED term
        counter -- the current row number of the table, used to alternate row colors
     """
     if counter % 2:
          # Use colored rows
          write_list.append('<tr bgcolor="#efefef">\n<td>' + term + '</td>\n<td>' + definition + '</td>\n</tr>\n')
     else:
          # Use white (default) rows
          write_list.append('<tr>\n<td>' + term + '</td>\n<td>' + definition + '</td>\n</tr>\n')

def print_title(title_text):
     """Print inputted text between a series of dashes to mark important text

        Keyword argument:
        title_text -- the text to be printed in a title format
     """
     print "\n-----------------------------------------------------"
     print title_text
     print "-----------------------------------------------------\n"

if __name__ == '__main__':
     """Main function, sets everything in the program up"""
     # Check all of the alphabet web pages
     url_collection = list(string.ascii_uppercase)
     # And check the one number web page
     url_collection.append('0')

     # Print the opening program statement
     print_title("Initiating IPED Glossary Web Scrape")

     # Loop over all of the IPED pages
     for page in url_collection:
          
          # Create page header but change the HTML header for the 0-9 page
          page_header = ' '
          if page == '0':
               page_header = '0-9'
          else:
               page_header = page

          # Get the IPED data and add it to the file
          get_data(page, page_header)
          
          # Let the user know what's going on
          print "Processing IPED Glossary Pages - Page " + page_header + " Complete"

     # Add a top table navigation bar heading tag
     # Not appending this to the write_list so that it can go on top   
     html_file.write('<h2>')
     
     # Loop over the successful pages and create a link to each
     for page in successful_pages:
          html_file.write('<a href="#' + page + '">' + page + '</a> ')

     # Finish writing the navigation bar to the file
     html_file.write('</h2>\n<br />\n')
     # Append the link to top to the write_list
     write_list.append('<br /><a href="#top"></a><br /><br />')
     # Write the data tables to the file
     html_file.writelines(write_list)

     # Close the file     
     html_file.close()
     print_title("IPED Glossary Web Scrape Complete")
