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
- FastAPI: A modern, web framework for building APIs with Python, used for creating RESTful services in this project.
- Docker compose: Containerization technology used to streamline deployment and ensure consistent environments across
different stages of development and production.
- PostgreSQL with TimescaleDB: The database backend, chosen for its robustness and enhanced with TimescaleDB for
efficient time-series data management.
- Redis: An in-memory data structure store, used as a cache and message broker to improve the performance and scalability of the system.

### Features
This project currently includes the following services / modules, each with its own dedicated README for more detailed information:

- [raw_data]([raw_data/README.md): Handles the ingestion and processing of raw market data.
- [rules]([rules/README.md): Implements the trading rules and decision logic based on the strategies.
- [forecast]([forecast/README.md): Forecasts market movements based on historical data and statistical models.
- [positions]([positions/README.md): Tracks and manages open positions and their performance.
- [common]([common/README.md): Module contains shared utilities and models used across different services.
Please note that this list is not exhaustive. Services like portfolios, strategies, and others are not yet included but will be added systematically over time, in line with the original project's approach.

## How to run this project?
Before you proceed, it's crucial that you have a solid understanding of the original pysystemtrade project.

Familiarity with its structure and functionality will greatly help you in working with this fork.
### Prerequisites
- Install python 3.12, idally using [uv](https://github.com/astral-sh/uv)
- Install [go](https://go.dev/) for project init
- Install [Docker](https://www.docker.com/) with docker compose
- Install make (we will move to Just in the future)

### Running the project
To start the project, run the following command in your terminal:
```bash
make init
```

Then you can start the project by running the following command in your terminal:

```bash
make run
```
This command will:

- Create necessary binaries
- Initialize the environment
- Download required data
- Start the application
- Run any pending migrations
- Seed the database with raw data (this may take a few minutes)

Once completed, all endpoints will be available for testing via Swagger at http://localhost:8xxx/docs.

For more details about port configurations, refer to the Docker Compose file.

#### Troubleshoting
Sometimes the migrate tool fails to connect to the database, if this happens, you can run init command again (mostly works),
or run migrations and seeds manualy by commands in databse/Makefile


## Why all of this?
The motivation behind this project is rooted in my deep appreciation for Robert Carver's work.
His contributions to the field of systematic trading and quantitative analysis are truly remarkable.
I encourage you to explore his blog, read his books, and follow his insights:
- [blog](https://qoppac.blogspot.com/)
- [books](https://www.systematicmoney.org/)
- [Rob`s Twitter ](https://x.com/investingidiocy)

The original pysystemtrade project is a testament to his expertise, but I believe that there is room for improvement.
Particularly in terms of performance, scalability, testability, and readability.
While I can't guarantee that my code fully achieves these goals, it is a sincere attempt to push the boundaries.


## Future Considerations

This is a prioritized list of issues and areas for improvement:
- Finish base functionality of pysystemtrade application
- Grpc Integration: Implementing gRPC for better communication between core services.
- API Gateway: Setting up an API Gateway as the entry point for the entire application.
- Testing: currently it does not exist
- Performance Optimization: Switching from Pandas to Polars for faster data processing.
- Refactoring Plans: Breaking down raw_data service into smaller, more manageable components.
- Logging: Currently, logging happens only in the terminal. A proper logging solution should be implemented for better traceability and debugging.
- Monitoring: Monitoring does not exist and needs to be established for better observability of trading system.
- CI/CD Pipeline: Setting up a continuous integration and deployment pipeline.
- Infrastructure: moving towards a Kubernetes-based infrastructure.

Any feedback or contributions to these areas would be highly appreciated as we continue to develop and refine this project.
