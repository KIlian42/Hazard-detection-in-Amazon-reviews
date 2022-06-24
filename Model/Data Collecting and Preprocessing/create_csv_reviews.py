path = '/Users/kiliankramer/Desktop/MRP2 Scraping/'

ratings = []
reviews = []
asin = []

for i in range(1,9):
    print(i)
    dataset = str(path) + 'Electronics-' + str(i) + 'of8.json'
    with open(str(dataset), 'r') as file:
        data = file.read().replace('\n', '').replace(';', ',')
    file.close()
    data = data.split('{"overall": ')
    for i in data[1:]:
        ratings.append(i[:1])
        review_start = i.find('"reviewText": ')
        review_end = i[review_start+15:].find('", ')
        reviews.append(i[review_start+15:review_start+15+review_end])
        asin_start = i.find('"asin": ')
        asin_end = i[asin_start + 8:].find('", ')
        asin.append(i[asin_start + 9:asin_start + 7 + asin_end])

print(9)
with open(str(path) + 'Electronics_reviews_1_star.csv', 'w') as csvfile:
    csvfile.write('asin;rating;review\n')
    for i, rating in enumerate(ratings):
        if str(rating) == '1':
            csvfile.write(str(asin[i]) + ';' + str(ratings[i]) + ';' + str(reviews[i]) + '\n')
csvfile.close()

print(10)
with open(str(path) + 'Electronics_reviews_1-2_star.csv', 'w') as csvfile:
    csvfile.write('asin;rating;review\n')
    for i, rating in enumerate(ratings):
        if str(rating) == '1' or str(rating) == '2':
            csvfile.write(str(asin[i]) + ';' + str(ratings[i]) + ';' + str(reviews[i]) + '\n')
csvfile.close()

print(11)
with open(str(path) + 'Electronics_reviews_1-3_star.csv', 'w') as csvfile:
    csvfile.write('asin;rating;review\n')
    for i, rating in enumerate(ratings):
        if str(rating) == '1' or str(rating) == '2' or str(rating) == '3':
            csvfile.write(str(asin[i]) + ';' + str(ratings[i]) + ';' + str(reviews[i]) + '\n')
csvfile.close()

print(12)
with open(str(path) + 'Electronics_reviews_1-5_star.csv', 'w') as csvfile:
    csvfile.write('asin;rating;review\n')
    for i, rating in enumerate(ratings):
        csvfile.write(str(asin[i]) + ';' + str(ratings[i]) + ';' + str(reviews[i]) + '\n')
csvfile.close()