# Bait El Zakat - FastAPI Backend

A FastAPI-based backend application for Bait El Zakat that integrates with Geidea POS terminals for payment processing.

## Overview

This application provides a REST API to:
- Manage zakat and charity services
- Process payments through Geidea POS terminals
- Record and track transactions
- Generate transaction logs

## Technical Stack

- **Framework**: FastAPI
- **Database**: SQLite
- **Payment Processing**: Geidea POS dll
- **Python Version**: 3.13+

## Configuration

The application uses a `.config` file for configuration with the following parameters:

```
sqlite_file_name,
pos_comport,
transaction_timeout_in_secs,
kiosk_id
```

**Important**: Ensure this `.config` file is present in the working directory when running the application.

## Logging System

The application implements a comprehensive logging system:

- Uses a custom JSON formatter for structured logging
- Logs are stored in JSONL format in the `logs/bait-zakat.jsonl` file
- Implements a queue-based logging handler to prevent blocking operations
- Log rotation with up to 3 backup files of 20MB each

The logging configuration is stored in `src/queued-json-file-logging-config.json`.

## API Endpoints

- **GET /services/** - List all available services
- **POST /transactions/** - Create a new payment transaction

## Building a Distributable EXE

To create a standalone Windows executable:

```bash
pyinstaller --noconfirm --onefile --windowed --name "bait-al-zakat_backend" --clean --add-data "C:\Users\maste\Desktop\bait-el-zakaa\fastapi-backend\meezaapi_v1_9.dll;." --add-data "C:\Users\maste\Desktop\bait-el-zakaa\fastapi-backend\src\queued-json-file-logging-config.json;."  "C:\Users\maste\Desktop\bait-el-zakaa\fastapi-backend\src\main.py"
```

This will package all necessary files into a single EXE file.

### Important Note for Distribution

The `.config` file must be placed in the same directory as the EXE file when distributing the application. The application reads configuration settings from this file at runtime.

## Development Setup

1. Ensure Python 3.13+ is installed
2. Install dependencies: `pip install -e .` 
3. Create a `.config` file with required settings
4. Run the application: `python src/main.py`

## Database

The application automatically creates and initializes the SQLite database with predefined services on first run.