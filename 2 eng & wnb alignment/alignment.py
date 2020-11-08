from nltk.corpus import wordnet as wn

pos_seed_set = []
neg_seed_set = []

with open("eng_pos.txt", "r") as f1: ###################CHANGE TO YOUR OWN FILE PATH
    pos_seed_set = f1.read().split(", ")
pos_seed_set = [wn.synset(i[8:-2]) for i in pos_seed_set]

with open("eng_neg.txt", "r") as f2: ###################CHANGE TO YOUR OWN FILE PATH
    neg_seed_set = f2.read().split(", ")
neg_seed_set = [wn.synset(i[8:-2]) for i in neg_seed_set]

bahasa_pos = []
bahasa_neg = []

for pos_syn in pos_seed_set: #get all bahasa synsets
    for lemma in pos_syn.lemma_names("zsm"):
        bahasa_pos += [lemma]
print(set(bahasa_pos))
print(len(set(bahasa_pos)))

for neg_syn in neg_seed_set:
    for lemma in neg_syn.lemma_names("zsm"):
        bahasa_neg += [lemma]
print(set(bahasa_neg))
print(len(set(bahasa_neg)))

f3 = open("bahasa_pos.txt", "a") #print all bahasa words to file
for w_pos in set(bahasa_pos):
    f3.write(w_pos)
    f3.write("\n")
f3.close()

f4 = open("bahasa_neg.txt", "a") 
for w_neg in set(bahasa_neg):
    f4.write(w_neg)
    f4.write("\n")
f4.close()
