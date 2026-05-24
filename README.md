&lt;div align="center"&gt;

&lt;!-- Animated Header --&gt;
&lt;img src="https://capsule-render.vercel.app/api?type=waving&color=0:667eea,50:764ba2,100:f093fb&height=250&section=header&text=Face%20Recognition%20Attendance%20System&fontSize=42&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Edge%20AI%20%7C%20Embedded%20Computer%20Vision%20%7C%20Real-Time%20Inference&descSize=18&descAlignY=55" /&gt;

&lt;!-- Research Badges --&gt;
&lt;p&gt;
  &lt;img src="https://img.shields.io/badge/Edge_AI-Raspberry%20Pi%204-FF6B6B?style=for-the-badge&logo=raspberrypi&logoColor=white&labelColor=0d1117" /&gt;
  &lt;img src="https://img.shields.io/badge/Computer_Vision-OpenCV%20%7C%20dlib-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white&labelColor=0d1117" /&gt;
  &lt;img src="https://img.shields.io/badge/Deployment-TensorFlow%20Lite-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white&labelColor=0d1117" /&gt;
  &lt;img src="https://img.shields.io/badge/Framework-Flask-000000?style=for-the-badge&logo=flask&logoColor=white&labelColor=0d1117" /&gt;
&lt;/p&gt;

&lt;p&gt;
  &lt;img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white" /&gt;
  &lt;img src="https://img.shields.io/badge/Status-Research%20Prototype-success?style=flat-square" /&gt;
  &lt;img src="https://img.shields.io/badge/License-MIT-blue?style=flat-square" /&gt;
  &lt;img src="https://img.shields.io/badge/IEEE%20Indexed-Publication%20Ready-00629B?style=flat-square&logo=ieee&logoColor=white" /&gt;
&lt;/p&gt;

&lt;/div&gt;

---

&lt;!-- Abstract Section --&gt;
## 📜 Research Abstract

&gt; **A Real-Time Edge AI Framework for Automated Attendance Monitoring via Embedded Face Recognition**

This repository presents a lightweight, privacy-preserving attendance system that deploys deep face recognition pipelines directly on **Raspberry Pi 4** edge hardware. By shifting inference from cloud infrastructure to embedded devices, our framework achieves **sub-second latency** for multi-face detection and recognition while ensuring complete data sovereignty — no biometric data leaves the local device.

**Key Contributions:**
- 🧠 End-to-end face encoding pipeline optimized for ARM Cortex-A72 architecture
- ⚡ Real-time inference at **~15 FPS** on Raspberry Pi 4 (4GB)
- 🔒 Zero-cloud architecture — all biometric processing occurs locally
- 📊 Automated attendance analytics with Excel/PDF export capabilities
- 🌐 Flask-based web dashboard for remote monitoring within LAN

---

&lt;!-- Architecture Diagram --&gt;
## 🏗️ System Architecture

&lt;div align="center"&gt;

```mermaid
graph LR
    A[Pi Camera Module] --&gt;|MJPEG Stream| B[OpenCV Capture]
    B --&gt; C[Face Detection&lt;br/&gt;Haar Cascade / HOG]
    C --&gt; D[Facial Landmark&lt;br/&gt;Encoding]
    D --&gt; E[Embedding&lt;br/&gt;Comparison]
    E --&gt;|Threshold &gt; 0.6| F[Attendance&lt;br/&gt;Logging]
    E --&gt;|Unknown Face| G[Alert / Re-enroll]
    F --&gt; H[SQLite Database]
    H --&gt; I[Flask Dashboard]
    I --&gt; J[Excel / PDF&lt;br/&gt;Reports]
