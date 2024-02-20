import csv
import requests
from bs4 import BeautifulSoup

def search_google(query):
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def scrape_search_results(html):
    soup = BeautifulSoup(html, 'html.parser')
    search_results = []
    for result in soup.find_all('div', class_='tF2Cxc'):
        title = result.find('h3').get_text()
        url = result.find('a')['href']
        snippet = result.find('span', class_='aCOpRe').get_text() if result.find('span', class_='aCOpRe') else ""
        search_results.append({'Title': title, 'URL': url, 'Snippet': snippet})
    return search_results

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'URL', 'Snippet']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow(item)

if __name__ == "__main__":
    # Example queries
    queries = [
        "Identify the industry in which Canoo operates, along with its size, growth rate, trends, and key players.",
        "Analyze Canoo's main competitors, including their market share, products or services offered, pricing strategies, and marketing efforts.",
        "Identify key trends in the market, including changes in consumer behavior, technological advancements, and shifts in the competitive landscape.",
        "Gather information on Canoo's financial performance, including its revenue, profit margins, return on investment, and expense structure."
    ]

    # Perform searches and scrape data for each query
    scraped_data = []
    for query in queries:
        print(f"Searching and scraping data for query: {query}")
        search_results_html = search_google(query)
        search_results = scrape_search_results(search_results_html)
        scraped_data.extend(search_results)

    # Save scraped data to a CSV file
    save_to_csv(scraped_data, 'search_results.csv')
