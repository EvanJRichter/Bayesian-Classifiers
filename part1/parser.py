TEST_OPTION = 'test'
TRAINING_OPTION = 'training'
TEST_IMG_PATH = 'digitdata/testimages'
TEST_LABEL_PATH = 'digitdata/testlabels'
TRAINING_IMG_PATH = 'digitdata/trainingimages'
TRAINING_LABEL_PATH = 'digitdata/traininglabels'

def test_classification(imgs):
    return
def classify_img(img, likelyhoods):



def get_likelyhoods(groups):
    likelyhoods = []
    for group in groups:
        likelyhoods.append(get_likelyhood(group))

    print likelyhoods[0]
    return likelyhoods

def get_likelyhood(group):
    total_count = len(group)
    width = len(group[0])
    height = width
    k = 1.0 # Laplacian smoothing
    v = width * height # Laplacian smoothing

    likelyhood = []
    for i in range (width):
        arr = []
        for j in range (height):
            arr.append(0.0 + k)
        likelyhood.append(arr)

    for img in group:
        for i in range (width):
            for j in range (height):
                if img[i][j] == 1:
                    likelyhood[i][j] += 1

    for i in range (width):
        for j in range (height):
            likelyhood[i][j] = likelyhood[i][j]/ (total_count * v)

    return likelyhood

def parse_data(option):
    imgs = parse_img(option)
    labels = parse_label(option)
    return (imgs, labels)

def parse_img(option):
    if option == TEST_OPTION:
        f = open(TEST_IMG_PATH, 'r')
    if option == TRAINING_OPTION:
        f = open(TRAINING_IMG_PATH, 'r')

    i = 0
    curr_img = []
    imgs = []
    for line in f:
        if i < 27:
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

def parse_label(option):
    if option == TEST_OPTION:
        f = open(TEST_LABEL_PATH, 'r')
    if option == TRAINING_OPTION:
        f = open(TRAINING_LABEL_PATH, 'r')

    label = []
    for line in f:
        label.append(int(line[0]))
    return label

def group_imgs(imgs, labels):
    groups = []
    for i in range (10):
        groups.append([])

    count = len(imgs)
    for i in range(count):
        label = labels[i]
        img = imgs[i]
        groups[label].append(img)

    return groups

def get_priors(groups):
    total = 0.0
    priors = []
    for group in groups:
        count = len(group)
        priors.append(count)
        total += count

    for count in priors:
        count = count / total

    return priors
