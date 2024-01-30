import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

image_M = cv2.imread("Milkyway.png", 0)
image_C = cv2.imread("Cells.png", 0)

width0, height0 = image_M.shape
maxNeighbour = max(math.floor(math.sqrt(height0)), math.floor(math.sqrt(width0)))
print(maxNeighbour)


def min_filter(img, N, BG):
    height, width = img.shape
    p = N // 2
    new_image = np.zeros_like(img)
    image_padded = np.pad(img, ((p, p), (p, p)), 'constant', constant_values=(BG, BG))
    for i in range(p, height + p):
        for j in range(p, width + p):
            new_image[i - p][j - p] = np.min(image_padded[i - p:i + p + 1, j - p:j + p + 1])
    return new_image


def max_filter(img, N, BG):
    height, width = img.shape
    p = N // 2
    new_image = np.zeros_like(img)
    image_padded = np.pad(img, ((p, p), (p, p)), 'constant', constant_values=(BG, BG))
    for i in range(p, height + p):
        for j in range(p, width + p):
            new_image[i - p][j - p] = np.max(image_padded[i - p:i + p + 1, j - p:j + p + 1])
    return new_image


def img_process(img, M, N, BG):
    out_image = np.zeros_like(img)
    height, width = img.shape
    if M == 0:
        image1 = min_filter(img, N, BG)
        image2 = max_filter(image1, N, BG)
        for i in range(height):
            for j in range(width):
                out_image[i][j] = img[i][j].astype(np.int32) - image2[i][j].astype(np.int32)
            if out_image[i][j] > 255:
                out_image[i][j] = 255
            elif out_image[i][j] < 0:
                out_image[i][j] = 0
        out_image = out_image.astype(np.uint8)
    if M == 1:
        image1 = max_filter(img, N, BG)
        image2 = min_filter(image1, N, BG)
        for i in range(height):
            for j in range(width):
                out_image[i][j] = img[i][j].astype(np.int32) - image2[i][j].astype(np.int32) + 255
            if out_image[i][j] > 255:
                out_image[i][j] = 255
            elif out_image[i][j] < 0:
                out_image[i][j] = 0
        out_image = out_image.astype(np.uint8)

    return out_image


def scale(img):
    height, width = img.shape
    flat_gray = img.reshape((width * height,)).tolist()
    A = min(flat_gray)
    B = max(flat_gray)

    if A == 0 and B == 255:
        return img

    output = np.uint8(255 / (B - A) * (img - A) + 0.5)
    return output


out = img_process(image_M, 0, 11, 0)
cv2.imshow('out', out)


out2 = scale(out)
cv2.imshow('out2', out2)
cv2.waitKey(0)
'''
plt.figure(figsize=(150, 150))
index = 1
for k in range(17, maxNeighbour):
    imgA = max_filter(image0, k, 0)
    plt.subplot(4, 4, index)
    index += 1
    plt.imshow(imgA, "gray")

plt.show()'''

plt.figure(figsize=(60, 60))
for i in range(1, 5):
    N_M = 2 * i + 1
    imageA = min_filter(image_M, N_M, 0)
    plt.subplot(2, 2, i)
    plt.imshow(imageA, "gray")

plt.show()
