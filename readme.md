# 🎥 YouTube Video Success Predictor

A Machine Learning project that predicts the success category of a YouTube video using metadata such as title, description, tags, and engagement metrics.

This project demonstrates an end-to-end ML workflow including data preprocessing, feature engineering, model training, evaluation, and deployment-ready architecture.

---

## 🚀 Project Overview

YouTube video performance depends on multiple factors such as engagement, content presentation, and publishing patterns.
This project builds a predictive model that classifies videos into success categories based on available metadata.

### 🎯 Prediction Categories

* **Low** — Less than 50K views
* **Medium** — 50K to 200K views
* **High** — 200K to 1M views
* **Viral** — More than 1M views

---

## 🧠 Machine Learning Pipeline

The project follows a structured ML workflow:

1. Data Collection & Understanding
2. Data Cleaning & Preprocessing
3. Feature Engineering
4. Model Training (XGBoost)
5. Model Evaluation
6. Feature Importance Analysis

---

## 📊 Dataset

Dataset used:

* YouTube Trending Videos Dataset (India)

Features available:

* Title
* Description
* Tags
* Publish Time
* Views
* Likes
* Dislikes
* Comment Count
* Category ID

---

## ⚙️ Feature Engineering

The following features were created:

### Text-Based Features

* Title length
* Description length
* Number of tags
* Title word count
* Uppercase word count

### Engagement Features

* Like-to-view ratio
* Comment-to-view ratio
* Like-to-comment ratio

### Time-Based Features

* Publish hour

---

## 🤖 Model Used

### XGBoost Classifier

Chosen because:

* Strong performance on tabular datasets
* Handles non-linear relationships well
* Provides feature importance insights

Model accuracy achieved:

```
~60% accuracy (baseline model)
```

---

## 📈 Evaluation Metrics

* Accuracy Score
* Confusion Matrix
* Feature Importance Visualization

---

## 🛠 Tech Stack

* Python
* Pandas
* NumPy
* Scikit-learn
* XGBoost
* Matplotlib
* Jupyter Notebook
* VS Code

---

## 📁 Project Structure

```
youtube-video-success-predictor/
│
├── data/                  # Dataset (ignored in Git)
├── notebooks/             # Development notebooks
├── models/                # Saved models
├── app/                   # API / deployment (future)
├── README.md
└── .gitignore
```

---

## 🔮 Future Improvements

* Neural Network with text embeddings
* Sentence Transformers for title understanding
* FastAPI deployment
* Web interface for prediction
* Real-time YouTube API integration

---

## 👨‍💻 Author

**Arya Tiwari**
B.Tech CSE | Machine Learning & Full Stack Development
