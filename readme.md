1. go through all the HTML file
	- search for relevant tags to get the content
	- tokenize the content

2. create an inverted index out of all the token
	- token -> freq -> [(docID list, tf-idf)]

3. upload the index into a database (mongoDB)

4. create query system
	- look through index for the given query
	- list out all the docID that contains the word
