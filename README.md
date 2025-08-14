# 🏨 Hotel Revenue Analysis 2024 with PySpark

This project uses **PySpark** and **Machine Learning** to analyze factors impacting hotel revenues in 2024.

## 📋 Problem Statement

Hotel booking cancellations can significantly disrupt operations, leading to lost revenue and inefficient resource allocation. The goal is to build a predictive model that identifies the likelihood of a booking being cancelled, enabling proactive strategies such as overbooking, dynamic pricing, and targeted guest engagement.

## 🎯 Objectives

- **Analyze** factors that impact hotel revenue
- **Predict** occupancy rate (high/low)
- **Predict** cancellation rate
- **Identify** business optimization levers

## 📊 Dataset

- **Source**: [Hotel Revenue 2024 - Kaggle](https://www.kaggle.com/datasets/omarsobhy14/hotel-revenue2024)


## Docker Installation

1. **Clone the repository**

```bash
git clone https://github.com/tabodino/hotel-revenue-analysis.git
cd hotel-revenue-analysis
```

2. **Build Docker image**
```bash
docker build -t hotel-booking-analysis .
```

3. **Run container**
```bash
docker run -it --rm -p 8888:8888 hotel-booking-analysis
```

## 📝 License

This project is under MIT license. See `LICENSE` file for more details.
