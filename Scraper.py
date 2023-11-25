import requests
from bs4 import BeautifulSoup
import csv

csv_filename = r'C:\Users\HP\Downloads\Blogs_Scraped.csv'

with open(csv_filename, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Date', 'Title', 'Image URL', 'Likes'])

    page_number=1
    while True:
        url = f"https://rategain.com/blog/page/{page_number}/"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        blog_entries = soup.find_all('article', class_='blog-item')
        if len(blog_entries)==0:
            break
        for entry in blog_entries:
            date = entry.find('div', class_='bd-item').find('span').text.strip()
            title = entry.find('h6').find('a').text.strip()
            if entry.find('div', class_='img'):
                image_url = entry.find('div', class_='img').find('a')['data-bg']
            else:
                image_url=""
            likes = entry.find('a', class_='zilla-likes').find('span').text.strip()
            csv_writer.writerow([date, title, image_url, likes])
        page_number+=1


