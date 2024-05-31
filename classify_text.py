import fasttext
from janome.tokenizer import Tokenizer

# モデルの読み込み
model = fasttext.load_model('text_classification_model.bin')

# トークナイザの初期化
tokenizer = Tokenizer()

# テキストをカテゴリ分類する関数
def classify_text(text, threshold=0.5):
    tokens = tokenizer.tokenize(text, wakati=True)
    processed_text = ' '.join(tokens)
    labels, probabilities = model.predict(processed_text)
    # probabilitiesをprintする
    print(f"probabilities: {probabilities}")
    if probabilities[0] < threshold:
        return '意味なし'
    return labels[0].replace('__label__', '')

# ユーザー入力を受け取り分類するループ
if __name__ == "__main__":
    while True:
        user_input = input("文章を入力してください（終了するには 'exit' と入力）：")
        if user_input.lower() == 'exit':
            break
        category = classify_text(user_input)
        print(f"入力された文章: {user_input}")
        print(f"カテゴリ: {category}")
