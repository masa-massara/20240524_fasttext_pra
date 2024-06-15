import fasttext
from janome.tokenizer import Tokenizer
from utterance_analyzer import UtteranceAnalyzerEcho

# モデルの読み込み
model = fasttext.load_model("text_classification_model.bin")

# トークナイザの初期化
tokenizer = Tokenizer()


# FastTextを用いた分類関数
def classify_with_fasttext(text, threshold=0.5):
    tokens = tokenizer.tokenize(text, wakati=True)
    processed_text = " ".join(tokens)
    labels, probabilities = model.predict(processed_text)
    print(f"FastText probabilities: {probabilities}")
    if probabilities[0] < threshold:
        return "意味なし"
    return labels[0].replace("__label__", "")


# UtteranceAnalyzerを用いた分類関数
def classify_with_utterance_analyzer(text):
    analyzer = UtteranceAnalyzerEcho()
    state = {"utt": text}
    result = analyzer.get_result(state)
    return result


# ユーザー入力を受け取り分類するループ
if __name__ == "__main__":
    while True:
        user_input = input("文章を入力してください（終了するには 'exit' と入力）：")
        if user_input.lower() == "exit":
            break
        fasttext_category = classify_with_fasttext(user_input)
        analyzer_result = classify_with_utterance_analyzer(user_input)
        print(f"入力された文章: {user_input}")
        print(f"FastTextカテゴリ: {fasttext_category}")
        print(f"UtteranceAnalyzer結果: {analyzer_result['最大の意味カテゴリ']}")
