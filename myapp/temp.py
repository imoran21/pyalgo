with open('stock.txt') as f:

	a =  {  x.split("	")[0]: x.split("	")[1].strip('\n') for x in f}

	print a

 