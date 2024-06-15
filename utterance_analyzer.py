#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
発話理解を扱うプログラム
"""

from janome.tokenizer import Tokenizer


class UtteranceAnalyzer:
    """
    発話理解を扱うクラス
    """

    def get_result(self, state):
        """
        理解結果を返すメソッド
        """
        _ = state
        return {"utt": ""}  # 辞書型として返す

    @staticmethod
    def echo(an_object):
        """
        静的解析ツール(lint)対策
        """
        return an_object


class UtteranceAnalyzerEcho(UtteranceAnalyzer):
    """ """

    def get_result(self, state):
        sentence_meaning = self._analyze_phrases(state["utt"])
        proper_nouns = self._extract_proper_nouns(state["utt"])
        nouns = self._extract_nouns(state["utt"])

        # 最大値のカテゴリを取得
        max_category, max_value = self._get_max_category(sentence_meaning)
        max_category_japanese = (
            self._translate_category_to_japanese(max_category)
            if max_value > 0
            else "意味なし"
        )

        return {
            "utt": state["utt"],
            "meaning": sentence_meaning,
            "固有名詞": proper_nouns,
            "名詞": nouns,
            "最大の意味カテゴリ": max_category_japanese,
        }

    def _analyze_phrases(self, utterance):
        sentence_meaning = {
            "methods": 0,
            "thanks": 0,
            "sympathy": 0,
            "location_questions": 0,
            "mood_questions": 0,
            "deny": 0,
            "plan": 0,
            "request": 0,
        }
        phrases = {
            "methods": ["どのように", "どうやって", "手順", "方法", "行き方"],
            "thanks": ["ありがとう", "感謝", "助かる", "助かり", "助かり"],
            "sympathy": [
                "すごい",
                "とても",
                "本当に",
                "いいね",
                "ありだね",
                "良いね",
                "いいと思う",
            ],
            "location_questions": ["どこ", "どの辺り", "場所"],
            "mood_questions": [
                "どんな",
                "どの様な",
                "どのような",
                "雰囲気",
                "どういう",
                "何が出来る",
            ],
            "deny": [
                "ない",
                "いない",
                "なかった",
                "いなかった",
                "じゃない",
                "あんまり",
            ],
            "plan": [
                "するつもり",
                "予定",
                "計画",
                "行くつもり",
            ],
            "request": [
                "がいい",
                "して",
                "行きたい",
                "行ってみたい",
                "食べたい",
                "飲みたい",
                "見てみたい",
            ],
        }

        for category, category_phrases in phrases.items():
            for phrase in category_phrases:
                if phrase in utterance:
                    sentence_meaning[category] += 1

        return sentence_meaning

    def _extract_proper_nouns(self, utterance):
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize(utterance)
        proper_nouns = [
            token.surface
            for token in tokens
            if token.part_of_speech.startswith("名詞,固有名詞")
        ]
        return proper_nouns

    def _extract_nouns(self, utterance):
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize(utterance)
        nouns = [
            token.surface for token in tokens if token.part_of_speech.startswith("名詞")
        ]
        return nouns

    def _translate_category_to_japanese(self, category):
        category_translation = {
            "methods": "方法・手段の質問",
            "thanks": "感謝",
            "sympathy": "共感",
            "location_questions": "場所の質問",
            "mood_questions": "雰囲気の質問",
            "deny": "否定",
            "plan": "予定",
            "request": "要望",
        }
        return category_translation.get(category, "意味なし")

    def _get_max_category(self, sentence_meaning):
        max_value = max(sentence_meaning.values())
        if list(sentence_meaning.values()).count(max_value) > 1 or max_value == 0:
            return "none", 0
        return max(sentence_meaning, key=sentence_meaning.get), max_value
