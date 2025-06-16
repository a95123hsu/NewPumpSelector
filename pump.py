import streamlit as st
import pandas as pd
from datetime import datetime
import logging

# Import from our modules
from config import (
    DEFAULT_VALUES, PAGE_CONFIG, FLOW_UNIT_CONVERSIONS,
    HEAD_UNIT_CONVERSIONS, ESSENTIAL_COLUMNS, PERFORMANCE_COLUMNS,
    ELECTRICAL_COLUMNS, PHYSICAL_COLUMNS, ERROR_MESSAGES
)
from data_loader import (
    load_pump_data, load_pump_curve_data,
    validate_pump_data, validate_curve_data
)
from visualization import create_pump_curve_chart, create_comparison_chart
from translations import get_text, TRANSLATIONS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# App config
st.set_page_config(**PAGE_CONFIG)

# Initialize language in session state if not already set
if 'language' not in st.session_state:
    st.session_state.language = "English"

# Initialize pump curve selection state - FIXED
if 'selected_curve_models' not in st.session_state:
    st.session_state.selected_curve_models = []

# --- Header ---
col_logo, col_title, col_lang = st.columns([1, 5, 3])
with col_logo:
    st.image("https://www.hungpump.com/images/340357", width=160)
with col_title:
    st.markdown(f"<h1 style='color: #0057B8; margin: 0; padding-left: 15px;'>{get_text('Hung Pump')}</h1>", unsafe_allow_html=True)
with col_lang:
    # Language selector in the header
    selected_lang = st.selectbox(
        "Language / 語言",
        options=list(TRANSLATIONS.keys()),
        index=list(TRANSLATIONS.keys()).index(st.session_state.language),
        key="lang_selector"
    )
    # Update language when selector changes
    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        st.rerun()

# --- Title and Reset Button ---
st.title(get_text("Pump Selection Tool"))

# Load the data
try:
    with st.spinner(get_text("Loading Curve")):
        pumps = load_pump_data()
        curve_data = load_pump_curve_data()
        
        # Validate data
        is_valid, error_msg = validate_pump_data(pumps)
        if not is_valid:
            st.error(error_msg)
            st.stop()
            
        is_valid, error_msg = validate_curve_data(curve_data)
        if not is_valid:
            st.error(error_msg)
            st.stop()
            
except Exception as e:
    logger.error(f"Error loading data: {str(e)}")
    st.error(ERROR_MESSAGES["failed_data"].format(error=str(e)))
    st.stop()

if pumps.empty:
    st.error(get_text("No Data"))
    st.stop()

# Show data freshness information
col_data1, col_data2 = st.columns(2)
with col_data1:
    st.caption(get_text("Data loaded", n_records=len(pumps), timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
with col_data2:
    if not curve_data.empty:
        st.caption(get_text("Curve Data Loaded", count=len(curve_data)))

# Create columns with buttons close together on the left side
col1, col2, col_space = st.columns([1, 1.2, 5.8])

with col1:
    refresh_clicked = st.button(get_text("Refresh Data"), help="Refresh data from database", type="secondary", use_container_width=True)
    if refresh_clicked:
        # Clear cache to force data reload
        st.cache_data.clear()
        st.rerun()
    
with col2:
    # Reset All Inputs Button
    reset_clicked = st.button(get_text("Reset Inputs"), key="reset_button", help="Reset all fields to default", type="secondary", use_container_width=True)
    if reset_clicked:
        for key, val in DEFAULT_VALUES.items():
            st.session_state[key] = val
        # Also reset pump selection
        st.session_state.selected_curve_models = []

# Apply custom styling
st.markdown("""
<style>
button[data-testid="baseButton-secondary"] {
    background-color: #e63946;
    color: white;
    white-space: nowrap;
}
</style>
""", unsafe_allow_html=True)

# --- Step 1: Initial Selection ---
st.markdown(get_text("Step 1"))

# Clean up Category values to ensure consistent filtering
if "Category" in pumps.columns:
    # Convert all category values to strings and strip whitespace
    pumps["Category"] = pumps["Category"].astype(str).str.strip()
    # Replace NaN, None, etc. with empty string for consistent handling
    pumps["Category"] = pumps["Category"].replace(["nan", "None", "NaN"], "")
    # Get unique categories excluding blank/empty values
    unique_categories = [c for c in pumps["Category"].unique() if c and c.strip() and c.lower() not in ["nan", "none"]]
    
    # Create a mapping between translated categories and original categories
    translated_categories = []
    original_to_translated = {}
    translated_to_original = {}
    
    # First, add the "All Categories" option
    all_categories_translated = get_text("All Categories")
    translated_categories.append(all_categories_translated)
    translated_to_original[all_categories_translated] = get_text("All Categories")
    
    # Then process each category from the database
    for cat in sorted(unique_categories):
        # Get translated category if available, otherwise use the original
        translated_cat = get_text(cat)
        translated_categories.append(translated_cat)
        # Store mappings in both directions
        original_to_translated[cat] = translated_cat
        translated_to_original[translated_cat] = cat
    
    # Use translated categories for display
    category_options = translated_categories
else:
    category_options = [get_text("All Categories")]
    translated_to_original = {get_text("All Categories"): get_text("All Categories")}

# Display the translated category dropdown
category_translated = st.selectbox(get_text("Category"), category_options)

# Get the original category name for filtering
if category_translated in translated_to_original:
    category = translated_to_original[category_translated]
else:
    category = category_translated  # Fallback if translation not found

# Use "Show All Frequency" instead of "Select..." for frequency
if "Frequency (Hz)" in pumps.columns:
    pumps["Frequency (Hz)"] = pd.to_numeric(pumps["Frequency (Hz)"], errors='coerce')
    freq_options = sorted(pumps["Frequency (Hz)"].dropna().unique())
    frequency = st.selectbox(get_text("Frequency"), [get_text("Show All Frequency")] + freq_options)
else:
    frequency = st.selectbox(get_text("Frequency"), [get_text("Show All Frequency")])

# Use "Show All Phase" instead of "Select..." for phase
if "Phase" in pumps.columns:
    pumps["Phase"] = pd.to_numeric(pumps["Phase"], errors='coerce')
    phase_options = [p for p in sorted(pumps["Phase"].dropna().unique()) if p in [1, 3]]
    phase = st.selectbox(get_text("Phase"), [get_text("Show All Phase")] + phase_options)
else:
    phase = st.selectbox(get_text("Phase"), [get_text("Show All Phase"), 1, 3])

# Get all available columns from the dataset for later use in column selection
if not pumps.empty:
    # Define essential columns that are always shown
    essential_columns = ESSENTIAL_COLUMNS
    # Include all columns except DB ID
    available_columns = [col for col in pumps.columns if col not in ["DB ID"]]
    
    # Separate essential and optional columns
    optional_columns = [col for col in available_columns if col not in essential_columns]
else:
    essential_columns = []
    optional_columns = []

# --- 🏢 Application Section - Only show when Booster is selected ---
if category == "Booster":
    st.markdown(get_text("Application Input"))
    st.caption(get_text("Floor Faucet Info"))

    num_floors = st.number_input(get_text("Number of Floors"), min_value=0, step=1, key="floors")
    num_faucets = st.number_input(get_text("Number of Faucets"), min_value=0, step=1, key="faucets")
    
    # Calculate auto values for Booster application
    auto_flow = num_faucets * 15
    auto_tdh = num_floors * 3.5
else:
    # Reset these values when Booster is not selected
    auto_flow = 0
    auto_tdh = 0
    num_floors = 0
    num_faucets = 0

# --- 🌊 Pond Drainage ---
st.markdown(get_text("Pond Drainage"))

length = st.number_input(get_text("Pond Length"), min_value=0.0, step=0.1, key="length")
width = st.number_input(get_text("Pond Width"), min_value=0.0, step=0.1, key="width")
height = st.number_input(get_text("Pond Height"), min_value=0.0, step=0.1, key="height")
drain_time_hr = st.number_input(get_text("Drain Time"), min_value=0.01, step=0.1, key="drain_time_hr")

pond_volume = length * width * height * 1000
drain_time_min = drain_time_hr * 60
pond_lpm = pond_volume / drain_time_min if drain_time_min > 0 else 0

if pond_volume > 0:
    st.caption(get_text("Pond Volume", volume=round(pond_volume)))
if pond_lpm > 0:
    st.success(get_text("Required Flow", flow=round(pond_lpm)))

# --- Underground and particle size ---
underground_depth = st.number_input(get_text("Pump Depth"), min_value=0.0, step=0.1, key="underground_depth")
particle_size = st.number_input(get_text("Particle Size"), min_value=0.0, step=1.0, key="particle_size")

# --- Auto calculations ---
if category == "Booster":
    auto_flow = max(num_faucets * 15, pond_lpm)
    auto_tdh = max(num_floors * 3.5, height)
else:
    auto_flow = pond_lpm
    auto_tdh = underground_depth if underground_depth > 0 else height

# --- 🎛️ Manual Input Section ---
st.markdown(get_text("Manual Input"))

flow_unit_options = ["L/min", "L/sec", "m³/hr", "m³/min", "US gpm"]
flow_unit_translated = [get_text(unit) for unit in flow_unit_options]
flow_unit_map = dict(zip(flow_unit_translated, flow_unit_options))

flow_unit = st.radio(get_text("Flow Unit"), flow_unit_translated, horizontal=True)
flow_unit_original = flow_unit_map.get(flow_unit, "L/min")
flow_value = st.number_input(get_text("Flow Value"), min_value=0.0, step=10.0, value=float(auto_flow), key="flow_value")

head_unit_options = ["m", "ft"]
head_unit_translated = [get_text(unit) for unit in head_unit_options]
head_unit_map = dict(zip(head_unit_translated, head_unit_options))

head_unit = st.radio(get_text("Head Unit"), head_unit_translated, horizontal=True)
head_unit_original = head_unit_map.get(head_unit, "m")
head_value = st.number_input(get_text("TDH"), min_value=0.0, step=1.0, value=float(auto_tdh), key="head_value")

# --- Estimated application from manual ---
if category == "Booster":
    estimated_floors = round(head_value / 3.5) if head_value > 0 else 0
    estimated_faucets = round(flow_value / 15) if flow_value > 0 else 0

    st.markdown(get_text("Estimated Application"))
    col1, col2 = st.columns(2)
    col1.metric(get_text("Estimated Floors"), estimated_floors)
    col2.metric(get_text("Estimated Faucets"), estimated_faucets)

# --- Result Display Limit ---
st.markdown(get_text("Result Display"))

# Column Selection in Result Display Control section
if not pumps.empty and optional_columns:
    with st.expander(get_text("Column Selection"), expanded=False):
        # Create two columns for the selection interface
        col_selection_left, col_selection_right = st.columns([1, 1])
        
        with col_selection_left:
            st.caption(get_text("Essential Columns"))
            st.write(", ".join([col for col in essential_columns if col in available_columns]))
            
            # Select/Deselect All buttons
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                select_all = st.button(get_text("Select All"), key="select_all_cols", use_container_width=True)
            with col_btn2:
                deselect_all = st.button(get_text("Deselect All"), key="deselect_all_cols", use_container_width=True)
        
        with col_selection_right:
            st.caption(get_text("Select Columns"))
            
            # Initialize selected columns in session state if not exists
            if 'selected_columns' not in st.session_state:
                # Default selection - Model will be first as essential, then these optional columns
                default_selected = [
                    "Category", "Frequency (Hz)", "Phase", "Q Rated/LPM", "Head Rated/M", "Max Flow (LPM)", "Max Head (M)",
                    "Product Link"
                ]
                st.session_state.selected_columns = [col for col in default_selected if col in optional_columns]
            
            # Handle Select All / Deselect All button clicks
            if select_all:
                st.session_state.selected_columns = optional_columns.copy()
            if deselect_all:
                st.session_state.selected_columns = []
            
            # Create checkboxes for each optional column - store current state without immediate update
            current_selection = []
            for col in optional_columns:
                is_selected = col in st.session_state.selected_columns
                if st.checkbox(col, value=is_selected, key=f"col_check_{col}"):
                    current_selection.append(col)
            
            # Store the current selection in a temporary state (don't update main state yet)
            st.session_state.temp_selected_columns = current_selection
else:
    # Use the last confirmed selection from search, or default if none
    selected_optional_columns = st.session_state.get('selected_columns', [])

result_percent = st.slider(get_text("Show Percentage"), min_value=5, max_value=100, value=100, step=1)

# --- Search Logic ---
if st.button(get_text("Search")):
    # Update the column selection when search is pressed
    if 'temp_selected_columns' in st.session_state:
        st.session_state.selected_columns = st.session_state.temp_selected_columns
        selected_optional_columns = st.session_state.selected_columns
    else:
        selected_optional_columns = st.session_state.get('selected_columns', [])
    
    filtered_pumps = pumps.copy()
    
    # Handle frequency and phase filtering with "Show All" options
    try:
        # Convert types appropriately with error handling before filtering
        filtered_pumps["Frequency (Hz)"] = pd.to_numeric(filtered_pumps["Frequency (Hz)"], errors='coerce')
        filtered_pumps["Phase"] = pd.to_numeric(filtered_pumps["Phase"], errors='coerce')
        
        # Apply frequency filter - skip filtering if "Show All Frequency" is selected
        if frequency != get_text("Show All Frequency"):
            if isinstance(frequency, str):
                try:
                    freq_value = float(frequency)
                    filtered_pumps = filtered_pumps[filtered_pumps["Frequency (Hz)"] == freq_value]
                except ValueError:
                    filtered_pumps = filtered_pumps[filtered_pumps["Frequency (Hz)"] == frequency]
            else:
                filtered_pumps = filtered_pumps[filtered_pumps["Frequency (Hz)"] == frequency]
        
        # Apply phase filter - skip filtering if "Show All Phase" is selected
        if phase != get_text("Show All Phase"):
            if isinstance(phase, str):
                try:
                    phase_value = int(phase)
                    filtered_pumps = filtered_pumps[filtered_pumps["Phase"] == phase_value]
                except ValueError:
                    filtered_pumps = filtered_pumps[filtered_pumps["Phase"] == phase]
            else:
                filtered_pumps = filtered_pumps[filtered_pumps["Phase"] == int(phase)]
    except Exception as e:
        logger.error(f"Error filtering by frequency/phase: {str(e)}")
        st.error(f"Error filtering by frequency/phase: {str(e)}")

    # Apply category filter - use the original English category name for filtering
    if category != get_text("All Categories"):
        filtered_pumps = filtered_pumps[filtered_pumps["Category"] == category]

    # Convert flow to LPM
    flow_lpm = flow_value
    if flow_unit_original in FLOW_UNIT_CONVERSIONS:
        flow_lpm *= FLOW_UNIT_CONVERSIONS[flow_unit_original]

    # Convert head to meters
    head_m = head_value if head_unit_original == "m" else head_value * HEAD_UNIT_CONVERSIONS["ft"]

    # Use Q Rated/LPM and Head Rated/M instead of Max Flow and Max Head
    # Ensure numeric conversion for flow and head with improved handling
    # Replace NaN with 0 to avoid comparison issues
    filtered_pumps["Q Rated/LPM"] = pd.to_numeric(filtered_pumps["Q Rated/LPM"], errors="coerce").fillna(0)
    filtered_pumps["Head Rated/M"] = pd.to_numeric(filtered_pumps["Head Rated/M"], errors="coerce").fillna(0)

    # Apply filters with safe handling of missing values
    if flow_lpm > 0:
        filtered_pumps = filtered_pumps[filtered_pumps["Q Rated/LPM"] >= flow_lpm]
    if head_m > 0:
        filtered_pumps = filtered_pumps[filtered_pumps["Head Rated/M"] >= head_m]
    if particle_size > 0 and "Pass Solid Dia(mm)" in filtered_pumps.columns:
        # Convert to numeric first to handle potential string values
        filtered_pumps["Pass Solid Dia(mm)"] = pd.to_numeric(filtered_pumps["Pass Solid Dia(mm)"], errors="coerce").fillna(0)
        filtered_pumps = filtered_pumps[filtered_pumps["Pass Solid Dia(mm)"] >= particle_size]

    # Store filtered pumps in session state for curve visualization
    st.session_state.filtered_pumps = filtered_pumps
    st.session_state.user_flow = flow_lpm
    st.session_state.user_head = head_m
    
    # Reset pump curve selection when new search is performed
    st.session_state.selected_curve_models = []

    st.subheader(get_text("Matching Pumps"))
    st.write(get_text("Found Pumps", count=len(filtered_pumps)))

    if not filtered_pumps.empty:
        results = filtered_pumps.copy()
        
        # Sort by Q Rated/LPM and Head Rated/M for better user experience
        if "Q Rated/LPM" in results.columns and "Head Rated/M" in results.columns:
            # Properly handle data types before calculations
            results["Q Rated/LPM"] = pd.to_numeric(results["Q Rated/LPM"], errors="coerce").fillna(0)
            results["Head Rated/M"] = pd.to_numeric(results["Head Rated/M"], errors="coerce").fillna(0)
            
            # Sort by closest match to requested flow and head
            results["Flow Difference"] = abs(results["Q Rated/LPM"] - flow_lpm)
            results["Head Difference"] = abs(results["Head Rated/M"] - head_m)
            
            # Weight differences properly and handle NaN values
            results["Match Score"] = results["Flow Difference"] + results["Head Difference"]
            results = results.sort_values("Match Score")
            
            # Remove temporary columns used for sorting
            results = results.drop(columns=["Flow Difference", "Head Difference", "Match Score"])
        
        # Sort by ID first (excluding DB ID), then apply percentage filter
        if "id" in results.columns:
            results = results.sort_values("id")
        elif "ID" in results.columns:
            results = results.sort_values("ID")
        elif "Model" in results.columns:
            results = results.sort_values("Model")
        elif "Model No." in results.columns:
            results = results.sort_values("Model No.")
        
        # Apply percentage limit after sorting by ID
        max_to_show = max(1, int(len(results) * (result_percent / 100)))
        displayed_results = results.head(max_to_show).copy()
        
        # Apply column selection - build columns in logical order
        columns_to_show = []
        
        # 1. Essential identification columns first
        if "Model" in displayed_results.columns:
            columns_to_show.append("Model")
        elif "Model No." in displayed_results.columns:
            columns_to_show.append("Model No.")
        
        # Add other essential columns (id, ID) - excluding DB ID
        for col in essential_columns:
            if col in displayed_results.columns and col not in columns_to_show and col not in ["DB ID"]:
                columns_to_show.append(col)
        
        # 2. Category (if selected)
        if "Category" in selected_optional_columns and "Category" in displayed_results.columns:
            columns_to_show.append("Category")
        
        # 3. Performance specifications (if selected)
        for col in PERFORMANCE_COLUMNS:
            if col in selected_optional_columns and col in displayed_results.columns and col not in columns_to_show:
                columns_to_show.append(col)
        
        # 4. Electrical specifications (if selected)
        for col in ELECTRICAL_COLUMNS:
            if col in selected_optional_columns and col in displayed_results.columns and col not in columns_to_show:
                columns_to_show.append(col)
        
        # 5. Physical specifications (if selected)
        for col in PHYSICAL_COLUMNS:
            if col in selected_optional_columns and col in displayed_results.columns and col not in columns_to_show:
                columns_to_show.append(col)
        
        # 6. Other selected columns (excluding Product Link for now)
        for col in selected_optional_columns:
            if col in displayed_results.columns and col not in columns_to_show and col != "Product Link":
                columns_to_show.append(col)
        
        # 7. Product Link always last (if selected)
        if "Product Link" in selected_optional_columns and "Product Link" in displayed_results.columns:
            columns_to_show.append("Product Link")
        
        # If no columns selected, show a message
        if not columns_to_show:
            st.warning("⚠️ No columns selected for display. Please select at least one column from the Column Selection section above.")
        else:
            # Filter the dataframe to only show selected columns (ensuring DB ID is excluded)
            displayed_results = displayed_results[columns_to_show]
            
            # Display the results
            st.write(get_text("Matching Results"))
            
            # Show information about displayed results and columns
            if len(displayed_results) > 0:
                st.write(get_text("Showing Results", count=len(displayed_results)))
                st.caption(f"📋 Displaying {len(displayed_results.columns)} columns: {', '.join(displayed_results.columns[:5])}{'...' if len(displayed_results.columns) > 5 else ''}")
                st.info(get_text("Select Pumps"))
            
            # Create column configuration for product links and proper formatting
            column_config = {}
            
            # Configure the ID column for default sorting if it exists (excluding DB ID)
            if "id" in displayed_results.columns:
                column_config["id"] = st.column_config.NumberColumn(
                    "ID",
                    help="ID",
                    format="%d"
                )
            elif "ID" in displayed_results.columns:
                column_config["ID"] = st.column_config.NumberColumn(
                    "ID",
                    help="ID",
                    format="%d"
                )
            
            # Configure the Product Link column if it exists
            if "Product Link" in displayed_results.columns:
                column_config["Product Link"] = st.column_config.LinkColumn(
                    "Product Link",
                    help="Click to view product details",
                    display_text=get_text("View Product")
                )
            
            # Better formatting for Q Rated/LPM and Head Rated/M columns
            if "Q Rated/LPM" in displayed_results.columns:
                flow_label = get_text("Q Rated/LPM")
                flow_help = get_text("Rated flow rate in liters per minute")
                column_config["Q Rated/LPM"] = st.column_config.NumberColumn(
                    flow_label,
                    help=flow_help,
                    format="%.1f LPM"
                )
            
            if "Head Rated/M" in displayed_results.columns:
                head_label = get_text("Head Rated/M")
                head_help = get_text("Rated head in meters")
                column_config["Head Rated/M"] = st.column_config.NumberColumn(
                    head_label,
                    help=head_help,
                    format="%.1f m"
                )
            
            # Configure other numeric columns with proper formatting
            if "Max Flow (LPM)" in displayed_results.columns:
                column_config["Max Flow (LPM)"] = st.column_config.NumberColumn(
                    "Max Flow (LPM)",
                    help="Maximum flow rate in liters per minute",
                    format="%.1f LPM"
                )
            
            if "Max Head (M)" in displayed_results.columns:
                column_config["Max Head (M)"] = st.column_config.NumberColumn(
                    "Max Head (M)",
                    help="Maximum head in meters",
                    format="%.1f m"
                )
            
            # Add checkbox column for selection
            model_column = "Model" if "Model" in displayed_results.columns else "Model No."
            
            # Create a copy with checkbox column
            display_df = displayed_results.copy()
            
            # Add selection column at the beginning
            display_df.insert(0, "Select", False)
            
            # Configure checkbox column
            column_config["Select"] = st.column_config.CheckboxColumn(
                "Select",
                help="Select pumps to view performance curves",
                default=False,
            )
            
            # Display the dataframe with checkboxes
            edited_df = st.data_editor(
                display_df,
                column_config=column_config,
                hide_index=True,
                use_container_width=True,
                num_rows="fixed",
                disabled=[col for col in columns_to_show if col != "Select"],  # Only enable Select column
                key="pump_selection_table"
            )
            
            # Get selected pumps
            if "Select" in edited_df.columns:
                selected_rows = edited_df[edited_df["Select"] == True]
                if not selected_rows.empty and model_column in selected_rows.columns:
                    selected_models = selected_rows[model_column].tolist()
                    st.session_state.selected_curve_models = selected_models
            
            # Alternative approach with multiselect below table
            st.markdown("---")
            
            # Check which models have curve data available
            if model_column in displayed_results.columns:
                available_models = displayed_results[model_column].dropna().unique().tolist()
                curve_models = curve_data["Model No."].dropna().unique()
                models_with_curves = [model for model in available_models if model in curve_models]
                
                if models_with_curves:
                    # Create multiselect for pump selection
                    selected_models_multi = st.multiselect(
                        get_text("Select Pumps for Curves"),
                        models_with_curves,
                        default=st.session_state.get('selected_curve_models', []),
                        help="You can select multiple pumps to compare their curves",
                        key="pump_curve_multiselect"
                    )
                    
                    # Update session state without rerun
                    if selected_models_multi != st.session_state.selected_curve_models:
                        st.session_state.selected_curve_models = selected_models_multi
                else:
                    st.info("ℹ️ No curve data available for the pumps in your search results.")
    else:
        st.warning(get_text("No Matches"))

# --- PUMP CURVE VISUALIZATION SECTION ---
# Only show curve section if we have search results and curve data
if not curve_data.empty and 'filtered_pumps' in st.session_state and not st.session_state.filtered_pumps.empty:
    # Check if we have selected models
    if 'selected_curve_models' in st.session_state and st.session_state.selected_curve_models:
        st.markdown(get_text("Pump Curves"))
        
        # Show selected pumps info
        selected_count = len(st.session_state.selected_curve_models)
        st.success(get_text("Selected Pumps", count=selected_count))
        
        # Get user flow and head values
        user_flow = st.session_state.get('user_flow', 0)
        user_head = st.session_state.get('user_head', 0)
        
        # Check which selected models have curve data
        available_curve_models = []
        for model in st.session_state.selected_curve_models:
            if model in curve_data["Model No."].values:
                available_curve_models.append(model)
        
        if available_curve_models:
            if len(available_curve_models) == 1:
                # Show single pump curve
                st.subheader(get_text("Performance Curve", model=available_curve_models[0]))
                with st.spinner(get_text("Loading Curve")):
                    try:
                        fig = create_pump_curve_chart(curve_data, available_curve_models[0], user_flow, user_head)
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.warning(get_text("No Curve Data"))
                    except Exception as e:
                        logger.error(f"Error creating pump curve: {str(e)}")
                        st.error(f"Error creating pump curve: {str(e)}")
                        
            elif len(available_curve_models) > 1:
                # Show comparison chart
                st.subheader(get_text("Multiple Curves"))
                st.caption(f"Comparing: {', '.join(available_curve_models)}")
                with st.spinner(get_text("Loading Comparison")):
                    try:
                        fig_comp = create_comparison_chart(curve_data, available_curve_models, user_flow, user_head)
                        if fig_comp:
                            st.plotly_chart(fig_comp, use_container_width=True)
                    except Exception as e:
                        logger.error(f"Error creating comparison chart: {str(e)}")
                        st.error(f"Error creating comparison chart: {str(e)}")
            
            # Show individual curves for each pump when multiple are selected
            if len(available_curve_models) > 1:
                with st.expander("View Individual Pump Curves", expanded=False):
                    for model in available_curve_models:
                        st.subheader(get_text("Performance Curve", model=model))
                        try:
                            fig = create_pump_curve_chart(curve_data, model, user_flow, user_head)
                            if fig:
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.warning(get_text("No Curve Data"))
                        except Exception as e:
                            logger.error(f"Error creating curve for {model}: {str(e)}")
                            st.error(f"Error creating curve for {model}: {str(e)}")
        else:
            st.warning("The selected pumps do not have curve data available.")
    else:
        # Show message to select pumps from the table
        st.info(get_text("Charts Update Info"))
