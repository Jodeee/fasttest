#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
try:
    import cv2
except:
    pass

class OpencvUtils(object):

    def __init__(self,baseimage, matchimage, height):

        self.baseimage = baseimage
        self.matchimage = matchimage
        self.height = height
        self.iszoom = False

    def extract_minutiae(self):
        """
        提取特征点
        :return:
        """
        if os.path.exists(self.matchimage):
            self.baseimage = cv2.imread(self.baseimage)
            # self.baseimage = cv2.resize(self.baseimage, dsize=(int(self.baseimage.shape[1] / 2), int(self.baseimage.shape[0] / 2)))
            self.matchimage = cv2.imread(self.matchimage)

            view_height = self.height
            image_height = self.baseimage.shape[0]
            if view_height * 2 == image_height:
                self.iszoom = True

        else:
            raise FileExistsError(self.matchimage)

        # 创建一个SURF对象
        surf = cv2.xfeatures2d.SURF_create(1000)

        # SIFT对象会使用Hessian算法检测关键点，并且对每个关键点周围的区域计算特征向量。该函数返回关键点的信息和描述符
        keypoints1, descriptor1 = surf.detectAndCompute(self.baseimage, None)
        keypoints2, descriptor2 = surf.detectAndCompute(self.matchimage, None)

        if descriptor2 is None:
            return None

        # 特征点匹配
        matcher = cv2.FlannBasedMatcher()
        matchePoints = matcher.match(descriptor1, descriptor2)

        # #提取强匹配特征点
        minMatch = 1
        maxMatch = 0
        for i in range(len(matchePoints)):
            if minMatch > matchePoints[i].distance:
                minMatch = matchePoints[i].distance
            if maxMatch < matchePoints[i].distance:
                maxMatch = matchePoints[i].distance
        if minMatch > 0.2:
            return None
        # #获取排列在前边的几个最优匹配结果
        DMatch = None
        MatchePoints = []
        for i in range(len(matchePoints)):
            if matchePoints[i].distance == minMatch:
                try:
                    keypoint = keypoints1[matchePoints[i].queryIdx]
                    x, y = keypoint.pt
                    if self.iszoom:
                        x = x / 2.0
                        y = y / 2.0
                    keypoints1 = [keypoint]

                    dmatch = matchePoints[i]
                    dmatch.queryIdx = 0
                    MatchePoints.append(dmatch)
                except:
                    continue

        # 绘制最优匹配点
        outImg = None
        outImg = cv2.drawMatches(self.baseimage, keypoints1, self.matchimage, keypoints2, MatchePoints, outImg, matchColor=(0, 255, 0),
                                 flags=cv2.DRAW_MATCHES_FLAGS_DEFAULT)
        # cv2.imwrite("outimg.png", outImg)

        matchinfo = {
            'x':int(x),
            'y':int(y),
            'ocrimg':outImg
        }
        return matchinfo

