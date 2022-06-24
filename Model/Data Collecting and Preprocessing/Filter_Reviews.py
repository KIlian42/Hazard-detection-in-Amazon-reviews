import pandas as pd

if __name__ == '__main__':
    # filter hazards
    filtered_reviews = []
    filtered_reviews_negative = []
    data = pd.read_csv('Electronics_reviews_1_star.csv', delimiter=';')
    data = data.sample(frac=1)
    print(data.shape)
    counter = 0
    counter_negative = 0
    for index, row in data.iterrows():
        # print(row.review)
        review_text = str(row['review']).lower()
        review_text = review_text.replace(',', ' , ').replace('.', ' . ')
        if (counter_negative < 5380 and 'smell' not in review_text and 'burn' not in review_text
            and 'cable' not in review_text and 'melt' not in review_text
            and 'battery' not in review_text and 'explod' not in review_text
            and 'arcing' not in review_text and 'electrical shock' not in review_text
            and 'electric shock' not in review_text and 'extremely hot' not in review_text
            and 'extreme hot' not in review_text and 'extremely dangerous' not in review_text
            and 'scorch mark' not in review_text and 'safety alert' not in review_text):
            counter_negative += 1
            print(str(index), str(counter_negative), row['review'])
            filtered_reviews_negative.append(['negative', row['review']])
            continue
        if 'smell' in review_text and 'burn' in review_text:
            # 3076
            counter += 1
            print(str(index), str(counter), row['review'])
            # filtered_reviews.append(['smell burn', row['review']])
            filtered_reviews.append(['positive', row['review']])
            continue
        if 'cable' in review_text and 'melt' in review_text:
            # 383
            counter += 1
            print(str(index), str(counter), row['review'])
            # filtered_reviews.append(['cable melt', row['review']])
            filtered_reviews.append(['positive', row['review']])
            continue
        if 'battery' in review_text and 'explod' in review_text:
            # 386
            counter += 1
            print(str(index), str(counter), row['review'])
            # filtered_reviews.append(['battery explode', row['review']])
            filtered_reviews.append(['positive', row['review']])
            continue
        if 'arcing' in review_text:
            # 97
            counter += 1
            print(str(index), str(counter), row['review'])
            # filtered_reviews.append(['arcing', row['review']])
            filtered_reviews.append(['positive', row['review']])
            continue
        if 'electrical shock' in review_text or 'electric shock' in review_text:
            # 79
            counter += 1
            print(str(index), str(counter), row['review'])
            # filtered_reviews.append(['electrical shock', row['review']])
            filtered_reviews.append(['positive', row['review']])
            continue
        if 'extremely hot' in review_text or 'extreme hot' in review_text:
            # 1260
            counter += 1
            print(str(index), str(counter), row['review'])
            # filtered_reviews.append(['extremely hot', row['review']])
            filtered_reviews.append(['positive', row['review']])
            continue
        if 'extremely dangerous' in review_text:
            # 38
            counter += 1
            print(str(index), str(counter), row['review'])
            # filtered_reviews.append(['extremely dangerous', row['review']])
            filtered_reviews.append(['positive', row['review']])
            continue
        if 'scorch mark' in review_text:
            # 28
            counter += 1
            print(str(index), str(counter), row['review'])
            # filtered_reviews.append(['scorch mark', row['review']])
            filtered_reviews.append(['positive', row['review']])
            continue
        if 'safety alert' in review_text:
            # 6
            counter += 1
            print(str(index), str(counter), row['review'])
            # filtered_reviews.append(['safety alert', row['review']])
            filtered_reviews.append(['positive', row['review']])
            continue
        '''
        if 'cut' in review_text and 'finger' in review_text:
            # 916
            counter += 1
            print(str(index), str(counter), row['review'])
            continue
        '''
        '''
        if ('hot plug' in review_text or 'hot socket' in review_text) and 'burn' in review_text:
            # 3
            counter += 1
            print(str(index), str(counter), row['review'])
            continue
        '''

    print('Total positive:', counter, 'Total negative:', counter_negative)
    print(data.shape)

    with open('Filtered_Reviews.csv', 'w') as csvfile:
        csvfile.write('label;review\n')
        for index, review in enumerate(filtered_reviews):
            csvfile.write(str(review[0]) + ';' + str(review[1]) + '\n')
            csvfile.write(str(filtered_reviews_negative[index][0]) + ';' + str(filtered_reviews_negative[index][1]) + '\n')
    csvfile.close()



