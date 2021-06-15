import random
import cv2
import json
import os
from detectron2.utils.visualizer import ColorMode
from detectron2.engine import DefaultTrainer
from detectron2.structures import BoxMode
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.utils.visualizer import Visualizer
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2 import model_zoo
import numpy as np
import torch
import detectron2
import pycocotools

MetadataCatalog.get("logo_test").set(thing_classes=["logo"])
logo_metadata = MetadataCatalog.get("logo_test")

model = "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"

cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file(model))
cfg.INPUT.MASK_FORMAT = 'bitmask'
cfg.MODEL.DEVICE = "cpu"
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1

cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "model_final.pth")
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.4
cfg.DATASETS.TEST = ("logo_test", )
predictor = DefaultPredictor(cfg)

def imsize(box):
  return (box[3]-box[1])*(box[2]-box[0])

def predict(image):
  height, width, _ = image.shape
  image_size = height * width * 0.1

  alphaimage = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)

  outputs = predictor(image)

  masks = outputs["instances"].pred_masks.cpu().numpy()
  boxes = outputs["instances"].pred_boxes.tensor.cpu().numpy()

  for x in range(0,len(outputs["instances"].pred_masks)):
    boxtemp = boxes[x].astype(int)
    masktemp = masks[x]

    yield alphaimage[boxtemp[1]:boxtemp[3],boxtemp[0]:boxtemp[2]] * masktemp[boxtemp[1]:boxtemp[3],boxtemp[0]:boxtemp[2], None]
    