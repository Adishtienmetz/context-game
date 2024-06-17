import spacy

nlp = spacy.load('en_core_web_md')

best_guesses = []
best_guesses = [(None, -1000) for i in range(5)]

def semantic_similarity(word1, word2):
    token1 = nlp(word1)
    token2 = nlp(word2)
    return token1.similarity(token2)

def update_best_guesses(guess, score):
    length = len(best_guesses) - 1
    if(best_guesses[length][1] < score):
        best_guesses[length] = (guess, score)
    i = length - 1
    while(i >= 0 and best_guesses[i][1] < score):
        best_guesses[i], best_guesses[i+1] = best_guesses[i+1], best_guesses[i]
        i -= 1

target_word = "school"

while(True):
    print("guess a word!")
    guess = input()
    if guess == target_word:
        print('you won!')
        break
    score = 100 * semantic_similarity(target_word, guess)
    print("guess score: " + str(score))
    update_best_guesses(guess, score)
    for num, (guess, score) in enumerate(best_guesses):
        if(guess):
            print('' + str(num+1) + '. ' + str(guess) + ', score: ' + str(score))
    print('---------------------------------------------------')
    print()