import os

def search_file(file): # 递归读取文件
    if os.path.isdir(file):
        lst = os.listdir(file)
        for f in lst:
            if os.path.isdir(os.path.join(file, f)):
                search_file(os.path.join(file, f))
            elif len(f.split('.')) == 1:
                continue
            elif f.split('.')[1] == 'py':
                start(os.path.join(file, f))
    else:
        start(file)
        
def start(file):
    global sum
    num = 0
    try:
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                # 跳过空行和注释行
                line = line.strip()
                if line == '' or line.startswith('#') or line.startswith('"') or line.startswith("'"):
                    continue
                else:
                    num += 1
        sum += num
        print(f'{os.path.basename(file)} 写了{num}行代码')
    except FileNotFoundError:
        print(f'错误：找不到文件 "{file}"')
    except UnicodeDecodeError:
        print('错误：文件编码不是UTF-8，请检查文件编码')
    except Exception as e:
        print(f'读取文件时发生错误：{e}')

file = input('输入你的python代码文件地址：')
sum = 0
search_file(file)
print(f'你一共写了{sum}行代码')