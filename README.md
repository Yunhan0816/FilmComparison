# FilmComparison
A Python data analysis tool that reads the data from two different excel files consisting of attributes of films and tv products. It analyzes and compares each one of them and generates python dictionaries with same or the most similar products in pairs with different similarity scores.

## Preparation for Data
### 1. Pandas and Dictionary
Used pandas to read the data from two different excel files consisting of over two thousands film and tv products with their attributes: title, show_type, director, actor, imdb_link, year, writer, country, and summary. It reads the data and save them in data frames for further analysis. 
Save the read data into python dictionaries: {assetId: value}. Here, the value is the corresponding value in different attributes. 
For example, ccms_director = {id1: director1, id2: director2, id3: director3...} 

### 2. Remove text seperator
Remove all the text seperator while storing the director, actor, and writer into different dictionaries. Functions built: divide_comma(d) and divide_slash(d).

### 3. Jieba
Uased Jieba, a Chinese text segmentation Python module for cutting the words into segmentations for easier analysis of similarities. This module is used for analyzing title similarity and summary similarity. 

### 4. Remove stop words
In summary analysis, wrote a text file consisting of all the stop words to be removed. Removed all the stop words in the text in order to generate better similarity score.

### 5. Combine writer, director, and actor
Combine each asset's director, actor, and writer into one set corresponding to its ID for easier future analysis. 

## Comparison and Similarity Calculation
### 1. Gensim
Used Gensim, a module that generates text similarities. Click here, my blog explaining how to use jieba and Gensim to calculate text similarity https://medium.com/better-programming/introduction-to-gensim-calculating-text-similarity-9e8b55de342d, for further information

### 2. Compare director, actor, and writer
Built a helper function that compares director, actor and writer together and generate similarity scores. 
 
### 3. Main function
Combine all the different situations based on the completion of the data in excels. For example, if an asset does not have its attribute of "summary," the function compares its other attributes with other assets. 
Find intersections for each dictionaries consisting of the similarity scores between IDs. 

## Output
{'10393100': {'4301224': 0.5442176103591919}, '10388212': {'1985677': 0.8548175692558289}, '10388709': {'4078592': 0.9465906918048859}, '10480703': {'24827387': 0.909143473704656}, '10392406': {'25820460': 0.39450199604034425}, '10024839': {'2129132': 0.20977436915040015}, '10376664': {'26301742': 0.6314144368682588...} 
This is an example of the output, consisting of the ID pairs with their similarity score. 
