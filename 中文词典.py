import re
#0. 导入词典相关常量
import  翻译.数据类型 as 模型
import 翻译.词典相关常量 as 词典常量
import  翻译.自定义词典 as 自定义词典 


# 1. 导入16个词典数据文件到  词典数据 中
词典数据 ={}
i=0
print("词典数据导入中，请耐心等待")
while i < 16 :
    print(i)
    fr1 = open('词典数据/词典'+ str(i) +'.ts','r+',encoding='utf-8')
    dic1 = eval(fr1.read())   #读取的str转换为字典
    #print(dic["Asama"])
    #print(dic["-ability"]
    词典数据.update(dic1)
    fr1.close()
    i=i+1
print("词典数据导入完毕")

# 2. 导入 词形变化数据 
fr1 = open("词典数据/词形变化.ts",'r+',encoding='utf-8')
dic1 = eval(fr1.read())   #读取的str转换为字典
#print(dic["Asama"])
#print(dic["-ability"])
fr1.close()
词形变化数据 = dic1

#3. 定义英文词词形
词形_原型变换形式 = "原型变换形式"
词形类型 = {
  "p": "过去式", #past tense
  "d": "过去分词",
  "i": "现在分词", # -ing
  "3": "第三人称单数",
  "r": "形容词比较级", #-er
  "t": "形容词最高级", #-est
  "s": "名词复数形式",
  "0": "原型",
  "1": 词形_原型变换形式,
  "f": "第yi人称单数",
}

# 4. 驼峰及下划线命名处理
def camel_to_underline( camel_format):
     '''
         驼峰命名格式转下划线命名格式
     '''
     underline_format=''
     if isinstance(camel_format, str):
         for _s_ in camel_format:
            #underline_format += _s_ if _s_.islower() else '_'+_s_.lower()
            underline_format += '_'+_s_.lower() if (_s_.islower()==False and  _s_.lower().islower() ) else _s_
                        
     return underline_format

     
def underline_to_camel( underline_format):
     '''
         下划线命名格式驼峰命名格式
     '''
     camel_format = ''
     if isinstance(underline_format, str):
         for _s_ in underline_format.split('_'):
             camel_format += _s_.capitalize()
     return camel_format

def 拆分骆驼命名(命名: str): 
    命名 = camel_to_underline(命名)
    if 命名[0] == '_':
        命名 =  命名[1:]
        #print(命名)
    return 命名.split('_')

def 消除英文小括号内容(字符串: str):
    样式 = re.compile(r'\(\S+?\)')
    return 样式.sub('', 字符串)

def 消除括号内容(中文释义: str, 开括号: str, 闭括号: str):
    开括号位置 = 中文释义.find(开括号)
    闭括号位置 = 中文释义.find(闭括号)
    if (开括号位置 == -1 | 闭括号位置 == -1) :
        return 中文释义
    
    括号内容 = 中文释义[开括号位置 : 闭括号位置 + 1]
    #print(括号内容)
    return 中文释义.replace(括号内容, "")

def 消除所有括号内容(中文释义: str): 
    #不确定是否存在多个括号的情况: 清理后.replace(/ *（[^）]*） */g, ""); //
    #清理掉了 所有小括号 和中括号 （）[]
    清理后 = 消除括号内容(中文释义, "（", "）")
    清理后 = 消除英文小括号内容(清理后)
    样式 = re.compile(r'\[\S+?\]')
    #清理后 = 清理后.replace(/ *\[[^)]*\] */g, "")
    return 样式.sub('', 清理后).strip()
    
# 5. 取给定英文段落中所有词
#// 假设每个字段除了词, 其他都是非英文字符.
#// 仅翻译无空格的片段

# 处理后词 = 释义处理.取原型(处理后词, 提取词形(词典.词形变化数据[处理后词]));
def 取原型(词: str, 词形):
    if (词形):
        原词 = 词
        为复数形式 = False
        for  某词形 in 词形:
            if (某词形['类型'] == "原型变换形式") and ("名词复数形式" in 某词形['变化']) or ("现在分词" in 某词形['变化']):
                为复数形式 = True
          
            if (某词形['类型'] == "原型") :
                #print()
                原词 = 某词形['变化']
         
        if  (为复数形式) :
            return 原词
       
    return 词

#英文词 = "contorts"
#取原型(英文词, 提取词形(词形变化数据[英文词]))


def 取字段中所有词(字段文本: str):
    #删去所有前后空格后再提取单词
    删除前后空格 = 字段文本.strip()
    #确认无空格
    #if (!删除前后空格.match(/^[^\s]+$/g)) :
    #if not re.match(r'^[^\s]+$',删除前后空格):    
    #    return []
    单词 = re.findall(r'[a-zA-Z]+',删除前后空格)
    if 单词:
        分词 = []
        for 某单词 in 单词:
            分词.extend(拆分骆驼命名(某单词))
        return 分词
    return []

# 6.提取英文单词所有词形
#处理后词 = 释义处理.取原型(处理后词, 提取词形(词典.词形变化数据[处理后词]));
def  提取词形(原字符串: str): 
    变化 = []
    if not 原字符串: 
        return 变化
  
    词形字段 = 原字符串.split("/")
    
    for 某字段 in 词形字段:
        分段 = 某字段.split(":")
        #print(分段[0])
        类型 = 词形类型[分段[0]]
        原型变化形式 = []
        if (类型 == 词形_原型变换形式) :
            for 变化形式 in 分段[1] :
                原型变化形式.append(词形类型[变化形式])
        
        XXX = ("" if len(分段) == 1 else (原型变化形式 if 类型 == 词形_原型变换形式 else 分段[1]))
        #print(类型)
        变化.append({'类型': 类型,  '变化': XXX})
    return 变化
#提取词形( "s:contours/d:contoured/i:contouring/p:contoured/3:contours")  
#s:inputs/d:input/0:input/1:d/i:inputting/p:input/3:inputs/f:inputs
#提取词形( "0:contour/1:dp/d:contoured") 

def 取按词性释义(中文释义): 
    '''
    对一个英文单词的中文释义提取词性后返回一个字典（词性，翻译）
    
    'n. 罩；风帽；（布质）面罩；学位连领帽（表示学位种类）\nv. 覆盖；用头巾包；使(马,鹰等)戴头罩；给…加罩\n[网络] 胡德；兜帽；引擎盖'
    
    返回
    
    {'n.': ['罩；风帽；（布质）面罩；学位连领帽（表示学位种类）'],
     'v.': ['覆盖；用头巾包；使(马,鹰等)戴头罩；给…加罩'],
     '[网络]': ['胡德；兜帽；引擎盖']}
     
     
    '''
    所有释义 = 中文释义.split('\n')
    词性到释义 ={}
    for  除去词性 in 所有释义:
        首空格位置 = 除去词性.strip().find(' ')
        #print(除去词性[0: 首空格位置],首空格位置)
        当前词性 = 除去词性[0: 首空格位置] if 首空格位置 > 0  else  ''       
        #print(当前词性)
        if (当前词性 and  当前词性 in 词典常量.词性) :
            除去词性 = 除去词性[len(当前词性):].strip()
        else :
            当前词性 = ''
        
        #按逗号分隔词义
        # TODO: 也有分号分隔
        词义 = 除去词性.split(r'[；;,]');
        此词性的释义 = []
        for  某词义 in 词义:
            此词性的释义.append(某词义.strip())
            词性到释义[当前词性] = 此词性的释义 # 添加

    return 词性到释义
#中文翻译 = 'n. 罩；风帽；（布质）面罩；学位连领帽（表示学位种类）\nv. 覆盖；用头巾包；使(马,鹰等)戴头罩；给…加罩\n[网络] 胡德；兜帽；引擎盖'
#中文翻译.split('\n')
#取按词性释义(中文翻译)


#所有词条 = [{'词': 'contort', '释义': 'contort'}, {'词': 'contour', '释义': 'contour'}]
#所有词 =['contorts', 'contouring']
#选取释义(所有词条, 所有词)
def 选取释义(所有词条, 所有词):
    所有释义 = []
    if (len(所有词条) == 2) :        
        词1释义 = 所有词条[0]['释义']
        词2释义 = 所有词条[1]['释义']
        if (词1释义 and (词典常量.词性_形容词 in 取按词性释义(词1释义))
          and 词2释义 and  ( 词典常量.词性_名词 in 取按词性释义(词2释义)) ):
            所有释义.append(首选(词1释义, 词典常量.词性_形容词))
            所有释义.append(首选(词2释义, 词典常量.词性_名词))
            return 所有释义

        for i  in  range(len(所有词条)):
            词条 = 所有词条[i]
            所有释义.append(首选(词条['释义'], 词典常量.词性_计算机) if  词条['释义'] else 所有词[i])
    #print(所有词条)
    #print(所有词)
    for 词条, 词 in zip(所有词条, 所有词):
        print(词条['释义'], '***',词典常量.词性_计算机)
        所有释义.append(词 if  词条['释义']=='' else 首选(词条['释义'], 词典常量.词性_计算机))
    return 所有释义 

def 首选(中文释义: str ,首选词性: str): 
    '''
    从翻译中找出制定词性的翻译
    
    中文翻译 = 'n. 罩；风帽；（布质）面罩；学位连领帽（表示学位种类）\nv. 覆盖；用头巾包；使(马,鹰等)戴头罩；给…加罩\n[网络] 胡德；兜帽；引擎盖'
    首选(中文翻译,'v.')
    #'覆盖；用头巾包；使戴头罩；给…加罩'
    
    '''
    if not 中文释义:
        return
    
    首选词义 = ""
    
    
    #// TODO: 减少重复调用
    词性到释义 = 取按词性释义(中文释义)
    if ((词典常量.词性_计算机) in 词性到释义) :
        首选词义 = 词性到释义.get(词典常量.词性_计算机)[0]
    elif ((首选词性) in 词性到释义) :
        首选词义 = 词性到释义.get(首选词性)[0];
    else:
        #// 取第一个词性的第一释义
        for k in 词性到释义:
            首选词义 = 词性到释义[k][0]
            break
    #print(首选词义)   
    首选词义 = 消除所有括号内容(首选词义)
    return 首选词义

#所有词条 = [{'词': 'contort', '释义': 'vt. 扭弯, 曲解\\nvi. 扭弯', '词形': [{'类型': '过去式', '变化': 'contorted'}, {'类型': '过去分词', '变化': 'contorted'}, {'类型': '现在分词', '变化': 'contorting'}, {'类型': '第三人称单数', '变化': 'contorts'}, {'类型': '名词复数形式', '变化': 'contorts'}]}, {'词': 'contour', '释义': 'n. 轮廓\\nvt. 画轮廓\\na. 显示轮廓的\\n[计] 轮廓', '词形': [{'类型': '名词复数形式', '变化': 'contours'}, {'类型': '过去分词', '变化': 'contoured'}, {'类型': '现在分词', '变化': 'contouring'}, {'类型': '过去式', '变化': 'contoured'}, {'类型': '第三人称单数', '变化': 'contours'}]}, {'词': 'contoured', '释义': 'a. 波状外形的', '词形': [{'类型': '原型', '变化': 'contour'}, {'类型': '原型变换形式', '变化': ['过去分词', '过去式']}, {'类型': '过去分词', '变化': 'contoured'}]}]
#所有词 =['contorts', 'contouring', 'contoured']
#首选('vt. 扭弯, 曲解\nvi. 扭弯 ','[计]' )

def 取释义(选中文本: str): 
    所有词 = 取字段中所有词(选中文本)
    
    所有词条 = []
    for  单词 in 所有词:
        处理后词 = 单词
        #print(处理后词)
        if 处理后词 in 自定义词典.不翻译 :
            #// TODO: 使用"单词条"数据结构
            #print(处理后词)
            所有词条.append({'词': 处理后词,'释义': 处理后词})
            continue
        #// 仅在命名包含多词时取原型
        
        
        
       
        if 处理后词 in 词形变化数据.keys():
            #print(词形变化数据[处理后词])
            if (len(所有词) > 1) :
                处理后词 = 取原型(处理后词, 提取词形(词形变化数据[处理后词]))
            所有词形 = 提取词形(词形变化数据[处理后词])
        else:
            continue
        
        所有词条.append({
              '词': 处理后词,
              '释义': 词典数据[处理后词],
              '词形': 所有词形
            })
        #print(所有词条)
        #print('&&&&&&&&&&')
        
        
    释义 = 选中文本
    if ( len(所有词条)> 1) :
        短语释义 = 按短语查询(所有词条)
        if not (短语释义== None ):
            释义 = 短语释义
        else :
            #print('$$$$$',选中文本,'$$$$$', 所有词条,'$$$$$', 所有词)
            释义 = 逐词翻译(选中文本, 所有词条, 所有词)   
    elif (len(所有词条) == 1) :
        #// TODO: 简化词条 (以适应状态栏宽度)
        释义 = 所有词条[0]['释义']
  
    return ({'原字段': 选中文本, '释义': 释义, '各词': 所有词条})
                    
#选中文本 = "input"
#取释义(选中文本)

def 按短语查询(所有词条):
    所有词 = []
    for  词条 in 所有词条:
        所有词.append(词条['词'])
    短语 = " ".join(所有词)
    if 短语  in 自定义词典.常用短语.keys():
        return 自定义词典.常用短语[短语]
    if 短语 in 词典数据 .keys():
        return  首选(词典数据[短语], 词典常量.词性_计算机)
#xx= [{'词': 'contort', '释义': 'contort'}, {'词': 'contour', '释义': 'contour'}, {'词': 'contoured', '释义': 'contoured'}]
#按短语查询(xx)== None

def 逐词翻译(选中文本, 所有词条, 所有词):
    释义 = 选中文本
    首选释义 = 选取释义(所有词条, 所有词)
    各释义 = []
    for 序号 in  range(len(所有词)):
        下一词 = 所有词[序号]
        位置 = 释义.find(下一词)

        if (位置 > 0) :
            各释义.append(释义[0: 位置])
            if 所有词条[序号]['词']  in 自定义词典.常用命名.keys():
                #print(自定义词典.常用命名[所有词条[序号]['词']])
                各释义.append(自定义词典.常用命名[所有词条[序号]['词']])
            else:
                #print(首选释义[序号])
                各释义.append(首选释义[序号])
            
            #各释义.append(自定义词典.常用命名[所有词条[序号]['词']] or 首选释义[序号])
            释义 = 释义[位置 + len(下一词):]
      
    if (释义 != "") :
        各释义.append(释义)
      
    if (len(各释义)> 1 and  各释义[0].find("...") > 0) :
        释义 = 各释义[0].replace("...", "".join(各释义.splice(1)))
    else :
        释义 = "".join(各释义)
    
    return 释义

#选中文本 = 'contorts  contouring contoured'
#所有词条 = [{'词': 'contort', '释义': 'contort'}, {'词': 'contour', '释义': 'contour'}, {'词': 'contoured', '释义': 'contoured'}]
#所有词 =['contorts', 'contouring', 'contoured']





#全文翻译(hamletTxt,items)
def 全文翻译(输入文件=None):
    文件= 输入文件
    if 输入文件 == None:        
        文件= input('请输入需要翻译的文件')
    新内容,词集 = getText(文件)
    symbols = 词集
    原命名列表 = []
    #新内容 = 文件
    for 标识符 in symbols:
        if str.islower(标识符[0][0].lower()):
            原命名列表.append(消除英文小括号内容(标识符[0]))
    原命名列表.sort(key=lambda x:len(x),reverse=True)
    for  原命名 in 原命名列表:
        #print(原命名)
        #      
        #翻译 =  中文释义 if len(取字段中所有词(原命名)) > 1 else 首选(中文释义, 词典常量.词性_计算机)
        
        #中文释义 = 取释义(原命名)['释义']
        #中文释义 = eval(repr(中文释义).replace('\\\\', '\\'))
        '''
        if len(取字段中所有词(原命名)) > 1:
            翻译 = 短句翻译(原命名)
        else:        
            翻译 =  首选(中文释义, 词典常量.词性_计算机).split(',')[0].split(';')[0].split('；')[0]  #if len(取字段中所有词(原命名)) > 1 else    中文释义
        '''
        翻译 = 短句翻译(原命名)
        翻译 =  消除所有括号内容(翻译)   
        if (翻译 != None):            
            新内容 = re.sub(r'(\W)('+ 原命名+r')(\W)',r'\1'+翻译+r'\3', 新内容)
            #新内容 = re.sub(原命名,翻译, 新内容)
    with open(文件[0:文件.find('.')]+ '_cn'+文件[文件.find('.'):] ,'w+', encoding='utf-8') as f:
        f.write(新内容)
    return 新内容


#对所有英文词按照词频排序
def getText(文件):                             #定义函数读取文件
    txt = open(文件,"r").read()    
    txt1 = txt
    txt = txt.lower()                      #将所有字符转换为小写
    for ch in '!@#$%^&*()-+=\\[]}{|;:\'\"`~,<.>?/':  #  '!@#$%^&*(_)-+=\\[]}{|;:\'\"`~,<.>?/'
        txt = txt.replace(ch, " ")         #将所有特殊符号用空格替代
    #return txt
    hamletTxt = txt
    words = hamletTxt.split()                  #用空格分隔文本并生成列表
    counts = {}
    for word in words:
        counts[word]=counts.get(word,0)+1      #生成字典的内容:若该键存在则取其值并+1
    items=list(counts.items())                 #返回所有键值对信息，生成列表
    items.sort(key=lambda x:x[1],reverse=True) #对列表反排序:降序排列
    return (txt1,items)


def 短句翻译 (英文句子):
    str1=''
    for 单词 in 英文句子.split():
        #print(单词)
        #中文释义 = 取释义(单词)['释义'].split(',')[0].split('；')[0]
        if '_' in 单词:
            下划线单词 = ''
            for 词 in 单词.split("_"):
                下划线单词 = 下划线单词.strip()+'_'+ 短句翻译(词)
            str1 = str1 + 下划线单词[1:] + ' '
        #要添加 elif 函数，实现驼峰数据翻译
        elif '_' in camel_to_underline(单词):
            #print(单词)
            下划线单词 = ''
            驼峰词 = camel_to_underline(单词)
            if 驼峰词[0] == '_':
                驼峰词= 驼峰词[1:]
            for 词 in 驼峰词.split("_"):
                下划线单词 = 下划线单词.strip()+'冖'+ 短句翻译(词) #乛冖亠
            str1 = str1 + 下划线单词[1:] + ' '
        else:
            中文释义 = 取释义(单词)['释义']
            中文释义 = eval(repr(中文释义).replace('\\\\', '\\'))
            #print(中文释义)
            翻译 =   首选(中文释义, 词典常量.词性_计算机)
            #print(取释义(单词)['释义'].split(',')[0].split('；')[0])
            翻译 = 翻译.split(',')[0].split('；')[0].split(';')[0]
            翻译 =  消除所有括号内容(翻译)
            str1 = str1 + 翻译 + ' '
    return str1


