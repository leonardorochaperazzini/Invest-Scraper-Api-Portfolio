from service.Invest import run_invest_scraping_and_save_data

MAX_WORKERS = 1

def main():
    run_invest_scraping_and_save_data(
        max_workers = MAX_WORKERS,
        limit = 2
    )

if __name__ == "__main__":
    main()