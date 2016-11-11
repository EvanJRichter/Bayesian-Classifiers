import parser

TEST_OPTION = 'test'
TRAINING_OPTION = 'training'

if __name__ == "__main__":
    ## TRAINING DATA
    TR_imgs, TR_labels = parser.parse_data(TRAINING_OPTION)
    TR_groups = parser.group_imgs(TR_imgs, TR_labels)
    TR_priors = parser.get_priors(TR_groups)
    TR_likelyhoods = parser.get_likelyhoods(TR_groups)

    # TESTING DATA
    TS_imgs, TS_labels = parser.parse_data(TEST_OPTION)
    TS_output_label = parser.classify(TR_likelyhoods, TS_imgs)
    stats = parser.analyse(TS_labels, TS_output_label)
