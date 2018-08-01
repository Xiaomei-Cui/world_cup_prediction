from wordcloud import WordCloud
import jieba.analyse as analyse
import numpy as np
from PIL import Image

text = open('comment.txt',encoding='gb18030').read()
tags=analyse.extract_tags(text,36, withWeight=False)
StopWords=['这部','这个','一部','不是','呜呜','这样']
stopwords=set(StopWords)
Mask = np.array(Image.open('mask.png'))
words=' '.join(tags)
wc = WordCloud(background_color='white',mask=Mask,stopwords=stopwords,repeat=True,max_words=200,max_font_size=300,font_path=r'C:\windows\fonts\STXINGKA.TTF').generate(words)
wc.to_file('words_cloud.png')