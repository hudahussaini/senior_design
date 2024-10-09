import os
import pymupdf
import nltk
import string
from project.main import create_docs

# Used after create_docs before preprocessing
# Needs further testing & refinement
# Just spits out list of keywords currently

nltk.download('punkt_tab')
author_folder_path = "/Users/abolt/Desktop/Test PDFs"
pdf_files = [os.path.join(author_folder_path, f) for f in os.listdir(author_folder_path)
             if os.path.isfile(os.path.join(author_folder_path, f)) and f.endswith('.pdf')]
docs = create_docs(pdf_files)

def get_keywords(docs_list):
    stop_words = ["Introduction", "Copyright", "1.", "1", "1.Introduction", "\\n1."]
    keywords = []
    for doc in docs_list:
        if doc.find("Keywords") != -1:
            doc_keywords = []
            split_doc = doc.split()
            keyword_index = -1
            for word in split_doc:
                if "Keywords" in word:
                    keyword_index = split_doc.index(word)
                    break
            keyword_words = []
            if keyword_index != -1:
                for i in range(keyword_index + 1, keyword_index + 20):
                    word = split_doc[i]
                    if word in stop_words:
                        break
                    if "," not in word and ";" not in word and "." not in word:
                        keyword_words.append(word)
                        continue
                    if "," in word or ";" in word or "." in word:
                        if len(keyword_words) != 0:
                            keyword_words.append(word)
                            keyword = " ".join(keyword_words)
                            keyword_words = []
                            keyword = keyword.translate(str.maketrans('', '', string.punctuation)).lower()
                            doc_keywords.append(keyword)
                            if "." in word:
                                break
                        else:
                            word = word.translate(str.maketrans('', '', string.punctuation)).lower()
                            doc_keywords.append(word)
                for keyword in doc_keywords:
                    keywords.append(keyword)

    return keywords


# docs = test_doc
keys = get_keywords(docs)

print(keys)
