IMG_LENGTH = 28
IMG_WIDTH = 28

TEST_OPTION = 'test'
TRANING_OPTION = 'traning'
TEST_IMG_PATH = 'digitdata/testimages'
TEST_LABEL_PATH = 'digitdata/testlabels'
TRAINING_IMG_PATH = 'digitdata/traningimages'
TRANING_LABEL_PATH = 'digitdata/traininglabels'


def parse_data(option):
    return (parseImg(option), parseLabel(option))

def parseImg(option):
    if option == TEST_OPTION:
        f = open(TEST_IMG_PATH, 'r')
    if option == TRANING_OPTION:
        f = open(TRANING_IMG_PATH, 'r')

    i = 0
    curr_img = []
    imgs = []
    for line in f:
        if i < 28:
            img_row = []
            for char in line:
                if char == " ":
                    img_row.append(0)
                elif char == "#" or char == "+":
                    img_row.append(1)
            curr_img.append(img_row)
            i += 1
        else:
            imgs.append(curr_img)
            curr_img = []
            i = 0

    return imgs

def parseLabel(option):
    if option == TEST_OPTION:
        f = open(TEST_LABEL_PATH, 'r')
    if option == TRANING_OPTION:
        f = open(TRANING_LABEL_PATH, 'r')

    label = []
    for line in f:
        label.append(line[0])
    return label
