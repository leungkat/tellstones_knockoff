#placing things on the table
line = []
#0 for face up, 1 for face down
pool = [["sword", 0], ["shield", 0], ["knight", 0], ["king", 0], ["hammer", 0], ["scales", 0], ["flag", 0]]
list_of_stones = ["sword", "shield", "knight", "king", "hammer", "scales", "flag"]
menu = "Choose an action: \n1. Place \n2. Hide \n3. Swap \n4. Challenge \n5. Peek \n6. Boast \n"
game = True
numberHidden = 0

def printLine():
	print("============================LINE==================================")
	
	for x in line:
		if x[1] == 0:
			print("[ " + x[0] + " ]", end = " ")
		else:
			print("[ HIDDEN ]", end = " ")
	print()
	print("==================================================================")



while game:

	printLine()
	
	action = input(menu)
	
	if action == "1": #PLACE
	
		if len(pool) == 0:
			print("All stones have been placed!")
		else:
			choose = False
			while choose == False:
				print("Choose a stone from the pool: " )
				i = 1
				for x in pool:
					numbering = str(i)+". "
					print( numbering + x[0] )
					i = i + 1
				choice = input()
				choice = int(choice)
				
				if (choice > 0) and (choice < 8):
					choose = True
				
			choice = pool.pop(choice-1)
			if len(line) == 0:
				line.append(choice)

			else:
				choose = False
				while choose == False:
					printLine()
					placement = input("Place on left or right of the line? \n1. Left \n2. Right \n")
					if placement == "1":
						line.insert(0, choice)
						choose = True
					elif placement == "2":
						line.append(choice)
						choose = True
					
	elif action == "2": #HIDE
		choose = False
		if len(line) == 0:
			print("There is nothing on the line")
			choose = True
		
		elif len(line) == numberHidden:
			print("All stones are hidden!")
			choose = True
			
		while choose == False:
			print("Choose a stone to hide: ")
			i = 1
			for x in line:
				numbering = str(i) + ". "
				print(numbering, end = " ")
				i = i + 1
			choice = input()
			choice = int(choice)
			if (choice < len(line)+1) and (choice > 0):
				if line[choice-1][1] == 1:
					print("Already hidden!")
				else:
					choose = True
					line[choice-1][1] = 1
					numberHidden = numberHidden+1
	elif action == "3": #SWAP
		if len(line) < 2:
			print("Not enough stones in the line to swap")
		else:
			choose = False
			while choose == False:
				print("Choose a stone to swap")
				i = 1
				for x in line:
					numbering = str(i) + ". "
					print(numbering, end = " ")
					i = i + 1
				stone1 = input()
				stone1 = int(stone1)
				if (stone1 < len(line)+1) and (stone1 > 0):
					choose = True
			
			choose = False
			while choose == False:
				print("Choose a stone to swap with")
				i = 1
				for x in line:
					if i is not stone1:
						numbering = str(i) + ". "
						print(numbering, end = " ")
						i = i + 1
				stone2 = input()
				stone2 = int(stone2)
				if (stone2 < len(line)+1) and (stone2 > 0):
					choose = True
			
			swap = line[stone1-1]
			line[stone1 - 1]  = line[stone2 - 1]
			line[stone2 - 1] = swap
			
	elif action == "4": #CHALLENGE
		choose = False
		if numberHidden == 0:
			print("There are no hidden stones to challenge!")
			choose = True
		
		while choose == False: #remember choice-1 is the one we need to call
			choice = input("Choose a stone to challenge!")
			choice = int(choice)
			if(choice < len(line)+1) and (choice > 0) and (line[choice -1][1] == 1):
				choose = True
			else:
				print("Invalid selection!")
		if numberHidden is not 0:
			printLine()
			print("Guess the stone in place number " + str(choice))
			guess = input("1. sword \n2. shield \n3. knight \n4. king \n5. hammer \n6. scales \n7. flag\n")
			guess = int(guess)-1
			guess = list_of_stones[guess]
			
			if line[choice-1][0] == guess:
				print("That's correct!")
			else:
				print("That's incorrect. The answer is " + line[choice-1][0])
			
			line[choice-1][1] = 0
			numberHidden= numberHidden-1
		
	elif action == "5": #PEEK
	
		choose = False
		if len(line) == 0:
			print("There are no stones on the line!")
		elif numberHidden == 0:
			print("There are no hidden stones to peek at!")
		else:
			while choose == False:
				choice = input("Choose a hidden stone to peek at!")
				choice = int(choice)
				
				if(choice < len(line)+1) and (choice > 0) and (line[choice -1][1] == 1):
					choose = True
				else:
					print("Invalid selection!")
			
			print("The stone at place " + str(choice) + " is " + line[choice-1][0] + "!")
		
	elif action == "6": #BOAST
		win = True
		if numberHidden == 0:
			print("No stones are hidden!")
			
		else:
			i = 1
			for x in line:
				print("Guess the stone in place " + str(i))
				guess = input("1. sword \n2. shield \n3. knight \n4. king \n5. hammer \n6. scales \n7. flag\n")
				guess = int(guess)-1
				guess = list_of_stones[guess]
				
				if line[i-1][0] == guess:
					print("That's correct!")
				else:
					print("That's incorrect. The answer is " + line[i-1][0])
					print("You lose!")
					win = False
					break
				i = i + 1
			if win:
				print("All correct! You win!")
			break
	else:
		print("Invalid input.")