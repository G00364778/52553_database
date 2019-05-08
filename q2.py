
# Main function
def main():
	# Initialise array
	array = []

	display_menu()
	
	while True:
		choice = input("Enter choice: ")
		
		if (choice == "1"):
			array = fill_array()
			display_menu()
		elif (choice == "2"):
			print(array)
			display_menu()
		elif (choice == "3"):
			find_gt_in_array(array)
			display_menu()
		elif (choice == "4"):
			break
		else:
			display_menu()
			
			
def fill_array():
# Write the necessary code to fill the array.
# -1 should not be part of the array

    arr=[]
    while True:
        choice=input("Enter value to add, -1 to end: ")
        if choice == "-1":
            return arr
        else:
            if choice.isnumeric()==True:
                arr.append(int(choice))
            else:
                print("Not a number, try again!")
       

def find_gt_in_array(array):
# Write the necessary code to get a number from the user
# and print out all numbers in the array that are greater
# than this number
    biggerVals=[]
    while True:
        choice=input("Find numbers greater than?: ")
        if choice.isnumeric() == True:
            biggerThan=int(choice)
            break
        else:
            print("Not a number, try again")
    for i in range(len(array)):
        if array[i]>biggerThan:
            biggerVals.append(array[i])
    print(biggerVals)


def display_menu():
    print("")
    print("MENU")
    print("=" * 4)
    print("1 - Fill Array")
    print("2 - Print Array")
    print("3 - Find > in Array")
    print("4 - Exit")

if __name__ == "__main__":
	# execute only if run as a script 
	main()
