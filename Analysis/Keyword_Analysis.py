import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import urllib.request
import numpy as np
import squarify as squ

from konlpy.tag import Mecab
from wordcloud import WordCloud

plt.style.use('seaborn-white')

fontPath = 'C:/Windows/Fonts/NanumBarunGothic.ttf'
font = fm.FontProperties(fname=fontPath, size=10)
plt.rc('font', family='NanumBarunGothic')


raw = urllib.request.urlopen('https://raw.githubusercontent.com/e9t/nsmc/master/ratings.txt').readlines()

# 한글변환
raw = [x.decode() for x in raw[1:]]
reviews = []
for i in raw:
  reviews.append(i.split('\t')[1])
# print (reviews[:5])

# 형태소 분석을 이용한 명사 추출
tagger = Mecab()

nouns = []
for review in reviews:
  for noun in tagger.nouns(review):
    nouns.append(noun)
#nouns[:10]

# 불용어(Stopwords) 사전 만들기
stop_words = "영화 전 난 일 걸 뭐 줄 만 건 분 개 끝 잼 이거 번 중 듯 때 게 내 말 나 수 거 점 것"
stop_words = stop_words.split(' ')
#print(stop_words)

# 불용어를 제외하여 형태소 분석 수행
nouns = []
for review in reviews:
  for noun in tagger.nouns(review):
    if noun not in stop_words:
      nouns.append(noun)
#nouns[:10]

# 단어 빈도수 측정
from collections import Counter

nouns_counter = Counter(nouns)
top_nouns = dict(nouns_counter.most_common(50))

top_nouns

# 단어 빈도 시각화
y_pos = np.arange(len(top_nouns))

plt.figure(figsize=(12,12))
plt.barh(y_pos, top_nouns.values())
plt.title('Word Count')
plt.yticks(y_pos, top_nouns.keys())
plt.show()

# WordCloud를 이용해 객체를 생성해주고, generate_from_frequencies() 함수로 빈도 수에 따라 워드클라우드 생성

wc = WordCloud(background_color='white', font_path='./font/NanumBarunGothic.ttf')
wc.generate_from_frequencies(top_nouns)

# WordCloud 시각화 (이미지 시각화 함수인 imshow() 함수를 사용)
figure = plt.figure(figsize=(12,12))
ax = figure.add_subplot(1, 1, 1)
ax.axis('off')
ax.imshow(wc)
plt.show()


# squarify 트리맵 시각화

norm = mpl.colors.Normalize(vmin=min(top_nouns.values()),
                            vmax=max(top_nouns.values()))

colors = [mpl.cm.Blues(norm(value)) for value in top_nouns.values()]

squ.plot(label=top_nouns.keys(),
              sizes=top_nouns.values(),
              color=colors,
              alpha=.7)




