# Olympic Data Analysis Web App

## Overview

The Olympic Data Analysis Web App is a comprehensive tool designed to explore and analyze Olympic data. This application provides a variety of features, including medal tallies, overall analysis, country-wise analysis, and athlete-wise analysis, offering users deep insights into Olympic history and trends. The project also includes a Jupyter Notebook file that demonstrates the same analysis.

## Features

- **Medal Tally:** View medal tallies for selected years and countries.
- **Overall Analysis:** Gain insights into the overall statistics of the Olympics, including the number of editions, hosts, sports, events, athletes, and participating nations. Visualizations include line charts and heat maps.
- **Country-wise Analysis:** Analyze the performance of individual countries, including their medal tally, sports in which they excel, and their top athletes.
- **Athlete-wise Analysis:** Explore detailed statistics on athletes, including age distribution and the probability of winning medals based on age and sport.

## Technologies Used

- **Streamlit:** For creating the interactive web application.
- **Pandas:** For data manipulation and analysis.
- **Seaborn:** For creating statistical data visualizations.
- **Matplotlib:** For plotting 2D graphs.
- **Plotly:** For creating interactive plots (used `plotly.express` and `plotly.figure_factory`).
- **Jupyter Notebook:** To provide an alternative interface for the analysis, showcasing the same project.

## Deployment

The web app is deployed on [Railway](https://olympic-data-analysis.up.railway.app/), making it accessible online for users to explore the data and analysis.

## Installation

To run the project locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/shubhy04/Olympic-Data-Analysis.git
    ```

2. Activate the virtual environment:

    - For Windows:
      ```bash
      .venv\Scripts\activate
      ```

    - For macOS/Linux:
      ```bash
      source .venv/bin/activate
      ```
      
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

5. Open your browser and go to:
    ```
    http://localhost:8501
    ```

## Usage

- The **Medal Tally** feature allows users to select a year and country to view corresponding medal counts.
- The **Overall Analysis** provides a comprehensive look at Olympic statistics through line charts and heat maps.
- The **Country-wise Analysis** focuses on the performance of specific countries, detailing their medal history and top-performing sports.
- The **Athlete-wise Analysis** delves into individual athlete data, offering insights into age distributions and medal probabilities.
