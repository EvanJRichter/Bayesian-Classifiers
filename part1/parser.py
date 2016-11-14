import operator, math
import matplotlib.pyplot as plt

TEST_OPTION = 'test'
TRAINING_OPTION = 'training'
TEST_IMG_PATH = 'digitdata/testimages'
TEST_LABEL_PATH = 'digitdata/testlabels'
TRAINING_IMG_PATH = 'digitdata/trainingimages'
TRAINING_LABEL_PATH = 'digitdata/traininglabels'

def find_low_high_examples(imgs, labels, posteriori):
    total = len(imgs)
    for k in range(10):
        k_imgs = []
        k_labels = []
        k_posteriori = []
        for i in range(total):
            if labels[i] == k:
                k_imgs.append(imgs[i])
                k_labels.append(labels[i])
                k_posteriori.append(posteriori[i])
        find_low_high_example(k_imgs, k_labels, k_posteriori)


def find_low_high_example(imgs, labels, posteriori):
    max_value = max(posteriori)
    max_index = posteriori.index(max_value)

    min_value = min(posteriori)
    min_index = posteriori.index(min_value)

    print "------------------------"
    print imgs[max_index]
    print "------------------------"
    print imgs[min_index]

def collect_odds_data(likelyhoods):
    find_odds(5, 9, likelyhoods)
    find_odds(8, 3, likelyhoods)
    find_odds(5, 3, likelyhoods)
    find_odds(9, 4, likelyhoods)
    return

def find_odds(num1, num2, likelyhoods):
    odds = [[0.0] * 28 for i in range(28)]
    for i in range (28):
        for j in range (28):
            odds[i][j] = math.log(likelyhoods[num1][i][j] / likelyhoods[num2][i][j])

    print_graph(likelyhoods[num1], num1)
    print_graph(likelyhoods[num2], num2)
    print_graph(odds, "odds of " + str(num1) + " and " + str(num2))


def print_graph(likelyhoods, num):
    plt.imshow(likelyhoods, cmap='jet', interpolation='nearest')
    plt.xlabel(num)
    plt.show()

def create_matrix(true_labels, empircal_labels):
    matrix = [[0.0] * 10 for i in range(10)]
    class_count = [0.0] * 10
    class_correct = [0.0] * 10

    count = len(true_labels)
    for i in range (count):
        x = true_labels[i]
        y = empircal_labels[i]
        matrix[x][y] += 1
        class_count[x] += 1
        if x == y:
            class_correct[x] += 1

    for i in range(10):
        class_correct[i] = class_correct[i] / class_count[i]
        for j in range(10):
            matrix[i][j] = matrix[i][j] / class_count[i]
            matrix[i][j] = matrix[i][j] * 100

    print "SUCCESS RATE PER CLASS:"
    print class_correct

    print "CONFUSION MATRIX:"
    print_matrix(matrix)
    return matrix

def print_matrix(matrix):
    for row in matrix:
        string = ''
        print ""
        for element in row:
            string += format(element, '.2f') + "\t"
        print string

def analyse(true_labels, empircal_labels, imgs, posteriori):
    count = len(true_labels)
    wrong = 0.0

    for i in range (count):
        if true_labels[i] != empircal_labels[i]:
            wrong += 1

    print "SUCCESS RATE: "
    print (count - wrong) / count

def classify_group(imgs, likelyhoods, priors):
    labels = []
    posteriori = []
    for img in imgs:
        label, post = classify_img(img, likelyhoods, priors)
        labels.append(label)
        posteriori.append(post)
    return labels, posteriori

def classify_img(img, likelyhoods, priors):
    width = len(img)
    height = len(img[0])
    class_count = len(likelyhoods)
    posteriori = [0.0] * class_count

    for i in range (width):
        for j in range (height):
            for k in range (class_count):
                probability = float(img[i][j] * likelyhoods[k][i][j] * priors[k] )
                probability = math.log1p(probability)
                posteriori[k] += probability

    max_value = max(posteriori)
    max_index = posteriori.index(max_value)
    return (max_index, posteriori)

def get_likelyhoods(groups):
    likelyhoods = []
    for group in groups:
        likelyhoods.append(get_likelyhood(group))
    return likelyhoods

def get_likelyhood(group):
    total_count = 10
    width = len(group[0])
    height = len(group[0][0])
    k = 0.10 # Laplacian smoothing
    v = width * height # Laplacian smoothing
    likelyhood = [[0.0 + k] * height for i in range(width)]

    for img in group:
        for i in range (width):
            for j in range (height):
                if img[i][j] == 1:
                    likelyhood[i][j] += 1

    for i in range (width):
        for j in range (height):
            likelyhood[i][j] = likelyhood[i][j] / (total_count * v)

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
        img_row = []
        for char in line:
            if char == " ":
                img_row.append(0)
            elif char == "#" or char == "+":
                img_row.append(1)
        curr_img.append(img_row)
        i += 1
        if i == 28:
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

    # priors = [x / total for x in priors]
    return priors
