from urllib import request
import os
import time
import json

'''Creates a dataset of middle grades and young adult hardcover books using the
New York Times API.'''

API_KEY = '1muAIGCEibpAhfxQ1cuXlmWbXlokKswI'
NYT_PATH = 'https://api.nytimes.com/svc/books/v3/lists/'

def get_pub_dates(categories):
    '''Get the the various nytimes lists and return a dictionary oldest listed
    dates for the provided NYT list categories'''

    url = NYT_PATH + 'names.json?api-key=' + API_KEY
    result = request.urlopen(url)
    data = json.loads(result.read())

    # save the publication times in a dictionary as a tuple
    pub_dates = {}
    for booklist in data["results"]:
        if booklist['list_name_encoded'] in categories:
            pub_dates[booklist['list_name_encoded']] = booklist['oldest_published_date']

    return pub_dates


def get_data_for_date(category, pub_date):
    '''Get a json of the items on the NYT Bestseller list given a category and
    publication date'''

    url = NYT_PATH + pub_date + '/' + category + '.json?api-key=' + API_KEY
    print('Looking up list for ' + category + ' on ' + pub_date + '.')


    site_connected = False
    while not site_connected:
        try:
            result = request.urlopen(url)
            data = json.loads(result.read())
            site_connected = True

        except urllib2.URLError as error:
            print("Request failed. Retrying in 10 seconds. URL: " + url)
            time.sleep(10)

    # with open(category + '_' + pub_date + '.json', 'w') as file:
        # json.dump(data, file, indent=4)

    return data

def main():

    data_dumps_path = os.path.join(os.getcwd(), 'data-dumps\\')
    if not os.path.isdir(data_dumps_path):
        os.mkdir(data_dumps_path)

    # the dictionary that will store all best seller information
    best_sellers = {}

    # get the oldest publication dates for the provided categories
    categories = ['childrens-middle-grade-hardcover', 'young-adult-hardcover']
    categories = get_pub_dates(categories)

    # for each category, get all lists up to present day and parse info into
    # the best_sellers dictionary
    # incr = 0
    for category in categories:

        next_published_date = categories[category]
        while next_published_date != '':
            booklist = get_data_for_date(category, next_published_date)

            # add book names and relevant information to best_sellers
            for book in booklist['results']['books']:

                if book['title'] not in best_sellers:
                    best_sellers[book['title']] = {
                        'author' : book['author'],
                        'isbn' : book['primary_isbn13'],
                        'publisher' : book['publisher']}

            # update the next date to look for
            next_published_date = booklist['results']['next_published_date']


            # write dictionary to text file for debugging
            # with open(data_dumps_path + 'datadump_' + str(incr) + '.json', 'w') as file:
                # json.dump(best_sellers, file, indent=4)
            # incr += 1

            # pause to avoid hitting the api call limit (10 requests per min)
            time.sleep(6)

    with open('bestsellers.json', 'w') as file:
        json.dump(best_sellers, file, indent=4)

main()
