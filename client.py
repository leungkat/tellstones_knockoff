import socket
import sys

#global variables
line = []
#0 for face up, 1 for face down
pool = [["sword", 0], ["shield", 0], ["knight", 0], ["king", 0], ["hammer", 0], ["scales", 0], ["flag", 0]]
list_of_stones = ["sword", "shield", "knight", "king", "hammer", "scales", "flag"]
menu = "Choose an action: \n1. Place \n2. Hide \n3. Swap \n4. Challenge \n5. Peek \n6. Boast \n"
game = True
numberHidden = 0
clientNumber = 0
MY_POINTS = 0
OPP_POINTS = 0
turn = 1


def printLine():
	print("============================LINE==================================")
	
	for x in line:
		if x[1] == 0:
			print("[ " + x[0] + " ]", end = " ")
		else:
			print("[ HIDDEN ]", end = " ")
	print()
	print("==================================================================")
	
if __name__ == "__main__":
	try:
		#checking for correct usage
		if len(sys.argv) != 5:
			print("python3 client.py –s <serverAddress> –p <serverPort>")
			sys.exit()

		#gathering information from command line
		UDP_IP = sys.argv[2]
		UDP_PORT = int(sys.argv[4])
		MESSAGE =  str.encode("register")

		#sending the message
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #internet, udp
		sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

		#confirming register message
		data, addr = sock.recvfrom(1024)
		clientNumber = int(data.decode("utf-8"))

		#----------------------------------------------------------------------------------------#
		
		endturn = False
		
		while game:
			
			if turn == clientNumber:
				printLine()
				action = input(menu)
				
				SEND_ACTION = ""
				
				if action == "1": #PLACE
					if len(pool) == 0:
						print("All stones have been placed!")
					else:
						SEND_ACTION = "PLACE "
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
								SEND_ACTION = SEND_ACTION + " " + str(choice)
							
						choice = pool.pop(choice-1)
						if len(line) == 0:
							line.append(choice) 
							SEND_ACTION = SEND_ACTION + " C"

						else:
							choose = False
							while choose == False:
								printLine()
								placement = input("Place on left or right of the line? \n1. Left \n2. Right \n")
								if placement == "1":
									line.insert(0, choice)
									choose = True
									SEND_ACTION = SEND_ACTION + " 1"
								elif placement == "2":
									line.append(choice)
									choose = True
									SEND_ACTION = SEND_ACTION + " 2"
								
				elif action == "2": #HIDE
					choose = False
					if len(line) == 0:
						print("There is nothing on the line")
						choose = True
					
					elif len(line) == numberHidden:
						print("All stones are hidden!")
						choose = True
						
					while choose == False:
						SEND_ACTION = "HIDE"
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
								SEND_ACTION = SEND_ACTION + " " + str(choice)
								
				elif action == "3": #SWAP
					if len(line) < 2:
						print("Not enough stones in the line to swap")
					else:
						SEND_ACTION = "SWAP"
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
						
						SEND_ACTION = SEND_ACTION + " " + str(stone1) + " " + str(stone2)
						
				elif action == "4": #CHALLENGE
					choose = False
					if numberHidden == 0:
						print("There are no hidden stones to challenge!")
						choose = True
					
					while choose == False: #remember choice-1 is the one we need to call
						SEND_ACTION = "CHALLENGE"
						choice = input("Choose a stone to challenge!")
						choice = int(choice)
						if(choice < len(line)+1) and (choice > 0) and (line[choice -1][1] == 1):
							choose = True
							SEND_ACTION = SEND_ACTION + " " + str(choice)
						else:
							print("Invalid selection!")
						
						line[choice-1][1] = 0
						numberHidden= numberHidden-1
					
				elif action == "5": #PEEK
				
					choose = False
					if len(line) == 0:
						print("There are no stones on the line!")
					elif numberHidden == 0:
						print("There are no hidden stones to peek at!")
					else:
						SEND_ACTION = "PEEK"
						while choose == False:
							choice = input("Choose a hidden stone to peek at!")
							choice = int(choice)
							
							if(choice < len(line)+1) and (choice > 0) and (line[choice -1][1] == 1):
								choose = True
								SEND_ACTION = SEND_ACTION + " " + str(choice)
							else:
								print("Invalid selection!")
						
						print("The stone at place " + str(choice) + " is " + line[choice-1][0] + "!")
					
				elif action == "6": #BOAST
					
					if numberHidden == 0:
						print("No stones are hidden!")
					else: 
						SEND_ACTION = "BOAST"
					
				else:
					print("Invalid input.")
				
				if SEND_ACTION != "":
					if turn == 1:
						turn = 2
					else:
						turn = 1
				
					sock.sendto(SEND_ACTION.encode(), (UDP_IP, UDP_PORT))
					printLine()
			else:#else wait your turn 
				print("Please wait your turn.")
				returnAction = False
				returnThis = ""
				data, addr = sock.recvfrom(1024)
				data = data.decode("utf-8").split()
				action = data[0] 
				
				if action == "PLACE":
					choice = int(data[1])
					choice = pool.pop(choice-1)
					if len(line) == 0:
						line.append(choice) 
						print("Opponent has placed " + choice[0] + " on the line!")
					else:
						placement = data[2]
						if placement == "1":
							line.insert(0, choice)
							print("Opponent has placed " + choice[0] + " on the left!")
						elif placement == "2":
							line.append(choice)
							print("Opponent has placed " + choice[0] + " on the right!")
					
				elif action == "HIDE":
					choice = int(data[1])
					line[choice-1][1] = 1
					numberHidden = numberHidden+1
					print("Opponent has hidden stone number " + str(choice)+ "!")
					
				elif action == "SWAP":
					stone1 = int(data[1])
					stone2 = int(data[2])
					swap = line[stone1-1]
					line[stone1 - 1]  = line[stone2 - 1]
					line[stone2 - 1] = swap
					print("Opponent has swapped stones " + str(stone1) + " and " + str(stone2)+ "!")
					
				elif action == "CHALLENGE":
					choice = int(data[1])
					print("Opponent has challenged you to guess the stone number " + str(choice) + "!")
					printLine()
					print("Guess the stone in place number " + str(choice))
					guess = input("1. sword \n2. shield \n3. knight \n4. king \n5. hammer \n6. scales \n7. flag\n")
					guess = int(guess)-1
					guess = list_of_stones[guess]
					
					if line[choice-1][0] == guess:
						print("That's correct!")
						MY_POINTS = MY_POINTS + 1
						returnThis = "CORRECT"
					else:
						print("That's incorrect. The answer is " + line[choice-1][0])
						OPP_POINTS = OPP_POINTS + 1
						returnThis = "WRONG"
					
					line[choice-1][1] = 0
					numberHidden= numberHidden-1
					returnAction = True
					
				elif action == "PEEK":
					print("Opponent has peeked at stone number " + data[1]+"!")
				elif action == "BOAST":
					returnAction = True
					
					print("Opponent is boasting!")
					choice = -1
					while (choice != 1) and (choice != 2) and (choice != 3):
						choice = input("Would you like to: \n1. Believe them \n2. Challenge them \n3. Steal the boast")
						choice = int(choice)
						
					if choice == 1:
						OPP_POINTS = OPP_POINTS + 1
						returnThis = "BELIEVE"
					elif choice == 2:
						returnThis = "PROVE"
					else:
						win = True
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
								win = False
								game = False
								OPP_POINTS = 3
								returnThis = "WIN"
								break
							i = i + 1
						if win:
							MY_POINTS = 3
							game = False
							returnThis = "LOSE"
				elif action == "CORRECT":
					print("Opponent has won your challenge!")
					OPP_POINTS = OPP_POINTS + 1
				elif action == "WRONG":
					print("Opponent has lost your challenge!")
					MY_POINTS = MY_POINTS + 1
				elif action == "BELIEVE":
					print("Opponent believes your boast!")
					MY_POINTS = MY_POINTS + 1
				elif action == "PROVE":
					returnAction = True
					print("Opponent has challenged your boast!")
					win = True
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
							win = False
							OPP_POINTS = 3
							returnThis = "WIN"
							break
						i = i + 1
					if win:
						MY_POINTS = 3
						game = False
						returnThis = "LOSE"
				elif action == "WIN":
					print("Opponent has stolen your boast and won!")
					MY_POINTS = 3
					game = False
				elif action == "LOSE":
					print("Opponent has stolen your boast and lost!")
					OPP_POINTS = 3
					game = False
						
				else:
					print("Error. Could not get opponent action.")
				
				
				if returnAction == False:
					if turn == 1:
							turn = 2
					else:
						turn = 1
				else:
					sock.sendto(returnThis.encode(), (UDP_IP, UDP_PORT))
			if MY_POINTS == 3 or OPP_POINTS == 3:
				game = False
		if MY_POINTS == 3:
			print("Congrats! You win!")
		else:
			print("You lose!")
	except KeyboardInterrupt: #handling ctrl+c
		print("terminating client...")	
		sys.exit()
