path = '/Users/kiliankramer/Desktop/MRP2 Scraping/'

main_categories = []
categories = []
brands = []
asin = []

for i in range(1,9):
    print(i)
    dataset = str(path) + 'meta_Electronics-' + str(i) + 'of8.json'
    with open(str(dataset), 'r') as file:
        data = file.read().replace('\n', '').replace(';', ',')
    file.close()

    data = data.split('{"category": ')
    for i in data[1:]:
        categories_end = i.find(']')
        main_categories_start = i.find('"main_cat": ')
        main_categories_end = i[main_categories_start + 11:].find('", ')
        brands_start = i.find('"brand": ')
        brands_end = i[brands_start + 8:].find('", ')
        asin_start = i.find('"asin": ')
        asin_end = i[asin_start + 8:].find('", ')

        categories.append(i[1:categories_end])
        main_categories.append(i[main_categories_start+13:main_categories_start+11+main_categories_end])
        brands.append(i[brands_start + 10:brands_start + 8 + brands_end])
        asin.append(i[asin_start + 9:asin_start + 7 + asin_end])

print(len(categories))
print(len(main_categories))
print(len(brands))
print(len(asin))

with open(str(path) + 'meta_Electronics.csv', 'w') as csvfile:
    csvfile.write('asin;brand;category;main_category\n')
    for i, rating in enumerate(categories):
        csvfile.write(str(asin[i]) + ';' + str(brands[i]) + ";" + str(categories[i]) + ";" + str(main_categories[i]) + '\n')
csvfile.close()