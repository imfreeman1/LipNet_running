import re
import string
from collections import Counter

# Source: https://github.com/commonsense/metanl/blob/master/metanl/token_utils.py
def untokenize(words):
    """
    Untokenizing a text undoes the tokenizing operation, restoring
    punctuation and spaces to the places that people expect them to be.
    Ideally, `untokenize(tokenize(text))` should be identical to `text`,
    except for line breaks.
    """
    text = ' '.join(words)  # words 리스트 요소를 모두 ' ' 구분자를 넣어서 하나의 문자열로 합침
    step1 = text.replace("`` ", '"').replace(" ''", '"').replace('. . .',  '...')  # 문자열 ``는 "로,  ''는 "로, . . .는 ...로 변경 => 따옴표는 큰 따옴표로, 온점 공백 제거
    step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")  #  ( 는  (로,  ) 는 ) 로 변경 => 괄호 공백 하나 제거
    step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)  # step2 에서 r' ([.,:;?!%]+)([ \'"`])' 에 해당하는 부분을 r"\1\2"로 변경
    step4 = re.sub(r' ([.,:;?!%]+)$', r"\1", step3)  # step3 에서 r' ([.,:;?!%]+)$' 에 해당하는 부분을 r"\1"로 변경
    step5 = step4.replace(" '", "'").replace(" n't", "n't").replace(
         "can not", "cannot")  # 문자열  '는 '로,  n't는 n't로, can not은 cannot으로 변경 => 공백 하나 제거
    step6 = step5.replace(" ` ", " '")  # 문자열  ` 는  '로 변경
    return step6.strip()  # 문자열 양옆 공백 제거

# Source: https://stackoverflow.com/questions/367155/splitting-a-string-into-words-and-punctuation
def tokenize(text):
    # re.findall(r"패턴 문자열", "문자열", 옵션)
    return re.findall(r"\w+|[^\w\s]", text, re.UNICODE)  # pattern 과 일치하는 것을 모두 찾아서 list로 반환

# Source: http://norvig.com/spell-correct.html (with some modifications)
class Spell(object):
    def __init__(self, path):
        # step 1. open(path).read(): path 텍스트 파일 읽어오기
        # step 2. self.words(step 1): 
        self.dictionary = Counter(list(string.punctuation) + self.words(open(path).read()))

    def words(self, text):
        # \w: 숫자가 아닌 문자  # [^a-zA-Z0-9_]
        # +: 최소 1번 이상 반복될 때 사용 => 반복 횟수 1부터 시작
        # 문자열을 모두 소문자로 변경해서 
        return re.findall(r'\w+', text.lower())  # 리스트 반환

    def P(self, word, N=None):
        "Probability of `word`."
        # N 이 비어있으면
        if N is None:
            N = sum(self.dictionary.values())  # 단어 사전 값들의 합 저장
        return self.dictionary[word] / N  # float 반환 # 단어 사전 키 값 / N

    def correction(self, word):
        "Most probable spelling correction for word."  # 단어에 대해 가장 가능성 높은 맞춤법 교정
        return max(self.candidates(word), key=self.P)

    def candidates(self, word):
        "Generate possible spelling corrections for word."  # 단어에 대해 가능한 맞춤법 수정 생성
        return (self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word)) or [word])

    def known(self, words):
        "The subset of `words` that appear in the dictionary of WORDS."
        # words 리스트 요소가 self.dictionary 에 있는 키 값일 경우만 가져와서 set()를 통해 중복 제거
        return set(w for w in words if w in self.dictionary)  # 세트 반환

    def edits1(self, word):
        "All edits that are one edit away from `word`."  # 편집 거리 1
        letters    = 'abcdefghijklmnopqrstuvwxyz'
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
        inserts    = [L + c + R               for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edits2(self, word):
        "All edits that are two edits away from `word`."  # 편집 거리 2
        # list comprehension 을 통해 리스트 요소를 self.edits1() 함수에 넣음 -> 그 결과를 self.edits1() 함수에 넣음 -> 그 결과를 요소로 가짐
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))  # 리스트 반환

    # Correct words
    def corrections(self, words):
        # list comprehension 을 통해 리스트 요소를 self.correction(word) 결과를 요소로 가짐  
        return [self.correction(word) for word in words]  # 리스트 반환

    # Correct sentence
    def sentence(self, sentence):
        # 문자열 -> 토큰화 -> 올바른지 검사 -> 언토큰화
        return untokenize(self.corrections(tokenize(sentence)))  # 문자열 반환