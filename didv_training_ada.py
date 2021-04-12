"""
Module: didv_training_ada

Author: Shenkai Wang, Junmian Zhu, Raymond Blackwell, and Felix R. Fischer

Description: Train an AdaBoost model using the data in 'didv_training.pkl'

UC Berkeley's Copyright and Disclaimer Notice

Copyright ©2021. The Regents of the University of California (Regents). All Rights Reserved.
Permission to use, copy, modify, and distribute this software and its documentation for
educational, research, and not-for-profit purposes, without fee and without a signed licensing agreement,
is hereby granted, provided that the above copyright notice, this paragraph and the following two paragraphs appear in all copies,
modifications, and distributions.

Contact The Office of Technology Licensing, UC Berkeley, 2150 Shattuck Avenue, Suite 510, Berkeley, CA 94720-1620,
(510) 643-7201, otl@berkeley.edu, http://ipira.berkeley.edu/industry-info for commercial licensing opportunities.

IN NO EVENT SHALL REGENTS BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS,
ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF REGENTS HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
THE SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED HEREUNDER IS PROVIDED "AS IS". REGENTS HAS NO OBLIGATION TO PROVIDE MAINTENANCE,
SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
"""

import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
import joblib
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score

def split_dataset(x, y, ratio = 0.2):
    np.random.seed(42)
    shuffled_indices = np.random.permutation(len(x))
    split_point = int(len(x)*ratio)
    x1 = x[shuffled_indices[split_point:]]
    x2 = x[shuffled_indices[:split_point]]
    y1 = y[shuffled_indices[split_point:]]
    y2 = y[shuffled_indices[:split_point]]
    return x1, x2, y1, y2

# 'didv_training.pkl' has already been normalized in data_cleanup.py 
with open('didv_training.pkl', 'rb') as file:
    didv_training_list = pickle.load(file)
didv_total = didv_training_list[0]
didv_label = didv_training_list[1]
didv_label = didv_label >=2
didv_trainval, didv_test, label_trainval, label_test = split_dataset(
    didv_total, didv_label)
didv_train, didv_val, label_train, label_val = split_dataset(
    didv_trainval, label_trainval, 0.25)
ada_clf = AdaBoostClassifier(
    DecisionTreeClassifier(min_samples_leaf = 5), n_estimators = 1000,
    algorithm = "SAMME.R", learning_rate = 0.5)
#didv_trainval_score = cross_val_predict(ada_clf, didv_trainval,
#                                          label_trainval, cv = 3,
#                                          method = "predict_proba")

ada_clf.fit(didv_trainval, label_trainval)
joblib.dump(ada_clf, "ml_model_ada.pkl")
didv_predict = ada_clf.predict(didv_test)
#print(precision_score(label_trainval, didv_trainval_predict))
#print(recall_score(label_trainval, didv_trainval_predict))
print(precision_score(label_test, didv_predict))
print(recall_score(label_test, didv_predict))

params = {'mathtext.default': 'regular' }
plt.rcParams.update(params)
v = np.linspace(-1.5, 2, 896)
count = 0
for i in range(len(label_test)):
    if label_test[i] == False and didv_predict[i] == True:
        didv_test[i] += count
        plt.plot(v, didv_test[i])
        count += 1
        if count == 5:
            break
plt.title('Sample False Positives')
plt.xlabel(r'$V_{bias}$ (V)')
plt.ylabel('dI/dV (a.u.)')
plt.show()

count = 0
for i in range(len(label_test)):
    if label_test[i] == True and didv_predict[i] == False:
        didv_test[i] += count
        plt.plot(v, didv_test[i])
        count += 1
        if count == 5:
            break
plt.title('Sample False Negatives')
plt.xlabel(r'$V_{bias}$ (V)')
plt.ylabel('dI/dV (a.u.)')
plt.show()

#precisions, recalls, thresholds = precision_recall_curve(label_trainval, didv_trainval_score[:, 1])
#plt.plot(thresholds, precisions[:-1], "b--", label = "Precision")
#plt.plot(thresholds, recalls[:-1], "g-", label = "Recall")
#plt.legend()
#plt.xlabel('Threshold')
#plt.axis([0, 1, 0, 1])
#plt.show()
#print("ROC score: ", roc_auc_score(label_trainval, didv_trainval_score[:, 1]))
#fpr, tpr, thresholds = roc_curve(label_trainval, didv_trainval_score[:, 1])
#roc_data = {'fpr': fpr,
#            'tpr': tpr,
#            'thresholds': thresholds}
#with open('ada_roc_data.pkl', 'wb') as file:
#    pickle.dump(roc_data, file)
#plt.plot(fpr, tpr)
#plt.plot([0, 1], [0, 1], 'k--')
#plt.axis([0, 1, 0, 1])
#plt.xlabel('False Positive Rate')
#plt.ylabel('True Positive Rate')
#plt.show()
