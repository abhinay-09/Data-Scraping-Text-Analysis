import os
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import syllapy
import re
import pandas as pd


def read_file(file_path):
    with open(file_path, 'r',encoding="utf-8") as file:
        return file.read()



def cal_metrics(text):
    # Tokenizing the text into words and sentences
    words = word_tokenize(text)
    sentences = sent_tokenize(text)

    stopword_files = os.listdir("StopWords")
    all_stopwords = set()
    for file_name in stopword_files:
        with open(os.path.join("StopWords",file_name), 'r', encoding='latin-1') as stop_file:
            stopwords = stop_file.read()
        stopword_token = word_tokenize(stopwords)
        all_stopwords.update(stopword_token)
        filter_words = [word for word in words if word.isalnum() and word not in all_stopwords]


    # 1. Positive Score
    with open(os.path.join("MasterDictionary","positive-words.txt"), 'r', encoding='utf-8')as pos_file:
        positive_words = pos_file.read()

    positive_tokens = word_tokenize(positive_words)
    positive_score = len([pos_word for pos_word in filter_words if pos_word in positive_tokens])

    # 2. Negative Score
    with open(os.path.join("MasterDictionary","negative-words.txt"), 'r', encoding='latin-1')as neg_file:
        negative_words = neg_file.read()

    negative_tokens = word_tokenize(negative_words)
    negative_score = len([neg_word for neg_word in filter_words if neg_word in negative_tokens])
    
    # 3. Polarity Score
    polarity_score = (positive_score - negative_score)/((positive_score + negative_score) + 0.000001)

    # 4. Subjectivity Score
    subject_score = (positive_score + negative_score)/(len(filter_words)+0.000001)

    # 5. Avg sentence length
    avg_sentence_length = len(words)/len(sentences) if sentences else 0

    # 6. Percentage of complex word
    complex_word = [comp for comp in words if syllapy.count(comp) > 2]
    percentage_complex_word = len(complex_word)/len(words) *100 if words else 0

    # 7. Fog Index
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_word)

    # 8. Avg Sentence length and Avg number of words per sentence

    # 9. Complex word count
    complex_word_count = len(complex_word)
    
    # 10. Word count
    stop_words = set(nltk.corpus.stopwords.words('english'))
    con_word = [word for word in words if word.isalnum() and word not in stop_words]
    word_count = len(con_word)

    # 11. Syllables per words
    syllables_per_words = sum(syllapy.count(syl_word) for syl_word in words) / len(words) if words else 0

    # 12. Personal pronouns
    personal_pronoun = r'\b(I|we|my|our|us)\b'
    personal_pronoun_count = len(re.findall(personal_pronoun, " ".join(words)))

    # 13. Avg word length
    avg_word_length = sum(len(word) for word in words) /len(words) if words else 0

    return {
        "POSITIVE SCORE" : positive_score,
        "NEGATIVE SCORE"  : negative_score,
        "POLARITY SCORE" : polarity_score,
        "SUBJECTIVITY SCORE" : subject_score,
        "AVG SENTENCE LENGTH" : avg_sentence_length,
        "PERCENTAGE OF COMPLEX WORDS" : percentage_complex_word,
        "FOG INDEX" : fog_index,
        "AVG NUMBER OF WORDS PER SENTENCE" : avg_sentence_length,
        "COMPLEX WORD COUNT" : complex_word_count,
        "WORD COUNT" : word_count,
        "SYLLABLE PER WORD" : syllables_per_words,
        "PERSONAL PRONOUNS" : personal_pronoun_count,
        "AVG WORD LENGTH" : avg_word_length,
    }

def main():
    data_folder = os.listdir("articles")
    all_data =[]
    for file_path in data_folder:
        url_id = os.path.splitext(file_path)[0]
        file_path = os.path.join("articles", file_path)
        text = read_file(file_path)
        metric_data = cal_metrics(text)
        metric_data["URL_ID"] = url_id
        all_data.append(metric_data)

    metric_df = pd.DataFrame(all_data)
    url_df = pd.read_excel('input.xlsx')
    merge_df = pd.merge(url_df, metric_df, on= "URL_ID", how="inner")
    merge_df.to_excel("output.xlsx", index=False)
        

if __name__ =="__main__":
    main()