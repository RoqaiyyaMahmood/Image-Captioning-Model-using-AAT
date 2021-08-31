import os
import json
from inltk.inltk import tokenize
from inltk.inltk import setup


val = json.load(open('/Adapative_aligned_image_cap/AAT/data/annotations/captions_val2014.json', 'r'))
train = json.load(open('/Adapative_aligned_image_cap/AAT/data/annotations/captions_train2014.json', 'r'))
data = json.load(open('/Adapative_aligned_image_cap/AAT/data/split_coco.json', 'r'))

print (train.keys())
print (train['info'])
print (len(train['images']))
print (len(train['annotations']))
print (train['images'][0])
print (train['annotations'][0])

print (val.keys())
print (val['info'])
print (len(val['images']))
print (len(val['annotations']))
print (val['images'][0])
print (val['annotations'][0])

# combine all images and annotations together
imgs = val['images'] + train['images']
annots = val['annotations'] + train['annotations']


# for efficiency lets group annotations by image
itoa = {}

for a in annots:
    imgid = a['image_id']
    if not imgid in itoa: itoa[imgid] = []
    itoa[imgid].append(a)

# create the json blob
out = []
for i,img in enumerate(imgs):
    imgid = img['id']
    
    # coco specific here, they store train/val images separately
    loc = 'train2014' if 'train' in img['file_name'] else 'val2014'
    
    jimg = {}
    jimg['filepath'] =loc
    
    sentids = []
    annotsi = itoa[imgid]
    for a in annotsi:
        sentids.append(a['id'])
    jimg['sentids'] = sentids
    
    jimg['filename']=img['file_name']
    jimg['imgid'] = i
    
    jimg['split']=data[str(imgid)]
    
    sents = []
    annotsi = itoa[imgid]
    for a in annotsi:
        tokens_dict={}
        tokens_dict['tokens']=tokenize(a['caption'], 'hi')
        tokens_dict['raw']=a['caption']
        tokens_dict['imgid']=i
        tokens_dict['sentid']=a['id']
        sents.append(tokens_dict)
    jimg['sentences'] = sents
    jimg['cocoid'] = imgid
    
    out.append(jimg)
    
new_json={}
new_json['images']=out
new_json['dataset']='coco'


with open("/Adapative_aligned_image_cap/AAT/data/dataset_hindi_coco.json", "w") as outfile: 
    json.dump(new_json, outfile)
