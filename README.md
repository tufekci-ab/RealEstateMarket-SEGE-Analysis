# **District-Level Socioeconomic Scores & Housing Prices**  
## *Real Estate Listings and Regional Development Analysis*  

My project will analyze the strength of the connection between real estate prices in Turkey and the **Socio-Economic Development Index (SEGE)** score of the district they are located in. I will collect data about real estate listings, and after filtering and cleaning the data, I will analyze:  

> **"How does Socio-Economic Development affect housing prices?"**  

---

## **Motivation**  

Housing prices have been a hot topic for the last years in Turkey. We know for sure that factors like **square meter size, number of rooms, and property age** affect the listing price of a house. However, it would be valuable to determine whether the **socio-economic development of a district** has a strong effect on listing prices.  

My project aims to answer the following questions:  
- **Do more developed districts have higher housing prices?**  
- **Are there meaningful price differences between districts with different socioeconomic levels?**  

---

## **Data Sources**  

### **Real Estate Listings**  
- **Source:** Web scraping from online listing websites (potentially including franchise companies like *Coldwell Banker* and *Century 21*).  
- **Data Fields:**  
  - District  
  - Price  
  - Square meters  
  - Number of rooms  
  - Age  
  - Property type  
- **Filtering Criteria:**  
  - Listings **not** priced between **3,000,000 TL and 50,000,000 TL** will be excluded to remove extreme values.  

### **Socioeconomic Development Index (SEGE)**  
- **Source:** 2022 District-level **SEGE Report** from the *Ministry of Industry and Technology*.  
  - [🔗 SEGE Report (PDF)](https://www.sanayi.gov.tr/assets/pdf/birimler/2022-ilce-sege.pdf)  
- **Data Fields:**  
  - **Development ranking** (from **1 - most developed** to **6 - least developed**).  
  - **Development scores** of each district.  

---

## **Objectives**  

**Understand the Key Factors Affecting Real Estate Listing Price**  
- Identify which features are most important for pricing, such as **square meter size, number of rooms, house type, and building age**.  

**Analyze the Relationship Between Socio-Economic Development and Real Estate Prices**  
- Examine how the **socio-economic development** of a district is related to **real estate prices**. Is the effect significant?  

**Modeling the Relationships**  
- Develop a **pricing model** using data from **square meter size, number of rooms, house type, building age, and SEGE Score**.  

**Visualize the Relations**  
- Highlight key insights and relationships using **graphs and infographics**.  

---

## **Hypothesis**  

**Null Hypothesis (H₀):**  
There is **no significant relationship** between the **Socio-Economic Development Index (SEGE) score** of a district and **real estate prices**.  

**Alternative Hypothesis (H₁):**  
There is a **significant relationship** between the **Socio-Economic Development Index (SEGE) score** of a district and **real estate prices**.  

---

## **Dataset**  

### **Real Estate Listings**  
- **District** – The district where the property is listed (**TR: İlçe**)  
- **Price** – The listing price of the property (**TL**)  
- **Square Meters** – The total area of the property (**m²**)  
- **Number of Rooms** – Total number of rooms in the property  
- **Building Age** – Age of the building (**years**)  
- **Property Type** – Apartment, villa, etc.  

### **Socioeconomic Development Index (SEGE)**  
- **District Name** – The name of the district  
- **Development Rank** – Socioeconomic ranking from **1 (most developed) to 6 (least developed)**  
- **Development Score** – Numerical SEGE score of the district  

### **Additional Information & Data Processing**  
- Listings will be collected through **web scraping**.  
- **Outliers** (extremely high or low prices) will be removed based on predefined thresholds (**3,000,000 TL – 50,000,000 TL**).  
- The dataset will be stored in an **Excel sheet** and preprocessed for analysis.  

---

## **Tools and Techniques To Use**  

- **Web Scraping** – Using Python with `BeautifulSoup`  
- **Data Cleaning & Preparation** – Using Python (`Pandas`, `NumPy`)  
- **Exploratory Data Analysis (EDA)** – Calculation of variance, median price, distribution analysis using Python  
- **Visualization** – Visualizing relations using `Matplotlib` in Python  
- **Regression Modeling** – Implementing regression modeling using **Random Forest** in Python  
- **Deep Learning** – Creating deep learning models using `TensorFlow/Keras`  

---
## **Limitations**  
  We will have limitations regarding the fact that the data will not include certain features, such as proximity to hospitals and schools. Additionally, something to consider is that this dataset will include pricing data for houses listed on the market through the channels we scrape. This may introduce some biases in the data. It is also important to note that the listing price of a house alone is not sufficient to predict its value. Listing prices and final sale prices may differ slightly for some listings and significantly for others.

Furthermore, more advanced filtering techniques can be applied, such as filtering out extreme data based on price per square meter within each district separately."

---

## **Conclusion**  

This project's mission is to understand the impact of the socioeconomic development of a district (İlçe) on real estate prices in Turkey. Using data science, web scraping, and deep learning techniques, we will analyze whether district-level SEGE scores significantly influence property prices. Additionally, we will attempt to model the relationships between key factors affecting real estate pricing.  

The results of this study will hopefully offer a data-driven perspective on the housing market in Turkey and its relationship with the regional development of districts.  

---


