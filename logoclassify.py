"""
Reproduce Imagnenet results of Snell et al Prototypical networks.
"""
import numpy as np
from PIL import Image
import torch
import argparse
import os
from torchvision import transforms
import pprint as pp

import matplotlib.pyplot as plt
import pandas as pd
from torch.optim import Adam
from torch.utils.data import DataLoader
import cv2

from few_shot.config import PATH
from few_shot.callbacks import *
from few_shot.core import EvaluateFewShot, NShotTaskSampler, prepare_nshot_task
from few_shot.datasets import MiniImageNet, OmniglotDataset
from few_shot.metrics import categorical_accuracy
from few_shot.models import get_few_shot_encoder
from few_shot.proto import proto_net_episode
from few_shot.train import fit
from few_shot.utils import setup_dirs

setup_dirs()
device = torch.device('cpu')

###########
# Dataset #
###########
images = []
id_to_classname = {}
i = 0
for root, folders, files in os.walk('data_custom/'):
    if len(files) == 0:
        continue

    class_name = root.split('/')[-1]
    id_to_classname[i] = class_name
    i += 1
    for f in files:
        images.append({
            'class_name': class_name,
            'filepath': os.path.join(root, f)
        })

df = pd.DataFrame(images)

df = df.assign(id=df.index.values)

unique_characters = sorted(df['class_name'].unique())
class_name_to_id = {
    unique_characters[i]: i for i in range(len(df['class_name'].unique()))}
df = df.assign(class_id=df['class_name'].apply(
    lambda c: class_name_to_id[c]))

#########
# Model #
#########

# HAVE TO CHANGE TO LOAD FROM MODELS
model = get_few_shot_encoder(3)
model.load_state_dict(torch.load(
    "models/proto_nets/logos_nt=1_kt=4_qt=2_nv=1_kv=1_qv=1.pth", map_location=torch.device('cpu')))
model.eval()
model.to(device, dtype=torch.double)


############
# Prepare  #
############

n_train = 4
# All the classes
k_train = len(df['class_name'].unique())
q_train = 0

optimiser = Adam(model.parameters(), lr=1e-3)
loss_fn = torch.nn.NLLLoss().cuda()

transform = transforms.Compose([
        transforms.CenterCrop(200),
        transforms.Resize(84),
        transforms.ToTensor(),
        # transforms.Normalize(mean=[0.485, 0.456, 0.406],
        #                      std=[0.229, 0.224, 0.225])
    ])

def getimage(filepath: str):
    instance = Image.open(filepath)
    instance = transform(instance)
    return instance

def classify(image):
    batch_images = []
    batch_id = []

    # Get support images
    support_k = {k: None for k in range(0, k_train)}
    for k in range(0, k_train):
        # Select support examples
        support = df[df['class_id'] == k].sample(n_train)
        for i, s in support.iterrows():
            batch_images.append(getimage(s['filepath']))
            batch_id.append(s['class_id'])

    batch = [torch.stack(batch_images), torch.tensor(batch_id)]

    # Add query image
    print(type(image))
    image_to_add = transform(Image.fromarray(image))
    image_to_add = torch.unsqueeze(image_to_add[:3], 0)

    batch[0] = torch.cat((batch[0], image_to_add), 0)
    batch[1] = torch.cat((batch[1], torch.tensor([2])), 0)

    # Prepare to launch model
    x, y = prepare_nshot_task(n_train, k_train, q_train+1)(batch)

    loss, y_pred = proto_net_episode(
        model,
        optimiser,
        loss_fn,
        x,
        y,
        n_train,
        k_train,
        q_train+1,
        distance='l2',
        train=False,
    )

    model(x)

    # fig, axs = plt.subplots(k_train, 2)
    # # Change size
    # fig.set_size_inches(18.5, 10.5, forward=True)

    # # Adjust with the correlation
    # for image in range(0, k_train):
    #     print(y_pred[0][image].item())
    #     # x[image] = x[image].mul(y_pred[0][image].item())

    # # Set images with the left being the support and right the query

    # for image in range(0, k_train+1):
    #     a = np.array(x[image])
    #     # a = a.astype(np.uint16) * 255
    #     # a = a[[1,2,0]]
    #     a = a.transpose((1, 2, 0))
    #     axs[image % k_train][int(image/k_train)].imshow(a)
    # # Remove axis`
    # for axis in axs:
    #     for a in axis:
    #         a.axis('off')

    # plt.show()
    print(torch.argmax(y_pred))
    return id_to_classname[torch.argmax(y_pred).item()]
