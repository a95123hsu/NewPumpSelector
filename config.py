import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Default Values
DEFAULT_VALUES = {
    "floors": 0,
    "faucets": 0,
    "length": 0.0,
    "width": 0.0,
    "height": 0.0,
    "drain_time_hr": 0.01,
    "underground_depth": 0.0,
    "particle_size": 0.0,
    "flow_value": 0.0,
    "head_value": 0.0
}

# Flow Unit Conversions
FLOW_UNIT_CONVERSIONS = {
    "L/sec": 60,
    "m³/hr": 1000/60,
    "m³/min": 1000,
    "US gpm": 3.785
}

# Head Unit Conversions
HEAD_UNIT_CONVERSIONS = {
    "ft": 0.3048  # Convert feet to meters
}

# Essential Columns
ESSENTIAL_COLUMNS = ["id", "ID", "Model", "Model No."]

# Performance Columns
PERFORMANCE_COLUMNS = ["Q Rated/LPM", "Head Rated/M", "Max Flow (LPM)", "Max Head (M)"]

# Electrical Columns
ELECTRICAL_COLUMNS = ["Frequency (Hz)", "Phase"]

# Physical Columns
PHYSICAL_COLUMNS = ["Pass Solid Dia(mm)", "HP", "Power(KW)", "Outlet (mm)", "Outlet (inch)"]

# Error Messages
ERROR_MESSAGES = {
    "no_data": "No pump data available. Please check your connection.",
    "invalid_input": "Please enter valid values for all required fields.",
    "failed_connection": "Failed to connect to database: {error}",
    "failed_data": "Failed to load data: {error}",
    "no_curve_data": "No curve data available for this pump model",
    "invalid_selection": "Please select at least one pump to view curves"
}

# Chart Colors
CHART_COLORS = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']

# Page Configuration
PAGE_CONFIG = {
    "page_title": "Pump Selector",
    "layout": "wide"
}

# Data Loading Configuration
DATA_LOADING = {
    "page_size": 1000,
    "cache_ttl": 60  # seconds
} 