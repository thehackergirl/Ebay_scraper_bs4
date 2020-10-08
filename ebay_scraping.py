import csv
import requests
from bs4 import BeautifulSoup


def get_page(url):
    response = requests.get(url)

    if not response.ok:
        print('Server responded: ', response.status_code)
    else:
        soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_detailed_data(soup):
    try:
        title = soup.find('span', id='vi-lkhdr-itmTitl').text
    except:
        title = ''
    print(title)

    try:
        price = soup.find('span', id='prcIsum').text.strip().split()[1].split('$')[1]
    except:
        price = ''
    print(price)
    data = {
        'title': title,
        'price': price
    }
    return data


def get_index_data(soup):
    try:
        links = soup.find_all('a', class_='s-item__link')
    except:
        links = []

    urls = [item.get('href') for item in links]
    return urls


def write_csv(data, url):
    with open('output.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)

        row = [data['title'], data['price'], url]

        writer.writerow(row)


def main():
    url = 'https://www.ebay.com/sch/i.html?_nkw=hang+drum&_pgn=1'
    get_page(url)
    products = get_index_data(get_page(url))

    for link in products:
        data = get_detailed_data(get_page(link))
        write_csv(data, link)


if __name__ == '__main__':
    main()