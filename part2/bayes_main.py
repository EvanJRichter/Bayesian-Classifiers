import bayes

def run_bayes(trainfile, testfile, test_type):
    b = bayes.Bayes()
    return b.init(trainfile, testfile, test_type)


if __name__ == '__main__':
    print "Multinomial Movie Reviews", run_bayes('./movie_review/rt-train.txt', './movie_review/rt-test.txt', "Multinomial")
    print ""
    print "Multinomial Conversations", run_bayes('./fisher_2topic/fisher_train_2topic.txt', './fisher_2topic/fisher_test_2topic.txt', "Multinomial")
    print ""
    print "Bernoulli Movie Reviews", run_bayes('./movie_review/rt-train.txt', './movie_review/rt-test.txt', "Bernoulli")
    print ""
    print "Bernoulli Conversations", run_bayes('./fisher_2topic/fisher_train_2topic.txt', './fisher_2topic/fisher_test_2topic.txt', "Bernoulli")
