import os
import json
val = json.load(open('annotations/captions_val2014.json', 'r'))
train = json.load(open('annotations/captions_train2014.json', 'r'))
print (val.keys())
print (val['info'])
print (len(val['images']))
print (len(val['annotations']))
print (val['images'][0])
print (val['annotations'][0])


# combine all images and annotations together
imgs = val['images'] + train['images']                                                #imgs is a list
annots = val['annotations'] + train['annotations']                                    #annots is a list

# for efficiency lets group annotations by image
itoa = {}                                                                             #initialize itoa dict, that groups annotations by image (an image can have atleast 5 or more than 5 captions and hence annotations)
for a in annots:                                                                      #parse the annots list
    imgid = a['image_id']                                                             #initialize key value of itoa to image id of annotation
    if not imgid in itoa: itoa[imgid] = []                                            #create a list to store grouped annotations against imgid (int value) key
    itoa[imgid].append(a)                                                             #add annotation to list


#now itoa is a dictionary of the form { imgid : [{annotation 1}, {}, ....],.....}

# create the json blob
 #but the out json file is an array,while the prepro_labels script reads a dictionary
out = []                                                                              #create a list to structure the blob                                       
for i,img in enumerate(imgs):                                                         #iterate through imgs list with img variable for elements and i as count
    imgid = img['id']                                                                 #initialize imgid
    
    # coco specific here, they store train/val images separately
    loc = 'train2014' if 'train' in img['file_name'] else 'val2014'
    
    jimg = {}
    jimg['file_path'] = os.path.join(loc, img['file_name'])
    jimg['id'] = imgid
    
    sents = []
    annotsi = itoa[imgid]
    for a in annotsi:
        sents.append(a['caption'])
    jimg['captions'] = sents
    out.append(jimg)
    
json.dump(out, open('dataset_coco_hindi.json', 'w'))
