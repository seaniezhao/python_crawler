import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys
import os.path

def getSift():
    im = cv2.imread('E:/img/test/1.png')
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    #opencv 读取图片默认BGR
    sift = cv2.xfeatures2d.SIFT_create()
    keypoints,descriptors = sift.detectAndCompute(gray, None)
    img = im
    cv2.drawKeypoints(gray, keypoints, img)
    cv2.imshow('test', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def matchSift3():
    ''''' 
    匹配sift特征 
    '''
    img1 = cv2.imread('E:/img/test/0.jpg', 0)  # queryImage
    img2 = cv2.imread('E:/img/test/1.png', 0)  # trainImage
    sift = cv2.xfeatures2d.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)
    # 蛮力匹配算法,有两个参数，距离度量(L2(default),L1)，是否交叉匹配(默认false)
    bf = cv2.BFMatcher()
    #返回k个最佳匹配
    matches = bf.knnMatch(des1, des2, k=2)
    # cv2.drawMatchesKnn expects list of lists as matches.
    #opencv3.0有drawMatchesKnn函数
    # Apply ratio test
    # 比值测试，首先获取与A 距离最近的点B（最近）和C（次近），只有当B/C
    # 小于阈值时（0.75）才被认为是匹配，因为假设匹配是一一对应的，真正的匹配的理想距离为0
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append([m])
    img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good[:10], None, flags=2)

    plt.imshow(img3), plt.show()

def round6(src):
    if src%1==0.5:
        return int(src)
    return round(src)

def rmbluewatermark(path):
    watermark = cv2.imread('E:/img/test/0.jpg')

    print(path)
    try:
        img2 = cv2.imdecode(np.fromfile(path, dtype=np.uint8), 1)
    except Exception:
        fsock = open("E:/img/test/fail.txt", "a")
        fsock.write(path+'\n')
        fsock.close()
        return

    if img2 is None:
        fsock = open("E:/img/test/fail.txt", "a")
        fsock.write(path+'\n')
        fsock.close()
        return

    #img2 = cv2.imread(path)
    desrow = img2.shape[0]
    descol = img2.shape[1]


    watermarkrow = round6(desrow * 0.8)
    watermarkcol = round6(descol * 0.8)
    res = cv2.resize(watermark, (watermarkcol, watermarkrow))


    indexrow = round6(desrow * 0.1)
    indexcol = round6(descol * 0.1)

    #img2[indexrow:watermarkrow+indexrow, indexcol:watermarkcol+indexcol] = img2[indexrow:watermarkrow+indexrow, indexcol:watermarkcol+indexcol] - res*0.08

    for i in range(0, watermarkrow):
        for j in range(0, watermarkcol):
            srcPt = img2[i + indexrow, j + indexcol]


            x = srcPt[0] - res[i, j, 0] * 0.08
            y = srcPt[1] - res[i, j, 1] * 0.08
            z = srcPt[2] - res[i, j, 2] * 0.08
            if x < 0:
                x = 0
            if y < 0:
                y = 0
            if z < 0:
                z = 0

            img2[i+indexrow, j+indexcol] = [x,y,z]

            x = round(srcPt[0]*1.1)
            y = round(srcPt[1]*1.1)
            z = round(srcPt[2]*1.1)
            if x > 255:
                x = 255
            if y > 255:
                y = 255
            if z > 255:
                z = 255

            img2[i + indexrow, j + indexcol] = [x, y, z]


    newpath = path[:-4]+"_p.png"
    #cv2.imwrite(newpath, img2)
    cv2.imencode('.png', img2)[1].tofile(newpath)
    #cv2.imshow('test', img2)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()


#matchSift3()
#getSift()
#removewatermark('E:/img/test/20.png')
#removewatermark('E:/img/test/2.png')
rootdir = "E:/img/newPic"                                   # 指明被遍历的文件夹


for parent, dirnames, filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字

    for filename in filenames:                        #输出文件信息

        #if filename[-3:] == "png"  and '_' not in filename  and '内容页图片' in parent:
        if filename[-3:] == "png" and '_p' not in filename:
                pass
                #rmbluewatermark(os.path.join(parent, filename))



