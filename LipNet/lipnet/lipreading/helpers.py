def text_to_labels(text):   #라벨의 text 만들기
    ret = []        # 빈 리스트
    for char in text:   
        if char >= 'a' and char <= 'z':     # char가 'a'보다 크거나 같고, 'z'보다 작거나 같은 경우
            ret.append(ord(char) - ord('a'))    # ret에 (char의 유니코드 - a의 유니코드) append함.
        elif char == ' ':
            ret.append(26)      # ret에 ' '의 유니코드를 append하는 듯.
    return ret

def labels_to_text(labels):     # 라벨에서 텍스트
    # 26 is space, 27 is CTC blank char
    text = ''       #빈 텍스트
    for c in labels:    
        if c >= 0 and c < 26:  # c가 0보다 크거나 같고, c가 26보다 작을때
            text += chr(c + ord('a'))   # text에 (c+ord('a'))의 문자를 더함.
        elif c == 26:       # c가 26이면
            text += ' '     # 텍스트에 빈칸을 더함.
    return text