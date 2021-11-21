import re
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GRU, Embedding
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.models import load_model


# 케라스에서 제공하는 IMDB 리뷰 데이터는 앞서 배운 로이터 뉴스 데이터에서 훈련 데이터와 테스트 데이터를 우리가 직접 비율을 조절했던 것과는 
# 달리 이미 훈련 데이터와 테스트 데이터를 50:50 비율로 구분해서 제공합니다. 
# 로이터 뉴스 데이터에서 사용했던 test_split과 같은 데이터의 비율을 조절하는 파라미터는 imdb.load_data에서는 지원하지 않습니다.

(X_train, y_train), (X_test, y_test) = imdb.load_data()

# imdb.data_load()의 파라미터로 num_words를 사용하면 이 데이터에서 등장 빈도 순위로 몇 번째에 해당하는 단어까지를 사용할 것인지를 의미합니다. 
# 예를 들어서 10,000을 넣으면, 등장 빈도 순위가 1~10,000에 해당하는 단어만 사용하게 됩니다. 
# 즉, 단어 집합의 크기는 10,000이 됩니다. 지금은 별도로 제한하지 않겠습니다.

print('훈련용 리뷰 개수 : {}'.format(len(X_train)))
print('테스트용 리뷰 개수 : {}'.format(len(X_test)))
num_classes = len(set(y_train))
print('카테고리 : {}'.format(num_classes))


# print(X_train[0])
# print(y_train[0])

# 첫번째 훈련용 리뷰의 레이블에 해당하는 y_train[0]의 값은 1입니다. 이 값은 첫번째 훈련 데이터가 2개의 카테고리 중 1에 해당하는 카테고리임을 의미합니다. 
# 이 예제의 경우 감성 정보로서 0 또는 1의 값을 가지는데, 이 경우에는 긍정을 의미하는 1의 값을 가집니다.

len_result = [len(s) for s in X_train]

print('리뷰의 최대 길이 : {}'.format(np.max(len_result)))
print('리뷰의 평균 길이 : {}'.format(np.mean(len_result)))

plt.subplot(1,2,1)
plt.boxplot(len_result)
plt.subplot(1,2,2)
plt.hist(len_result, bins=50)
#plt.show()

# 대체적으로 1,000이하의 길이를 가지며, 특히 100~500길이를 가진 데이터가 많은 것을 확인할 수 있습니다. 
# 반면, 가장 긴 길이를 가진 데이터는 길이가 2,000이 넘는 것도 확인할 수 있습니다. 레이블의 분포를 확인해보겠습니다.

#unique_elements, counts_elements = np.unique(y_train, return_counts=True)
#print("각 레이블에 대한 빈도수:")
#print(np.asarray((unique_elements, counts_elements)))

# 25,000개의 리뷰가 존재하는데 두 레이블 0과 1은 각각 12,500개로 균등한 분포를 가지고 있습니다. 
# X_train에 들어있는 숫자들이 각각 어떤 단어들을 나타내고 있는지 확인해보겠습니다. 
# imdb.get_word_index()에 각 단어와 맵핑되는 정수가 저장되어져 있습니다. 
# 주의할 점은 imdb.get_word_index()에 저장된 값에 +3을 해야 실제 맵핑되는 정수입니다. 이것은 IMDB 리뷰 데이터셋에서 정한 규칙입니다.

# index_to_word에 인덱스를 집어넣으면 전처리 전에 어떤 단어였는지 확인할 수 있습니다. 
# IMDB 리뷰 데이터셋에서는 0, 1, 2, 3은 특별 토큰으로 취급하고 있습니다. 
# 그래서 정수 4부터가 실제 IMDB 리뷰 데이터셋에서 빈도수가 가장 높은 실제 영단어입니다.

word_to_index = imdb.get_word_index()
index_to_word = {}
for key, value in word_to_index.items():
    index_to_word[value+3] = key

#print('빈도수 상위 1등 단어 : {}'.format(index_to_word[4]))
#print('빈도수 상위 3938등 단어 : {}'.format(index_to_word[3941]))

for index, token in enumerate(("<pad>", "<sos>", "<unk>")):
  index_to_word[index] = token

#print(' '.join([index_to_word[index] for index in X_train[0]]))
# 첫번째 훈련용 리뷰의 X_train[0]이 인덱스로 바뀌기 전에 어떤 단어들이었는지 확인해보겠습니다.

vocab_size = 10000
(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words = vocab_size)

# 리뷰 최대 길이는 500으로 제한합니다. 각 리뷰는 문장의 길이가 다르기 때문에, 모델이 처리할 수 있도록 길이를 동일하게 해주어야 합니다. 
# 이때 사용하는 것이 pad_sequences()입니다. 길이는 max_len에 넣는 값으로 정해집니다. 
# 훈련 데이터가 정한 길이를 초과하면 초과분을 삭제하고, 부족하면 0으로 채웁니다.
max_len = 500
X_train = pad_sequences(X_train, maxlen=max_len)
X_test = pad_sequences(X_test, maxlen=max_len)

# Embedding()은 두 개의 인자를 받는데, 첫번째 인자는 단어 집합의 크기이며 두번째 인자는 임베딩 후의 벡터 크기입니다. 
# 여기서는 100을 선택했습니다. 즉, 입력 데이터에서 모든 단어는 100차원의 임베딩 벡터로 표현됩니다.
embedding_dim = 100
hidden_units = 128

model = Sequential()
model.add(Embedding(vocab_size, embedding_dim))
model.add(GRU(hidden_units))
model.add(Dense(1, activation='sigmoid'))
# 이진 분류이므로 출력층은 뉴런 하나와 활성화 함수로 시그모이드 함수를 사용합니다.

# 검증 데이터의 손실(loss)이 증가하면, 과적합 징후이므로 검증 데이터 손실이 4회 증가하면 학습을 중단하는 조기 종료(EarlyStopping)를 사용합니다. 
# 또한, ModelCheckpoint를 사용하여 검증 데이터의 정확도가 이전보다 좋아질 경우에만 모델을 저장하도록 합니다.
es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=4)
mc = ModelCheckpoint('GRU_model.h5', monitor='val_acc', mode='max', verbose=1, save_best_only=True)

# 긍정인지 부정인지에 대한 이진 판별값이 출력이 되기 때문에, 손실 함수는 binary_crossentropy를 사용합니다. 
# 최적화 함수는 rmsprop를 사용하였습니다. 또한, 에포크마다 정확도를 구하기위해 accuracy를 추가해줍니다. 에포크는 총 10회를 수행하겠습니다.
model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
history = model.fit(X_train, y_train, epochs=15, callbacks=[es, mc], batch_size=60, validation_split=0.2)

# 훈련 과정에서 검증 데이터의 정확도가 가장 높았을 때 저장된 모델인 'GRU_model.h5'를 로드합니다.
loaded_model = load_model('GRU_model.h5')
print("\n 테스트 정확도: %.4f" % (loaded_model.evaluate(X_test, y_test)[1]))

# 테스트 데이터에 대해서 정확도 88.93%를 얻습니다. 임의의 문장에 대해서 리뷰의 긍, 부정을 예측하고자 합니다.
#  이를 위해서는 모델에 넣기 전에 임의의 문장에 대해서 전처리를 해주어야 합니다. 

# sentiment_predict은 입력된 문장에 대해서 기본적인 전처리와 정수 인코딩, 패딩을 한 후에 모델의 입력으로 사용하여 예측값을 리턴하는 함수입니다.
def sentiment_predict(new_sentence):
  # 알파벳과 숫자를 제외하고 모두 제거 및 알파벳 소문자화
  new_sentence = re.sub('[^0-9a-zA-Z ]', '', new_sentence).lower()

  # 정수 인코딩
  encoded = []
  for word in new_sentence.split():
    try :
      # 단어 집합의 크기를 10,000으로 제한.
      if word_to_index[word] <= 10000:
        encoded.append(word_to_index[word]+3)
      else:
      # 10,000 이상의 숫자는 <unk> 토큰으로 변환.
        encoded.append(2)
    # 단어 집합에 없는 단어는 <unk> 토큰으로 변환.
    except KeyError:
      encoded.append(2)

  pad_sequence = pad_sequences([encoded], maxlen=max_len) # 패딩
  score = float(loaded_model.predict(pad_sequence)) # 예측

  if(score > 0.5):
    print("{:.2f}% 확률로 긍정 리뷰입니다.".format(score * 100))
  else:
    print("{:.2f}% 확률로 부정 리뷰입니다.".format((1 - score) * 100))

# IMDB 사이트에 접속해서 영화 블랙팬서의 1점 리뷰를 가져왔습니다. 
test_input = "This movie was just way too overrated. The fighting was not professional and in slow motion. I was expecting more from a 200 million budget movie. The little sister of T.Challa was just trying too hard to be funny. The story was really dumb as well. Don't watch this movie if you are going because others say its great unless you are a Black Panther fan or Marvels fan."
# 부정으로 제대로 예측하는지 테스트해보겠습니다.
sentiment_predict(test_input)