import pandas as pd
import csv
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

if __name__ == '__main__':
    global_reviews = 0
    scraping_speed = 1  # in seconds
    scraping_counter = 1

    # GET ROOT HTML
    #driver = webdriver.Safari()
    #data = driver.get('https://www.amazon.com')
    #soup = BeautifulSoup(driver.page_source, 'html.parser')
    #file = open('amazondata.html', 'w')
    #file.write(str(soup))
    #file.close()

    # GET MENU ELEMENTS
    f = open('amazon.html')
    soup = BeautifulSoup(f, features='html.parser')
    menu = soup.find('ul', {'data-menu-id': '5'})
    f = open("electronic_categories_amazon_root.csv", "w")
    f.write('category;url\n')
    for category in menu.find_all(href=True)[1:]:
        print(category.string+';'+'https://www.amazon.com/-/en'+str(category['href']))
        f.write(category.string+';'+'https://www.amazon.com/-/en'+str(category['href'])+'\n')
    f.close()

    # GET LAYER1 HTML:
    driver = webdriver.Safari()
    categories = pd.read_csv('electronic_categories_amazon_root.csv', delimiter=';')
    for index, row in categories.iterrows():
        data = driver.get(row['url'])
        time.sleep(scraping_speed)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        file_name = row['category'].replace(' ', '_').replace('&','and')
        completeName = os.path.join('layer1_html/', file_name+'.html')
        file = open(completeName, 'w')
        file.write(str(soup))
        file.close()

    # GET LAYER1 ELEMENTS
    f_w = open("electronic_categories_amazon_layer1.csv", "w")
    f_w.write('category;layer1;url\n')
    categories = pd.read_csv('electronic_categories_amazon_root.csv', delimiter=';')
    for index, row in categories.iterrows():
        file_name = row['category'].replace(' ', '_').replace('&','and')
        completeName = os.path.join('layer1_html/', file_name+'.html')
        f = open(completeName)
        soup = BeautifulSoup(f, features='html.parser')
        f.close()
        menu = soup.find('div', {'id': 'departments'})
        for category in menu.find_all(href=True):
            value = category.find('span', {'class': 'a-size-base a-color-base'})
            print(row['category'] + ';' + value.string + ';' + 'https://www.amazon.com/-/en' + str(category['href']))
            f_w.write(row['category'] + ';' + value.string + ';' + 'https://www.amazon.com/-/en' + str(category['href']) + '\n')
    f_w.close()

    # GET LAYER2 HTML:
    driver = webdriver.Safari()
    categories = pd.read_csv('electronic_categories_amazon_layer1.csv', delimiter=';')
    try:
        os.mkdir('layer2_html/')
    except OSError:
        print('Path already exists')
    for index, row in categories.iterrows():
        data = driver.get(row['url'])
        time.sleep(scraping_speed)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        file_name = row['layer1'].replace(' ', '_').replace('&','and')
        completeName = os.path.join('layer2_html/', file_name+'.html')
        file = open(completeName, 'w')
        file.write(str(soup))
        file.close()

    # GET LAYER2 ELEMENTS
    f_w = open("electronic_categories_amazon_layer2.csv", "w")
    f_w.write('category;layer1;layer2;url\n')
    categories = pd.read_csv('electronic_categories_amazon_layer1.csv', delimiter=';')
    for index, row in categories.iterrows():
        file_name = row['layer1'].replace(' ', '_').replace('&','and')
        completeName = os.path.join('layer2_html/', file_name+'.html')
        f = open(completeName)
        soup = BeautifulSoup(f, features='html.parser')
        f.close()
        menu = soup.find('div', {'id': 'departments'})
        if menu != None:
            for category in menu.find_all(href=True):
                value = category.find('span', {'class': 'a-size-base a-color-base'})
                already_exist = 0
                for column in categories.columns:
                    if row[column] == value.string:
                        already_exist = 1
                if already_exist == 1:
                    continue
                print(row['category'] + ';' +  row['layer1'] + ';' + value.string + ';' + 'https://www.amazon.com/-/en' + str(category['href']))
                f_w.write(row['category'] + ';' +  row['layer1'] + ';' + value.string + ';' + 'https://www.amazon.com/-/en' + str(category['href']) + '\n')
        else:
            value = 'None'
            print(row['category'] + ';' + row['layer1'] + ';' + str(value) + ';' + row['url'])
            f_w.write(row['category'] + ';' + row['layer1'] + ';' + str(value) + ';' + row['url'] + '\n')
    f_w.close()

    # GET LAYER3 HTML:
    driver = webdriver.Safari()
    categories = pd.read_csv('electronic_categories_amazon_layer2.csv', delimiter=';')
    try:
        os.mkdir('layer3_html/')
    except OSError:
        print('Path already exists')
    for index, row in categories.iterrows():
        if row['layer2'] == 'None':
            print('nothing:'+str(index))
            continue
        data = driver.get(row['url'])
        time.sleep(scraping_speed)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        file_name = row['layer2'].replace(' ', '_').replace('&','and')
        completeName = os.path.join('layer3_html/', file_name+'.html')
        file = open(completeName, 'w')
        file.write(str(soup))
        file.close()

    # GET LAYER3 ELEMENTS
    f_w = open("electronic_categories_amazon_layer3.csv", "w")
    f_w.write('category;layer1;layer2;layer3;url\n')
    categories = pd.read_csv('electronic_categories_amazon_layer2.csv', delimiter=';')
    for index, row in categories.iterrows():
        if row['layer2'] == 'None':
            value = 'None'
            print(row['category'] + ';' + row['layer1'] + ';' + row['layer2'] + ';' + str(value) + ';' + row['url'])
            f_w.write(row['category'] + ';' + row['layer1'] + ';' + row['layer2'] + ';' + str(value) + ';' + row['url'] + '\n')
            continue
        file_name = row['layer2'].replace(' ', '_').replace('&','and')
        completeName = os.path.join('layer3_html/', file_name+'.html')
        f = open(completeName)
        soup = BeautifulSoup(f, features='html.parser')
        f.close()
        menu = soup.find('div', {'id': 'departments'})
        if menu == None:
            value = 'None'
            print(row['category'] + ';' + row['layer1'] + ';' + row['layer2'] + ';' + str(value) + ';' + row['url'])
            f_w.write(row['category'] + ';' + row['layer1'] + ';' + row['layer2'] + ';' + str(value) + ';' + row['url'] + '\n')
        else:
            added = 0
            for category in menu.find_all(href=True):
                value = category.find('span', {'class': 'a-size-base a-color-base'})
                #already_exist = 0
                #for index2, row2 in categories.iterrows():
                #    if row2['category'] == value.string or row2['layer1'] == value.string or row2['layer2'] == value.string:
                #        already_exist = 1
                #        break
                #if already_exist == 1:
                #    continue
                print(row['category'] + ';' +  row['layer1'] + ';' + row['layer2'] + ';' + value.string + ';' + 'https://www.amazon.com/-/en' + str(category['href']))
                f_w.write(row['category'] + ';' +  row['layer1'] + ';' + row['layer2'] + ';' + value.string + ';' + 'https://www.amazon.com/-/en' + str(category['href']) + '\n')
                #added = 1
            #if added == 0:
            #    value = 'None'
            #    print(row['category'] + ';' + row['layer1'] + ';' + row['layer2'] + ';' + str(value) + ';' + row['url'])
            #    f_w.write(row['category'] + ';' + row['layer1'] + ';' + row['layer2'] + ';' + str(value) + ';' + row['url'] + '\n')
    f_w.close()

    # Get Products
    driver = webdriver.Safari()
    f_w = open("electronic_articles_amazon.csv", "w")
    f_w.write('category;layer1;layer2;reviews;url\n')
    categories = pd.read_csv('electronic_categories_amazon_layer2.csv', delimiter=';')
    for index, row in categories.iterrows():
        print(row['layer2'])
        current_page = 1
        next_page_url = ''
        current_counter = 0
        while current_page <= 20:
            if current_page == 1:
                data = driver.get(row['url'])
            else:
                data = driver.get(next_page_url)
            time.sleep(scraping_speed)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            items = soup.find('div', {'class': 's-main-slot s-result-list s-search-results sg-row'})
            if items != None:
                for item in items.find_all('div', {'data-component-type': 's-search-result'}):
                    sponsored = item.find('div', {
                        'class': 'a-section a-spacing-none a-spacing-top-small s-title-instructions-style'})
                    if sponsored != None:
                        sponsored = sponsored.find('div', {'class': 'a-row a-spacing-micro'})
                        if sponsored != None: continue
                    reviews = item.find('div', {'class': 'a-section a-spacing-none a-spacing-top-micro'})
                    if reviews == None: continue
                    reviews = reviews.find('a', {
                        'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style'})
                    if reviews == None: continue
                    reviews = reviews.find('span')
                    if reviews == None: continue
                    reviews = reviews.string
                    reviews = reviews.replace(',', '')
                    reviews = int(reviews)
                    if reviews >= 20:
                        new_item_url = item.find('div', {
                            'class': 's-product-image-container aok-relative s-image-overlay-grey s-text-center s-padding-left-small s-padding-right-small s-spacing-small s-height-equalized'})
                        if new_item_url == None: continue
                        new_item_url = new_item_url.find('a')['href']
                        if new_item_url == None: continue
                        new_item_url = 'https://www.amazon.com/-/en' + new_item_url
                        f_w.write(row['category'] + ';' + row['layer1'] + ';' + row['layer2'] + ';' + str(
                            reviews) + ';' + str(new_item_url) + '\n')
                        current_counter += 1
                        if current_counter >= 200: break
            current_page += 1
            next_page = 'Go to page ' + str(current_page)
            next_page_url_tag = soup.find('span', {'class', 's-pagination-strip'})
            if next_page_url_tag == None: break
            next_page_url_tag = soup.find('a', {'aria-label': next_page})
            if next_page_url_tag == None: break
            next_page_url = next_page_url_tag['href']
            next_page_url = 'https://www.amazon.com/-/en' + str(next_page_url)

    # Get Products Metadata
    #products = pd.read_csv('electronic_articles_amazon_metadata.csv', delimiter=';')
    #print(products.columns)
    #print(products.head)

    driver = webdriver.Safari()
    data = driver.get('https://www.amazon.com/-/en/Blue-Handcart-Pairs-Cardboard-Glasses/dp/B01CUIXHVS/ref=sr_1_4?qid=1648288553&rnid=172532&s=electronics&sr=1-4')
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    element = driver.find_element(By.XPATH, 'cr-summarization-attributes-list')
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    soup2 = soup.find('div', {'id': 'cr-summarization-attributes-list'})
    print(soup2.prettify())

    category_counter = 1
    previous_category = ''
    driver = webdriver.Safari()
    f_w = open("electronic_articles_amazon_metadata.csv", "a")
    #f_w.write('category;layer1;layer2;product title;price;brand;manufactur;manufactur country;product avaiable since;bestseller rank;reviews total;reviews distribution;collected reviews;1-3 star reviews;feature ratings;often mentioned attributes;product table HTML;product keypoints HTML;product description HTML;technical details HTML;product asin;product url;store name;store url\n')
    products = pd.read_csv('electronic_articles_amazon.csv', delimiter=';')
    for index, product in products.iterrows():
        if index < 32040:
            continue

        current_category = product['layer2']
        if previous_category != '' and previous_category == current_category:
            category_counter += 1
        if category_counter > 5:
            if previous_category != current_category:
                category_counter = 1
            else:
                print('hi1')
                continue
        previous_category = product['layer2']

        brand_exists = 0
        Product_Title = ''
        Product_Price = ''
        Product_Brand = '' #Product_Store, Product_Table or Product_Technical_Details
        Product_Manufactur = '' #Technical_Details
        Product_Manufactur_Country = '' #Technical_Details
        Product_Avaiable_Since = ''  #Technical_Details
        Product_Bestseller_Rank = '' #Technical_Details
        ###
        Product_Reviews_Total = '' #current_table
        Product_Collected_Reviews = ''
        Product_Rating_Distribution = ''
        Product_1_2_3_Reviews = ''
        Product_Feature_Ratings = ''
        Product_Reviews_Mentioned_Attributes = ''
        ###
        Product_Table_HTML = ''
        Product_Keypoints_HTML = '' #"About this item"
        Product_Description_HTML = ''
        Product_Technical_Details_HTML = ''
        ###
        Product_Asin = '' #Technical_Details
        Product_Url = '' #current table
        Product_Store_Name = '' #Head
        Product_Store_Url = '' #Head
        ###
        # Start scraping
        try:
            data = driver.get(product['url'])
            time.sleep(scraping_speed)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
        except:
            print('hi2')
            continue

        Product_Title_soup = soup.find('span', {'id': 'productTitle'})
        if Product_Title_soup != None: Product_Title = Product_Title_soup.string.replace(';', ' ') #Title
        Product_Price_soup = soup.find('td', {'class': 'a-span12'})
        if Product_Price_soup != None:
            Product_Price_soup = Product_Price_soup.find('span', {'class': 'a-offscreen'})
            if Product_Price_soup != None: Product_Price = Product_Price_soup.string.replace(';', ' ') #Price
        Product_Brand_soup = soup.find('td', {'class': 'a-span9'})
        #if Product_Brand_soup != None:
        #    Product_Brand_soup = Product_Brand_soup.find('span')
        #    if Product_Brand_soup != None: Product_Brand = Product_Brand_soup.string.replace(';', ' ') #Brand

        '''
        Product_Table_soup = soup.find('table', {'class': 'a-normal a-spacing-micro'})
        if Product_Table_soup != None: Product_Table_HTML = str(Product_Table_soup).replace(';', ' ') #Product table
        Product_Keypoints_soup = soup.find('ul', {'class': 'a-unordered-list a-vertical a-spacing-mini'})
        if Product_Keypoints_soup != None: Product_Keypoints_HTML = str(Product_Keypoints_soup).replace(';', ' ') #Product keypoints
        Product_Description_soup = soup.find('div', {'id': 'productDescription'})
        if Product_Description_soup != None: Product_Description_HTML = str(Product_Description_soup).replace(';', ' ') #Product description
        '''
        Product_Technical_Details_soup = soup.find('table', {'id': 'productDetails_detailBullets_sections1'})
        if Product_Technical_Details_soup != None:
            #Product_Technical_Details_HTML = str(Product_Technical_Details_soup).replace(';', ' ') #Product technical details
            for entry in Product_Technical_Details_soup.find_all('tr'):
                table_key = entry.find('th')
                table_value = entry.find('td')
                if table_key == None or table_value == None: continue
                table_key = table_key.string
                table_value = table_value.string
                if table_key == ' ASIN ': #ASIN
                    Product_Asin = table_value.replace(';', ' ')
                elif table_key == ' Brand ': #Brand
                    Product_Brand = table_value.replace(';', ' ').replace('Brand: ', '').replace('Visit the ', '').replace(' Store', '')
                    brand_exists = 1
                elif table_key == ' Manufacturer ': #Manufactur
                    Product_Manufactur = table_value.replace(';', ' ')
                elif table_key == ' Country of Origin ': #Manufactur country
                    Product_Manufactur_Country = table_value.replace(';', ' ')
                elif table_key == ' Date First Available ': #Avaiable since
                    Product_Avaiable_Since = table_value.replace(';', ' ')
                #elif table_key == ' Best Sellers Rank ': #Bestseller rank
                #    table_value = table_value.find('span').find('span')
                #    Product_Bestseller_Rank = str(table_value.string).replace(';', ' ')

        try:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
        except:
            continue
        Product_Reviews_Total = product['reviews'] #Total reviews
        reviews_distribution = []
        Reviews_soup = soup.find('table', {'id': 'histogramTable', 'class': 'a-normal a-align-center a-spacing-base'})
        if Reviews_soup != None:
            for entry in Reviews_soup.find_all('tr'):
                entry = entry.find('td', {'class': 'a-text-right a-nowrap'})
                if entry == None:
                    reviews_distribution.append(0)
                    continue
                entry = entry.find('a')
                if entry == None:
                    reviews_distribution.append(0)
                    continue
                reviews_distribution.append(int(entry.string.replace(' ', '').replace('%', '')))
        Product_Rating_Distribution = str(reviews_distribution) #Reviews distribution
        features = []
        Product_Feature_Ratings_soup = soup.find('div', {'id': 'cr-summarization-attributes-list'})
        if Product_Feature_Ratings_soup != None:
            for feature in Product_Feature_Ratings_soup.find_all('div', {'data-hook': 'cr-summarization-attribute'}):
                feature_name = feature.find('span', {'class': 'a-size-base a-color-base'})
                feature_score = feature.find('span', {'class': 'a-size-base a-color-tertiary'})
                if feature_name != None and feature_score != None:
                    features.append([feature_name.string.replace(';', ' '), feature_score.string.replace(';', ' ')])
            Product_Feature_Ratings = str(features) #Product feature scores
        Product_Reviews_Mentioned_Attributes_soup = soup.find('div', {'class': 'cr-lighthouse-terms'})
        mentioned_attributes = []
        if Product_Reviews_Mentioned_Attributes_soup != None:
            for term in Product_Reviews_Mentioned_Attributes_soup.find_all('span', {'class': 'cr-lighthouse-term '}):
                mentioned_attributes.append(term.string.replace(';', ' '))
            Product_Reviews_Mentioned_Attributes = str(mentioned_attributes) #Product mentioned attributes
        Product_Url = product['url'] #Product url
        Product_Store_Name_soup = soup.find('a', {'id': 'bylineInfo', 'class': 'a-link-normal'})
        if Product_Store_Name_soup != None:
            Product_Store_Name = Product_Store_Name_soup.string.replace(';', ' ').replace('Brand: ', '').replace('Visit the ', '').replace(' Store', '') #Store name
            if brand_exists == 0:
                Product_Brand = Product_Store_Name
            Product_Store_Url = 'https://www.amazon.com/-/en'+str(Product_Store_Name_soup['href']) #Store url

        reviews = []
        reviews_counter = 0
        Product_reviews_soup = soup.find('a', {'data-hook': 'see-all-reviews-link-foot'})
        if Product_reviews_soup != None:
            all_reviews_url = 'https://www.amazon.com/-/en' + Product_reviews_soup['href']
            try:
                print('hi3')
                data = driver.get(all_reviews_url)
            except:
                continue
            time.sleep(scraping_speed/5)
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            next = soup.find('ul', {'class': 'a-pagination'})
            if next != None: next = next.find('li', {'class', 'a-last'})
            if next != None: next = next.find('a')
            if next != None: next = 'https://www.amazon.com/-/en' + next['href']
            page = 1
            soup = soup.find('div', {'class': 'a-column a-span6 view-point-review critical-review a-span-last'})
            while soup != None and page <= 3:
                soup = soup.find('a', {'data-reftag': 'cm_cr_arp_d_viewpnt_rgt'})
                if soup != None:
                    all_reviews_url = 'https://www.amazon.com/-/en' + soup['href']
                    data = driver.get(all_reviews_url)
                    time.sleep(scraping_speed)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find('div', {'id': 'cm_cr-review_list'})
                    if soup != None:
                        for review in soup.find_all('div', {'data-hook': 'review'}):
                            review_rating = ''
                            review_title = ''
                            review_text = ''
                            rating = review.find('a', {'class': 'a-link-normal'})
                            try:
                                if rating != None: review_rating = rating['title'][:1].replace("'", "").replace('"', '').replace(';', ' ').replace('<span>', '').replace('\n', '').replace(',', ' ').replace('[', ' ').replace(']', ' ')
                            except:
                                print('                                     '+str(rating))
                            title = review.find('a', {'data-hook': 'review-title'})
                            if title != None:
                                title = title.find('span')
                                if title != None:
                                    review_title = title.string.replace("'", "").replace('"', '').replace(';', ' ').replace('<span>', '').replace('\n', '').replace(',', ' ').replace('[', ' ').replace(']', ' ')
                            text = review.find('span', {'data-hook': 'review-body'})
                            if text != None:
                                text = text.find('span')
                                if text != None:
                                    review_text = str(text).replace("'", "").replace('"', '').replace(';', ' ').replace('<span>', '').replace('\n', '').replace(',', ' ').replace('[', ' ').replace(']', ' ')
                            reviews.append([review_rating, review_title, review_text])
                            reviews_counter += 1
                if next != None:
                    try:
                        data = driver.get(next)
                    except:
                        print(next)
                        page = 3
                        continue
                    time.sleep(scraping_speed)
                    try:
                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                    except:
                        print('hi4')
                        page = 3
                        continue
                    page += 1
        Product_Collected_Reviews = str(reviews_counter) #Collected reviews
        Product_1_2_3_Reviews = str(reviews)
        global_reviews += reviews_counter

        if Product_Title == '' and scraping_speed < 64:
            scraping_speed = scraping_speed * 2
        elif Product_Title != '':
            scraping_counter += 1
        if scraping_counter > 1 and scraping_speed >= 2:
            scraping_counter = 1
            scraping_speed = scraping_speed / 2
        elif scraping_counter > 3 and scraping_speed > 0.5:
            scraping_counter = 1
            scraping_speed = scraping_speed / 2

        f_w.write(str(product['category']) + ';' + str(product['layer1']) + ';' + str(product['layer2']) + ';' + str(Product_Title) + ';' + str(Product_Price) + ';' + str(Product_Brand) + ';' + str(Product_Manufactur) + ';' + str(Product_Manufactur_Country) + ';' + str(Product_Avaiable_Since) + ';' + str(Product_Bestseller_Rank) + ';' + str(Product_Reviews_Total) + ';' + str(Product_Rating_Distribution) + ';' + str(Product_Collected_Reviews) + ';' + str(Product_1_2_3_Reviews) + ';' + str(Product_Feature_Ratings) + ';' + str(Product_Reviews_Mentioned_Attributes) + ';' + str(Product_Table_HTML) + ';' + str(Product_Keypoints_HTML) + ';' + str(Product_Description_HTML) + ';' + str(Product_Technical_Details_HTML) + ';' + str(Product_Asin) + ';' + str(Product_Url) + ';' + str(Product_Store_Name) + ';' + str(Product_Store_Url) + '\n')
        print('scraping speed: ' + str(scraping_speed) + '; total reviews: '+str(global_reviews)+'; index:'+str(index)+'; product:'+product['category']+':'+product['layer1']+':'+product['layer2']+';'+product['url'])
    f_w.close()
    print(global_reviews)



    '''
    s = '5 stars represent 78% of rating'
    #s = '3 stars represent 4% of rating'
    i = s.find('%')
    s_sub = s[i-2:i]
    s_sub = int(s_sub)
    print(s_sub)
    '''
















