
# Invest Project

This project is an application to manage and analyze investments. It uses Docker to facilitate the setup and execution of the required services, including the application server, a Selenium server for scrapers, and a PostgreSQL database.

## Getting Started

To start the project, follow the commands below:

### Docker Commands

- **Build the application:**
  ```bash
  docker-compose -f docker-compose-app.yml -p app1 build
  ```

- **Run the Selenium service:**
  ```bash
  docker-compose -f docker-compose-selenium-server.yml up
  ```

- **Run the database service:**
  ```bash
  docker-compose -f docker-compose-db.yml -p db-1 up
  ```

- **Run the application:**
  ```bash
  docker-compose -f docker-compose-app.yml -p app1 up
  ```

## Data Model

The data model is located at `./migration/invest.ddb` and was created using the website [https://www.drawdb.app/](https://www.drawdb.app/).
