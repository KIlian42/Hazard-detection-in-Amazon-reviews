import pandas as pd

if __name__ == '__main__':
    data = pd.read_csv('meta_Electronics.csv', delimiter=';')

    print(data.head)
    print(data['brand'].value_counts(ascending=1))

    '''
    counter = 0
    for index, row in data.iterrows():
        review_text = str(row['review']).lower()
        review_text = review_text.replace(',', ' , ').replace('.', ' . ')
        if 'battery' in review_text and 'explod' in review_text:
            counter += 1
            print(str(index), str(counter), row['review'])
    '''