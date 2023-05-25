#!/usr/bin/env python
# coding: utf-8

# In[27]:


import requests
from bs4 import BeautifulSoup

# Set the number of pages to scrape
num_pages = 20

# Base URL for the product listings
base_url = "https://www.amazon.in/s"

# Parameters for the search query
params = {
    "k": "bags",
    "crid": "2M096C61O4MLT",
    "qid": "1653308124",
    "sprefix": "ba%2Caps%2C283",
    "ref": "sr_pg_1"
}

# Initialize lists to store scraped data
product_urls = []
product_names = []
product_prices = []
ratings = []
review_counts = []

# Scrape data from each page
for page in range(1, num_pages + 1):
    params["ref"] = f"sr_pg_{page}"
    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all product listings on the page
    listings = soup.find_all("div", {"data-component-type": "s-search-result"})

    # Extract information from each listing
    for listing in listings:
        # Product URL
        url_element = listing.find("a", class_="a-link-normal s-no-outline")
        if url_element is not None:
            url = "https://www.amazon.in" + url_element["href"]
        else:
            url = None
        product_urls.append(url)

        # Product Name
        name_element = listing.find("span", class_="a-size-medium a-color-base a-text-normal")
        if name_element is not None:
            product_names.append(name_element.text)
        else:
            product_names.append(None)

        # Product Price
        price_element = listing.find("span", class_="a-price-whole")
        if price_element is not None:
            product_prices.append(price_element.text.replace(",", ""))
        else:
            product_prices.append(None)

        # Rating
        rating_element = listing.find("span", class_="a-icon-alt")
        if rating_element is not None:
            ratings.append(rating_element.text.split()[0])
        else:
            ratings.append(None)

        # Number of Reviews
        reviews_element = listing.find("span", class_="a-size-base")
        if reviews_element is not None:
            review_counts.append(reviews_element.text)
        else:
            review_counts.append(None)

# Print the scraped data
for i in range(len(product_urls)):
    print(f"Product {i+1}:")
    print("URL:", product_urls[i])
    print("Name:", product_names[i])
    print("Price:", product_prices[i])
    print("Rating:", ratings[i])
    print("Number of Reviews:", review_counts[i])
    print()


# In[28]:


import requests
from bs4 import BeautifulSoup

base_url = 'https://www.amazon.in/s'
search_query = 'bags'
pages_to_scrape = 20

for page in range(1, pages_to_scrape + 1):
    params = {
        'k': search_query,
        'crid': '2M096C61O4MLT',
        'qid': 1653308124,
        'sprefix': 'ba,aps,283',
        'ref': f'sr_pg_{page}',
    }

    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.content, 'html.parser')

    products = soup.find_all('div', {'data-component-type': 's-search-result'})

    for product in products:
        # Extract the product details
        product_url = product.find('a', {'class': 'a-link-normal s-no-outline'})['href']
        product_name = product.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text
        product_price = product.find('span', {'class': 'a-price-whole'}).text

        # Ratings and reviews are optional fields, not all products have them
        rating_element = product.find('span', {'class': 'a-icon-alt'})
        rating = rating_element.text.split()[0] if rating_element else 'N/A'

        review_element = product.find('span', {'class': 'a-size-base'})
        review_count = review_element.text if review_element else 'N/A'

        # Print or store the extracted data as required
        print('Product URL:', product_url)
        print('Product Name:', product_name)
        print('Product Price:', product_price)
        print('Rating:', rating)
        print('Number of Reviews:', review_count)
        print('---')

    print(f'Page {page} scraping completed.')



# In[29]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = 'https://www.amazon.in'

search_query = 'bags'
pages_to_scrape = 20
products_to_scrape_per_page = 10
total_products_to_scrape = pages_to_scrape * products_to_scrape_per_page

data = []

for page in range(1, pages_to_scrape + 1):
    params = {
        'k': search_query,
        'crid': '2M096C61O4MLT',
        'qid': 1653308124,
        'sprefix': 'ba,aps,283',
        'ref': f'sr_pg_{page}',
    }

    response = requests.get(base_url + '/s', params=params)
    soup = BeautifulSoup(response.content, 'html.parser')

    products = soup.find_all('div', {'data-component-type': 's-search-result'})

    for product in products:
        # Extract the product details
        product_url = base_url + product.find('a', {'class': 'a-link-normal s-no-outline'})['href']
        product_name = product.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text
        product_price = product.find('span', {'class': 'a-price-whole'}).text

        # Ratings and reviews are optional fields, not all products have them
        rating_element = product.find('span', {'class': 'a-icon-alt'})
        rating = rating_element.text.split()[0] if rating_element else 'N/A'

        review_element = product.find('span', {'class': 'a-size-base'})
        review_count = review_element.text if review_element else 'N/A'

        # Hit the product URL to scrape additional information
        product_response = requests.get(product_url)
        product_soup = BeautifulSoup(product_response.content, 'html.parser')

        # Extract additional information
        description_element = product_soup.find('div', {'id': 'productDescription'})
        description = description_element.text.strip() if description_element else 'N/A'

        asin_element = product_soup.find('th', text='ASIN')
        asin = asin_element.find_next('td').text.strip() if asin_element else 'N/A'

        product_description_element = product_soup.find('div', {'id': 'feature-bullets'})
        product_description = product_description_element.get_text('\n').strip() if product_description_element else 'N/A'

        manufacturer_element = product_soup.find('a', {'id': 'bylineInfo'})
        manufacturer = manufacturer_element.text.strip() if manufacturer_element else 'N/A'

        # Append the data to the list
        data.append([product_url, product_name, product_price, rating, review_count, description, asin, product_description, manufacturer])

    print(f'Page {page} scraping completed.')

# Export the data to a CSV file
headers = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews',
           'Description', 'ASIN', 'Product Description', 'Manufacturer']
df = pd.DataFrame(data, columns=headers)
df.to_csv('product_data.csv', index=False)

print('Data exported to product_data.csv')


# In[ ]:




