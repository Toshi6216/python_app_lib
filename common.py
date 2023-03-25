import unicodedata

def get_east_asian_width_count(text): #文字数カウント 全角は2文字 半角は1文字としてカウント
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWA': #'F':全角英数 'W':漢字、かな文字、句読点など 'A':ギリシャ文字など 
            count += 2
        else:
            count += 1
    return count
