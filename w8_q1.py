'''
Applied Databases - Topic 8 Exercise Sheet 
 
1. Write a Python program that has 2 arrays in the main function: 
    • One containing several elements which are numbers. 
    • The other empty. 

Write another function which accepts a number as a parameter and returns the number doubled. 
 
The main function should call this function for each element of the 1st array and populate the 2nd array with the doubled values. 
When the 2nd array is full it should be printed out. 
 
'''

def doublenum(num):
    return num*2

def main():
    arr1=[1,3,4,6,8,9,14,2]
    arr2=[]
    for i in range(len(arr1)):
        arr2.append(doublenum(arr1[i]))
    print(arr2)

if __name__ == "__main__":
    main()