#!/usr/bin/env python3
"""Brain Imaging Analysis Kit Shared Response Model runner"""

import argparse
import math
import os
import urllib.request

import matplotlib.pyplot as plt
import numpy as np
import scipy.io

from scipy.stats import stats
from sklearn.metrics import confusion_matrix
from sklearn.svm import NuSVC

import brainiak.funcalign.srm

def main():
    parser = argparse.ArgumentParser(
            description="Shared Response Model runner")
    parser.add_argument("bids_dir", help="Input directory")
    parser.add_argument("output_dir", help="Output directory")
    parser.add_argument("analysis_level",
            help="Level of the analysis that will be performed",
            choices=["participant", "group"])
    parser.add_argument("--participant_label",
            help="Labels for participants to be analyzed", nargs="+")
    args = parser.parse_args()

    if args.analysis_level == "participant":
        pass
    elif args.analysis_level == "group":
        srm_image_prediction(args.output_dir)

def plot_confusion_matrix(cm, fout, title="Confusion Matrix"):
    """Plot a confusion matrix for each subject"""
    plt.figure()
    subjects = len(cm)
    root_subjects = math.sqrt(subjects)
    cols = math.ceil(root_subjects)
    rows = math.ceil(subjects/cols)
    classes = cm[0].shape[0]
    for subject in range(subjects):
        plt.subplot(rows, cols, subject+1)
        plt.imshow(cm[subject], interpolation='nearest', cmap=plt.cm.bone)
        plt.xticks(np.arange(classes), range(1,classes+1))
        plt.yticks(np.arange(classes), range(1,classes+1))
        cbar = plt.colorbar(ticks=[0.0,1.0], shrink=0.6)
        cbar.set_clim(0.0, 1.0)
        plt.xlabel("Predicted")
        plt.ylabel("True label")
        plt.title("{0:d}".format(subject + 1))
    plt.suptitle(title)
    plt.tight_layout()
    plt.savefig(fout)

def srm_image_prediction(output_dir):
    movie_data_file, dummy = urllib.request.urlretrieve(
            "https://www.dropbox.com/s/7areadyb6ddvl5h/movie_data.mat?dl=1",
            os.path.join(output_dir, "movie_data.mat"))
    movie_data = scipy.io.loadmat(movie_data_file)
    
    # Convert data to a list of arrays matching SRM input.
    # Each element is a matrix of voxels by TRs.
    movie_data = list(movie_data['movie_data_lh'])
    subjects = len(movie_data)
    
    # Z-score the data
    for subject in range(subjects):
        movie_data[subject] = stats.zscore(movie_data[subject],axis=1,ddof=1)
    
    # Run SRM with the movie data
    srm = brainiak.funcalign.srm.SRM(n_iter=10, features=50)
    srm.fit(movie_data)
    
    # Load the input data that contains the image stimuli and its labels for
    # training a classifier
    image_data_file, dummy = urllib.request.urlretrieve(
            "https://www.dropbox.com/s/wks4fwgzetmeqb4/image_data.mat?dl=1",
            os.path.join(output_dir, "image_data.mat"))
    image_data = scipy.io.loadmat(image_data_file)
    # Convert data to a list of arrays matching SRM input.
    # Each element is a matrix of voxels by TRs.
    image_data = list(image_data['image_data_lh'])
    
    assert (image_data[0].shape[0] == movie_data[0].shape[0],
            "Number of voxels in movie data and image data do not match!")
    
    # Z-score the image data
    for subject in range(subjects):
        image_data[subject] = stats.zscore(image_data[subject],axis=1,ddof=1)
    
    # Z-score the shared response data
    image_data_shared = srm.transform(image_data)
    for subject in range(subjects):
        image_data_shared[subject] = stats.zscore(image_data_shared[subject],
                axis=1, ddof=1)
    
    # Read the labels of the image data for training the classifier.
    labels_data_file, dummy = urllib.request.urlretrieve(
            "https://www.dropbox.com/s/ogd26q6fro4l2d2/label.mat?dl=1",
            os.path.join(output_dir, "label.mat"))
    labels = scipy.io.loadmat(labels_data_file)
    labels = np.squeeze(labels['label'])
    
    # Run a leave-one-out cross validation with the subjects
    train_labels = np.tile(labels, subjects-1)
    test_labels = labels
    accuracy = np.zeros((subjects))
    cm = [None] * subjects
    for subject in range(subjects):
        # Concatenate the subjects' data for training into one matrix
        train_subjects = list(range(subjects))
        train_subjects.remove(subject)
        TRs = image_data_shared[0].shape[1]
        train_data = np.zeros((image_data_shared[0].shape[0],
                len(train_labels)))
        for train_subject in range(len(train_subjects)):
            start_index = train_subject*TRs
            end_index = start_index+TRs
            train_data[:, start_index:end_index] = image_data_shared[
                    train_subjects[train_subject]]
    
        # Train a Nu-SVM classifier using scikit learn
        classifier = NuSVC(nu=0.5, kernel='linear')
        classifier = classifier.fit(train_data.T, train_labels)
    
        # Predict on the test data
        predicted_labels = classifier.predict(image_data_shared[subject].T)
        accuracy[subject] = (sum(predicted_labels == test_labels) 
                             / len(predicted_labels))
    
        # Create a confusion matrix to see the accuracy of each class
        cm[subject] = confusion_matrix(test_labels, predicted_labels)
    
        # Normalize the confusion matrix
        cm[subject] = (cm[subject].astype('float')
                       / cm[subject].sum(axis=1)[:, np.newaxis])
    
    
    # Plot and print the results
    plot_confusion_matrix(cm, os.path.join(output_dir, "confusion_matrix.pdf"))
    with open(os.path.join(output_dir, "accuracy.txt"), 'w') as fout:
        print(np.mean(accuracy), np.std(accuracy), file=fout)

if __name__ == "__main__":
    main()
