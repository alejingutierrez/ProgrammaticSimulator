# ProgrammaticSimulator

## Overview

ProgrammaticSimulator is a web-based application that simulates the process of setting up and evaluating programmatic advertising campaigns. It is designed as an educational tool to help users understand the interplay of various factors like brand selection, audience targeting, interest specification, campaign objectives, and budget in achieving campaign outcomes. The simulator provides quantitative metrics and qualitative feedback to guide learning.

## Features

*   **Brand Selection:** Choose from approximately 20 Colombian brands across diverse categories (Banca, Energía, CPG, Airlines, Retail, Telecom, Tech, Construcción).
*   **Audience Targeting:** Select from approximately 15 detailed Colombian audience profiles with unique characteristics and affinities.
*   **Granular Interest Targeting:** Refine targeting by selecting from a list of approximately 35 detailed interests.
*   **Campaign Objectives:** Define campaign goals from options like "Reconocimiento de Marca," "Tráfico al Sitio Web," "Interacción con la Marca," and "Conversiones."
*   **Budget Input:** Specify the campaign budget in COP.
*   **Realistic Simulation Outcomes:**
    *   Overall campaign performance score (1-10).
    *   Estimated core metrics: Impressions, Clics, CPM (Costo Por Mil), CPC (Costo Por Clic), and total Budget Spent.
    *   Estimated secondary metrics: Calculated Interactions and Conversions based on campaign settings and goal.
*   **Contextual Feedback:** Receive detailed suggestions and comments based on your campaign setup to understand performance drivers and identify areas for improvement.

## Project Structure

The project is organized into frontend, backend, and test directories:

*   `programmatic_simulator/`
    *   `frontend/`: Contains the HTML, CSS, and JavaScript for the user interface.
        *   `index.html`: The main page for the simulator.
        *   `css/style.css`: Styles for the application.
        *   `js/app.js`: Frontend JavaScript logic for fetching data, submitting simulations, and displaying results.
    *   `backend/`: Contains the Flask backend server, simulation logic, and data.
        *   `data/market_data.py`: Stores predefined Colombian brands, audience profiles, detailed interests, and campaign goals. This is a key file for customizing simulation entities.
        *   `simulator/campaign_logic.py`: Contains the core algorithm for simulating campaign performance, calculating metrics, scoring, and generating feedback.
        *   `main.py`: The Flask application entry point, defining API routes for market data and campaign simulation.
    *   `tests/`: Contains unit tests for the project.
        *   `backend/test_campaign_logic.py`: Unit tests for the backend simulation logic.
    *   `requirements.txt`: Lists Python dependencies for the backend.
    *   `README.md`: This file.

## Setup and Running the Simulator

### Prerequisites

*   Python 3.x (tested with 3.10+)

### Installation & Setup

1.  **Clone the Repository** (or ensure you have the project files):
    If this were a Git repository, you would clone it. For now, assume you have the `programmatic_simulator` directory.

2.  **Navigate to the Project Directory:**
    Open your terminal or command prompt and navigate into the main project directory:
    ```bash
    cd path/to/programmatic_simulator
    ```

3.  **Create and Activate a Virtual Environment** (Recommended):
    ```bash
    python -m venv venv
    ```
    Activate the virtual environment:
    *   On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        venv\Scripts\activate
        ```

4.  **Install Dependencies:**
    Ensure your virtual environment is activated. Then install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Backend Server

1.  Ensure you are in the `programmatic_simulator` directory and your virtual environment is activated.
2.  Run the Flask development server:
    ```bash
    python backend/main.py
    ```
3.  The backend server should start, typically running on `http://localhost:5001`. You'll see output in your terminal indicating it's running.

### Accessing the Frontend

1.  Once the backend server is running, open the `frontend/index.html` file directly in your web browser (e.g., by double-clicking it or using "File > Open" in your browser).

## Running Tests

To run the unit tests for the backend simulation logic:

1.  Navigate to the `programmatic_simulator` directory in your terminal (this is the directory that contains the `tests` folder and the `programmatic_simulator` package folder).
2.  Ensure your virtual environment is activated and dependencies are installed.
3.  Run the unittest discovery command:
    ```bash
    python -m unittest discover -s tests -p "test_*.py"
    ```
    Alternatively, to run a specific test file (assuming you are in the `programmatic_simulator` root directory):
    ```bash
    python -m unittest programmatic_simulator.tests.backend.test_campaign_logic
    ```

## Key Data Files

*   **`programmatic_simulator/backend/data/market_data.py`**: This file is central to the simulator's content. It defines the available Colombian brands, audience profiles, detailed interests, and campaign objectives. Modifying this file allows for customization and expansion of the simulation scenarios.

## Potential Future Enhancements

*   **Advanced Budget Allocation:** Sliders or inputs to allocate budget across different simulated channels (e.g., Display, Video, Social).
*   **Ad Format Selection:** Allow users to choose different ad formats which could influence CTR and costs.
*   **Dayparting:** Simulate campaign performance based on selected times of day or days of the week.
*   **Geographic Sub-targeting:** Introduce options for targeting specific regions or cities within Colombia.
*   **More Sophisticated KPI Tracking:** Implement more nuanced calculations for Engagement and Conversion metrics beyond the current placeholders.
*   **Learning Modules:** Integrate educational content directly alongside the simulator features to explain concepts.
*   **Campaign Saving/Loading:** Allow users to save their campaign configurations and results for later review or comparison.
*   **Visualizations:** Add charts or graphs to display campaign results and trends more visually.
