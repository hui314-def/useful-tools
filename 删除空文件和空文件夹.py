import os

def delete(path):
    if os.listdir(path)==[]:
        os.rmdir(path)
        print('删除空文件夹：',path)
    else:
        for i in os.listdir(path):
            new_path=os.path.join(path,i)
            if os.path.isdir(new_path):
                delete(new_path)
            else:
                if os.path.getsize(new_path)==0:
                    os.remove(new_path)
                    print('删除空文件：',new_path)

path=input('输入你要删除的文件夹路径，默认删除空文件夹及其空文件:')

if os.path.isdir(path):
    delete(path)
else:
    print('文件夹不存在')
