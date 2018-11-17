import numpy as np
import math
import cv2
from PIL import Image
import matplotlib.pyplot as plt

from scipy.ndimage import gaussian_filter
from scipy.ndimage import sobel

class EdgeDetection:
    def __init__(self):
        self.threshold_1 = 220
        self.threshold_2 = 150

    def calc_offset(self, angle):
        if math.cos(angle) == 0:
          dl = 0
        else:
            dl = math.cos(angle) / abs(math.cos(angle))
        if math.sin(angle) == 0:
            dk = 0
        else:
            dk = math.sin(angle) / abs(math.sin(angle))
        return [dl, dk]
    
    def round_angles(self, angles):
        ret_angles = np.zeros((len(angles), len(angles[0])))
        comp = math.pi / 16

        for i in range(0, len(angles)):
            for j in range (0, len(angles[0])):
                for k in range(0, 7):
                    ret_angles[i][j] = k * math.pi / 8 if angles[i][j] - k * math.pi / 8 <= comp else ret_angles[i][j]

        return ret_angles
    
    def operator(self, operande):
        filtered_image = gaussian_filter(operande, 2)

        sobel_x = cv2.Sobel(filtered_image, cv2.CV_64F, 1, 0, ksize=5)
        sobel_y = cv2.Sobel(filtered_image, cv2.CV_64F, 0, 1, ksize=5)

        grad_mags = np.sqrt(np.square(np.array(sobel_x)) + np.square(np.array(sobel_y)))
        grad_mags = (grad_mags / np.amax(np.amax(grad_mags, 1), 0))*255
        grad_mags = grad_mags.astype(int)

        second_sobel_x = sobel(grad_mags.tolist(), 0)
        second_sobel_y = sobel(grad_mags.tolist(), 1)
        grad_angles = self.round_angles(np.arctan(np.divide(np.array(second_sobel_y), np.array(second_sobel_x))))
        
        return [grad_mags, grad_angles]

    def non_maxima_supp(self, grad_image):
        grad_mags = grad_image[0].tolist()
        # print(grad_mags)

        testarray = np.asarray(grad_mags)
        testImg = Image.fromarray(testarray)
        plot = plt.imshow(testImg)
        plt.show()

        #print('grad_mags', grad_mags)
        grad_angles = grad_image[1].tolist()

        #print('len(grad_mags)',len(grad_mags))
        #print('len(grad_mags[0])',len(grad_mags[0]))

        for i in range(0, len(grad_mags)):
            for j in range(0, len(grad_mags[i])):
                if i == 0 or j == 0 or i == len(grad_mags) - 1 or j == len(grad_mags[i]) - 1:
                    grad_mags[i][j] = 0

        for i in range(0, len(grad_mags)):
            for j in range(0, len(grad_mags[i])):


                if grad_mags[i][j] > 0:
                    l = i
                    k = j
                    offset = self.calc_offset(grad_angles[i][j])

                    dl = offset[0]
                    dk = offset[1]

                    while grad_mags[l][k] < grad_mags[int(l + dl)][int(k + dk)] or grad_mags[l][k] < grad_mags[int(l - dl)][int(k - dk)]:

                        grad_mags[l][k] = 0

                        if grad_mags[int(l + dl)][int(k + dk)] > grad_mags[int(l - dl)][int(k - dk)]:
                            l = int(l + dl)
                            k = int(k + dk)
                        else:
                            l = int(l - dl)
                            k = int(k - dk)

                        offset = self.calc_offset(grad_angles[l][k])
                        dl = offset[0]
                        dk = offset[1]

        return grad_mags

    #calculate the mask in function of the tresholds.
    #2 indicates a strong edge. 1 indicates a weak edge. 0 indicates a edge to cut
    def class_thresholding(self, image_maxima):
        mask = np.zeros((len(image_maxima), len(image_maxima[0])))
        print('len 1', len(image_maxima))
        print('len 2', len(image_maxima[0]))
        for i in range(0, len(image_maxima)):
            for j in range(0, len(image_maxima[i])):
                print('i',i,'j',j)
                if image_maxima[i][j] > self.threshold_1:
                    mask[i][j] = 2
                elif image_maxima[i][j] < self.threshold_1 and image_maxima[i][j] > self.threshold_2:
                    mask[i][j] = 1
        return mask

    def hysterisis_rec(self, mask, l, k):
        no_more_edge = True
        
        for m in range(-1, 1):
            for n in range(-1, 1):
                if not(m == 0 and n == 0):
                    no_more_edge = True if mask[l + m][k + n] != 0 else no_more_edge

        if no_more_edge:
            return False

        res = False
        for m in range(-1, 1):
            for n in range(-1, 1):
                if not(m == 0 and n == 0) and mask[l + m][k + n] != 0:
                    res = res or self.hysterisis_rec(mask, l + m, k + n)

        res = res or mask[l, k] == 2

        return res

    def hysterisis(self, mask, maxima):
        for i in range(0, len(maxima)):
            for j in range(0, len(maxima[i])):
                if mask[i][j] == 1:
                    is_strong = self.hysterisis_rec(mask, i, j)
                    if is_strong:
                        mask[i][j] = 2
                    else:
                        mask[i][j] = 0

        return mask

    def apply_mask(self, mask, maxima):
        mask = (np.matrix(mask) / 2).tolist()
        return (np.matrix(mask) * np.matrix(maxima)).tolist()

    def detect_edges(self, image):

        grad_image = self.operator(image)
        
        image_maxima = self.non_maxima_supp(grad_image)
        print(image_maxima)
        
        mask = self.class_thresholding(image_maxima)

        updated_mask = self.hysterisis(mask, image_maxima)

        testarray = np.asarray(image_maxima)
        testImg = Image.fromarray(testarray)
        plot = plt.imshow(testImg)
        plt.show()

        return self.apply_mask(updated_mask, image_maxima)






