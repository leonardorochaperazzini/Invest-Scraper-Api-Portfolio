
# Invest Scraper Api Portfolio

This project is an application to manage and analyze investments. It uses Docker to facilitate the setup and execution of the required services, including the application server, a Selenium server for scraping, and a PostgreSQL database.

## Getting Started

To start the project, follow the commands below:

### Docker Commands

- **Run test applications:**
  ```bash
  docker-compose -f docker-compose-test.yml up --abort-on-container-exit
  ```

- **Run application:**
  ```bash
  docker-compose -f docker-compose.yml up 
  ```

  To enter on api docs access http://localhost:8000/docs

## Data Model

The data model is located at `./migration/invest.ddb` and was created using the website [https://www.drawdb.app/](https://www.drawdb.app/).

## PROD

# Api

https://invest-scraper-api.onrender.com - Powered by Render (https://render.com)

# Database 

Powered by Neon postgres (https://neon.tech)

