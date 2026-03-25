# 👁️ EYE-Q: Smart Eye Health Monitoring System

## 📌 Overview
**EYE-Q** is an advanced IoT-based eye health monitoring system designed to measure and analyze key eye parameters such as **Intraocular Pressure (IOP)** and **blue light exposure** in real-time.

The system combines ultrasonic sensing, embedded systems, and AI-based analysis to provide a **non-invasive, portable, and affordable solution** for early detection of eye-related conditions like glaucoma.

---

## 🚀 Features
- 👁️ Non-contact IOP Measurement using ultrasonic elastography  
- 🔵 Blue Light Exposure Detection with real-time categorization  
- 📊 Live Monitoring Dashboard (Web APK / IoT integration)  
- ⚠️ Smart Alerts System (LED + Buzzer feedback)  
- 📡 Cloud Integration for data logging and analysis  
- 🔧 Low-cost & Portable Design  

---

## 🧠 System Architecture

### 1. Ultrasonic IOP Measurement Module
- Uses 40 kHz ultrasonic transducers (Tx & Rx)  
- Measures corneal stiffness via echo signal  
- Envelope detection + amplification  
- Processed using ADS1115 ADC  

### 2. Blue Light Detection Module
- Uses TCS34725 color sensor  
- Measures intensity of blue light exposure  
- Categorizes exposure into:
  - Safe  
  - Moderate  
  - High  
  - Dangerous  

### 3. Processing Unit
- Raspberry Pi 4  
- Handles:
  - Data acquisition  
  - Signal processing  
  - IoT communication  

### 4. Alert System
- LED indicators:
  - No blink → Safe  
  - 3 blinks → Moderate  
  - 5 blinks → High  
  - 10 blinks → Dangerous  
- Buzzer for critical alerts  

### 5. IoT Dashboard
- Real-time visualization of:
  - IOP values  
  - Blue light exposure  
  - Alerts & history  

---

## ⚙️ Hardware Components

- Raspberry Pi 4 Model B  
- Ultrasonic Transducers (HY40A12R09-1)  
- ADS1115 16-bit ADC  
- TCS34725 Color Sensor  
- LM358P / NE5532P Op-Amps  
- IRLZ44 MOSFET  
- Diodes (1N4148, 1N5819, UF4007)  
- Resistors & Capacitors  
- LED + Buzzer Module  
- Power Supply  

---

## 💻 Software & Technologies

- Python (Data Processing & Control)  
- I2C Communication Protocol  
- Embedded Signal Processing  
- Web Dashboard (Frontend Integration)  
- IoT Cloud Integration  

---

## 🔌 Working Principle

1. Ultrasonic waves are transmitted towards the eye  
2. Reflected signals are received and processed  
3. Envelope detection extracts useful signal features  
4. ADC converts analog signals to digital  
5. Raspberry Pi analyzes data to estimate IOP  
6. Blue light sensor measures exposure simultaneously  
7. Data is displayed on dashboard and alerts are triggered  

---

## 📊 Future Improvements

- 🤖 AI-based prediction of eye diseases  
- 📱 Mobile app integration  
- 📡 Wireless wearable version  
- 🔍 Higher precision IOP measurement (target: **0.5 mmHg**)  
- ☁️ Advanced cloud analytics  

---

## 🏆 Applications

- Early glaucoma detection  
- Daily eye health monitoring  
- Screen-time safety tracking  
- Smart healthcare systems  
- Remote patient monitoring  

---

## 👨‍💻 Author

**Ratnakar Sahoo**  
B.Tech, Electronics & Telecommunication Engineering  
Veer Surendra Sai University of Technology (VSSUT), Burla  

---

## 📜 License
This project is for educational and research purposes.  
You may modify and use it with proper credits.

---

## 🤝 Contributions
Contributions, suggestions, and improvements are welcome!  
Feel free to fork this repository and submit a pull request.
