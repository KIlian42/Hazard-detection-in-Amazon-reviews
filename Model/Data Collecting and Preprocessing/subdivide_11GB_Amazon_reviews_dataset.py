# TO DO: Change the path/folder:

path = '/Users/kiliankramer/Desktop/MRP2 Scraping/'

with open(str(path) + 'Electronics.json', 'r') as file:
    data = file.read().replace('\n', '')
file.close()

# print(len(data))
output1 = data[:1500000000]
output2 = data[1500000000:3000000000]
output3 = data[3000000000:4500000000]
output4 = data[4500000000:6000000000]
output5 = data[6000000000:7500000000]
output6 = data[7500000000:9000000000]
output7 = data[9000000000:10500000000]
output8 = data[10500000000:]

file = open(str(path) + 'Electronics-1of8.json', 'w')
file.write(output1)
file.close()

file = open(str(path) + 'Electronics-2of8.json', 'w')
file.write(output2)
file.close()
print('4')

file = open(str(path) + 'Electronics-3of8.json', 'w')
file.write(output3)
file.close()

file = open(str(path) + 'Electronics-4of8.json', 'w')
file.write(output4)
file.close()

file = open(str(path) + 'Electronics-5of8.json', 'w')
file.write(output5)
file.close()

file = open(str(path) + 'Electronics-6of8.json', 'w')
file.write(output6)
file.close()

file = open(str(path) + 'Electronics-7of8.json', 'w')
file.write(output7)
file.close()

file = open(str(path) + 'Electronics-8of8.json', 'w')
file.write(output8)
file.close()