import nltk
import emoji

#open pos lexicon
with open("pos_lex.txt", "r") as f:
    pos_lex = f.read().split("\n")
f.close()

#open neg lexicon
with open("neg_lex.txt", "r") as f:
    neg_lex = f.read().split("\n")
f.close()

#open negators
with open("negators.txt", "r") as f:
    negators = f.read().split("\n")
f.close()

#open intensifiers
with open("intensifiers.txt", "r") as f:
    intensifiers = f.read().split("\n")
f.close()

#open diminishers
with open("diminishers.txt", "r") as f:
    diminishers = f.read().split("\n")
f.close()

#open pos emojis 
with open("pos_emojis.txt", "r", encoding = "utf-8") as f:
    pos_emojis = f.read().split("\n")
f.close()

#open neg emojis 
with open("neg_emojis.txt", "r", encoding = "utf-8") as f:
    neg_emojis = f.read().split("\n")
f.close()

def tag_negations(text): #detect negation scope and tag sentiment words under scope of negation
    negation = False
    delims = "?.,!:;"
    result = []
    for word in text:
        stripped = word.strip(delims).lower()
        negated = "NEG_" + stripped if negation else stripped
        result.append(negated)
        if word in negators: 
            negation = not negation

        if any(c in word for c in delims):
            negation = False    
    return result

# open document
f1 = open("doc.txt", encoding="utf8")
doc = f1.read()

print("~~~Original document~~~\n" + doc + "\n")

# preprocessing of document
doc = doc.lower() #lower case conversion
doc = nltk.word_tokenize(doc) #tokenization

#stopwords removal
stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'other', 'some', 'such', 'only', 'own', 'same', 'so', 'than', 's', 't', 'can', 'will', 'just', 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y']
doc = [i for i in doc if i not in stopwords]

#tag negations (this will append "NEG_" to all words after a negation in the sentence until the end of sentence punctuation symbol)
doc = tag_negations(doc)
doc = [w for w in doc if w != "" and w != "NEG_"]

print("~~~Preprocessed document~~~\n" + str(doc) + "\n")

polarity_label = ""
polarity_score = 0

print("~~~Matches with lexicon~~~")

#compute polarity_score in an open ended range
for i in range(len(doc)):
    term = doc[i]
    
    #checks to see if emojis appear in doc    
    if term in emoji.UNICODE_EMOJI:
        if term in pos_emojis:
            polarity_score += 2
            print("pos emoji detected: ", term, "[+2]")            
        if term in neg_emojis:
            polarity_score -= 2
            print("neg emoji detected: ", term, "[-2]")     
    
    #checks to see if intensifier+term combo appears, and boosts score of term to +2
    if doc[i-1] in intensifiers and term in pos_lex:
        polarity_score += 2
        print("intensifier + pos_match: ", doc[i-1], term, "[+2]")
    
    #checks to see if diminisher+term combo appears, and diminishes score of term to +0.5    
    elif doc[i-1] in diminishers and term in pos_lex:
        polarity_score += 0.5
        print("diminisher + pos_match: ", doc[i-1], term, "[+0.5]")
    
    #checks if term appears in pos_lex, and gives a score of +1
    elif str(term) in pos_lex:
        polarity_score += 1
        print("pos_match: " + str(term), "[+1.0]")
    
    #checks to see if intensifier+term combo appears, and boosts score of term to -2
    if doc[i-1] in intensifiers and term in neg_lex:
        polarity_score -= 2
        print("intensifier + neg_match: ", doc[i-1], term, "[-2]")
    
    #checks to see if diminisher+term combo appears, and diminishes score of term to -0.5    
    elif doc[i-1] in diminishers and term in neg_lex:
        polarity_score -= 0.5
        print("diminisher + neg_match: ", doc[i-1], term, "[-0.5]")
    
    #checks if term appears in pos_lex, and gives a score of -1
    elif str(term) in neg_lex:
        polarity_score -= 1
        print("neg_match: " + str(term) + "[-1]")            

   
    #handle negation by appending "NEG_" to any term under negation scope, and flipping its polarity 
    for posterm in pos_lex:
        if str(term) == "NEG_"  + posterm:
            polarity_score -= 1
            print("neg match (negated positive): " + str(term) + " [-1]")
    
    for negterm in neg_lex:
        if str(term) == "NEG_" + negterm:
            polarity_score += 1
            print("pos match (negated negative): " + str(term) + " [+1]")

print("\n")

if polarity_score > 5:
    polarity_score = 5
if polarity_score < -5:
    polarity_score = -5

print("Final polarity score (in range +5, -5): ", polarity_score)

#label doc with polarity based on matches with lexicon
if polarity_score > 0:
    polarity_label = "POSITIVE"
elif polarity_score < 0:
    polarity_label = "NEGATIVE"
else:
    polarity_label = "OBJECTIVE"

print("Final polarity label: " + polarity_label)
