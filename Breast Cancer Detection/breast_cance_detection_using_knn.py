# -*- coding: utf-8 -*-
"""Breast_Cance_Detection_using_KNN

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lmj0yBKncMMAREQdctkunEGMdaczfdD4

!wget = "https://scholar.cu.edu.eg/Dataset_BUSI.zip" --no-check-certificate
"""

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import cv2
import os
import matplotlib.pyplot as plt

# Step 1: Data Collection
benign_dir = '/content/dataset/benign'
malignant_dir = '/content/dataset/malignant'

# Step 2: Preprocessing
def load_images_from_directory(directory):
    images = []
    for filename in os.listdir(directory):
        if filename.endswith('.png'):
            img = cv2.imread(os.path.join(directory, filename))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)  # Convert to grayscale and set data type to 32-bit float
            img = cv2.resize(img, (224, 224))  # Resize to a standard size
            img = img / 255.0  # Normalize pixel values
            images.append(img)
    return images

benign_images = load_images_from_directory(benign_dir)
malignant_images = load_images_from_directory(malignant_dir)

# Step 3: Feature Extraction
def extract_features(images):
    features = []
    for image in images:
        # Extract statistical features (mean and standard deviation)
        mean_value = np.mean(image)
        std_value = np.std(image)
        features.append([mean_value, std_value])
    return np.array(features)

# Extract features
benign_features = extract_features(benign_images)
malignant_features = extract_features(malignant_images)

# Create labels
benign_labels = [0] * len(benign_features)
malignant_labels = [1] * len(malignant_features)

# Combine features and labels
X = np.concatenate((benign_features, malignant_features), axis=0)
y = np.array(benign_labels + malignant_labels)

# Step 4: Data Splitting
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Flatten the feature vectors
X_train_flat = X_train.reshape(X_train.shape[0], -1)
X_test_flat = X_test.reshape(X_test.shape[0], -1)

# Step 5: Classification Model
knn_classifier = KNeighborsClassifier(n_neighbors=5)  # Vary the number of neighbors as needed
knn_classifier.fit(X_train_flat, y_train)

# Step 6: Evaluation
y_pred = knn_classifier.predict(X_test_flat)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f'Accuracy: {accuracy}')
print(report)

# Step 7: Export the Model as joblib file
model_filename = 'BreastCancerKNN.joblib'
joblib.dump(knn_classifier, model_filename)

