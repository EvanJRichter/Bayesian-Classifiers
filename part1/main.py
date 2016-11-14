import parser

TEST_OPTION = 'test'
TRAINING_OPTION = 'training'

if __name__ == "__main__":
    ## TRAINING DATA
    TR_imgs, TR_labels = parser.parse_data(TRAINING_OPTION)
    TR_groups = parser.group_imgs(TR_imgs, TR_labels)
    TR_priors = parser.get_priors(TR_groups)
    TR_likelyhoods = parser.get_likelyhoods(TR_groups)

    # # TESTING DATA
    TS_imgs, TS_labels = parser.parse_data(TEST_OPTION)
    TS_output_label, TS_posteriori = parser.classify_group(TS_imgs, TR_likelyhoods, TR_priors)
    stats = parser.analyse(TS_labels, TS_output_label, TS_imgs, TS_posteriori)
    confusion_matrix = parser.create_matrix(TS_labels, TS_output_label)
    parser.collect_odds_data(TR_likelyhoods)
    parser.find_low_high_examples(TS_imgs, TS_labels, TS_posteriori)
