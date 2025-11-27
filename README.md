# 🏨 Hotel Revenue Analysis 2024 with PySpark

<img src="docs/screenshots/hotel-revenue-2024.webp">

This project uses **PySpark** and **Machine Learning** to analyze factors impacting hotel revenues in 2024.

## 📋 Problem Statement

Hotel booking cancellations can significantly disrupt operations, leading to lost revenue and inefficient resource allocation. The goal is to build a predictive model that identifies the likelihood of a booking being cancelled, enabling proactive strategies such as overbooking, dynamic pricing, and targeted guest engagement.

## 🎯 Objectives

- **Analyze** factors that impact hotel revenue
- **Predict** occupancy rate (high/low)
- **Predict** cancellation rate
- **Identify** business optimization levers

## 📊 Dataset

### **Source**: [Hotel Revenue 2024 - Kaggle](https://www.kaggle.com/datasets/omarsobhy14/hotel-revenue2024)

### **Column details (from the Kaggle documentation)**

- **Date:** The date of the recorded data.
- **Month:** Numeric representation of the month.
- **Day of the Week:** Numeric representation of the day in a week.
- **Season:** Categorical representation of the season (e.g., Winter, Spring, Summer, Fall).
- **Public Holiday:** Binary indicator (0 or 1) denoting whether it's a public holiday.
- **Previous Month Revenue:** Revenue generated in the previous month.
- **Year-over-Year Revenue:** Revenue compared to the same month the previous year.
- **Monthly Trend:** Trend in revenue or occupancy for the month.
- **Occupancy Rate:** Percentage of rooms occupied.
- **Average Daily Rate (ADR):** Average rate charged per occupied room.
- **Revenue per Available Room (RevPAR):** Revenue generated per available room.
- **Booking Lead Time:** Average lead time between booking and stay.
- **Booking Cancellations:** Percentage of bookings cancelled.
- **Booking Source:** Source of the booking (e.g., Direct, OTA).
- **Guest Type:** Type of guest (e.g., Leisure, Business).
- **Repeat Guests:** Percentage of guests who are repeat visitors.
- **Nationality:** Nationality of guests.
- **Group Bookings:** Binary indicator denoting group bookings.
- **Discounts and Promotions:** Use of discounts or promotions.
- **Room Rate:** Average rate charged for rooms.
- **Local Events:** Presence of local events influencing occupancy.
- **Hotel Events:** Events hosted by the hotel affecting operations.
- **Competitor Rates:** Rates offered by competitors.
- **Weather Conditions:** Local weather conditions influencing guest behavior.
- **Economic Indicators:** Economic factors influencing hotel performance.
- **Staff Levels:** Staffing levels affecting service quality.
- **Guest Satisfaction:** Guest satisfaction ratings.
- **Maintenance Issues:** Issues related to maintenance affecting operations.
- **Marketing Spend:** Expenditure on marketing activities.
- **Online Reviews:** Ratings and reviews provided online.
- **Social Media Engagement:** Engagement metrics on social media platforms.
- **Seasonal Adjustments:** Adjustments made for seasonal variations.
- **Trend Adjustments:** Adjustments made for trending factors.
- **Room Revenue:** Total revenue from room bookings.
- **Food and Beverage Revenue:** Revenue from food and beverage services.
- **Other Services Revenue:** Revenue from other hotel services.
- **Total Revenue for the Month:** Overall revenue generated for the month.

### **Analyzed Features**:
  - Temporal features: Date, Month, Weekday, Season, Public_Holiday
  - Revenue metrics: ADR, RevPAR, Room_Revenue, Total_Revenue
  - Booking behavior: Booking_Channel, Cancellations, Group Bookings
  - Guest attributes: Type, Country, Market_Segment
  - Operational metrics: Fixed_Costs, Variable_Costs, Marketing_Spend

## 🚀 Installation and Setup

### Docker Installation

1. **Clone the repository**

```bash
git clone https://github.com/tabodino/hotel_booking_cancellation_prediction.git
cd hotel_booking_cancellation_prediction
```

2. **Build Docker image**
```bash
docker build -t hotel-booking-analysis .
```

3. **Run container**
```bash
docker run -it --rm -p 8888:8888 hotel-booking-analysis
```

### Local Installation (alternative)


1. **Create virtual environment**
```bash
python -m venv hotel_env
source hotel_env/bin/activate  # Linux/Mac
# or
hotel_env\Scripts\activate  # Windows
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Launch Jupyter notebook**
```bash
 jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --NotebookApp.token='' --NotebookApp.password=''
```

### Scripts

Download and preprocess data

```bash
python src/data/data_preprocessor.py
```

Launch MLflow UI

```bash
mlflow ui
```

Generate JSON report 

```bash
python src/hotel_hotel_analysis_export.py
```

Launch UI dashboard 
```bash
cd src/web
python -m http.server 8000
```

---

## 📝 License

This project is under MIT license. See `LICENSE` file for more details.


---

## 👤 Author

**Jean-Michel LIEVIN**  
Data Scientist | Full-Stack Developer

- 🌐 Portfolio: [github.com/tabodino](https://github.com/tabodino)
- 💼 LinkedIn: [linkedin.com/in/jean-michel-lievin-247591143](https://www.linkedin.com/in/jean-michel-lievin-247591143)
- 📧 Email: [jeanmichel.liev1@gmail.com](mailto:jeanmichel.liev1@gmail.com)

---

## 🛠️ Support

For issues and questions, open an issue on GitHub.

[![Support Email](https://img.shields.io/badge/support-email-blue?logo=gmail)](mailto:jeanmichel.liev1@gmail.com)
[![Open an Issue](https://img.shields.io/badge/GitHub-Issues-blue?logo=github)](https://github.com/tabodino/hotel_booking_cancellation_prediction/issues)