'''
講真的，我好久沒寫程式了，現在也不靠這個吃飯，笑死
'''
import re

fp = open('source.txt', 'r', encoding='UTF-8')

A = '</span><a class="yt-simple-endpoint style-scope yt-formatted-string" spellcheck="false" href="/watch?v=UtpOOPu80GA&amp;t=3177s" dir="auto">0:52:57</a><span dir="auto" class="style-scope yt-formatted-string"> STARGAZER～星の扉　/根岸さとり '
B = '</span><span dir="auto" class="style-scope yt-formatted-string">'

def text_filter(text, start, end = False, delete_blank = False, delete_else = False, replace_emoji = ''): #delete_else 請給字串，以|為間隔
    
    try:
        if end != False:
            find_target = re.findall(r'{}(.*?){}'.format(start, end), text)[0]
        elif end == False: #不設搜尋尾端的情況
            if replace_emoji != False :
                text = re.sub(r'</span><img.*?formatted-string">', replace_emoji, text) #表情符號砍掉，手法挺粗暴的不知道會不會這行出錯，出問題這行先註解掉看看
            #print(text)
            find_target = re.findall(r'{}(.*)'.format(start), text)[0]
            if '</span>' in find_target:
                find_target = find_target[:find_target.index('</span>')] #去掉</span>以後的字串，不知道為什麼有時候會寫上來，好像是下一行第一個字是表情符號造成的
        
            if delete_blank == True:
                find_target = re.sub('\xa0|\u0020|\u3000|\u00A0|&nbsp| |　', '', find_target) #我想的到的空格都刪掉，想不到的以後再說
            
            if delete_else != False:
                find_target = re.sub(delete_else, '', find_target)

        return find_target
    
    except:
        return('error in text_filter')






output_list = []
for line in fp:
    #print(line)
    if 'a class' in line:
        find_url = text_filter(line, 'href="', end = '"')
        find_text = text_filter(line, '</a><span dir="auto" class="style-scope yt-formatted-string">', delete_blank = True)
        
        print(find_url, find_text)
        
        output_list.append(find_url)
        
fp.close()