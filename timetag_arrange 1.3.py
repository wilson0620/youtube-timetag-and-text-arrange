'''
講真的，我好久沒寫程式了，現在也不靠這個吃飯，笑死
'''
print('opening program...')


print('reading module...')
import re
import pandas as pd


print('loading initial parameter...')
encoding='UTF-8'
output_list = []


print('loading fuction...')
def text_filter(text, #輸入字串
                start, #搜尋起始點
                end = False, #搜尋終點，通常不設終點就是在找歌曲敘述
                delete_blank = True, #刪除多數空格，關掉的話輸出可能會多一些有的沒的
                delete_else = False, #有什麼其他要刪的用這個功能，請給字串，以|為間隔
                cut_by = False, #如果搜尋結果要分割就用這個功能，請給字串
                replace_emoji = ''): #emoji不刪掉很容易出錯，不過這邊可以選擇要替代成什麼東西，請給字串
                #使用這些預設參數可以最大程度的讓程式不會出錯
    
    if end != False:
        try:
            find_target = re.findall(r'{}(.*?){}'.format(start, end), text)[0]
            find_target = re.sub('amp;', '', find_target) #複製原始碼不知道為什麼會多這個，會讓時間戳失效
            return ['https://www.youtube.com' + find_target]
        
        except:
            return ['error when getting timetag.']
    
    elif end == False: #不設搜尋尾端的情況
        try:
            if replace_emoji != False :
                text = re.sub(r'</span><img.*?formatted-string">', replace_emoji, text) #表情符號砍掉，手法挺粗暴的不知道會不會這行出錯，出問題這行先註解掉看看
            if delete_blank == True:
                text = re.sub('xa0|\u3000|\u00A0|&nbsp|	|　', '', text) #我想的到的空格都刪掉，想不到的以後再說(\u0020不刪)
            
            try:
                find_target = re.findall(r'{}(.*)'.format(start), text)[0]
            except:
                print('cannot find accurate TEXT start, try to get all text...')
                try:
                    find_target = re.findall(r'{}(.*)'.format('</a></span>'), text)[0]
                    print('sucess.')
                except:
                    print('error in ', text)
                    print('cannot find TEXT start, SKIP.')
                    return ['error when reading information.', '-']
                
            
            if '</span>' in find_target:
                find_target = find_target[:find_target.index('</span>')] #去掉</span>以後的字串，不知道為什麼有時候會寫上來，好像是下一行第一個字是表情符號造成的         
            if delete_else != False:
                find_target = re.sub(delete_else, '', find_target)
                
            if cut_by != False:
                try:
                    return [find_target[:find_target.index(cut_by)], find_target[find_target.index(cut_by)+1:]]
                except:
                    return[find_target, 'error when cutting(target not found?)']
            return [find_target, '-']
        
        except:
            print('error in ', text)
            return ['error when reading information.', '-']


def reading(identify_by = 'a class', #html語法中，a class是超連結的寫法，所以搜尋這句話有沒有a class判斷是否要執行動作
            text_start = '</a></span> ', #a class跟樣式宣告完後面就是要抓取的文字了，作為預設搜尋起點
            url_start = 'href="', #網址的開始語法，如果一句話有兩個網址，這支程式只會抓第一個
            url_end = '"', #網址結束的點
            cut_by = False, #看成果要怎麼分割，也可以不割
            next_ = False): #有要匹量輸出這個打開，可以在各匹成果之間加入一行空白方便區分
            #前四條預設參數非常不建議更改
    
    file_open = open('source.txt', 'r', encoding = encoding)
    
    for line in file_open:
        if identify_by in line:
            find_text = text_filter(line, text_start, cut_by = cut_by)
            find_url = text_filter(line, url_start, end = url_end)
            result = find_text + find_url
            print(result)
            
            output_list.append(result)
    
    if next_ == True:
        output_list.append(['-', '-', '-'])
        
    file_open.close()
    print('reading success')



#reading(cut_by = '/', next_ = True)

def output():
    try:
        df = pd.DataFrame(output_list, columns =['Name', 'Artist', 'Time tag'])
        df.to_excel('output.xlsx')
        print('output success')
        
    except:
        print('error when output(file not close?)')

print('')
print('successfully opened, ready to go.')



reading(cut_by = '/', next_ = True)
output()















