
# coding: utf-8

# In[1]:

import os 
import csv
import numpy as np
import time
import matplotlib as mpl
from app import app
from sklearn.externals import joblib

mpl.use('Agg')# MUST BE CALLED HERE
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def predictNB(dev_CSVfilename):
    LineReader = csv.reader(open(dev_CSVfilename), delimiter=',', quotechar='|')
    row_num = 0
    Rows = [(row[0],row[1]) for row in LineReader]
    print(len(Rows))
    # for i in range(3): print(Rows[i][0],len(Rows[i][1].split()))

    dev_data = [row[1] for row in Rows]
    dev_target = [row[0] for row in Rows]
    from collections import Counter
    MyCounter = Counter(dev_target)
    # idx2target = dict(enumerate(MyCounter.keys()) )
    filename = os.path.join(app.config['MODEL_FOLDER'],'idx2target.joblib.pkl')
    idx2target = joblib.load(filename)
    # tar2idx = dict( (idx2target[idx],idx) for idx in range(len(idx2target)))
    filename = os.path.join(app.config['MODEL_FOLDER'],'tar2idx.joblib.pkl')
    tar2idx = joblib.load(filename)

    
    dev_target_idx = [tar2idx[tar] for tar in dev_target]

    

    T0 = time.time()
    filename = os.path.join(app.config['MODEL_FOLDER'],'NBclassifier2.joblib.pkl')
    if not os.path.isfile(filename):
        filename = os.path.join(app.config['MODEL_FOLDER'],'NBclassifier.joblib.pkl')
    text_clf = joblib.load(filename)
    print("Elapsed time:",time.time() - T0)
    # In[7]:
    T0 = time.time()
    import numpy as np
    dev_predicted = text_clf.predict(dev_data)
    print("Elapsed time:",time.time() - T0)
    # In[8]:
    print(np.mean(dev_predicted == dev_target_idx))
    fname = os.path.join(app.config['RESULT_FOLDER'], "result.csv")
    print(len(idx2target))
    with open(fname,'w') as fd:
        spamwriter = csv.writer(fd,delimiter=',', quotechar='|')
        for i in range(len(dev_predicted)):
            spamwriter.writerow([idx2target[dev_predicted[i]], idx2target[dev_target_idx[i]] ])  
    # In[10]:
    # confusion matrix
    import numpy as np
    n_categories= len(tar2idx)
    confusion = np.zeros((n_categories, n_categories),dtype = np.float64)
    for i in range(len(dev_target_idx)):
        confusion[ dev_target_idx[i] ][dev_predicted[i]] += 1
    for i in range(n_categories):
        confusion[i] = confusion[i] / max(1,confusion[i].sum())

    # In[11]:

    # Set up plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(confusion)
    fig.colorbar(cax)
    # Set up axes
    ax.set_xticklabels([''] + list(tar2idx.keys()), rotation=90)
    ax.set_yticklabels([''] + list(tar2idx.keys()))

    # Force label at every tick
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    # sphinx_gallery_thumbnail_number = 2
    # plt.show()
    image_name = 'confusion.png'
    fig.savefig(image_name)
    fig.savefig(os.path.join(app.config['IMAGE_FOLDER'], image_name))
    return True

