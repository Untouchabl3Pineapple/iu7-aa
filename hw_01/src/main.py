def odd_even(data):
	n = len(data)
	isSorted = 0

	while isSorted == 0:
		isSorted = 1
        
		for i in range(1, n - 1, 2):
			if data[i] > data[i + 1]:
				data[i], data[i + 1] = data[i + 1], data[i]
				isSorted = 0					 
		for i in range(0, n - 1, 2):
			if data[i] > data[i + 1]:
				data[i], data[i + 1] = data[i + 1], data[i]
				isSorted = 0
	return data

print(odd_even([1, 34 ,-23, 6, 0]))