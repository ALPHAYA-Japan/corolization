# pylint: disable-all

import torch
from torch.utils.data import Dataset
from skimage.color import rgb2lab
from skimage.io import imread
from skimage.transform import resize
import torchvision.datasets as dsets
from os import listdir
from os.path import join, isfile

class CustomImages(Dataset):
    def __init__(self, root, train=True, color_space='lab', transform=None):
        """
            color_space: 'yub' or 'lab'
        """
        self.root_dir = root
        self.root_dir += join(self.root_dir,
                              '/train') if train else join(self.root_dir, '/test')
        self.filenames = [f for f in listdir(
            self.root_dir) if isfile(join(self.root_dir, f))]
        self.color_space = color_space
        if (self.color_space not in ['rgb', 'lab']):
            raise(NotImplementedError)
        self.transform = transform

    def __len__(self):
        return len(self.filenames)

    def __getitem__(self, idx):
        img = imread(join(self.root_dir, self.filenames[idx]))
        img = resize(img, (256, 256))
        if self.color_space == 'lab':
            img = rgb2lab(img)

        bwimg = img[:, :, 0:1].transpose(2, 0, 1)
        bwimg = torch.from_numpy(bwimg).float()
        abimg = img[:, :, 1:].transpose(2, 0, 1)
        label = np.zeros((313, abimg.shape[0], abimg.shape[1]))
        for h in range(label.shape[1]):
            for w in range(label.shape[2]):
                binidx = color2bin(abimg[:][h][w])
                label[binidx][h][w] = 1
        label = torch.from_numpy(label).float()

        if self.transform is not None:
            bwimg = self.transform(bwimg)

        return (bwimg, label)
