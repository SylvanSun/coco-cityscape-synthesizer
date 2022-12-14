from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
from utils.ood_category import load_category

if __name__ == '__main__':
    dataDir = '..'
    dataType = 'val2017'
    annFile = '{}/annotations/instances_{}.json'.format(dataDir, dataType)

    # initialize COCO api for instance annotations
    coco = COCO(annFile)
    # learning COCO api for categories
    cats = coco.loadCats(coco.getCatIds())

    # display COCO categories and super categories
    nms = [cat['name'] for cat in cats]
    print('COCO categories: \n{}\n'.format(' '.join(nms)))

    nms = set([cat['supercategory'] for cat in cats])
    # print('COCO super categories: \n{}'.format(' '.join(nms)))

    # get all images containing given categories, select one at random
    category = load_category("./utils/category.json")
    for cat in category:
        catIds = coco.getCatIds(catNms=[cat])
        imgIds = coco.getImgIds(catIds=catIds)
        img = coco.loadImgs(imgIds[np.random.randint(0, len(imgIds))])[0]

        image = io.imread('%s/%s/%s' % (dataDir, dataType, img['file_name']))
        # io.imsave('../figs/figs_demo/' + img['file_name'][6:12] + '_original.png', image)

        annIds = coco.getAnnIds(imgIds=img['id'], catIds=catIds, iscrowd=None)
        anns = coco.loadAnns(annIds)
        mask = coco.polygon_extract(anns, image.shape[0], image.shape[1])
        for ch in range(3):
            image[:, :, ch] *= mask
        io.imsave('../figs/figs_demo/' + img['file_name'][6:12] + '_masked.png', image)
