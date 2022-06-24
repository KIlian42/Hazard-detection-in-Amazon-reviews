import pandas as pd

path = '/Users/kiliankramer/Desktop/MRP2 Scraping/'

if __name__ == '__main__':
    data = pd.read_csv('Electronics_reviews_1_star.csv', delimiter=';')
    meta_data = pd.read_csv('meta_Electronics.csv', delimiter=';')

    # combine reviews with brand, main category, all categories
    asin = []
    ratings = []
    reviews = []
    brands = []
    main_categories = []
    categories = []

    print(data.shape)

    '''
    if (index <= 2):
        continue
    if (index > 3):
        break
    '''

    for index, row in data.iterrows():
        print(index)
        if (index <= 100000):
            continue
        if (index > 120000):
            break
        asin_str = row['asin']
        asin.append(row['asin'])
        ratings.append(row['rating'])
        reviews.append(row['review'])

        product = meta_data.loc[meta_data['asin'] == asin_str].iloc[0]
        brands.append(product['brand'])
        main_categories.append(product['main_category'])
        categories.append(product['category'])

    print(len(asin))
    print(len(ratings))
    print(len(reviews))
    print(len(brands))
    print(len(main_categories))
    print(len(categories))

    # with open(str(path) + 'combined_Electronics.csv', 'a') as csvfile:
    with open('combined_Electronics.csv', 'a') as csvfile:
        # csvfile.write('asin;rating;review;brand;category;main_category\n')
        for i, rating in enumerate(categories):
            csvfile.write(
                str(asin[i]) + ';' + str(ratings[i]) + ';' + str(reviews[i]) + ';' + str(brands[i]) + ";" + str(categories[i]) + ";" + str(main_categories[i]) + '\n')
    csvfile.close()
