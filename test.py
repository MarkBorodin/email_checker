from csv import reader

counter_t = 0
counter_f = 0

with open(f'media/results/result_HFK_Export_Prosperus_V1_KWVLybf.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    for line in read_obj.readlines():
        array = line.split(',')
        item = array[2]
        if item == 'True':
            counter_t += 1
        else:
            counter_f += 1

print(f'True: {counter_t}')
print(f'False: {counter_f}')

