# Taxi ETL

This project provides tools to download, process, and visualize NYC Taxi trip data. It includes:

- Data extraction from the NYC Taxi dataset
- A Streamlit UI for data visualization
- Modal deployment support for cloud hosting

## Installation and Usage

Setup modal: 
```bash
uv run modal setup
```

The project includes several convenience commands defined in `env.sh`:

```bash
# Run the UI with Modal (cloud deployment)
alias ui="uv run modal serve ui_modal.py"

# Run the UI locally with Streamlit
alias uil="APP_ENV=development uv run streamlit run ui.py"

# Deploy the UI to Modal
alias deploy="uv run modal deploy ui_modal.py"
```
