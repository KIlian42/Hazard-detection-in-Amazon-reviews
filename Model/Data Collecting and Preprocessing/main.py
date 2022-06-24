import pandas as pd

if __name__ == '__main__':
    with open('combined_Electronics.csv', 'r') as file:
        data = file.read()
    file.close()
    output = 'asin;rating;review;brand;all_categories;main_category\n' + str(data)
    file = open('combined_Electronics.csv', 'w')
    file.write(output)
    file.close()

    '''
    # filter by category, by brands
    data = pd.read_csv('combined_Electronics.csv', delimiter=';')
    data = data.loc[data['brand'] == 'Sony']
    data = data.loc[data['all_categories'] == 'Computers']
    for index, row in data.iterrows():
        print(row.main_category)
        print(row.review)
    '''

    # summarize: group 1 star ratings by main_category
    # keyword search for hazard detection, topic modeling, tf-idf
    # apply BI-LSTM
    # use Amazon/Aliexpress scraping bots for recent products


