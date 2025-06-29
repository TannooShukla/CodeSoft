# -*- coding: utf-8 -*-
"""Titanic_Survival_Task_1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1k8Xd6QGDf2Uwnae5tPCHp9FU9oxH0jO3
"""

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

# Load the Titanic dataset
df = pd.read_csv("/content/Titanic-Dataset.csv")

# Display initial data and check for missing values
print("First few rows of the dataset:")
print(df.head())

print("\nMissing values in each column:")
print(df.isnull().sum())

# Visualize survival counts by gender
plt.figure(figsize=(6, 4))
sns.countplot(data=df, x='Survived', hue='Sex')
plt.title("Survival Distribution by Gender")
plt.xlabel("Survived")
plt.ylabel("Count")
plt.show()

# Drop columns that are not useful for prediction
df.drop(['Name', 'Ticket', 'Cabin', 'PassengerId'], axis=1, inplace=True)

# Handle missing values
df['Age'].fillna(df['Age'].median(), inplace=True)
df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)

# Encode categorical variables
df['Sex'] = LabelEncoder().fit_transform(df['Sex'])
df['Embarked'] = LabelEncoder().fit_transform(df['Embarked'])

# Separate features and target variable
X = df.drop('Survived', axis=1)
y = df['Survived']

# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Define and train the MLP classifier
mlp = MLPClassifier(hidden_layer_sizes=(64, 32), activation='relu',
                    solver='adam', max_iter=300, learning_rate_init=0.01,
                    random_state=42)
mlp.fit(X_train, y_train)

# Visualize training loss over iterations
plt.plot(mlp.loss_curve_)
plt.title("MLP Training Loss Curve")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.grid(True)
plt.show()

# Predict and evaluate the model
y_pred = mlp.predict(X_test)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Display confusion matrix as a heatmap
plt.figure(figsize=(5, 4))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues')
plt.title("Confusion Matrix (Heatmap)")
plt.xlabel("Predicted Labels")
plt.ylabel("True Labels")
plt.show()

