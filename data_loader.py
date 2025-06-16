import pandas as pd
from supabase import create_client
import logging
from typing import Optional, Tuple
from config import SUPABASE_URL, SUPABASE_KEY, DATA_LOADING, ERROR_MESSAGES

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_supabase_client():
    """Initialize Supabase client with error handling."""
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {str(e)}")
        raise

def load_pump_data() -> pd.DataFrame:
    """
    Load pump data from Supabase with pagination and fallback to CSV.
    Returns:
        pd.DataFrame: Loaded pump data
    """
    try:
        supabase = init_supabase_client()
        all_records = []
        page_size = DATA_LOADING["page_size"]
        current_page = 0
        
        while True:
            response = supabase.table("pump_selection_data").select("*") \
                              .range(current_page * page_size, (current_page + 1) * page_size - 1) \
                              .execute()
            
            if not response.data:
                break
                
            all_records.extend(response.data)
            current_page += 1
            
            if len(response.data) < page_size:
                break
        
        df = pd.DataFrame(all_records)
        logger.info(f"Successfully loaded {len(df)} pump records from Supabase")
        return df
        
    except Exception as e:
        logger.error(f"Failed to load data from Supabase: {str(e)}")
        # Fallback to CSV
        try:
            df = pd.read_csv("Pump Selection Data.csv")
            logger.info(f"Successfully loaded {len(df)} pump records from CSV")
            return df
        except Exception as csv_error:
            logger.error(f"Failed to load CSV file: {str(csv_error)}")
            return pd.DataFrame()

def load_pump_curve_data() -> pd.DataFrame:
    """
    Load pump curve data from Supabase with pagination and fallback to CSV.
    Returns:
        pd.DataFrame: Loaded pump curve data
    """
    try:
        supabase = init_supabase_client()
        all_records = []
        page_size = DATA_LOADING["page_size"]
        current_page = 0
        
        while True:
            response = supabase.table("pump_curve_data").select("*") \
                              .range(current_page * page_size, (current_page + 1) * page_size - 1) \
                              .execute()
            
            if not response.data:
                break
                
            all_records.extend(response.data)
            current_page += 1
            
            if len(response.data) < page_size:
                break
        
        df = pd.DataFrame(all_records)
        logger.info(f"Successfully loaded {len(df)} curve records from Supabase")
        return df
        
    except Exception as e:
        logger.error(f"Failed to load curve data from Supabase: {str(e)}")
        # Fallback to CSV
        try:
            df = pd.read_csv("pump_curve_data_rows 1.csv")
            logger.info(f"Successfully loaded {len(df)} curve records from CSV")
            return df
        except Exception as csv_error:
            logger.error(f"Failed to load curve CSV file: {str(csv_error)}")
            return pd.DataFrame()

def validate_pump_data(df: pd.DataFrame) -> Tuple[bool, Optional[str]]:
    """
    Validate pump data for required columns and data types.
    Args:
        df (pd.DataFrame): Pump data to validate
    Returns:
        Tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    required_columns = ["Model", "Q Rated/LPM", "Head Rated/M"]
    
    # Check for required columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
    
    # Check data types
    try:
        df["Q Rated/LPM"] = pd.to_numeric(df["Q Rated/LPM"], errors="coerce")
        df["Head Rated/M"] = pd.to_numeric(df["Head Rated/M"], errors="coerce")
    except Exception as e:
        return False, f"Error converting data types: {str(e)}"
    
    return True, None

def validate_curve_data(df: pd.DataFrame) -> Tuple[bool, Optional[str]]:
    """
    Validate pump curve data for required columns and data types.
    Args:
        df (pd.DataFrame): Curve data to validate
    Returns:
        Tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    required_columns = ["Model No."]
    
    # Check for required columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
    
    return True, None 