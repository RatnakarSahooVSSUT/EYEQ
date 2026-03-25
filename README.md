# 👁️ EYE-Q: Smart Eye Health Monitoring System  
### 🚀 Non-Contact IOP Measurement & Blue Light Monitoring using IoT + Embedded Systems  

![IoT](https://img.shields.io/badge/Domain-IoT-blue)
![Embedded](https://img.shields.io/badge/Embedded-Raspberry%20Pi-green)
![Sensors](https://img.shields.io/badge/Sensors-Ultrasonic%20%7C%20TCS34725-orange)
![ADC](https://img.shields.io/badge/ADC-ADS1115-purple)
![Protocol](https://img.shields.io/badge/Protocol-I2C-yellow)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Focus](https://img.shields.io/badge/Focus-Healthcare%20Tech-red)
![License](https://img.shields.io/badge/License-Educational-lightgrey)

---

## 📌 Overview  

**EYE-Q** is an advanced **IoT-based smart eye health monitoring system** designed for **real-time, non-invasive analysis of critical eye parameters**, including **Intraocular Pressure (IOP)** and **blue light exposure**.

The system integrates **ultrasonic sensing, embedded signal processing, and IoT-based monitoring** to provide an **affordable, portable, and early detection solution for eye diseases such as glaucoma**.

---

## 🎯 Key Highlights  

- 👁️ **Non-contact IOP Measurement** using ultrasonic elastography  
- 🔵 **Blue Light Exposure Monitoring** with intelligent categorization  
- 📊 **Real-time IoT Dashboard (Web APK)**  
- ⚠️ **Smart Alert System (LED + Buzzer)**  
- 📡 **Cloud-enabled data logging & analytics**  
- 🔧 **Low-cost, portable healthcare solution**  
- 🎯 Target precision: **0.5 mmHg (IOP measurement goal)**  

---

## 🧠 System Architecture  

```
Ultrasonic Tx → Eye → Rx → Amplifier → Envelope Detector → ADC → Raspberry Pi → Dashboard
                                                            ↓
                                                   Alert System (LED + Buzzer)

TCS34725 Sensor → Raspberry Pi → Blue Light Analysis → Dashboard + Alerts
```

---

## ⚙️ Working Principle  

### 🔹 Ultrasonic IOP Measurement  
- 40 kHz ultrasonic waves transmitted towards cornea  
- Reflected echo captured using receiver  
- Signal processed using **multi-stage amplification + envelope detection**  
- Digital conversion via **ADS1115 (16-bit ADC)**  
- Raspberry Pi estimates **corneal stiffness → IOP correlation**  

### 🔹 Blue Light Detection  
- **TCS34725 sensor** measures RGB values  
- Blue light intensity extracted and categorized:  
  - Safe  
  - Moderate  
  - High  
  - Dangerous  

### 🔹 Data Processing & IoT  
- Raspberry Pi performs:  
  - Signal processing  
  - Threshold classification  
  - IoT data transmission  
- Real-time visualization on web dashboard  

### 🔹 Alert System  
- LED Indicators:  
  - No blink → Safe  
  - 3 blinks → Moderate  
  - 5 blinks → High  
  - 10 blinks → Dangerous  
- Buzzer triggers for critical conditions  

---

## 🛠️ Hardware Components  

- Raspberry Pi 4 Model B  
- Ultrasonic Transducers (HY40A12R09-1, 40 kHz Tx & Rx)  
- ADS1115 (16-bit ADC)  
- TCS34725 Color Sensor  
- LM358P / NE5532P Op-Amps  
- IRLZ44 MOSFET  
- Diodes (1N4148, 1N5819, UF4007)  
- Passive Components (Resistors, Capacitors)  
- LED + Buzzer Module  
- Power Supply  

---

## 💻 Software & Technologies  

- **Programming:** Python  
- **Communication:** I2C Protocol  
- **Processing:** Embedded Signal Processing  
- **Frontend:** Web Dashboard (Web APK)  
- **IoT:** Cloud Integration for monitoring & storage  

---

## 📊 System Features Breakdown  

| Module | Function |
|-------|--------|
| Ultrasonic System | Measures corneal stiffness |
| ADC (ADS1115) | Converts analog signals to digital |
| Raspberry Pi | Processing + control |
| TCS34725 | Blue light detection |
| IoT Dashboard | Visualization & logging |
| Alert System | User feedback |

---

## 🚧 Engineering Challenges  

- ⚠️ Weak ultrasonic signal detection  
- ⚠️ Noise in analog signal chain  
- ⚠️ Precise envelope extraction  
- ⚠️ Calibration for IOP accuracy  
- ⚠️ Blue light threshold tuning  

---

## ✅ Solutions Implemented  

- ✔️ Multi-stage amplification using LM358P / NE5532P  
- ✔️ Precision envelope detection circuit  
- ✔️ High-resolution ADC (ADS1115)  
- ✔️ Signal averaging for stability  
- ✔️ Optimized threshold-based classification  

---

## 📸 Results  

✔️ Real-time eye parameter monitoring  
✔️ Reliable blue light exposure detection  
✔️ Functional alert system  
✔️ Stable IoT dashboard integration  

---

## 📚 Learning Outcomes  

- Embedded system design (Raspberry Pi)  
- Analog + digital signal processing  
- Sensor interfacing (I2C, ADC)  
- IoT system integration  
- Biomedical sensing fundamentals  
- Hardware debugging & calibration  

---

## 🔮 Future Scope  

- 🤖 AI-based eye disease prediction  
- 📱 Mobile app integration  
- 📡 Wearable smart eye device  
- 🔍 High-precision IOP (≤ 0.5 mmHg target)  
- ☁️ Advanced cloud analytics & insights  

---

## 🏆 Applications  

- Early glaucoma detection  
- Continuous eye health monitoring  
- Screen-time safety tracking  
- Smart healthcare systems  
- Remote patient monitoring  

---

## 👨‍💻 Author  

**Ratnakar Sahoo**  
B.Tech, Electronics & Telecommunication Engineering  
Veer Surendra Sai University of Technology (VSSUT), Burla  

📍 Domain: Embedded Systems | IoT | Healthcare Technology  

---

## ⭐ Portfolio Description (For Resume / LinkedIn)  

**EYE-Q: Smart Eye Health Monitoring System**  
Developed a non-invasive IoT-based system for real-time eye health monitoring using Raspberry Pi. Designed ultrasonic signal processing circuits for IOP estimation and implemented blue light detection using TCS34725 sensor. Integrated ADC-based data acquisition, I2C communication, and cloud-connected dashboard with alert mechanisms. Demonstrated strong expertise in embedded systems, biomedical sensing, and real-time signal processing.

---

## 📜 License  

This project is intended for **educational and research purposes**.  
You may use and modify it with proper attribution.  

---

## 🤝 Contributions  

Contributions, suggestions, and improvements are welcome!  
Feel free to fork the repository and submit a pull request.  

---

⭐ *If you found this project impactful, consider starring the repo!*  
