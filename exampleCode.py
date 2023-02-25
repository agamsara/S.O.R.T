import sys
imdb = [x for x  in sys.stdin if x.isDigit()]
rotten =  [x for x  in sys.stdin if x.isDigit()]
average=(imdb+rotten)//2
print("Average Movie Score is : {}".format(average))

