these are the projects that i made while learning the cs50 ai course

-degrees: this program runs bfs algorithm on some csv data (movies: this is the movies csv, people: this is the actors csv, stars: this csv says which actors 
act in which mocvies) you need to enter two actors names from the people csv and you will get the connection between them

-to try it write this command in terminal:
 python degrees.py (small or large (these are the sizes of data you i have in the csv))

then the program will ask you to type two actors names so you can see them in the people csv and get the output of it

----------------------------------------------------------------------------------------------------------------------------------------------------
-tictactoe: a tictactoe game against an AI, this program uses minimax algorithm

-to try it write this command in terminal:
 python runner.py

then the program will ask you which side do you want (X or O)

----------------------------------------------------------------------------------------------------------------------------------------------------
-knights: this is the knights and knaves game, it takes some sentences from people and finds whos telling the truth and whos not

-to try it write this command in terminal: 
 python puzzle.py

then it will run four different puzzles that i made

----------------------------------------------------------------------------------------------------------------------------------------------------
-minesweeper: a minesweeper puzzle with an AI that helps you, if you click ai help it will make a random move if there is no safe move or a sefe move

-to try it write this command in terminal: 
 python runner.py

----------------------------------------------------------------------------------------------------------------------------------------------------
-pagerank: a page ranking program that takes a corpus that has some pages as input and finds the ranks of these pages importance with two algorithms
the first one is the sample page rank algorithm and the other is the iterate page rank

-to try it write this command in terminal: 
 python pagerank.py (corpus0 or corpus1 or corpus2)

then the program will give you the pagerank using the two algorithms (sample, iterate)

----------------------------------------------------------------------------------------------------------------------------------------------------
-pagerank: a page ranking program that takes a corpus that has some pages as input and finds the ranks of these pages importance with two algorithms
the first one is the sample page rank algorithm and the other is the iterate page rank

-to try it write this command in terminal: 
 python pagerank.py (corpus0 or corpus1 or corpus2)

then the program will ask you which side do you want (X or O)

----------------------------------------------------------------------------------------------------------------------------------------------------
-heredity: a program that takes as input a family data annd finds the probability of getting the gene from the mother or the father for all the sons

-to try it write this command in terminal: 
 python heredity.py (data/family0.csv or data/family1.csv or data/family2.csv)

then the program will give you the probability of all the children and the parents

----------------------------------------------------------------------------------------------------------------------------------------------------
-crossword: a crossword puzzles solver that takes a puzzle structure and a words file then it solves the puzzle according to the words from the file 
and you can put an image name with png type and get the solved puzzle as an image too in the same folder of the project

-to try it write this command in terminal:
 python generate.py (data/structure0.txt or data/structure1.txt or data/structure2.txt) (data/words0.txt or data/words1.txt or data/words2.txt) (output.png: optional)

then the program will give you a solved crossword puzzle (the puzzle may have some other solutions)

----------------------------------------------------------------------------------------------------------------------------------------------------
-shopping: a shopping program for a shopping web that has a csv with the information about a lot of users for example (BounceRates, ExitRates and else more) and wants to make an algorithm that sees if the user will complete a purchase or not by spliting the features and labels to train, test data and then fit an algorithm using the k-nearest neighbours and see the true predictions rate 

-to try it write this command in terminal: 
 python shopping.py shopping.csv

then the program will show you the true positive and true negative rates (i used k- nearest neighbour with n_neighbours = 1 you can use it with any other number and you will see higher rate than mine with the one nearest neighbor)

----------------------------------------------------------------------------------------------------------------------------------------------------
-nim: a nim game project that works with reinforcement, it trains the AI by letting him play against itself and he learns the best moves he can do then the AI plays against a human. You can choose how many times the AI should train

-to try it write this command in terminal:
 python play.py

 then the program will let the AI trains and after he finishes it will let you play against him

----------------------------------------------------------------------------------------------------------------------------------------------------
-traffic: a neural network model that reads 43 different street sign folders each folder contains a lot of different images of the same sign and then spliting the data to train and test, make the model with different layers, train it on the train data and last run it on the test data to see the accuracy

-to try it write this command in terminal(and you need to put a folder with different folders that contains images):
 python traffic.py (your folder name)

 then the program will give you the accuracy of the neural network
 NOTE: I didnt add the folder i have because it contains 43 folders with 150 images in each folder
 
 ----------------------------------------------------------------------------------------------------------------------------------------------------
