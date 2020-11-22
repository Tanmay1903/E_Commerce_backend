from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import sys

# Initialise objects

# 'r' stands for Regular Expression and '\w+' indicates that include All Words
tokenizer = RegexpTokenizer(r'\w+')

# Only calling english stopwords
en_stopwords = set(stopwords.words('english'))

ps = PorterStemmer()

def getStemmedReview(review):
    
    review = review.lower()
    review = review.replace('<br /><br />',' ')# removing <br /><br />  
    
    # Tokenize
    
# Tokenization is important so that each word is treated as word('loved') only not as character('l','o','v','e','d')
    tokens = tokenizer.tokenize(review)
    
    new_tokens = [token for token in tokens if token not in en_stopwords]
    
# Stemming is done to make a word 'loved' as 'love'
    stemmed_tokens = [ps.stem(token) for token in new_tokens]
    
#  We used ' '.join() func to make our list look like a string 
#  in which after every word me seperate them by putting a ' '. 
    cleaned_review = ' '.join(stemmed_tokens)
    
    return cleaned_review





