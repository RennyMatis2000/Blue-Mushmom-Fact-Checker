# A function for opening a web document given its URL
from urllib.request import urlopen

# Import the function for opening online documents and the class for creating requests
from urllib.request import urlopen, Request

# Import an exception sometimes raised when a web server denies access to a document, or a web document cannot be downloaded due to some communication error
from urllib.error import HTTPError, URLError

# Some standard Tkinter functions
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

# Functions for finding occurrences of a pattern defined via a regular expression.  
from re import *

# A function for displaying a web document in the host operating system's default web browser 
from webbrowser import open as urldisplay

# All the standard SQLite database functions
from sqlite3 import *

# A function to download and save a web document.
def download(url = 'http://www.wikipedia.org/',
             target_filename = 'downloaded_document',
             filename_extension = 'html',
             save_file = True,
             char_set = 'UTF-8',
             incognito = False):

    # Open the web document for reading
    request = url
    web_page = urlopen(request)
    
    try:
        request = url
        web_page = urlopen(request)
    except ValueError as message: 
        return None
    except HTTPError as message: 
        return None
    except URLError as message: 
        return None
    except Exception as message: 
        return None
    
    try:
        web_page_contents = web_page.read().decode(char_set)
    except UnicodeDecodeError as message:
        return None
    except Exception as message:
        return None

    # Optionally write the contents to a local text file
    # (silently overwriting the file if it already exists!)
    if save_file:
        try:
            text_file = open(f'{target_filename}.{filename_extension}', 'w', encoding = char_set)
            text_file.write(web_page_contents)
            text_file.close()
        except Exception as message:
            print(f"\nUnable to write to file '{target_filename}'")
            print(f"Error message was: {message}\n")

    # Return the downloaded document to the caller
    return web_page_contents

main_window = Tk()

# Develop the back-end

# Import a necessary function to ensure all headlines are read in human english text
from html import unescape

# Declare some necessary variables 
selected_source = IntVar()
source_name = ('[Please select a data source]')
the_age_url = ('https://www.theage.com.au/breaking-news')
the_sydney_morning_herald_url = ('https://www.smh.com.au/breaking-news')
abc_news_url = ('https://www.abc.net.au/news/justin')
headline_selected = ('No headline has been selected yet')
dateline_selected = ('No dateline has been selected yet')

# Create the function to save information about source, headline, dateline, and rating into the database
def save_reliability_information(news_source, headline, dateline, rating):
        # Make a connection to the reliability ratings database
        connection = connect(database = "reliability_ratings.db")

        # Get a cursor on the database
        reliability_ratings = connection.cursor()                 

        # Construct the SQLite insert statement to insert values into the table 'ratings' - the values have not been specified, as this causes syntax errors when the headline includes apostrophes due to being unescaped
        sql = f"INSERT INTO ratings (news_source, headline, dateline, rating) VALUES (?, ?, ?, ?)"

        # Execute the query, this includes the source, headline, dateline, and rating values that will be input
        reliability_ratings.execute(sql, (news_source, headline, dateline, rating))

        # Get the count of the number of rows inserted
        rows_inserted = reliability_ratings.rowcount

        # Commit the changes to the database
        connection.commit()

        # Close the cursor and connection
        reliability_ratings.close()
        connection.close()


# Function to indicate which source has been selected
def source_button_pressed():
    global source_name
    if selected_source.get() == 1:
        source_name = ('The Age')
    elif selected_source.get() == 2:
        source_name = ('The Sydney Morning Herald')
    elif selected_source.get() == 3:
        source_name = ('ABC News')
    system_status_description.config(state = 'normal')  
    system_status_description.delete('0.0', 'end')    
    system_status_description.insert('0.0', (f'{source_name} has been selected as a source.'))
    system_status_description.config(state = 'disabled', fg = 'Black')
        
# Function to indicate the show details button has been pressed, including selected source
def show_details_button_pressed():
        global source_name
        system_status_description.config(state = 'normal')  
        system_status_description.delete('0.0', 'end')    
        system_status_description.insert('0.0', (f'The original source for {source_name} is showing in your web browser...'))
        system_status_description.config(state = 'disabled', fg = 'Black')
        if source_name == ('The Age'):
            urldisplay(the_age_url)
        elif source_name == ('The Sydney Morning Herald'):
            urldisplay(the_sydney_morning_herald_url)
        elif source_name == ('ABC News'):
            urldisplay(abc_news_url)
        elif source_name == ('[Please select a data source]'):
            system_status_description.config(state = 'normal') 
            system_status_description.delete('0.0', 'end')    
            system_status_description.insert('0.0', ('ERROR: The show details button has been pressed, but no data source has been selected. If you wish to view the details of a data source, please select a data source first from the data source section.'))
            system_status_description.config(state = 'disabled', fg = 'Red')   
        
# Function to indicate the show latest button has been pressed, including selected source
def show_latest_button_pressed():
    try:
    
        global source_name
        global headline_selected
        global dateline_selected
        if source_name == ('The Age'):
            # Download the HTML code, unescape the code to ensure the text is in human english text, and then utilise regex to find a list of headlines and datelines in which the first instance from the list will be used for the age, displaying in UTC +10:00
            html_code_the_age = download(the_age_url, source_name, 'html', False, 'UTF-8', False)
            html_code_the_age = unescape(html_code_the_age)
            headline_regex_the_age = findall(r"""<a data-testid="article-link"[^>]*>(.*?)</a>""", html_code_the_age)
            dateline_regex_the_age = findall(r"""<time[^>]*dateTime="([^"]*)"[^>]*>""", html_code_the_age)
            headline_selected = headline_regex_the_age[0]
            dateline_selected = dateline_regex_the_age[0] +('(UTC+10:00 Time Zone)')
            # Edit the system status text to include the selected headline and dateline
            system_status_description.config(state = 'normal')  
            system_status_description.delete('0.0', 'end')    
            system_status_description.insert('0.0', (f"Latest news from {source_name} newspaper '{headline_selected}' \n '{dateline_selected}'."))
            system_status_description.config(state = 'disabled', fg = 'Black')
        elif source_name == ('The Sydney Morning Herald'):
            # Download the HTML code, unescape the code to ensure the text is in human english text, and then utilise regex to find a list of headlines and datelines in which the first instance from the list will be used for the sydney morning herald, displaying in UTC +10:00
            html_code_the_sydney_morning_herald = download(the_sydney_morning_herald_url, source_name, 'html', False, 'UTF-8', False)
            html_code_the_sydney_morning_herald = unescape(html_code_the_sydney_morning_herald)
            headline_regex_the_sydney_morning_herald = findall(r"""<a data-testid="article-link"[^>]*>(.*?)</a>""", html_code_the_sydney_morning_herald)
            dateline_regex_the_sydney_morning_herald = findall(r"""<time[^>]*dateTime="([^"]*)"[^>]*>""", html_code_the_sydney_morning_herald)
            headline_selected = headline_regex_the_sydney_morning_herald[0]
            dateline_selected = dateline_regex_the_sydney_morning_herald[0] +('(UTC+10:00 Time Zone)')
             # Edit the system status text to include the selected headline and dateline
            system_status_description.config(state = 'normal')  
            system_status_description.delete('0.0', 'end')    
            system_status_description.insert('0.0', (f"Latest news from {source_name} newspaper '{headline_selected}' \n '{dateline_selected}'."))
            system_status_description.config(state = 'disabled', fg = 'Black')
        elif source_name == ('ABC News'):
            # Download the HTML code, unescape the code to ensure the text is in human english text, and then utilise regex to find a list of headlines and datelines in which the first instance from the list will be used for abc news,
            # displaying time in UTC +00:00 also known as GMT and Zulu Time, for explicitness the time zone has been added at the end. The Z also represents Zulu Time which is indicative of UTC +00:00.
            html_code_abc_news = download(abc_news_url, source_name, 'html', False, 'UTF-8', False)
            html_code_abc_news = unescape(html_code_abc_news)
            headline_regex_abc_news = findall(r'''href="[^"]*" data-component="Link">(?:<span class="[^"]*" data-component="ScreenReaderOnly">[^<]*<!--.*?-->:<\/span>)?([^<]+)</a></span></h3><div''', html_code_abc_news)
            dateline_regex_c_abc_news = findall(r'''"true" dateTime="([^"]+)">''', html_code_abc_news)
            headline_selected = headline_regex_abc_news[0]
            dateline_selected = dateline_regex_c_abc_news[0] +('(UTC+00:00 Time Zone)')
            # Edit the system status text to include the selected headline and dateline
            system_status_description.config(state = 'normal')  
            system_status_description.delete('0.0', 'end')    
            system_status_description.insert('0.0', (f"Latest news from {source_name} newspaper '{headline_selected}' \n '{dateline_selected}'."))
            system_status_description.config(state = 'disabled', fg = 'Black')
        else:
            # Present an error in the system status if the user has not selected a data source
            system_status_description.config(state = 'normal') 
            system_status_description.delete('0.0', 'end')    
            system_status_description.insert('0.0', ('ERROR: The show latest button has been pressed, but no data source has been selected. If you wish to view the latest headline and dateline of a data source, please select a data source first from the data source section.'))
            system_status_description.config(state = 'disabled', fg = 'Red')

    except TypeError:
        system_status_description.config(state = 'normal') 
        system_status_description.delete('0.0', 'end')    
        system_status_description.insert('0.0', ('ERROR: No internet detected. A data source has been selected, but Blue Mushmom Fact Checker cannot access the internet to display the headline and dateline for this data source. Please connect to the internet if you wish to view this information.'))
        system_status_description.config(state = 'disabled', fg = 'Red')
        pass
    
    except URLError:
        system_status_description.config(state = 'normal') 
        system_status_description.delete('0.0', 'end')    
        system_status_description.insert('0.0', ('ERROR: Incorrect URL detected. A data source has been selected, but Blue Mushmom Fact Checker cannot access the URL to display the headline and dateline for this data source.'))
        system_status_description.config(state = 'disabled', fg = 'Red')
        pass
    
    except IndexError:
        system_status_description.config(state = 'normal') 
        system_status_description.delete('0.0', 'end')    
        system_status_description.insert('0.0', ('ERROR: No headline detected. A data source has been selected, but Blue Mushmom Fact Checker cannot access a valid headline and dateline to display for this data source.'))
        system_status_description.config(state = 'disabled', fg = 'Red')
        pass
        
# Function to indicate the save rating button has been pressed, including the value and source selected
def save_selected_rating():
    # Define some global variables and retrieve the rating_value to be used in the save_reliability_information function
    global source_name
    global headline_selected
    global dateline_selected
    rating_value = data_reliability_scaler.get()
    # Additionally, if there is no database located in the same file as the python program with the designated table, an Operational Error occurs - this error handling acknowledges that potential risk using try and except
    try:
    
        if source_name == ('The Age'):
            # Redo Regex code to ensure that users are able to access the headline and dateline without pressing show latest for the age
            html_code_the_age = download(the_age_url, source_name, 'html', False, 'UTF-8', False)
            html_code_the_age = unescape(html_code_the_age)
            headline_regex_the_age = findall(r"""<a data-testid="article-link"[^>]*>(.*?)</a>""", html_code_the_age)
            dateline_regex_the_age = findall(r"""<time[^>]*dateTime="([^"]*)"[^>]*>""", html_code_the_age)
            headline_selected = headline_regex_the_age[0]
            dateline_selected = dateline_regex_the_age[0]+('(UTC+10:00 Time Zone)')
            # Edit system status text to display rating and headline that is selected
            system_status_description.config(state = 'normal')  
            system_status_description.delete('0.0', 'end')    
            system_status_description.insert('0.0', (f'Reliability rating of {rating_value} saved in database for "{headline_selected}".'))
            system_status_description.config(state = 'disabled', fg = 'Black')
            # Call the function to save information about the source, headline, dateline and rating into the database
            save_reliability_information(source_name, headline_selected, dateline_selected, rating_value)
        elif source_name == ('The Sydney Morning Herald'):
            # Redo Regex code to ensure that users are able to access the headline and dateline without pressing show latest for the sydney morning herald
            html_code_the_sydney_morning_herald = download(the_sydney_morning_herald_url, source_name, 'html', False, 'UTF-8', False)
            html_code_the_sydney_morning_herald = unescape(html_code_the_sydney_morning_herald)
            headline_regex_the_sydney_morning_herald = findall(r"""<a data-testid="article-link"[^>]*>(.*?)</a>""", html_code_the_sydney_morning_herald)
            dateline_regex_the_sydney_morning_herald = findall(r"""<time[^>]*dateTime="([^"]*)"[^>]*>""", html_code_the_sydney_morning_herald)
            headline_selected = headline_regex_the_sydney_morning_herald[0]
            dateline_selected = dateline_regex_the_sydney_morning_herald[0]+('(UTC+10:00 Time Zone)')
            # Edit system status text to display rating and headline that is selected
            system_status_description.config(state = 'normal')  
            system_status_description.delete('0.0', 'end')    
            system_status_description.insert('0.0', (f'Reliability rating of {rating_value} saved in database for "{headline_selected}".'))
            system_status_description.config(state = 'disabled', fg = 'Black')
            # Call the function to save information about the source, headline, dateline and rating into the database
            save_reliability_information(source_name, headline_selected, dateline_selected, rating_value)
        elif source_name == ('ABC News'):
            # Redo Regex code to ensure that users are able to access the headline and dateline without pressing show latest for abc news
            html_code_abc_news = download(abc_news_url, source_name, 'html', False, 'UTF-8', False)
            html_code_abc_news = unescape(html_code_abc_news)
            headline_regex_abc_news = findall(r'''href="[^"]*" data-component="Link">(?:<span class="[^"]*" data-component="ScreenReaderOnly">[^<]*<!--.*?-->:<\/span>)?([^<]+)</a></span></h3><div''', html_code_abc_news)
            dateline_regex_c_abc_news = findall(r'''"true" dateTime="([^"]+)">''', html_code_abc_news)
            headline_selected = headline_regex_abc_news[0]
            dateline_selected = dateline_regex_c_abc_news[0] +('(UTC+00:00 Time Zone)')
            # Edit system status text to display rating and headline that is selected
            system_status_description.config(state = 'normal')  
            system_status_description.delete('0.0', 'end')    
            system_status_description.insert('0.0', (f'Reliability rating of {rating_value} saved in database for "{headline_selected}".'))
            system_status_description.config(state = 'disabled', fg = 'Black')
            # Call the function to save information about the source, headline, dateline and rating into the database
            save_reliability_information(source_name, headline_selected, dateline_selected, rating_value)
        else:
            # If no data source has been selected, provide an error message and stop the function
            system_status_description.config(state = 'normal')  
            system_status_description.delete('0.0', 'end')    
            system_status_description.insert('0.0', (f'ERROR: Button pressed to save the selected rating of {rating_value}, however no data source has been selected. Please ensure a data source is selected that will be rated with a rating of {rating_value}.'))
            system_status_description.config(state = 'disabled', fg = 'Red')
            pass
                
    except OperationalError: # If there is an Operational Error display a message indicating there is no database file in the same file location as the python program 
            system_status_description.config(state = 'normal')  
            system_status_description.delete('0.0', 'end')    
            system_status_description.insert('0.0', ('ERROR: No database has been located in this file location. Please ensure database file reliability_ratings.db is located in the same file location as the python program "Blue Mushmom Fact Checker" and contains the table "ratings".'))
            system_status_description.config(state = 'disabled', fg = 'Red')
            
    except TypeError:
            system_status_description.config(state = 'normal')  
            system_status_description.delete('0.0', 'end')    
            system_status_description.insert('0.0', (f'ERROR: No internet detected. Please connect to the internet to save the selected rating of {rating_value} for the headline and dateline of {source_name}'))
            system_status_description.config(state = 'disabled', fg = 'Red')
            
    except IndexError:
        system_status_description.config(state = 'normal') 
        system_status_description.delete('0.0', 'end')    
        system_status_description.insert('0.0', ('ERROR: No headline detected. A data source has been selected, but Blue Mushmom Fact Checker cannot access a valid headline and dateline to display for this data source.'))
        system_status_description.config(state = 'disabled', fg = 'Red')
        pass

# Develop the front-end user interface

# Define the font sizes
headline_font = ('Arial', 34)
body_font = ('Arial', 24)
medium_font = ('Arial', 14)

# Create a frame for checking system status
system_status = LabelFrame(main_window, text = 'System Status', font = headline_font, width = 12)
system_status.config(bg = 'Light Blue', fg = 'Black')
system_status.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'nsew')

# Create a widget that displays relevant text in the system status frame
system_status_description = Text(system_status, wrap = 'word', height = 10, state = 'normal', width = 55, font = medium_font)
system_status_description.insert('0.0', (source_name))
system_status_description.config(bg = 'Light Blue', fg = 'Black', state = 'disabled')
system_status_description.grid(row = 2, column = 1)

# Create a scrollbar for long text that would otherwise expand the system status label frame
system_status_scrollbar = Scrollbar(system_status, command = system_status_description.yview)
system_status_scrollbar.grid(row = 2, column = 2, sticky = 'ns')
system_status_description.config(yscrollcommand = system_status_scrollbar.set)

# Create the Data Source frame
data_source = LabelFrame(main_window, text = 'Data Source', font = headline_font, width = 12)
data_source.config(bg = 'Light Blue', fg = 'Black')
data_source.grid(row = 2, column = 1, rowspan = 3, padx = 5, pady = 5, sticky = 'nsew')

# Create widgets which are used to select which source
source_a = Radiobutton(data_source, text = 'The Age', command = source_button_pressed, font = medium_font, width = 6, variable = selected_source, value = 1)
source_a.config(bg = 'Light Blue', fg = 'Black')
source_a.grid(row = 1, column = 1, sticky = 'w', padx=(10,0))

source_b = Radiobutton(data_source, text = 'The Sydney Morning Herald', command = source_button_pressed, font = medium_font, width = 21, variable = selected_source, value = 2)
source_b.config(bg = 'Light Blue', fg = 'Black')
source_b.grid(row = 2, column = 1, sticky = 'w', padx=(10,0))

source_c = Radiobutton(data_source, text = 'ABC News', command = source_button_pressed, font = medium_font, width = 8, variable = selected_source, value = 3)
source_c.config(bg = 'Light Blue', fg = 'Black')
source_c.grid(row = 3, column = 1, sticky = 'w', padx=(10,0))
    
# Create widgets which are the tables for checking facts
show_latest = Button(data_source, text = "Show Latest", command = show_latest_button_pressed, font = body_font, width = 16)
show_latest.config(bg = 'Light Blue', fg = 'Black')
show_latest.grid(row = 4, column = 1)

# Create another widget
show_details = Button(data_source, text = 'Show Details', command = show_details_button_pressed, font = body_font, width = 16)
show_details.config(bg='Light Blue', fg = 'Black')
show_details.grid(row = 4, column = 2)

# Create the Data Reliability Frame
data_reliability = LabelFrame(main_window, text = 'Data Reliability', font = headline_font, width = 12)
data_reliability.config(bg = 'Light Blue', fg = 'Black')
data_reliability.grid(row = 5, column = 1, rowspan = 6, sticky = 'w')

# Create widgets to select reliability level
# Create a widget to indicate the scale is for selecting reliability
data_reliability_label = Label(data_reliability, text = 'Select the value on the Data Reliability Scale', font = body_font)
data_reliability_label.config(bg = 'Light Blue', fg = 'Black')
data_reliability_label.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'nsew')

# Create a widget to make a scale from 0 to 3 for data reliability
data_reliability_scaler = Scale(data_reliability, from_= 0, to = 3, orient = HORIZONTAL)
data_reliability_scaler.config(bg = 'Light Blue', fg = 'Black')
data_reliability_scaler.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = 'nsew')

# Create a button to save the rating selected by the scale widget
save_rating = Button(data_reliability, text = "Save Rating", command = save_selected_rating, font = medium_font, width = 12)
save_rating.config(bg = 'Light Blue', fg = 'Black')
save_rating.grid(row = 3, column = 1, sticky = 'nsew')

# Place the visual logo for the fact checker
try: # The visual logo image file can be missing from the file location of the python program and cause an error if it was to run the program, this is a potential error that is acknowledged with this error handling code
    visual_logo = PhotoImage(file = 'blue_mushmom_fact_checker.png')
    visual_logo_displayed = Label(main_window, image = visual_logo)
    visual_logo_displayed.config(bg = 'Light Blue')
    visual_logo_displayed.grid(row = 1, column = 2, rowspan = 5, sticky = 'nsew')
except:
    system_status_description.config(state = 'normal')  
    system_status_description.delete('0.0', 'end')    
    system_status_description.insert('0.0', ('ERROR: Image file "blue_mushmom_fact_checker.png" is not located in the same file location as the python program "Blue Mushmom Fact Checker". Please ensure the image file "blue_mushmom_fact_checker.png" is located in the same file location as the python program "Blue Mushmom Fact Checker".'))
    system_status_description.config(state = 'disabled', fg = 'Red')

# Adjust the program's style
main_window.title('Blue Mushmom Fact Checker')
try: # The icon logo image file can be missing from the file location of the python program and cause an error if it was to run the program, this is a potential error that is acknowledged with this error handling code
    icon_logo = PhotoImage(file = 'blue_mushmom_logo.png')
    main_window.iconphoto(False, icon_logo)
except:
    system_status_description.config(state = 'normal')  
    system_status_description.delete('0.0', 'end')    
    system_status_description.insert('0.0', ('Image file "blue_mushmom_logo.png" is not located in the same file location as the python program "Blue Mushmom Fact Checker". Please ensure the image file "blue_mushmom_logo.png" is located in the same file location as the python program "Blue Mushmom Fact Checker".'))
    system_status_description.config(state = 'disabled', fg = 'Red') 
main_window.config(bg = 'Light Blue')

# Start the event loop to detect user inputs
main_window.mainloop()
