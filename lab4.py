import utilities as ut

def parse_story(file_name):
    t = open(file_name, "r")

    text = t.read()

    for char in ut.BAD_CHARS:
        text = text.replace(char, '')
        
    for char in ut.VALID_PUNCTUATION:
        text = text.replace(char, " " + char + ' ')

    temp = text.split(" ")
    result = []

    for word in temp:
        word = word.lower()
        result.append(word)

    return result

def get_prob_from_counts(counts):
    total = sum(counts)
    result = []

    for number in counts:
        result.append(number/total)

    return result

def build_ngram_counts(words, n):
    #create result dictionary to be returned
    result = {}
    #for loop iterates through every valid word and inserts stuff in result as needed
    for index in range(len(words) - n):
        temp = [] #list to store values to be made into tuple for key
        
        for num in range(0, n): # for loop adds n words to temp list 
            temp.append(words[index + num])

        key = tuple(temp) # key value created

        value = words[index + n] # finds word after tuple and assigns to value

        if key in result.keys(): # checks if key is already in dictionary

            if value in result[key][0]:

                spot = result[key][0].index(value) #assigns spot where value is in result_value

                result[key][1][spot] += 1 #increases number associated with that value

            else:
                #adds value to result value lists
                result[key][0].append(value)
                result[key][1].append(1)
        else:
            result.update({key: [[value],[1]]})

    for key in result.keys():
        result[key][0], result[key][1] = (list(t) for t in zip(*sorted(zip(result[key][0], result[key][1]))))
    
    print(result)

def prune_ngram_counts(counts, prune_len):

    for key in counts.keys(): # iterates through every key in dictionary
    
        value_count_list = counts[key][1]
        value_word_list = counts[key][0]
        #variables to easily access list of counts and words for current key
        
        if len(value_count_list) > prune_len: #checks if old values are longer than prune len

            new_value = [[],[]]
            #variables for new value for key
            
            condition = False

            add_index = 0

            while not condition:
                new_value[0].append(value_word_list[add_index])
                new_value[1].append(value_count_list[add_index])
                add_index += 1

                try: value_count_list[add_index]

                except IndexError: break
                
                condition = ((value_count_list[add_index] < min(new_value[1])) & (len(new_value[0]) > prune_len - 1))
            counts[key] = new_value

    return counts

def probify_ngram_counts(ngram_counts):

    for key in ngram_counts.keys(): # iterates through every key in dictionary

        ngram_counts[key][1] = get_prob_from_counts(ngram_counts[key][1]) # turns counts into probabilities

    return ngram_counts

def gen_bot_list(ngram_model, seed, num_tokens = 0):
    result = [] # creates empty list as result variable

    current_ngram = seed# creates current ngram variable to be used for adding shit to list as seed (1st shit)
    for word in current_ngram:
        result.append(word) #adds seed to result

    if num_tokens == 0: #what to do if num_tokens is zero
        result = []

    elif len(result) >= num_tokens: #what to do if result longer than num_tokens
        result = result[-(num_tokens):]

    else: #what to do if result shorter than num_tokens
        condition = False
        condition = (len(result) >= num_tokens or (not (tuple(current_ngram) in ngram_model.keys())))
        #sets up condition for while loop

        while not condition: #while loop keeps adding next stuff to list as long as next element doesn't meet condition

            result.append(ut.gen_next_token(tuple(current_ngram), ngram_model))

            current_ngram = result[-(len(current_ngram)):]

            condition = (len(result) >= num_tokens or (not (tuple(current_ngram) in ngram_model.keys())))

    return result

def gen_bot_text(token_list, bad_author):

    result = "" # result empty string created
    
    if bad_author == True:#what to do if bad_author is true

        for index in range(len(token_list)): # loops through list adding everyhting
            result = result + " " + token_list[index]

    else: #what to do if bad_author is not true

        for index in range(len(token_list)): #loops through list adding everything with proper grammar
            cap = []
            
            for word in ut.ALWAYS_CAPITALIZE:
                cap.append(word.lower())

            if token_list[index] in ut.VALID_PUNCTUATION:
                result = result + token_list[index]

            elif index == 0:
                result = result + token_list[index].capitalize()

            elif ((token_list[index - 1] in ut.END_OF_SENTENCE_PUNCTUATION) or (token_list[index] in cap)):
                result = result + " " + token_list[index].capitalize()

            else:
                result = result + " " + token_list[index]

    return result
                    
if (__name__ == "__main__"):
    #ngram_model = {('the', 'child'): [['will', 'can', 'may'], [0.5, 0.25, 0.25]],  ('child', 'will'): [['the'], [1.0]],  ('will', 'the'): [['child'], [1.0]],  ('child', 'can'): [['the'], [1.0]],  ('can', 'the'): [['child'], [1.0]],  ('child', 'may'): [['go'], [1.0]],  ('may', 'go'): [['home'], [1.0]],  ('go', 'home'): [['S.'], [1.0]] }
    words = ['the', 'child', 'will', 'go', 'out', 'to', 'play', ',', 'and', 'the', 'child', 'can', 'not', 'be', 'sad', 'anymore', '.', 'sex']
    token_list = parse_story('308.txt')
    #print(parse_story('308.txt'))
    print(gen_bot_text(token_list, False))
    #gen_bot_text(token_list, False)