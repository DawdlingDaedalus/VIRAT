types_path = '/Users/p/Documents/Code/VIRAT/VIRAT_Ground_Dataset/diva_annotations/train/VIRAT_S_000200_03_000657_000899.types.yml'
geom_path = '/Users/p/Documents/Code/VIRAT/VIRAT_Ground_Dataset/diva_annotations/train/VIRAT_S_000200_03_000657_000899.geom.yml'

import yaml
import pandas as pd

with open(types_path, 'r') as file:
    types = yaml.safe_load(file)

try:
    with open(geom_path, 'r') as file:
        geom = yaml.safe_load(file)
except Exception as e:
    print(f"An error occurred: {e}")


# helper func
def get_labels_conf(types):
  # returns lists: labels, conf
  labels = []
  confs = []
  for i in types:
    try:
      if (i['types']['id1'] in track_id):
          label, conf = next(iter(i['types']['cset3'].items()))
          labels.append(label)
          confs.append(conf)
    except:
      pass

  return labels, confs


# create a ground truth dataframe, gtdf

detections = []
# no frame_num needed

# sample of geom with detections by frame_num
for i in geom:
  try:
    if i['geom']['id0'] > -1:
      detections.append(i)
  except:
    pass

# parse data from detections
idx = [i['geom']['id0'] for i in detections]
track_id = [i['geom']['id1'] for i in detections]
label, conf = get_labels_conf(types)
frame = [i['geom']['ts0'] for i in detections]
xmin, ymin, xmax, ymax = [], [], [], []
for i in detections:
  bb = i['geom']['g0'].split(' ')
  xmin.append(int(bb[0]))
  ymin.append(int(bb[1]))
  xmax.append(int(bb[2]))
  ymax.append(int(bb[3]))

# get class labels as int for comparison with predictions
label_int = labels_as_int(label)

gt = {'idx_gt': idx, 'track_id_gt': track_id, 'label_gt': label,
      'label_as_int_gt': label_int, 'conf_gt': conf, 'frame_gt': frame,
      'xmin_gt': xmin, 'ymin_gt': ymin, 'xmax_gt': xmax, 'ymax_gt': ymax}
gtdf = pd.DataFrame(gt)
gtdf
