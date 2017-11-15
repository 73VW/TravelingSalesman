import sys, os
from City import City

cityList = []

def ga_solve(file=None,gui=True,maxtime=0):
	return 0

def fillArrayWithData(fileName):
	with open(fileName) as f:
		for line in f:
			dataList = line.split()
			city = City(dataList[0],dataList[1],dataList[2])
			cityList.append(city)

if __name__ == '__main__':
	fillArrayWithData(sys.argv[1])