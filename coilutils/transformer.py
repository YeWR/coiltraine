import numpy as np
import torch

from PIL import Image


def colormap_cityscapes(n):
    cmap = np.zeros([n, 3]).astype(np.uint8)
    cmap[0, :] = np.array([128, 64, 128])
    cmap[1, :] = np.array([255, 215, 0])
    # cmap[2, :] = np.array([255, 215, 0])
    # cmap[3, :] = np.array([255, 215, 0])
    # cmap[4, :] = np.array([255, 215, 0])
    # cmap[5, :] = np.array([255, 215, 0])
    #
    # cmap[6, :] = np.array([255, 215, 0])
    # cmap[7, :] = np.array([255, 215, 0])
    # cmap[8, :] = np.array([255, 215, 0])
    # cmap[9, :] = np.array([255, 215, 0])
    # cmap[10, :] = np.array([255, 215, 0])
    #
    # cmap[11, :] = np.array([255, 215, 0])
    # cmap[12, :] = np.array([255, 215, 0])
    # cmap[13, :] = np.array([255, 215, 0])
    # cmap[14, :] = np.array([255, 215, 0])
    # cmap[15, :] = np.array([255, 215, 0])
    #
    # cmap[16, :] = np.array([255, 215, 0])
    # cmap[17, :] = np.array([255, 215, 0])
    # cmap[18, :] = np.array([255, 215, 0])
    # cmap[19, :] = np.array([255, 215, 0])

    return cmap


def colormap(n):
    cmap = np.zeros([n, 3]).astype(np.uint8)

    for i in np.arange(n):
        r, g, b = np.zeros(3)

        for j in np.arange(8):
            r = r + (1 << (7 - j)) * ((i & (1 << (3 * j))) >> (3 * j))
            g = g + (1 << (7 - j)) * ((i & (1 << (3 * j + 1))) >> (3 * j + 1))
            b = b + (1 << (7 - j)) * ((i & (1 << (3 * j + 2))) >> (3 * j + 2))

        cmap[i, :] = np.array([r, g, b])

    return cmap


class Bilabel:

    def __init__(self, rlabel):
        self.rlabel = rlabel

    def __call__(self, tensor):
        assert (isinstance(tensor, torch.LongTensor) or isinstance(tensor,
                                                                   torch.ByteTensor)), 'tensor needs to be LongTensor'
        tensor[tensor == self.rlabel] = 0
        tensor[tensor != self.rlabel] = 1
        return tensor


class Relabel:

    def __init__(self, olabel, nlabel):
        self.olabel = olabel
        self.nlabel = nlabel

    def __call__(self, tensor):
        assert (isinstance(tensor, torch.LongTensor) or isinstance(tensor,
                                                                   torch.ByteTensor)), 'tensor needs to be LongTensor'
        tensor[tensor == self.olabel] = self.nlabel
        return tensor


class ToLabel:

    def __call__(self, image):
        return torch.from_numpy(np.array(image)).long().unsqueeze(0)


class Colorize:

    def __init__(self, n=22):
        # self.cmap = colormap(256)
        self.cmap = colormap_cityscapes(256)
        self.cmap[n] = self.cmap[-1]
        self.cmap = torch.from_numpy(self.cmap[:n])

    def __call__(self, gray_image):
        size = gray_image.size()
        # print(size)
        color_image = torch.ByteTensor(3, size[1], size[2]).fill_(0)
        # color_image = torch.ByteTensor(3, size[0], size[1]).fill_(0)

        # for label in range(1, len(self.cmap)):
        for label in range(0, len(self.cmap)):
            mask = gray_image[0] == label
            # mask = gray_image == label

            color_image[0][mask] = self.cmap[label][0]
            color_image[1][mask] = self.cmap[label][1]
            color_image[2][mask] = self.cmap[label][2]

        return color_image

class Colorizes:

    def __init__(self, n=22):
        # self.cmap = colormap(256)
        self.cmap = colormap_cityscapes(256)
        self.cmap[n] = self.cmap[-1]
        self.cmap = torch.from_numpy(self.cmap[:n])

    def __call__(self, gray_images):
        size = gray_images.size()

        color_images = torch.ByteTensor(size[0], 3, size[2], size[3]).fill_(0)

        for i in range(size[0]):
            gray_image = gray_images[i].cpu().max(0)[1].data.unsqueeze(0)
            for label in range(0, len(self.cmap)):
                mask = gray_image[0] == label
                # mask = gray_image == label

                color_images[i][0][mask] = self.cmap[label][0]
                color_images[i][1][mask] = self.cmap[label][1]
                color_images[i][2][mask] = self.cmap[label][2]

        return color_images