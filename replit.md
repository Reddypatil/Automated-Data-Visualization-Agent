# DataWizard - AI-Powered Data Analytics Platform

## Overview

DataWizard is a comprehensive Streamlit-based web application that provides automated data analysis, visualization, and predictive modeling with AI-powered insights. Users upload datasets (CSV, Excel, JSON) and the system performs exploratory data analysis, generates beautiful visualizations, detects anomalies, analyzes correlations, and trains predictive models with natural language AI recommendations.

## User Preferences

- **Communication Style**: Simple, everyday language
- **Design Preference**: Modern, gradient-based purple/blue color scheme with smooth animations
- **Feature Priority**: AI insights, advanced analytics, predictive modeling

## Current Architecture

### Frontend Design
- **Theme**: Modern gradient (Purple #667eea → Violet #764ba2)
- **Layout**: 7-tab interface with clean card-based components
- **UI Elements**: Smooth transitions, rounded corners, box shadows, hover animations
- **Navigation**: Sidebar with quick guide, expandable sections, organized metrics

### Core Modules (11 Analytics Modules)

1. **data_ingestion.py** - Multi-format file loading (CSV, Excel, JSON)
2. **data_preprocessing.py** - Deduplication, forward-fill imputation
3. **eda_analysis.py** - Basic exploratory statistics
4. **ai_chart_selector.py** - AI-selected charts with detailed explanations
5. **visualization_generator.py** - Bar, histogram, scatter, box plots with seaborn
6. **insight_generator.py** - Statistical summary insights
7. **report_generator.py** - Text-based comprehensive reports
8. **data_profiling.py** - Column-level statistics
9. **anomaly_detection.py** - Z-score outlier detection
10. **correlation_analysis.py** - Pearson/Spearman correlation testing
11. **data_quality.py** - Missing values, duplicates, memory usage reports
12. **outlier_analysis.py** - Detailed outlier information with indices
13. **time_series_analysis.py** - Date-based trend and seasonal analysis
14. **predictive_models.py** - Linear/Logistic regression with evaluation
15. **ai_insights.py** - GPT-4o-mini powered natural language insights

### UI/UX Components
- Custom CSS styling in app.py with inline styles
- 7 main tabs: EDA, Quality, Visualizations, Analytics, AI Insights, Predictions, Report
- Feature cards, metric displays, expandable sections
- Beautiful gradient backgrounds and smooth animations

### Data Processing
- In-memory Pandas DataFrames
- No database persistence (stateless)
- Handles missing values with forward-fill
- Statistical analysis using SciPy
- ML models using scikit-learn

### External Integrations
- **OpenAI API**: GPT-4o-mini for natural language insights (via Replit AI Integrations)
- **Visualization Libraries**: Matplotlib, Seaborn
- **ML Libraries**: scikit-learn for regression/classification
- **PDF Generation**: reportlab (installed but not yet implemented)

## Features Implemented

### ✅ Completed Features
- Multi-format data ingestion
- Data quality reporting
- EDA with basic statistics
- AI-selected visualizations (bar, histogram, scatter, box plots)
- Correlation heatmaps with statistical tests
- Detailed outlier analysis
- Time series analysis with trend detection
- Predictive modeling (regression & classification)
- AI-powered natural language insights
- Download report functionality
- Beautiful modern UI with gradient design

## Suggested Features to Add

### High-Impact Features
1. **Data Transformation UI** - Interactive column operations (rename, drop, convert types)
2. **Custom SQL Query Builder** - Let users filter/group data visually
3. **Comparative Analysis** - Upload 2 datasets and compare
4. **Advanced Chart Customization** - User control over chart parameters
5. **Export to Multiple Formats** - CSV, Excel, JSON downloads
6. **Data Sampling** - Handle large datasets with sampling
7. **Feature Engineering Suggestions** - Auto-suggest derived columns
8. **Clustering Analysis** - K-means, hierarchical clustering visualization
9. **PDF Report Export** - Professional formatted PDF (reportlab integrated)
10. **Real-time Data Updates** - Refresh from URL/API endpoints
11. **Hypothesis Testing** - A/B testing, t-tests, ANOVA
12. **Natural Language Queries** - "Show me sales by region" → auto-generates analysis
13. **Collaborative Features** - Save/share analysis sessions
14. **Data Lineage Tracking** - Show transformation history
15. **Automated Insights Dashboard** - Key findings highlighted automatically

### Medium-Priority Features
- Custom color themes
- Dark mode
- Mobile responsive design
- API endpoint generation
- Batch processing
- Multi-file upload & merge
- Data validation rules
- Outlier removal with preview
- Model comparison tools
- Ensemble predictions

### Advanced Features
- Database connectivity (PostgreSQL, MySQL)
- Streaming data support
- Advanced NLP analysis
- Computer vision image analysis
- Custom model training with callbacks
- Feature importance analysis
- SHAP model explainability
- Real-time monitoring/alerts

## External Dependencies

```
streamlit - Web app framework
pandas - Data manipulation
numpy - Numerical computing
matplotlib - Visualization
seaborn - Statistical visualization
scipy - Statistical functions
scikit-learn - Machine learning
reportlab - PDF generation
```

## Deployment Status

- ✅ Running on port 5000
- ✅ Works with Replit's AI Integrations
- ✅ No database required
- ✅ Ready for production deployment

## Next Steps

1. Add PDF report generation (reportlab ready)
2. Implement data transformation UI
3. Add clustering analysis
4. Create custom chart builder
5. Add export functionality
