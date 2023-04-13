#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# --------------------------------------------------
# Description:
# --------------------------------------------------
# Author: Konfido <konfido.du@outlook.com>
# Created Date : April 4th 2020, 17:45:05
# Last Modified: April 4th 2020, 17:45:05
# --------------------------------------------------

from nltk.classify.maxent import MaxentClassifier
from sklearn.metrics import (accuracy_score, fbeta_score, precision_score,
                             recall_score)
import os
import pickle
import re
# import enchant
from names_dataset import NameDataset


class MEMM():
    def __init__(self):
        self.train_path = "../data/train"
        self.dev_path = "../data/dev"
        self.beta = 0
        self.max_iter = 0
        self.classifier = None
        self.m = NameDataset()


    def features(self, words, previous_label, position):
        """
        Note: The previous label of current word is the only visible label.

        :param words: a list of the words in the entire corpus
        :param previous_label: the label for position-1 (or O if it's the start
                of a new sentence)
        :param position: the word you are adding features for
        """

        features = {}
        """ Baseline Features """
        current_word = words[position]
        features['has_(%s)' % current_word] = 1
        features['prev_label'] = previous_label
        # if current_word[0].isupper(): features['Titlecase'] = 1

        #===== TODO: Add your features here =======#
        symbol = ['in','on','at','a','an','the','some',"'s",'.']
        day_and_month = ['Monday','Tueesday','Wednesday','Thursday','Friday','Saturday','Sunday'
                         ,'January','February','March','April','May','June','July','August','September','October','November','December']
        
        upper_Num = 0
        int_Num = 0
        for i in current_word:
            if i.isupper():
                upper_Num += 1
            try:
                if int(i).isnumeric():
                    int_Num += 1
            except:
                None

        #Final code 2

        # for i in day_and_month:
        #     if current_word[0].isupper() and current_word != i:
        #         features['day_monthcase'] = 1
        #         for j in symbol:
        #             if words[position - 1] != j:
        #                 features['symbolcase'] = 1
        #             else:
        #                 features['symbolcase'] = 0
        #         if upper_Num < len(current_word) and int_Num == 0:
        #             features['Titlecase'] = 1
        #         else:
        #             features['Titlecase'] = 0
        #         if self.m.search(current_word):
        #             features['dataset'] = 1
        #         else:
        #             features['dataset'] = 0
        #     else:
        #         features['day_monthcase'] = 0

        #Final code 2

        if words[position - 1] != '.' or words[position - 1] != "'s":
            for i in symbol:
                if words[position - 1] != i:
                    for j in day_and_month:
                        if current_word[0].isupper() and current_word != j:
                            if upper_Num < len(current_word) and int_Num == 0 : 
                                features['Titlecase'] = 1
                            else:
                                features['Titlecase'] = 0 


        #=============== TODO: Done ================#
        return features

    def load_data(self, filename):
        words = []
        labels = []
        for line in open(filename, "r", encoding="utf-8"):
            doublet = line.strip().split("\t")
            if len(doublet) < 2:     # remove emtpy lines
                continue
            words.append(doublet[0])
            labels.append(doublet[1])
        return words, labels

    def train(self):
        print('Training classifier...')
        words, labels = self.load_data(self.train_path)
        previous_labels = ["O"] + labels
        features = [self.features(words, previous_labels[i], i)
                    for i in range(len(words))]
        train_samples = [(f, l) for (f, l) in zip(features, labels)]
        classifier = MaxentClassifier.train(
            train_samples, max_iter=self.max_iter)
        self.classifier = classifier

    def test(self):
        print('Testing classifier...')
        words, labels = self.load_data(self.dev_path)
        previous_labels = ["O"] + labels
        features = [self.features(words, previous_labels[i], i)
                    for i in range(len(words))]
        results = [self.classifier.classify(n) for n in features]

        f_score = fbeta_score(labels, results, average='macro', beta=self.beta)
        precision = precision_score(labels, results, average='macro')
        recall = recall_score(labels, results, average='macro')
        accuracy = accuracy_score(labels, results)

        print("%-15s %.4f\n%-15s %.4f\n%-15s %.4f\n%-15s %.4f\n" %
              ("f_score=", f_score, "accuracy=", accuracy, "recall=", recall,
               "precision=", precision))

        return True

    def show_samples(self, bound):
        """Show some sample probability distributions.
        """
        words, labels = self.load_data(self.train_path)
        previous_labels = ["O"] + labels
        features = [self.features(words, previous_labels[i], i)
                    for i in range(len(words))]
        (m, z) = bound
        pdists = self.classifier.prob_classify_many(features[m:n])

        print('  Words          P(PERSON)  P(O)\n' + '-' * 40)
        for (word, label, pdist) in list(zip(words, labels, pdists))[m:n]:
            if label == 'PERSON':
                fmt = '  %-15s *%6.4f   %6.4f'
            else:
                fmt = '  %-15s  %6.4f  *%6.4f'
            print(fmt % (word, pdist.prob('PERSON'), pdist.prob('O')))

    def predict(self, sentence):
        words = sentence.strip().replace(".", "").split(" ")
        
        features = [self.features(words, "O", i)
                    for i in range(len(words))]
        
        pdists = self.classifier.prob_classify_many(features)

        return pdists
        
        # print('  Words          P(PERSON)  P(O)\n' + '-' * 40)
        # for (word, pdist) in list(zip(words, pdists)):
        #     fmt = '  %-15s  %6.4f  %6.4f'
        #     print(fmt % (word, pdist.prob('PERSON'), pdist.prob('O')))
        

    def dump_model(self):
        absolute_path = os.path.dirname(__file__)
        relative_path = "../model/model.pkl"
        full_path = os.path.join(absolute_path, relative_path)
        with open(full_path, 'wb') as f:
            pickle.dump(self.classifier, f)

    def load_model(self):
        absolute_path = os.path.dirname(__file__)
        relative_path = "../model/model.pkl"
        full_path = os.path.join(absolute_path, relative_path)
        with open(full_path, 'rb') as f:
            self.classifier = pickle.load(f)
