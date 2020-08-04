#!/usr/bin/env python3
# This file is covered by the LICENSE file in the root of this project.

import torch
import torch.nn as nn
import torch.optim as optim
import torch.backends.cudnn as cudnn
import torchvision.transforms as transforms
import imp
import yaml
import time
from PIL import Image
import __init__ as booger
import collections
import copy
import cv2
import scipy.misc
import os
import numpy as np

from tasks.semantic.modules.seq_segmentator import *
from tasks.semantic.postproc.KNN import KNN


class User():
  def __init__(self, ARCH, DATA, datadir, preddir, logdir, modeldir):
    # parameters
    self.ARCH = ARCH
    self.DATA = DATA
    self.datadir = datadir
    self.preddir = preddir
    self.logdir = logdir
    self.modeldir = modeldir

    # get the data
    parserModule = imp.load_source("parserModule",
                                   booger.TRAIN_PATH + '/tasks/semantic/dataset/' +
                                   self.DATA["name"] + '/vis_parser.py')
    self.parser = parserModule.Parser(root=self.datadir,
                                      pred_root=preddir,
                                      train_sequences=self.DATA["split"]["train"],
                                      valid_sequences=self.DATA["split"]["valid"],
                                      test_sequences=self.DATA["split"]["test"],
                                      labels=self.DATA["labels"],
                                      color_map=self.DATA["color_map"],
                                      learning_map=self.DATA["learning_map"],
                                      learning_map_inv=self.DATA["learning_map_inv"],
                                      sensor=self.ARCH["dataset"]["sensor"],
                                      mode='test',
                                      frame_num=4,
                                      max_points=self.ARCH["dataset"]["max_points"],
                                      batch_size=4,
                                      workers=self.ARCH["train"]["workers"],
                                      gt=True,
                                      shuffle_train=False)

    # concatenate the encoder and the head
    # with torch.no_grad():
    #   self.model = Segmentator(self.ARCH,
    #                            self.parser.get_n_classes(),
    #                            self.modeldir)
    #
    # # use knn post processing?
    self.post = None
    # if self.ARCH["post"]["KNN"]["use"]:
    #   self.post = KNN(self.ARCH["post"]["KNN"]["params"],
    #                   self.parser.get_n_classes())
    #
    # # GPU?
    # self.gpu = False
    # self.model_single = self.model
    # self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # print("Infering in device: ", self.device)
    # if torch.cuda.is_available() and torch.cuda.device_count() > 0:
    #   cudnn.benchmark = True
    #   cudnn.fastest = True
    #   self.gpu = True
    #   self.model.cuda()

  def infer(self):
    # do train set
    # self.infer_subset(loader=self.parser.get_train_set(),
    #                   to_orig_fn=self.parser.to_original)
    #
    # do valid set
    self.infer_subset(loader=self.parser.get_valid_set(),
                      to_orig_fn=self.parser.to_original)
    # do test set
    # self.infer_subset(loader=self.parser.get_test_set(),
    #                   to_orig_fn=self.parser.to_original)

    print('Finished Infering')

    return

  def infer_subset(self, loader, to_orig_fn):
    # switch to evaluate mode
    # self.model.eval()

    # empty the cache to infer in high res
    # if self.gpu:
    #   torch.cuda.empty_cache()

    with torch.no_grad():
      end = time.time()

      for i, (proj_colors, path_seq, path_name) in enumerate(loader):

        if self.post:
          pass
        else:
          # put in original pointcloud using indexes
          for batch_idx in range(proj_colors.shape[0]):
              for frame_idx in range(proj_colors.shape[1]):
                  cur_proj_colors = proj_colors[batch_idx, frame_idx].numpy()
                  # cur_proj_colors[..., 0], cur_proj_colors[..., 2] = cur_proj_colors[..., 2], cur_proj_colors[..., 0]
                  img_path = os.path.join(self.logdir, "sequences",
                                          path_seq[frame_idx][batch_idx], "imgs")
                  os.makedirs(img_path, exist_ok=True)
                  img_file = os.path.join(img_path, path_name[frame_idx][batch_idx].replace(".label", ".jpg"))
                  print(img_file)
                  scipy.misc.imsave(img_file, cur_proj_colors)
                  print("Infered seq", path_seq[frame_idx][batch_idx], "scan", path_name[frame_idx][batch_idx],
                        "in", time.time() - end, "sec")
                  end = time.time()



