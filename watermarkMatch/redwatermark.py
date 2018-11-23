import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys
import os.path

def round6(src):
    if src%1==0.5 or src%1==-0.5:
        return int(src)
    return round(src)

def createMask(shape):
    mask1 = cv2.imread('E:/img/redwatermark/xx_noStamp_outline.png')
    mask = cv2.cvtColor(mask1, cv2.COLOR_BGR2GRAY)
    emptyImage = np.zeros(shape, np.uint8)
    watermarkrow = mask.shape[0]
    watermarkcol = mask.shape[1]

    #if shape[0] < watermarkrow or shape[1] < watermarkcol:
        #return None

    desrow = shape[0]
    descol = shape[1]

    indexrow = round6((desrow-watermarkrow)/2)
    indexcol = round6((descol-watermarkcol)/2)

    for i in range(0, watermarkrow):
        for j in range(0, watermarkcol):
            if j+indexcol>=0 and i+indexrow>=0:
                if j+indexcol<shape[1] and i+indexrow<shape[0]:
                    emptyImage[i + indexrow, j + indexcol] = mask[i, j]


    return cv2.cvtColor(emptyImage, cv2.COLOR_BGR2GRAY)

def rmredwatermark(path):
    watermark = cv2.imread('E:/img/redwatermark/xx_noStamp.png')

    print(path)
    try:
        img2 = cv2.imdecode(np.fromfile(path, dtype=np.uint8), 1)
    except Exception:
        fsock = open("E:/img/redwatermark/fail.txt", "a")
        fsock.write(path+'\n')
        fsock.close()
        return

    if img2 is None:
        fsock = open("E:/img/redwatermark/fail.txt", "a")
        fsock.write(path+'\n')
        fsock.close()
        return

    mask = createMask(img2.shape)

    if mask is None:
        fsock = open("E:/img/redwatermark/maskfail.txt", "a")
        fsock.write( path)
        fsock.close()
        return


    watermarkrow = watermark.shape[0]
    watermarkcol = watermark.shape[1]

    #img2 = cv2.imread(path)
    desrow = img2.shape[0]
    descol = img2.shape[1]

    indexrow = round6((desrow-watermarkrow)/2)
    indexcol = round6((descol-watermarkcol)/2)

    #img2[indexrow:watermarkrow+indexrow, indexcol:watermarkcol+indexcol] = img2[indexrow:watermarkrow+indexrow, indexcol:watermarkcol+indexcol] - res*0.08

    for i in range(0, watermarkrow):
        for j in range(0, watermarkcol):

            if j+indexcol>=0 and i+indexrow>=0:
                if j+indexcol<descol and i+indexrow<desrow:
                    srcPt = img2[i + indexrow, j + indexcol]


                    x = srcPt[0] - watermark[i, j, 0] * 0.2
                    y = srcPt[1] - watermark[i, j, 1] * 0.2
                    z = srcPt[2] - watermark[i, j, 2] * 0.2


                    if x <= 0:
                        x = 0
                    if y <= 0:
                        y = 0
                    if z <= 0:
                        z = 0


                    img2[i+indexrow, j+indexcol] = [x,y,z]

                    if watermark[i, j, 0] != 0:
                        x = round(srcPt[0]/0.8)
                    if watermark[i, j, 1] != 0:
                        y = round(srcPt[1]/0.8)
                    if watermark[i, j, 2] != 0:
                        z = round(srcPt[2]/0.8)

                    if x > 255:
                        x = 255
                    if y > 255:
                        y = 255
                    if z > 255:
                        z = 255

                    img2[i + indexrow, j + indexcol] = [x, y, z]

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    #mask = cv2.dilate(mask, kernel)
    #mask = cv2.dilate(mask, kernel)
    dst = cv2.inpaint(img2, mask, 3, cv2.INPAINT_NS)


    dilate = cv2.dilate(img2, kernel)
    erode = cv2.erode(dilate, kernel)
    newpath = path[:-4]+"_p.png"

    cv2.imencode('.png', dst)[1].tofile(newpath)
    #cv2.imshow('dst', dst)
    #cv2.imshow('mask', mask)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()


#matchSift3()
#getSift()
#removewatermark('E:/img/test/20.png')
#createMask([1000, 1000])
#rmredwatermark('E:/img/redwatermark/2.png')

rootdir = r"D:\汽修\电路图\汽车列表\1、丰田\4、[广汽丰田] 雅力士\内容页图片\44、[2008广州丰田雅力士] 系统电路图-转向信号和危急警告灯"    # 指明被遍历的文件夹

for parent, dirnames, filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字

    for filename in filenames:                        #输出文件信息

        #if filename[-3:] == "png" and '_p' not in filename and '内容页图片' in parent:
        if filename[-3:] == "png" and '_p' not in filename and not os.path.exists(os.path.join(parent, filename[:-4]+'_p.png')):
                #print(filename[:-4])
                rmredwatermark(os.path.join(parent, filename))
                pass

