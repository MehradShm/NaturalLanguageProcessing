import json
import re
from hazm import *
import heapq
import time
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np 

def get_data(file_address):
    with open(file_address,'r') as file_data:
        data = json.load(file_data)
        return data

def normalize_document(content):
    not_valid_characters = r'[^بهگزارشودیخنجظمستحلعثصپکفئطض‌آق۲۵۰چء\^ذغ۱۷۹۶۸ژ۴۳1496327805؟. ‌]'
    normalizer = Normalizer()
    contenr = normalizer.normalize(content)
    content = re.sub('\$[^ا-ی]+;',"",content)
    content = re.sub('\r\n',' ',content)
    content = re.sub('\d+/\d+|\d+\.\d+|\d+:\d+','^',content)
    content = re.sub(not_valid_characters,'',content)
    content = re.sub('[۰-۹]+',' N ',content)
    content = re.sub('[\d]+',' N ', content)
    content = re.sub('[\^]+',' N ',content)
    content = re.sub(' +', ' ', content)
    return content

def Tokenize_Document(content):
    return word_tokenize(content)

def apply_changes_to_term_frequencies(term_frequencies, tokens):
    for token in tokens:
        tmp = token
        if '_' in tmp:
            tmp = token.replace('_','‌')
        if tmp in term_frequencies.keys():
            term_frequencies[tmp] += 1
        else:
            term_frequencies[tmp] = 1
    return term_frequencies

def normalize_corpus(data):
    term_frequencies, total_tokens, tokenized_corpus = {}, 0, []
    for document in data:
        normalized_document = normalize_document(document)
        tokenized_document = Tokenize_Document(normalized_document)
        tokenized_corpus.append(tokenized_document)
        term_frequencies = apply_changes_to_term_frequencies(term_frequencies,tokenized_document)
    return term_frequencies, tokenized_corpus

def calculate_total_tokens(term_frequencies):
    total_tokens = 0
    for term in term_frequencies.keys():
        total_tokens += term_frequencies[term]
    return total_tokens

def calculate_top_tokens(term_frequencies):
    cumulative_sum = 0
    term_frequency_pairs, most_frequent_terms, verified_tokens = [], [], []
    for term in term_frequencies.keys():
        heapq.heappush(term_frequency_pairs,(((-1)*term_frequencies[term],term)))
    for i in range(10000):
        most_frequent_terms.append(heapq.heappop(term_frequency_pairs))
        verified_tokens.append(most_frequent_terms[-1][1])
        cumulative_sum += (-1) * most_frequent_terms[-1][0]
    return most_frequent_terms,verified_tokens, cumulative_sum

def output_most_terms(most_frequent_terms,total_tokens):
    with open("most_frequent.txt",'w') as most_terms:
        for pair in most_frequent_terms:
            most_terms.write(pair[1] + "  :  " + ' %'+ str(((-1)*pair[0])*100/total_tokens) + '\n')

def is_unknown(token):
    global verified_tokens
    if (token in verified_tokens) or token == '.' or token =="؟":
        return token
    return 'UNK'

def make_sentences(data):
    global term_frequencies
    term_frequencies['UNK'] = 0
    sentences = []
    for document in data:
        current_sentence = ''
        for token in document:
            checked_token = is_unknown(token)
            current_sentence += (checked_token + ' ')
            if checked_token == 'UNK':
                term_frequencies[checked_token] +=1
            elif checked_token == '.' or checked_token == '؟':
                sentences.append(current_sentence)
                current_sentence = ''
        sentences.append(current_sentence)
    return sentences

def output_sentences(sentences):
    with open("sentences.txt",'w') as output:
        for sentence in sentences[:-1]:
            output.write('<s>'+ ' ' + sentence + '</s>' + ' \n')
        output.write('<s>'+ ' ' + sentences[-1] + '</s>')

def draw_plot(most_frequent_terms):
    x = [np.log10((most_frequent_terms[i][0] * -1)) for i in range(5000)]
    y = [np.log10(i+1) for i in range(5000)]
    plt.plot(x,y,'y', label = "power's law")
    plt.legend()
    plt.show()

if __name__ == '__main__':
    start_time = time.time()
    print("Started")
    input_data = get_data("/Users/mehrad/programmings/nlp/codes/data/corpus/train.json")
    term_frequencies, tokenized_corpus = normalize_corpus(input_data)
    total_tokens = calculate_total_tokens(term_frequencies)
    most_frequent_terms, verified_tokens, unknown_frequency = calculate_top_tokens(term_frequencies)
    most_frequent_terms.insert(0,(100 - unknown_frequency,"UNK"))    
    print(len(term_frequencies), " !!!! " , total_tokens)
    draw_plot(most_frequent_terms)
    output_most_terms(most_frequent_terms, total_tokens)
    print("Frequent Terms Written...")
    sentences = make_sentences(tokenized_corpus)
    print("Sentences Made...")
    output_sentences(sentences)
    end_time = time.time()
    print("execution time:", end_time-start_time )




