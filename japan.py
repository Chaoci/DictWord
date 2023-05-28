import sqlite3
import random

# 連接到你的database檔案
conn = sqlite3.connect('test1.db')
c = conn.cursor()

# 從japanese_characters table中選擇所需的欄位
c.execute('SELECT hiragana_katakana, romaji FROM japanese1')

# 將結果讀入一個list中
characters = c.fetchall()

# 開始測驗
a= 0
correct = 0
while True:
    # 隨機選擇一個假名
    hiragana_katakana, romaji = random.choice(characters)

    # 提示用戶輸入答案
    print('請輸入', hiragana_katakana, '的讀音：')
    answer = input()
    if answer == romaji:
        a = a+1
        correct+=1
        print('答對了！')
    else:
        a = a+1
        print('答錯了，正確的讀音是', romaji)

    # 詢問用戶是否繼續測試
    if a %10 == 0:
        print(f'目前分數是{correct}，總答題數是{a}。是否繼續測試？輸入 y 或 Y 繼續，其他任意鍵結束')
        continue_testing = input()
        if continue_testing.lower() != 'y':
            break

# 關閉連接
conn.close()