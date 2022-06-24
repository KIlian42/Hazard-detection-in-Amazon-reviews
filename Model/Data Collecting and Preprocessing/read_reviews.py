import pandas as pd

if __name__ == '__main__':
    data = pd.read_csv('Electronics_reviews_1_star.csv', delimiter=';')
    print(data.shape)
    print(data.head)

    # burn, cable, wire, NOT( disk, disc, dvd )
    # battery, explode
    # safety alert
    counter = 0
    for index, row in data.iterrows():
        review_text = str(row['review']).lower()
        review_text = review_text.replace(',', ' , ').replace('.', ' . ')
        if 'battery' in review_text and 'explod' in review_text:
            counter += 1
            print(str(index), str(counter), row['review'])
