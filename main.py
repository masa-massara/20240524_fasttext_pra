import os
import random
from janome.tokenizer import Tokenizer
import fasttext

# ディレクトリのパス
data_dir = '/Users/masay/programming/python/20240524_fasttext_pra/text'

# データを読み込む
categories = os.listdir(data_dir)
data = []

for category in categories:
    category_path = os.path.join(data_dir, category)
    if os.path.isdir(category_path):
        files = os.listdir(category_path)
        for file in files:
            file_path = os.path.join(category_path, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    data.append('__label__{} {}'.format(category, line.strip()))

# データをシャッフルして保存
random.shuffle(data)
with open('train_data.txt', 'w', encoding='utf-8') as f:
    for line in data:
        f.write(line + '\n')

# トレーニングデータの確認
with open('train_data.txt', 'r', encoding='utf-8') as f:
    for _ in range(10):
        print(f.readline())

# モデルを訓練する
model = fasttext.train_supervised('train_data.txt', epoch=5, lr=0.1, wordNgrams=2, verbose=2, minCount=1)

# モデルを保存する
model.save_model('text_classification_model.bin')

# トークナイザの初期化
tokenizer = Tokenizer()

# テキストをカテゴリ分類する関数
def classify_text(text, threshold=0.3):
    tokens = tokenizer.tokenize(text, wakati=True)
    processed_text = ' '.join(tokens)
    labels, probabilities = model.predict(processed_text)
    if probabilities[0] < threshold:
        return '意味なし'
    return labels[0].replace('__label__', '')

# ユーザー入力を受け取り分類するループ
while True:
    user_input = input("文章を入力してください（終了するには 'exit' と入力）：")
    if user_input.lower() == 'exit':
        break
    category = classify_text(user_input)
    print(f"入力された文章: {user_input}")
    print(f"カテゴリ: {category}")
