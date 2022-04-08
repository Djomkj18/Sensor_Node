import os # Need it to control over the filesystem


#https://codereview.stackexchange.com/questions/191974/median-filter-implementation-in-python
def median_filter(_data, filter_size):
    temp = []
    indexer = filter_size // 2
    for i in range(len(_data)):
        for z in range(filter_size):
            if i + z - indexer < 0 or i + z - indexer > len(_data) - 1:
                for c in range(filter_size):
                    temp.append(0)
            else:
                for k in range(filter_size):
                    temp.append(_data[i + z - indexer])

        temp.sort()
        _data[i] = temp[len(temp) // 2]
        temp = []
    return _data

filter_size = 7

#data = [26.5625, 26.5625, 26.5625, 26.5000, 26.5625, 26.5625, 26.5625, 26.5625, 26.5625, 26.5000, 26.5625, 26.5000, 26.5000, 26.5000, 26.5000, 26.5625, 26.5000, 26.5000, 26.5000, 26.5625, 26.5000, 26.5625, 26.5625]
#data = [26.5625, 26.5625, 26.5625, 26.5000, 26.5625, 26.5625, 26.5625, 2]
print(data)

filtered_data = median_filter(data, filter_size)

print(filtered_data)

'''
count = 0
with open('data_for_test.txt', "r") as f: # 400 to 750 
    for line in f:
        data.append(float(line.split()[0]))
        count = count + 1
        
        if count == 100:
            filtered_data = median_filter(data, filter_size)
            data = []
            with open('output_data_for_test.txt', "a") as g:
                for number in filtered_data:
                    g.write(str(number)+'\n')
                g.close()
            count = 0
            

    f.close()
print('**END**')
'''

'''
data = []
with open('small_data_for_test.txt', "r") as f: # 400 to 750 
    for line in f:
        data.append(float(line.split()[0]))

    f.close()

print('**Before**')

filtered_data = median_filter(data, filter_size)

print('**After**')

with open('output_data_for_test.txt', "w") as f:
    for number in filtered_data:
        f.write(str(number)+'\n')
    f.close()
print('**END**')
'''