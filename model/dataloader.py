"""
programmed to enable data input into the model

data is from folder /data
"""

import torch as t 
import torchvision as tv
from torchvision import transforms
import os
import json
import numpy as np
import pandas as pd
from PIL import Image

class data_set(t.utils.data.Dataset):
    def __init__(self, idx):
        self.idx = idx
        self.config = json.load(open('config.json'))
        self.data_root = self.config["Training_Dir"]
        self.names = np.array(os.listdir(self.data_root))[idx]
        self.label_path = self.config['Label_Path']
        self.init_transform()
        self.read_label()

    def read_label(self):
        dataframe = pd.read_csv(self.label_path)
        data = dataframe.values
        self.label = data[:,1][self.idx]

    def init_transform(self):
        self.transform = transforms.Compose([
            transforms.ToTensor()
        ])

    def __getitem__(self, index):
        data = np.load(os.path.join(self.data_root, self.names[index]))
        voxel = self.transform(data['voxel'].astype(np.float32))
        seg = data['seg'].astype(np.float32)
        label = self.label[index]
        data = voxel
        return data, label

    def __len__(self):
        return len(self.names)

class MyDataSet():
    def __init__(self):
        super().__init__()
        self.config = json.load(open('config.json'))
        self.data_root = self.config["Training_Dir"]
        self.data_names = np.array(os.listdir(self.data_root))
        self.DEVICE = t.device(self.config["DEVICE"])
        self.gray = self.config["gray"]

    def test_train_split(self, p=0.8):
        length = len(self.data_names)

        idx = np.array(range(length))
        np.random.shuffle(idx)
        self.train_idx = idx[:(int)(length*p)]
        self.test_idx = idx[(int)(length*p):]

        self.train_set = data_set(self.train_idx)
        self.test_set = data_set(self.test_idx)
        return self.train_set, self.test_set

# class In_the_wild_set(t.utils.data.Dataset):
#     def __init__(self):
#         super().__init__()
#         self.config = json.load(open('config.json'))
#         self.test_root = self.config["Test_Dir"]
#         self.test_names = os.listdir(self.test_root)
#         self.DEVICE = t.device(self.config["DEVICE"])
#         self.gray = self.config["gray"]
#         self.init_transform()

#     def init_transform(self):
#         """ preprocessing the image and label """
#         self.transform = transforms.Compose([
#             transforms.ToTensor(),
#         ])

#     def __getitem__(self, index):
#         data = np.load(os.path.join(self.test_root, self.test_names[index]))
#         voxel = self.transform(data['voxel'].astype(np.float32))
#         seg = data['seg'].astype(np.float32)
#         data = np.concatenate([voxel, seg])
#         return data

#     def __len__(self):
#         return len(self.test_names)


if __name__ == "__main__":

    DataSet = MyDataSet()
    train_set, test_set = DataSet.test_train_split()
    wild = In_the_wild_set()
    print(len(train_set))
    print(len(test_set))
    print(train_set[0][0].shape)
    print(test_set[0][0].shape)
    print(wild[0].shape)



