# Automated Data Visualization Agent

## Overview

This is a Streamlit-based web application that provides automated data analysis and visualization. Users upload datasets (CSV, Excel, or JSON), and the system performs exploratory data analysis, generates AI-powered insights, detects anomalies, creates visualizations, and builds simple predictive models. The application serves as an all-in-one data exploration tool that requires minimal user configuration.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit serves as both the UI framework and web server
- **Layout**: Uses Streamlit's tab-based navigation with 7 main sections (EDA, Quality, Visualizations, Analytics, AI Insights, Predictions, Report)
- **Design Pattern**: Single-page application with expandable sections and columns for organized display
- **Visualization Libraries**: Matplotlib and Seaborn for chart generation, rendered directly in Streamlit

### Backend Architecture
- **Structure**: Modular Python files, each handling a specific domain concern
- **Data Flow**: Linear pipeline from ingestion → preprocessing → analysis → visualization
- **Key Modules**:
  - `data_ingestion.py`: File loading (CSV, Excel, JSON)
  - `data_preprocessing.py`: Deduplication and forward-fill for missing values
  - `eda_analysis.py`: Basic exploratory statistics
  - `ai_chart_selector.py`: Rule-based chart recommendation based on column types
  - `visualization_generator.py`: Chart rendering using Matplotlib/Seaborn
  - `anomaly_detection.py`: Z-score based outlier detection
  - `correlation_analysis.py`: Pearson and Spearman correlation with significance testing
  - `predictive_models.py`: Linear and logistic regression using scikit-learn
  - `ai_insights.py`: OpenAI GPT integration for natural language insights

### Data Processing Approach
- **In-Memory Processing**: All data handled via Pandas DataFrames
- **No Database**: Application is stateless with no persistent storage
- **Preprocessing Strategy**: Simple approach using duplicate removal and forward-fill imputation
- **Statistical Methods**: SciPy for z-scores and correlation tests, scikit-learn for ML models

### AI/ML Components
- **Chart Selection**: Heuristic-based logic examining column data types and cardinality
- **Predictive Models**: Basic train/test split with Linear Regression and Logistic Regression
- **Anomaly Detection**: Z-score threshold method (>3 standard deviations)

## External Dependencies

### Python Packages (from requirements.txt)
- **streamlit**: Web application framework and UI
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **matplotlib**: Static visualizations
- **seaborn**: Statistical data visualization
- **scipy**: Statistical functions (z-scores, correlation tests)
- **scikit-learn**: Machine learning models and preprocessing
- **reportlab**: PDF report generation

### External APIs
- **OpenAI API**: Used in `ai_insights.py` for generating natural language insights
  - Model: `gpt-4o-mini`
  - Authentication: Expects `AI_INTEGRATIONS_OPENAI_API_KEY` environment variable
  - Gracefully degrades if API key is not configured

### File Format Support
- CSV files
- Excel files (.xlsx)
- JSON files