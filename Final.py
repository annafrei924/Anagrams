#"I hereby certify that this program is solely the result of my own work and is in compliance with the Academic Integrity policy of the course syllabus and the academic integrity policy of the CS department.”


import random
import Draw
import time

#all of these variables approved on 12/19/22 by Professor Broder
MAX_LETTERS = 8 #Maximum words length
MAX_TIME = 40 #gametime is for one minute
AVG_ANAGRAMS = 10 #amount of anagrams taken to find average
allWords = [] #list of words between 3 and MAX_LETTERS characters

#turns file of words into a list
def wordsToList(MAX_LETTERS): 
    #loop through and get rid of extra spaces/new lines
    with open("words.txt", "r") as a:
        for line in a.readlines(): 
            line = line.strip() 
            #if its appropriate length, all uppercase append to list of valid words
            if len(line) >= 3 and len(line) <= MAX_LETTERS: 
                allWords.append(line.upper()) 
    return allWords

#gets start word of MAX_LETTERS
def getTargetWord(MAX_LETTERS): 
    targetWord = ""
    #find random word until start word is right length
    while len(targetWord) != MAX_LETTERS: 
        targetWord = allWords[random.randint(0, len(allWords))] 
    return targetWord

#gets all possible anagrams of a word
def allPosAnswers(targetWord): 
    #tally the letters in the targetWord
    targetWordTally = {}
    for letter in targetWord:
        if letter in targetWordTally: targetWordTally[letter] += 1
        else: targetWordTally[letter]= 1   
    
    #create list of anagrams for a given word
    anagramList = [] 
    
    #loop through allWords
    for word in allWords: 
        counter = 0
        # tallies for each letter in the word in allWord
        wordTally = {} 
        for letter in word: 
            if letter in wordTally: wordTally[letter] += 1
            else: wordTally[letter] = 1
            
        #loops through letters again, and if valid, add to counter
        for char in word:  
            if char in targetWord and wordTally[char] <= targetWordTally[char]: 
                counter += 1    
        #if every letter is valid, word is valid
        if counter == len(word): anagramList.append(word) 
    return anagramList
    

#finds the average amount of anagrams that can come from a word
def averageAnagrams(iterateAmount): 
    total = 0
    #loops through, get a targetword, & find all possible anagrams
    for i in range(iterateAmount): 
        word = getTargetWord(MAX_LETTERS) 
        total += len(allPosAnswers(word)) 
    #return the average
    return total/iterateAmount 
    

#makes the gameboard
def makeBoard(shufStartWord, score, timeRemaining, guess, goodWords):
    
    #set overall background
    green = Draw.color(144,187,162)
    Draw.setBackground(green)
    
    #draw "header"
    blue = Draw.color(70,135,137) 
    Draw.setColor(blue)
    Draw.rect(150, 650, 700, 70)
    Draw.setFontSize(38)
    Draw.string("UNSCRAMBLE ME: ", 330, 100)
    
    Draw.setFontSize(70)  
    Draw.setColor(Draw.BLACK)
    Draw.string(shufStartWord, 310, 155)

    #draw the bottom
    Draw.setFontSize(38)
    Draw.string("GUESS: " + guess, 180, 665)
    
    Draw.setFontSize(30)
    Draw.string("Score: " + str(score), 800, 730)
    Draw.string("Time: " + str(timeRemaining), 100, 730)
    Draw.string("ANAGRAMS", 430, 730)
    
    #draws the list of goodwords
    #initial position
    if len(goodWords) > 0:
        x = 50
        y = 250  
        sevens = [7, 15, 23, 30] 
        
        #draw each word & move accordingly
        for i in range(len(goodWords)):
            Draw.setColor(blue)
            Draw.setFontSize(38)
            Draw.string(goodWords[i], x, y)
            y += 50 #moves it down for the next word
                    
        #once hit the bottom of the page, move to the next column
            if i in sevens: 
                x += 250
                y = 250     
                
#determines if a key is valid            
def validKey(shufStartWord, guess, key):
    guesskey = guess + key
    counter = 0
    
    #tally startWord
    startWordTally = {} 
    for letter in shufStartWord:
        if letter in startWordTally: startWordTally[letter] += 1
        else: startWordTally[letter]= 1   
    
    #tally guess word
    guessTally = {} 
    for letter in guesskey:
        if letter in guessTally: guessTally[letter] += 1
        else: guessTally[letter]= 1  
        
    #loops through guess again & if the letter is valid, add to counter
    for char in guesskey: 
        if char in shufStartWord and guessTally[char] <= startWordTally[char]: 
            counter += 1
        #if every letter is valid, returns True
        if counter == len(guesskey): return True

#Erases saved pressed keys - code from Professor Broder
def flushKeys():
    while Draw.hasNextKeyTyped():
        newKey = Draw.nextKeyTyped()  
    
#playing the game
def gameplay(MAX_TIME, minAnagrams):
    
    #clear board
    flushKeys()
    
    #initialize score & goodWords
    score = 0
    goodWords = []
    guess = ""
    
    #get a random startWord & find # of anagrams for it
    startWord = getTargetWord(MAX_LETTERS) 
    possibleAnagrams = len(allPosAnswers(startWord)) 
    
    #chooses proper startWord
    while possibleAnagrams < minAnagrams: 
        startWord = getTargetWord(MAX_LETTERS)
        possibleAnagrams = len(allPosAnswers(startWord))
    
    #get all possible answers for startWord & shuffle it
    anagramList = allPosAnswers(startWord) 
    shufStartWord = "".join(random.sample(startWord, len(startWord)))
    
    #start the timer
    startTime = time.time()
    remainingTime = int(MAX_TIME- (time.time() - startTime)) 
        
    #during the game
    while remainingTime > 0: 
        #if a key was pressed, make all letters uppercase
        if Draw.hasNextKeyTyped():  
            key = Draw.nextKeyTyped().upper() 
            #if its a valid key add to word
            if validKey(shufStartWord, guess, key) == True: 
                guess += key 
            #if the user hits delete
            if key == "BACKSPACE":
                if len(guess) > 0:
                    guess = guess[:len(guess) - 1]
            #if enter was hit, check if it's a real word & change score
            if key == "RETURN": 
                if guess in anagramList and guess not in goodWords: 
                    goodWords.append(guess)
                    score += len(guess)*10
                #reset guess  
                guess = "" 
        
        #constantly reprint new board with the right time & goodWords & score
        Draw.clear()
        remainingTime = int(MAX_TIME- (time.time() - startTime)) 
        makeBoard(shufStartWord, score, remainingTime, guess, goodWords)
        Draw.show()
    
def main():

    wordsToList(MAX_LETTERS)
    Draw.setCanvasSize(1000,1000)  
    
    #instructions
    Draw.picture("ANAGRAMS.gif", 15, 0)
    time.sleep(7)
    Draw.clear()
    
    #find minimum amount of anagrams for a word to be valid
    minAnagrams = averageAnagrams(AVG_ANAGRAMS)
    
    #play the agme
    gameplay(MAX_TIME, minAnagrams) 
    
    #when the timer ends
    Draw.setFontSize(60)
    Draw.setColor(Draw.WHITE)
    Draw.string("CLICK ANYWHERE TO REPLAY", 50, 20)
  
    #allows for infinite replays if the user clicks
    while True: 
       if Draw.mousePressed(): 
           gameplay(MAX_TIME, minAnagrams)
           Draw.setFontSize(60) 
           Draw.setColor(Draw.WHITE)
           Draw.string("CLICK ANYWHERE TO REPLAY", 50, 20)  
main()
