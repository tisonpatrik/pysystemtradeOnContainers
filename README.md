# pysystemtradeOnContainers

This project is an unofficial fork of the  [pysystemtrade](https://github.com/robcarver17/pysystemtrade) repository, which I have reimagined to align with modern coding standards and architectural principles while preserving its core functionality.
Please note that this project is still under active development, and many aspects may change over time.
## Overview

The original pysystemtrade project is a comprehensive system for systematic trading and quantitative analysis. Inspired by its robust functionality, this fork aims to modernize the codebase, making it more maintainable, scalable, and efficient by leveraging contemporary technologies.
### Key Technologies
- Python: The primary programming language used to keep the project's core functionality.
- FastAPI: A modern, high-performance web framework for building APIs with Python, used for creating RESTful services in this project.
- Docker compose: Containerization technology used to streamline deployment and ensure consistent environments across different stages of development and production.
- PostgreSQL with TimescaleDB: The database backend, chosen for its robustness and enhanced with TimescaleDB for efficient time-series data management.
- Redis: An in-memory data structure store, used as a cache and message broker to improve the performance and scalability of the system.

### Features
This project currently includes the following services, each with its own dedicated README for more detailed information:

- [seeder](seeder/README.md): Responsible for seeding initial data and configurations required for the system.
- [raw_data]([raw_data/README.md): Handles the ingestion and processing of raw market data.
- [risk]([risk/README.md): Manages risk calculations and risk management strategies.
- [rules]([rules/README.md): Implements the trading rules and decision logic based on the strategies.
- [forecast]([forecast/README.md): Forecasts market movements based on historical data and statistical models.
- [positions]([positions/README.md): Tracks and manages open positions and their performance.

Please note that this list is not exhaustive. Services like portfolios, strategies, and others are not yet included but will be added systematically over time, in line with the original project's approach.
