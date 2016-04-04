#!/usr/bin/python

import csv

### Getting the columns product_title and search_term in a two lists
def read_csv(filename):
	product_title, product_description, search_term = [], [], []
	combined, original_data = [], []
	with open(filename, 'rb') as csvfile:
		spamreader = csv.reader(csvfile)
		for row in spamreader:
			original_data.append(row)
			product_title.append(row[2])
			product_description.append(row[3])
			search_term.append(row[4])

	### the header of the column is ignored and all the three lists are combined to one
	combined.append(product_title[1:])
	combined.append(product_description[1:])
	combined.append(search_term[1:])
	return combined, original_data

### To get the words in the entry
def get_words_in_query(listtomodify):
	word_list = listtomodify.split(" ")
	return word_list

### To calculate OR score between a query and a string
def calculate_OR(search_query, search_in_string):
	current_max = 0
	search_in_string = [x.lower() for x in search_in_string]
	search_query = [x.lower() for x in search_query]
	#print search_query
	for word in search_query:
		word_count = search_in_string.count(word)
		if word_count >  current_max:
			current_max = word_count
	#print current_max
	return current_max

### To calculate AND score between a query and a string
def calculate_AND(search_query, search_in_string):
	search_in_string = [x.lower() for x in search_in_string]
	search_query = [x.lower() for x in search_query]
	for word in search_query:
		if word not in search_in_string:
			return 0
	return 1

def write_csv(filename, original_data, or_score_title, or_score_desc, and_score_title, and_score_desc):
	with open(filename, 'w') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',')
		temp = original_data[0] + ['or_title'] + ['or_description'] + ['and_title'] + ['and_description']
		spamwriter.writerows([temp])
		for i in range(len(or_score_title)):
			spamwriter.writerows([original_data[i+1] + [str(or_score_title[i])] + [str(or_score_desc[i])] + [str(and_score_title[i])] + [str(and_score_desc[i])]])
		
def main():
	### entry_list[0] -> product_title
	### entry_list[1] -> product_description
	### entry_list[2] -> search_term
	entry_list, original_data = read_csv("train_combined.csv")

	entry_word_list = []
	###Separating out words in string
	for column in range(len(entry_list)):
		temp = []
		for row in range(len(entry_list[column])):
			temp.append(get_words_in_query(entry_list[column][row]))
		entry_word_list.append(temp)

	###Initializing the OR and AND lists
	or_score_title, or_score_desc, and_score_title, and_score_desc = [], [], [], []

	###iterate over each entry of the search_term column
	for entry in range(len(entry_list[2])):
		or_score_title.append(calculate_OR(entry_word_list[2][entry], entry_word_list[0][entry]))
		or_score_desc.append(calculate_OR(entry_word_list[2][entry], entry_word_list[1][entry]))
		and_score_title.append(calculate_AND(entry_word_list[2][entry], entry_word_list[0][entry]))
		and_score_desc.append(calculate_AND(entry_word_list[2][entry], entry_word_list[1][entry]))

	write_csv("train_boolean.csv", original_data, or_score_title, or_score_desc, and_score_title, and_score_desc)

	#print and_score_title



if __name__ == "__main__":
	main()