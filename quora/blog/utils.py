import pymorphy2, re
from test_category.rus_stopwords import rus_stopwords
from product.stemer import Porter
from bs4 import BeautifulSoup


morph = pymorphy2.MorphAnalyzer()


def makeTags(text):
    cleantext = BeautifulSoup(text, "lxml").text
    my_new_string = re.sub(r"[^a-zA-Zа-яА-Я ]", "", cleantext)
    words = my_new_string.split(" ")

    tags = []
    for word in words:
        if word not in rus_stopwords and word != "":
            tags.append(word)
    s = set(tags)
    new_tags = []
    for tag in s:
        p = morph.parse(tag)[0]
        if "NOUN" in p.tag:
            new_tags.append(p.normal_form)
    return list(set(new_tags))
