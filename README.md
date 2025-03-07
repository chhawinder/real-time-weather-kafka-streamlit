# 🌦️ Real-Time Weather Streaming with Kafka & Streamlit

## 📌 Project Overview
This project streams real-time weather data from multiple cities using **Kafka** and visualizes it using **Streamlit**. The data is fetched from the OpenWeather API and stored in different partitions of a Kafka topic for efficient processing.

---

## 🚀 Getting Started
Follow these steps to set up and run the project.

### **1️⃣ Install & Run Kafka**
#### **Install Kafka**
Download and install Kafka from the [official Apache Kafka website](https://kafka.apache.org/downloads).

#### **Start Kafka & Zookeeper**
Navigate to the Kafka installation directory and run:
```bash
# Start Zookeeper
zookeeper-server-start.bat .\config\zookeeper.properties

# Start Kafka Server
.\bin\windows\kafka-server-start.bat .\config\server.properties
```

### **2️⃣ Create Kafka Topic**
Run the following command to create a topic named `weather-data`:
```bash
kafka-topics.bat --create --topic weather-data --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

#### **Verify Topic Creation**
Check if the topic is created:
```bash
.\bin\windows\kafka-topics.bat --list --bootstrap-server localhost:9092
```
Expected Output:
```
weather-data
```

---

### **3️⃣ Setup Virtual Environment**
Navigate to your project directory and create a virtual environment:
```bash
python -m venv myenv
```
Activate the virtual environment:
```bash
myenv\Scripts\activate
```

### **4️⃣ Clone the Repository & Install Dependencies**
Clone the project from GitHub:
```bash
git clone https://github.com/your-username/real-time-weather-kafka-streamlit.git
cd real-time-weather-kafka-streamlit
```
this repo should be inside the Virtual Enviorment

Install required Python libraries:
```bash
pip install -r requirements.txt
```

---

## 🔥 Running the Project

### **5️⃣ Set Up API Key**
Replace the API key in `Project_producer.py` with your **OpenWeather API Key**. You can obtain it from the [OpenWeatherMap Website](https://openweathermap.org/api).

```python
API_KEY = "your_api_key_here"  # Replace with your OpenWeather API key
```

### **6️⃣ Run the Scripts in Order**
#### **Start the Kafka Producer (Fetch Weather Data & Send to Kafka)**
```bash
python Project_producer.py
```
#### **Start the Kafka Consumer (Read Weather Data from Kafka)**
```bash
python Project_consumer.py
```
#### **Run Weather API Service (Optional Helper Service)**
```bash
python weather_api.py
```
#### **Start the Frontend (Visualize Data in Real-time)**
```bash
streamlit run frontend.py
```

---

## 📊 Features
✅ **Fetch weather data** for multiple cities every 10 seconds  
✅ **Kafka Producer** sends data to partitions  
✅ **Kafka Consumer** reads data from different partitions  
✅ **Streamlit Dashboard** with live graphs updating every 5 seconds  
✅ **Real-time visualization** of temperature, humidity, and other weather metrics  

---

## 🎨 UI Preview
The Streamlit frontend displays **interactive graphs** comparing weather conditions across cities in real time. The UI refreshes every 5 seconds for a smooth experience.

---

## 🛠️ Tech Stack
- **Python** (Data Processing & Kafka Client)
- **Apache Kafka** (Real-time Streaming)
- **Streamlit** (Frontend Visualization)
- **OpenWeather API** (Weather Data Source)

---

## 🤝 Contributing
Feel free to fork this repository, open issues, or submit pull requests!

---

## 📜 License
This project is open-source and available under the **MIT License**.

Happy Coding! 🚀

