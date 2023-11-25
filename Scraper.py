# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import csv

# Set the filename for the CSV file to store scraped data
csv_filename = r'Blogs_Scraped.csv'

# Open the CSV file in write mode
with open(csv_filename, 'w', newline='') as csvfile:
    # Create a CSV writer object
    csv_writer = csv.writer(csvfile)
    
    # Write the header row to the CSV file
    csv_writer.writerow(['Date', 'Title', 'Image URL', 'Likes'])

    # Initialize the page number for the blog pages
    page_number = 1
    
    # Start an infinite loop to iterate over blog pages until there are no more entries
    while True:
        # Construct the URL for the current blog page
        url = f"https://rategain.com/blog/page/{page_number}/"
        
        # Set the user agent header to simulate a browser request
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        
        # Send a GET request to the blog page URL
        response = requests.get(url, headers=headers)
        
        # Extract the HTML content from the response
        html_content = response.text
        
        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all blog entries on the page with the specified class
        blog_entries = soup.find_all('article', class_='blog-item')
        
        # If no blog entries are found, break out of the loop
        if len(blog_entries) == 0:
            break
        
        # Iterate over each blog entry and extract relevant information
        for entry in blog_entries:
            date = entry.find('div', class_='bd-item').find('span').text.strip()
            title = entry.find('h6').find('a').text.strip()
            
            # Check if the entry has an image, and extract its URL if present
            if entry.find('div', class_='img'):
                image_url = entry.find('div', class_='img').find('a')['data-bg']
            else:
                image_url = ""
            
            # Extract the number of likes for the blog entry
            likes = entry.find('a', class_='zilla-likes').find('span').text.strip()
            
            # Write the extracted information to the CSV file
            csv_writer.writerow([date, title, image_url, likes])
        
        # Move to the next page for the next iteration
        page_number += 1
