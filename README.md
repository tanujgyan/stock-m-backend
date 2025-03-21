# Stock Market Application Backend

This repository contains the backend API for a stock market application, built using Python and FastAPI. It provides endpoints for managing stock data, user watchlists, portfolios, and news.

## Features

* **Stock Data:** Retrieve real-time and historical stock information.
* **Watchlists:** Manage user watchlists for tracking favorite stocks.
* **Portfolios:** Track user stock portfolios and performance.
* **News:** Fetch relevant financial news.
* **User Authentication:** (To be implemented) Secure user authentication and authorization.
* **Database:** Uses PostgreSQL for data storage.
* **API:** Built with FastAPI for high performance and ease of use.

## Technologies Used

* **Python:** Programming language.
* **FastAPI:** Web framework for building the API.
* **Uvicorn:** ASGI server for running the API.
* **SQLAlchemy:** ORM for database interactions.
* **PostgreSQL:** Database system.
* **python-dotenv:** For managing environment variables.
* **requests:** For making HTTP requests to external APIs.

## Prerequisites

* Python 3.8+
* PostgreSQL database
* A financial data API key (e.g., Alpha Vantage, Polygon.io)

## Setup

1.  **Clone the Repository:**

    ```bash
    git clone [repository URL]
    cd stock-market-backend
    ```

2.  **Create a Virtual Environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate      # On Windows
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables:**

    * Create a `.env` file in the root directory.
    * Add your database credentials and API key:

    ```
    DATABASE_URL=postgresql://user:password@host/database
    FINANCIAL_API_KEY=your_api_key
    ```

5.  **Run the API:**

    ```bash
    uvicorn app.main:app --reload
    ```

6.  **Database Setup:**
    * Make sure your postgres database is running.
    * The tables will be automatically created on the first run of the api.

## API Endpoints

* `/stocks`: Stock-related endpoints.
* `/watchlist`: Watchlist management endpoints.
* `/portfolio`: Portfolio management endpoints.
* `/news`: News retrieval endpoints.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

[License]
