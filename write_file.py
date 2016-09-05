from sys import argv

script, cars = argv

target = open('./last_count.txt', 'w')
target.truncate()
target.write(u'{}'.format(cars))
target.close()
