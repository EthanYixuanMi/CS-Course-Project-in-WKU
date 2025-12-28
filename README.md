# Yixuan Mi’s Project Portfolio

[![Author](https://img.shields.io/badge/Author-Yixuan%20Mi-blue.svg)](https://github.com/EthanYixuanMi)
[![Education](https://img.shields.io/badge/Education-Wenzhou--Kean%20University-lightgrey.svg)](https://www.wku.edu.cn/en)
[![Status](https://img.shields.io/badge/Status-Portfolio%20Active-brightgreen.svg)](#)
[![Contact](https://img.shields.io/badge/Contact-Email-red.svg)](mailto:yixuanmi25@gmail.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)


Welcome to my project portfolio! This repository showcases the various projects I completed during my undergraduate studies at Wenzhou-Kean University. These projects demonstrate my skills in software development, artificial intelligence, data structures, and system design, which I honed throughout my academic journey.

---

## Repository Overview

This repository contains documentation and code for the following projects:

### 1. **Improved Genetic Algorithm for Graph Coloring** (Highlighted)
**Course**: CPS3440 - Analysis of Algorithms  

**Description**:  
A research-driven project that implements and evaluates six graph coloring algorithms, ranging from classical greedy heuristics to a customized, improved Genetic Algorithm (GA).  
The project focuses on **algorithmic design choices**, **theoretical behavior**, and **empirical performance evaluation** across diverse graph structures.

**Key Contributions:**
- Implementation of **6 graph coloring algorithms**: Greedy, LDF, Welsh–Powell, DSatur, Random Greedy, and an **Improved Genetic Algorithm**
- A **graph-specific GA design**, featuring:
  - Greedy-based color upper bound to reduce search space  
  - Lexicographic fitness prioritizing conflict elimination  
  - Repair operator for invalid individuals  
  - Guided mutation and elitism for stable convergence
- **Six comprehensive experiments**, including adversarial Crown graphs and statistical analysis over 30 trials
- Fully reproducible pipeline with **automatic figure generation and visualization**

**Technologies Used**: Python, NetworkX, Matplotlib, Genetic Algorithms, Experimental Evaluation     
[Learn More](https://github.com/EthanYixuanMi/Improved-GA-for-Graph-Coloring)   

---   

### 2. **SmartCourse: Course Selection System with AI Suggestion Module** (Highlighted)
**Course**: CPS3320 - Python Programming    

**Description**: SmartCourse is an intelligent course selection platform that simplifies scheduling by offering personalized recommendations based on students' academic history, major, and four-year plans. 

**Key Features:**
- **AI-Powered Guidance**: Combines course registration with an on-premise AI adviser, turning enrollment into a data-driven mentoring experience.
- **Lightweight & Modular**: Uses a Python codebase with plain-text storage, eliminating the need for heavy databases or cloud subscriptions, while allowing 
easy migration to SQL/REST. 
- **Dual UI for Flexibility**: CLI for quick admin tasks and Gradio for a modern web interface, ensuring accessibility with role-based permissions. 
- **Automated Notifications**:  Email alerts keep students and instructors updated without manual follow-ups.
- **Centralized Logging**: Simplifies auditing and tracking of system activity.
- **Cost & Privacy Benefits**: Local AI (via Ollama) avoids external API costs and enhances data security.
- **Improved Efficiency**: Reduces advising bottlenecks while providing personalized scheduling. 
- **Easy Maintenance**: Modular design ensures sustainable usability and straightforward updates.

**Technologies Used**: Python, Gradio UI Design, Ollama-served LLM, SMTP service, File I/O       
[Learn More](./CPS3320)

---

### 3. **Car Rental Management System**   
**Course**: CPS2232 - Data Structures    

**Description**: A robust system designed to streamline car rental services, catering to customers and rental companies. The system offers user-friendly interfaces, efficient data management, and role-based access control.

**Key Features:**
- **Vehicle Management**: Add, remove, and update vehicle information.
- **User Authentication**: Secure login for customers and administrators.
- **Transaction Management**: Real-time rental and return operations with logging.
- **Email Notifications**: Confirmation emails using JavaMail API.
- **Persistent Storage**: Dynamic data handled with ArrayList and synchronized with files.

**Technologies Used**: Java, JavaMail API, Maven, ArrayList, File Handling  
[Learn More](./CPS2232)

---

### 4. **Course Selection System**
**Course**: CPS2231 - Computer Programming  

**Description**: A menu-driven system replicating key functionalities of the Kean WISE system. It supports two user roles (students and instructors), enabling course registration and management.

**Key Features:**
- Role-specific menus for students and instructors.
- Encapsulation and validation for robust functionality.
- Scalable design for future enhancements.

**Technologies Used**: Java, Object-Oriented Programming, UML Design  
[Learn More](./CPS2231)

---

### 5. **Programming Fundamentals Project**
**Course**: CPS1231 - Foundation of Computer Science

**Description**: A beginner-level project applying fundamental programming techniques to build a menu-driven application with diverse functionalities such as quizzes, lottery simulations, and data visualization.

**Key Features:**
- Modular code structure with extensive documentation.
- Applications of Monte Carlo simulations and income tax calculators.

**Technologies Used**: Java, Basic Control Structures, Modular Programming  
[Learn More](./CPS1231)

---

## How to Navigate This Repository

The repository is organized into subdirectories for each project. Each subdirectory includes:
- Project code.
- Documentation.
- Relevant resources such as UML diagrams or presentation slides.

---

## Contact Information
- **Name**: Yixuan Mi  
- **Email**: [yixuanmi25@gmail.com](mailto:yixuanmi25@gmail.com)  
- **Education**: B.S. in Computer Science, Wenzhou-Kean University  

Thank you for visiting my repository! Feel free to explore and reach out with any questions or collaboration ideas.

