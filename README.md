Shopify Insights & Competitor Analysis API

A robust backend application designed to scrape Shopify stores, extract key business insights, persist the data, and perform intelligent competitor analysis using Large Language Models (LLMs).
🚀 Features

This application provides a comprehensive suite of tools for analyzing D2C brands hosted on Shopify.
Core Functionality

    In-depth Scraping: Extracts a wide range of data points from any Shopify store, including:

        Full Product Catalog

        Social Media Handles (Instagram, Facebook, etc.)

        Contact Details (Emails, Phone Numbers)

        Key Pages & Policies (About Us, FAQs, Refund & Privacy Policies)

    Content Extraction: Not only finds links to important pages but also scrapes and cleans their full text content.

    Database Persistence: All successfully scraped data is saved to a MySQL database for future analysis and retrieval using an "upsert" logic (insert or update).

Bonus Features

    Automated Competitor Analysis:

        Automatically discovers competitors for a given brand using web searches.

        Intelligently validates that discovered competitors are also on the Shopify platform before scraping.

    LLM-Powered Comparative Analysis:

        Leverages Google's Gemini Pro model via LangChain to generate a qualitative, comparative summary.

        The summary analyzes the main brand against its competitors on key metrics like product strategy, pricing, and brand voice.

    Robust API Design: Built with FastAPI, featuring:

        Pydantic models for strong data validation and automatic documentation.

        Asynchronous background tasks for non-blocking database operations.

        Comprehensive error handling for a resilient user experience.

🛠️ Tech Stack

    Backend Framework: FastAPI

    Programming Language: Python 3.11+

    Database: MySQL 8.0

    ORM: SQLAlchemy

    LLM Integration: LangChain, Google Generative AI (Gemini Pro)

    Web Scraping: Requests, BeautifulSoup4, GoogleSearch-Python

    Data Validation: Pydantic

    Environment Management: python-dotenv


⚙️ Setup and Installation

Follow these steps to set up and run the project locally.
  1. Prerequisites

    Python 3.11 or newer

    A running MySQL server (e.g., via XAMPP, Docker, or a cloud service)

    Git

  2. Clone the Repository

    git clone <your-repository-url>
    cd <repository-name>

  3. Set Up a Virtual Environment

    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

  4. Install Dependencies

    pip install -r requirements.txt

  5. Configure Environment Variables

  Create a file named .env in the project root.

  Add your database URL and Google API key to this file.

  # .env
    DATABASE_URL="mysql+pymysql://user:password@hostname/database_name"
    GOOGLE_API_KEY="your_google_api_key_here"

  6. Set Up the Database

  Connect to your MySQL server.

  Create a database (e.g., shopify_insights).

  Run the SQL script provided in the project (or below) to create the brands table.

    CREATE TABLE brands (
    id INT AUTO_INCREMENT PRIMARY KEY,
    website_url VARCHAR(255) UNIQUE NOT NULL,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    product_catalog JSON,
    social_handles JSON,
    contact_details JSON,
    privacy_policy_url VARCHAR(512),
    privacy_policy_content TEXT,
    refund_policy_url VARCHAR(512),
    refund_policy_content TEXT,
    about_us_url VARCHAR(512),
    about_us_content TEXT,
    contact_us_url VARCHAR(512),
    contact_us_content TEXT,
    faqs_url VARCHAR(512),
    faqs_content TEXT,
    blogs_url VARCHAR(512),
    blogs_content TEXT,
    track_order_url VARCHAR(512),
    track_order_content TEXT
    );

▶️ Running the Application

Once the setup is complete, you can start the FastAPI server using Uvicorn.

From the project's root directory, run:

    uvicorn src.main:app --reload

The server will be running at http://127.0.0.1:8000.
📖 API Endpoints
/get-insights
/competitorAnalysis
/llm-competitor-analysis
