# =============================================================================
# Expanding seeds into a lexicon using semantic relations from WordNet
# Updated Nov 5, 2020
# =============================================================================

from nltk.corpus import wordnet as wn
import itertools
import time

start_time = time.time()

def get_antonyms(syn):
    return set(itertools.chain(*[[a.synset() for a in l.antonyms()] for l in syn.lemmas()]))

def expansion(iterations, pos_seed_set, neg_seed_set): #expansion function

    for x in range(iterations): #define number of iterations

        f = open("output_pos.txt", "a") ###################CHANGE TO YOUR OWN FILE PATH
        f.write("\n" + "ITERATION: " + str(x+1) + "\n")

        f2 = open("output_neg.txt", "a") ###################CHANGE TO YOUR OWN FILE PATH
        f2.write("\n" + "ITERATION: " + str(x+1) + "\n")

        temp_pos_seed_set = []
        temp_neg_seed_set = []
        
        for pos_syn in pos_seed_set: #for each syn in pos seed set
                temp_pos_seed_set += pos_syn.also_sees() #add connected syns to pos seed set via also_sees relation
                temp_pos_seed_set += pos_syn.similar_tos() #add connected syns to pos seed set via similar_tos relation
                temp_neg_seed_set += get_antonyms(pos_syn) #add connected syns to neg seed set via antonym relation


        for neg_syn in neg_seed_set:
                temp_neg_seed_set += neg_syn.also_sees() #add connected syns to pos seed set via also_sees relation
                temp_neg_seed_set += neg_syn.similar_tos() #add connected syns to pos seed set via similar_tos relation
                temp_pos_seed_set += get_antonyms(neg_syn) #add connected syns to pos seed set via antonym relation
            

        pos_seed_set += set(temp_pos_seed_set)
        neg_seed_set += set(temp_neg_seed_set)
        
        f.write(str(sorted(set(pos_seed_set)))) #write expanded seed sets to file
        f.write("\n--->")
        f.write("size of set:" + " " + str(len(set(pos_seed_set))))
        f.close()  
        print(str(set(sorted(pos_seed_set))), "\n") ##verbose
        
        f2.write(str(sorted(set(neg_seed_set))))
        f2.write("\n--->")
        f2.write("size of set:" + " " + str(len(set(neg_seed_set))))
        f2.close()   
        print(str(set(neg_seed_set)), "\n") ##verbose            
        
#define initial seed sets
pos_seed_set =[]
neg_seed_set = []

with open("input_pos.txt", "r") as f3: ###################CHANGE TO YOUR OWN FILE PATH
    pos_seed_set = f3.read().split(", ")
pos_seed_set = [wn.synset(i[8:-2]) for i in pos_seed_set]

with open("input_neg.txt", "r") as f4: ###################CHANGE TO YOUR OWN FILE PATH
    neg_seed_set = f4.read().split(", ")
neg_seed_set = [wn.synset(i[8:-2]) for i in neg_seed_set]

iterations = 4 #define expansion iterations

expansion(iterations, pos_seed_set, neg_seed_set) #call expansion function

print("-----Execution time: %s seconds-----" % (time.time() - start_time))
