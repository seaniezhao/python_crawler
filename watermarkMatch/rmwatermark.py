from bluewatermark import rmbluewatermark
from redwatermark import rmredwatermark
import os.path

rootdir = "E:/常用资料89/7、拆装步骤(1440)"    # 指明被遍历的文件夹
#rootdir = "E:/常用资料89/1、正时匹配3002/汽车列表/54、马自达/11、[长安马自达] 马自达3/内容页图片"    # 指明被遍历的文件夹
for parent, dirnames, filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字

    for filename in filenames:                        #输出文件信息

        if filename[-3:] == "png" and '_' not in filename and '内容页图片' in parent:
                strlist = parent.split('\\')
                #print(strlist[-1] )
                picpath = os.path.join(parent, filename)
                if not os.path.exists(picpath[:-4] + "_p.png"):
                    if '[' in strlist[-1]:
                        #print("red"+picpath)

                        rmredwatermark(picpath)
                    else:
                        rmbluewatermark(picpath)
                        #print(picpath)
                #pass