import sys
arr = [x for x  in sys.stdin if x.isDigit()]
rotten = arr[0]
imdb=arr[1]
average=(imdb+rotten)//2
print("Average Movie Score is : {}".format(average))

