import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import PIL
from PIL import Image
import shutil
import zipfile
import glob
import os
import time

device= torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model = torchvision.models.resnet50(pretrained=True)

num_ftrs = model.fc.in_features
model.fc = nn.Sequential(
    nn.Dropout(0.5),
    nn.Linear(num_ftrs, 1024),
    nn.Dropout(0.2),
    nn.Linear(1024, 512),
    nn.Dropout(0.1),
    nn.Linear(512, 1),
    nn.Sigmoid()
)

model.to(device)

                                    # 여기에 모델 경로를 설정
model.load_state_dict(torch.load('blog/MODEL_STATE2.pt', map_location=device))

model.eval()

# 여기에 사진이 올라갈 폴더의 위치를 설정
test_dir = 'media/target'

test_files = os.listdir(test_dir)

for item in test_files:
    file_name, file_ext = os.path.splitext(item)
    if file_ext == '.png':
        im = Image.open(os.path.join(test_dir, item))
        bg = Image.new("RGB", im.size, (255,255,255))
        bg.paste(im,im)
        bg.save(os.path.join(test_dir, f'{file_name}.jpg'))
        os.remove(os.path.join(test_dir, item))

# png를 jpg로 바꾸는 과정을 거친 후 파일 목록 재생성
test_files = os.listdir(test_dir)


class CustomDataset(torch.utils.data.Dataset):
    def __init__(self, files, root, mode='test', transform=None):
        self.files = files
        self.root = root
        self.mode = mode
        self.transform = transform
    
    def __len__(self):
        return len(self.files)
    
    def __getitem__(self, index):
        img = PIL.Image.open(os.path.join(self.root, self.files[index]))
        if self.transform:
            img = self.transform(img)
        return img, self.files[index]

test_transform = torchvision.transforms.Compose([
    torchvision.transforms.Resize((224,224)),
    torchvision.transforms.ToTensor()
])

test_dataset = CustomDataset([test_files[0]], test_dir, transform=test_transform)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=32, shuffle=False)

with torch.no_grad():
    model.eval()
    ret = None
    for img, files in data_loader:
        img = img.to(device)
        pred = model(img)
        if ret is None:
            ret = pred.cpu().numpy()
        else:
            ret = np.vstack([ret, pred.cpu().numpy()])
numlist = ret.tolist()

floatnumlist = [float(s[0]) for s in numlist]
for i in range(len(floatnumlist)):
    floatnumlist[i] = int(floatnumlist[i]*100000)/100000

floatnum = floatnumlist[0]

sample_pred = ret[:]
sample_pred[sample_pred >= 0.5] = 1
sample_pred[sample_pred < 0.5] = 0

target_pred = sample_pred[0][0]

classes = {0:'cat', 1:'dog'}
print(f'{classes[target_pred]} : {floatnum}')

# target_pred가 1이면 개, 0이면 고양이
# floatnum은 모델이 이미지가 얼마나 개나 고양이를 닮았는지를 수치화한 값


