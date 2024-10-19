# pysystemtradeOnContainers

This project is an unofficial fork of the  [pysystemtrade](https://github.com/robcarver17/pysystemtrade) repository,
which I have reimagined to align with modern coding standards and architectural principles while preserving its core functionality.
Please note that this project is still under active development, and many aspects may change over time.
## Overview

The original pysystemtrade project is a comprehensive system for systematic trading and quantitative analysis.
Inspired by its robust functionality, this fork aims to modernize the codebase, making it more maintainable, scalable,
and efficient by leveraging contemporary technologies.

### Key Technologies
- Python: The primary programming language used to keep the project's core functionality.
- FastAPI: A modern, high-performance web framework for building APIs with Python, used for creating RESTful services in this project.
- Docker compose: Containerization technology used to streamline deployment and ensure consistent environments across
different stages of development and production.
- PostgreSQL with TimescaleDB: The database backend, chosen for its robustness and enhanced with TimescaleDB for
efficient time-series data management.
- Redis: An in-memory data structure store, used as a cache and message broker to improve the performance and scalability of the system.

### Features
This project currently includes the following services, each with its own dedicated README for more detailed information:

- [raw_data]([raw_data/README.md): Handles the ingestion and processing of raw market data.
- [rules]([rules/README.md): Implements the trading rules and decision logic based on the strategies.
- [forecast]([forecast/README.md): Forecasts market movements based on historical data and statistical models.
- [positions]([positions/README.md): Tracks and manages open positions and their performance.

Please note that this list is not exhaustive. Services like portfolios, strategies, and others are not yet included but will be added systematically over time, in line with the original project's approach.

## How to run this project?
Before you proceed, it's crucial that you have a solid understanding of the original pysystemtrade project.

Familiarity with its structure and functionality will greatly help you in working with this fork.
### Prerequisites

- Clone the Original [pysystemtrade](https://github.com/robcarver17/pysystemtrade) repo, bcs we need data from that.

- Clone and RUN the [pysystemtrade_preprocessing](https://github.com/tisonpatrik/pysystemtrade_preprocessing) repo

This preprocessing tool is essential for transforming the original pysystemtrade data into a format that is compatible with
our postgres schemas. The data from the original pysystemtrade project, once processed by the pysystemtrade_preprocessing tool,
will be stored in the pysystemtrade_preprocessing/data directory.
This directory will serve as a volume directory for our database in this project, ensuring seamless integration and data accessibility.

- Install python 3.12
- Install Docker with docker compose

### Running the project
Before running the project, you need to create a `.env` file in the root directory of this project with the following content:

```plaintext
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
POSTGRES_HOST=db_postgres
POSTGRES_PORT=5432
```

Then you can start the project by running the following command in your terminal:

```bash
make run
```
This command will start the Docker Compose process, initializing all the required containers.
Please check docker compose file for more details about ports.
All endpoints you can find in swagger so you can tested it in browser on url `http://localhost:8xxx/docs`

### Next Steps
After the containers are up and running, refer to the [seeder README](seeder/README.md) to inject data into the database.

## Why all of this?
The motivation behind this project is rooted in my deep appreciation for Robert Carver's work.
His contributions to the field of systematic trading and quantitative analysis are truly remarkable.
I encourage you to explore his blog, read his books, and follow his insights:
- [blog](https://qoppac.blogspot.com/)
- [books](https://www.systematicmoney.org/)
- [Rob`s Twitter (fu*k with X name...](https://x.com/investingidiocy)

The original pysystemtrade project is a testament to his expertise, but I believe that there is room for improvement.
Particularly in terms of performance, scalability, testability, and readability.
While I can't guarantee that my code fully achieves these goals, it is a sincere attempt to push the boundaries.


## Future Considerations

In the future, I plan to maintain a list of issues and areas for improvement, which will include:
- Known Issues: For example, the current lack of extensive testing.
- Refactoring Plans: Such as reworking the entire data injection process.
- Nice-to-Have Features: Potential enhancements like switching from Pandas to Polars,
implementing gRPC for better communication, or moving towards a Kubernetes-based infrastructure.

Any feedback or contributions to these areas would be highly appreciated as we continue to develop and refine this project.
