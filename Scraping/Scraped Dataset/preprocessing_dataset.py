import pandas as pd

if __name__ == '__main__':
    products = pd.read_csv('electronic_articles_amazon_metadata.csv', delimiter=';')
    #products = products.drop(['bestseller rank', 'feature ratings', 'product table HTML', 'product keypoints HTML', 'product description HTML',  'technical details HTML', 'often mentioned attributes'], axis=1)
    #products.to_csv('electronic_articles_amazon_metadata.csv', sep=';')

    #print(products['product title'][2])
    #counter = 0
    columns = products.columns
    star1 = []
    star2 = []
    star3 = []
    star4 = []
    star5 = []
    for index, product in products.iterrows():
        #if str(product['brand']).replace(' ', '').lower() != str(product['manufactur']).replace(' ', '').lower() and str(product['manufactur']) != 'nan' and str(product['brand']).replace(' ', '').lower() not in str(product['manufactur']).replace(' ', '').lower() and str(product['manufactur']).replace(' ', '').lower() not in str(product['brand']).replace(' ', '').lower():
        #    counter += 1
        #    print(str(product['brand']).replace(' ', '') + ' vs ' + str(product['manufactur']).replace(' ', ''))
        for column in columns:
            if products[column][index] != '':
                products[column][index] = str(products[column][index]).replace(',', ';')
        ratings = product['reviews distribution'].replace('[', '').replace(']', '').replace(' ', '').split(',')
        #print(str(ratings[0])+' '+str(ratings[1])+' '+str(ratings[2])+' '+str(ratings[3])+' '+str(ratings[4]))
        if len(ratings) == 5:
            percentage = int(ratings[0]) + int(ratings[1]) + int(ratings[2]) + int(ratings[3]) + int(ratings[4])
            if percentage != 0:
                star1.append(int((int(ratings[0])/percentage)*int(product['reviews total'])))
                star2.append(int((int(ratings[1])/percentage)*int(product['reviews total'])))
                star3.append(int((int(ratings[2])/percentage)*int(product['reviews total'])))
                star4.append(int((int(ratings[3])/percentage)*int(product['reviews total'])))
                star5.append(int((int(ratings[4])/percentage)*int(product['reviews total'])))
            else:
                star1.append('')
                star2.append('')
                star3.append('')
                star4.append('')
                star5.append('')
        else:
            star1.append('')
            star2.append('')
            star3.append('')
            star4.append('')
            star5.append('')
        if product['product avaiable since'] != '':
            products['product avaiable since'][index] = products['product avaiable since'][index][len(products['product avaiable since'][index])-6:].replace(' ', '').replace('n', '')
    s1 = pd.Series(star1)
    s2 = pd.Series(star2)
    s3 = pd.Series(star3)
    s4 = pd.Series(star4)
    s5 = pd.Series(star5)
    products['star5'] = s1
    products['star4'] = s2
    products['star3'] = s3
    products['star2'] = s4
    products['star1'] = s5
    #print(counter)
    #print(products['1-3 star reviews'][0])
    product_name = []
    for index, product in products.iterrows():
        for column in columns:
            if column == 'price':
                products[column][index] = products[column][index].replace('$', '')
            if products[column][index] == 'nan' or products[column][index] == 'a':
                products[column][index] = ''
            products[column][index] = str(products[column][index]).strip()
        pos = products['product url'][index].find('/dp')
        product_name.append(products['product url'][index][28:pos])
    product_n = pd.Series(product_name)
    products['product name'] = product_name
    products = products.drop(['1-3 star reviews', 'collected reviews', 'reviews distribution'], axis=1)
    products = products.rename(columns={'price': 'price in $'})
    products.to_csv('electronic_articles_amazon_metadata_new.csv', sep=',')

