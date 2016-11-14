import math 
import operator

class Bayes:

    def init(self, trainfile, testfile, bayes_type):
        word_neg = self.get_p_dict(trainfile, "-1", bayes_type)
        word_pos = self.get_p_dict(trainfile, "1", bayes_type)
        #print word_pos, word_neg
        #trainedwords = self.get_unique_words(trainfile)
        test_docs = self.get_docs(testfile)
        self.get_odds(word_neg, word_pos)
        self.get_top(word_neg, word_pos)
        return self.get_accuracy(test_docs, word_neg, word_pos)


    def get_p_dict(self, path, classtype, bayes_type):    
        #create dictionary of each unique word -> number of times that appears
        #keep track of total words
        unique_words = {}
        total_words = 0
        f = open(path, 'r')
        for line in f:
            line = line.split( )
            if line[0] == classtype:
                for i in line[1:]:
                    elem = i.split(":")
                    if elem[0] not in unique_words:
                        if bayes_type == "Multinomial":
                            unique_words[elem[0]] = int(elem[1])
                        else:
                            unique_words[elem[0]] = 1
                    else:
                        if bayes_type == "Multinomial":
                            unique_words[elem[0]] += int(elem[1])
                    total_words += int(elem[1])
        f.close()

        #go through dictionary again, replace value with (value + 1 / len(dict)+total words)
        normalized_words = {}
        laplacian = 0.05
        for key, value in unique_words.iteritems(): 
            normalized_words[key] = float(value + laplacian) / float(len(unique_words)+total_words*laplacian)
        return normalized_words

    def get_unique_words(self, path):    
        unique_words = []
        f = open(path, 'r')
        for line in f:
            line = line.split( )
            for i in line[1:]:
                elem = i.split(":")
                if elem[0] not in unique_words:
                    unique_words.append(elem[0])
        f.close()
        return unique_words

    def get_docs(self, path):
        docs = []
        f = open(path, 'r')
        for line in f:
            doc = []
            line = line.split( )
            doc.append(line[0])
            for i in line[1:]:
                elem = i.split(":")
                for k in range(int(elem[1])):
                    doc.append(elem[0])
            docs.append(doc)
        f.close()
        return docs

    def get_probability(self, doc, classifier):
        prob = 1.0
        for w in doc[1:]:
            if w in classifier:
                prob += math.log1p(float(classifier[w]))
        return prob

    def get_classification(self, doc, neg, pos):
        n = self.get_probability(doc, neg)
        p = self.get_probability(doc, pos)
        if n > p:
            return "-1"
        return "1"

    def get_accuracy(self, docs, neg, pos):
        correct = 0.0
        #correct_given = num
        pos_pos = 0.0
        neg_pos = 0.0
        pos_neg = 0.0
        neg_neg = 0.0

        for doc in docs:
            classification = self.get_classification(doc, neg, pos)
            if classification == doc[0]:
                correct += 1.0

            if classification == "1" and doc[0] == "1":
                pos_pos += 1.0
            if classification == "1" and doc[0] == "-1":
                pos_neg += 1.0
            if classification == "-1" and doc[0] == "1":
                neg_pos += 1.0
            if classification == "-1" and doc[0] == "-1":
                neg_neg += 1.0

        print ""
        print "classification\given      1       -1"
        print "                   1     ", pos_pos/len(docs), "   ", pos_neg/len(docs)
        print "                  -1     ", neg_pos/len(docs), "   ", neg_neg/len(docs)

        return float(correct) / float(len(docs) - 1.0)

    def get_top(self, neg, pos):
        sorted_neg = sorted(neg.items(), key=lambda tup: tup[1])
        sorted_pos = sorted(pos.items(), key=lambda tup: tup[1])

        print "Top 10 Negative"
        print sorted_neg[-10:-1]
        print "Top 10 Positive"
        print sorted_pos[-10:-1]

    def get_odds(self, neg, pos):
        odds = {}
        for key, pos_value in pos.iteritems(): 
            if key in neg:
                odds[key] = (pos_value / neg[key])

        #sorted_odds = sorted(odds.items(), key=operator.itemgetter(1)).reverse()

        sorted_odds = sorted(odds.items(), key=lambda tup: tup[1])
        print "ODDS : ", sorted_odds[-10:-1]









