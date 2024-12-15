
# Invest Scraper Portfolio

This project is an application to manage and analyze investments. It uses Docker to facilitate the setup and execution of the required services, including the application server, a Selenium server for scraping, and a PostgreSQL database.

## Getting Started

To start the project, follow the commands below:

### Docker Commands

  - **Build application as api:**
  ```bash
  docker-compose -f docker-compose-api.yml -p app1 build
  ```

- **Run Selenium service:**
  ```bash
  docker-compose -f docker-compose-selenium-server.yml up
  ```

- **Run database service:**
  ```bash
  docker-compose -f docker-compose-db.yml -p db-1 up
  ```

- **Run application as api:**
  ```bash
  docker-compose -f docker-compose-api.yml -p app1 up
  ```

## Data Model

The data model is located at `./migration/invest.ddb` and was created using the website [https://www.drawdb.app/](https://www.drawdb.app/).

## PROD

# Api

Powered by Render (https://render.com)

# Database 

Powered by Neon postgres (https://neon.tech)

