# Intelligent Waste Classification and Sorting System

## Project Overview
This project focuses on developing an intelligent waste classification and sorting system utilizing **deep learning** to promote efficient waste management. By leveraging **Convolutional Neural Networks (CNNs)** for image classification, the system automates the identification and categorization of waste into four predefined categories: **metal, paper, glass, and plastic**. The system integrates this classification capability with a hardware prototype waste bin that automatically rotates to align with the correct waste compartment, ensuring systematic waste disposal.

## Features
- **Image Classification:** A CNN model trained on the **Garbage Classification Dataset** sourced from Kaggle to identify waste categories.
- **Automated Sorting:** A hardware prototype waste bin with rotational functionality for precise sorting.
- **Cloud Deployment:** The trained model is deployed on **Amazon AWS**, enabling real-time image recognition via a cloud endpoint.
- **Efficient Waste Management:** A methodical approach for waste detection, identification, and sorting.

## Project Objectives
1. Develop a robust CNN-based image classification model for waste detection.
2. Optimize and evaluate multiple CNN architectures to select the best-performing model.
3. Implement an automated hardware waste bin prototype for waste sorting based on classification results.
4. Deploy the deep learning model on a cloud platform for real-time image classification.

## Methodology

### 1. Dataset Preparation
- **Dataset Source:** Kaggle's Garbage Classification Dataset.
- **Classes:** Metal, Paper, Glass, and Plastic.
- **Data Split:** 
  - **Training Data:** 80% of the dataset.
  - **Validation Data:** 20% of the dataset.

### 2. Model Development and Training
- Several **CNN architectures** were trained and tested using the prepared dataset.
- Hyperparameter tuning was conducted to optimize model performance.
- The best-performing model in terms of accuracy and efficiency was selected for deployment.

### 3. Model Deployment
- The final model was deployed on **Amazon AWS Cloud Services**, enabling scalable and efficient image recognition.
- An API endpoint was generated for the hardware prototype to communicate with the deployed model.

### 4. Hardware Integration
- **Waste Bin Design:** A compartmentalized bin with five sections (one for each of the four waste categories and an overflow compartment).
- **Control Unit:** The hardware uses the model's classification results to rotate and align the bin's opening with the appropriate compartment.

## Results
- The selected CNN model achieved high accuracy in classifying waste into the predefined categories.
- Real-time predictions from the AWS-deployed model effectively guided the waste bin's sorting mechanism.
- The prototype successfully demonstrated automated sorting, fulfilling the project’s objectives of efficient waste management.

## Hardware Components
- **Compartmentalized Waste Bin:** Divided into sections for metal, paper, glass, and plastic.
- **Rotational Mechanism:** Enables alignment with the correct waste compartment.
- **Control Unit:** Processes classification results and triggers bin rotation.

## Software Components
- **Deep Learning Model:** Convolutional Neural Network for waste classification.
- **Cloud Integration:** Amazon AWS for model deployment and endpoint creation.
- **Programming Language:** Python.

## Tools and Technologies
- **Deep Learning Frameworks:** TensorFlow/Keras.
- **Cloud Platform:** Amazon AWS.
- **Dataset Source:** Kaggle.
- **Hardware Control:** Microcontroller (e.g., Arduino/Raspberry Pi).

## Conclusion
This project demonstrates the practical application of deep learning for waste management, combining an **accurate CNN-based classification system** with a **functional hardware prototype** to create an intelligent and automated waste sorting solution. The integration of cloud deployment and automated hardware ensures scalability and real-world applicability in promoting efficient and sustainable waste management practices.

## Future Work
- **Expand Dataset:** Include additional waste categories for broader applicability.
- **Improve Hardware:** Enhance the bin's sorting speed and capacity.
- **Edge Deployment:** Optimize the model for on-device deployment to reduce latency and reliance on cloud services.

## Acknowledgments
Special thanks to the contributors of the **Kaggle Garbage Classification Dataset** and to all team members who contributed to the successful completion of this project.
