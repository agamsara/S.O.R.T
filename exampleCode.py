import sys
imdb = [x for x  in sys.stdin if x.isDigit()]
rotten =  [x for x  in sys.stdin if x.isDigit()]

print("Average Movie Score is : %d",(imdb+rotten)//2)

