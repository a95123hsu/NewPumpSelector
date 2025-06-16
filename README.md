# Pump Selection Tool

A Streamlit-based web application for selecting and comparing water pumps based on various criteria.

## Features

- Multi-language support (English and Traditional Chinese)
- Interactive pump selection based on multiple criteria
- Real-time performance curve visualization
- Automatic calculations for common applications
- Responsive and user-friendly interface
- Data persistence with Supabase backend
- CSV fallback for offline operation

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Supabase account (for online data storage)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd pump-selection-tool
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your Supabase credentials:
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

## Project Structure

```
pump-selection-tool/
├── config.py           # Configuration and constants
├── data_loader.py      # Data loading and validation
├── visualization.py    # Chart creation and visualization
├── translations.py     # Translation dictionaries
├── pump.py            # Main application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run pump.py
```

2. Open your web browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

3. Use the interface to:
   - Select pump category, frequency, and phase
   - Input application requirements
   - View matching pumps
   - Compare pump performance curves
   - Export results

## Data Sources

The application uses two main data sources:
1. Supabase database (primary)
2. CSV files (fallback)

Required CSV files:
- `Pump Selection Data.csv`: Main pump data
- `pump_curve_data_rows 1.csv`: Pump performance curves

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please contact [support email/contact].

## Acknowledgments

- Streamlit team for the amazing framework
- Plotly for interactive visualizations
- Supabase for the backend infrastructure 
