# Insights - Weather Display Web Application

## About
Weather Display Web Application is a Django-based web application that enables users to input a simple location to fetch and display precise weather data. The application utilizes the Geocoding API to determine location coordinates and the OpenMeteo API to retrieve relevant weather information, presented through a user-friendly HTML interface.

## Features
- **Location Input:** Users enter a location to receive precise weather details.
- **API Integration:** Utilizes the Geocoding API for location coordinates and the OpenMeteo API for weather data.
- **User-friendly Interface:** HTML pages provide a clean and easy-to-navigate interface.
- **Real-time Data:** Ensures up-to-date weather information for accuracy.

## Technologies Used
- **Django:** Manages server-side logic, routing, and data handling.
- **HTML:** Structures the frontend presentation.
- **CSS:** Styling. 

## Getting Started
To run this application locally, follow these steps.

### Prerequisites
- Python 3.8 or higher
- Django 3.2 or higher

### Installation and Running the application
1. Clone the repo
   ```sh
   git clone https://github.com/sumi0309/Insights.git

2. Install django
   ```sh
   pip install django

3. Run the server
   ```sh
   cd Insights
   python manage.py runserver

### Usage
Once the server is running, open your web browser and visit http://127.0.0.1:8000 to start using the application. Enter a location in the provided input field to view the weather data. The system will retrieve and display current weather conditions, temperature, humidity, wind speed, and more, ensuring you have all the necessary information at your fingertips.
