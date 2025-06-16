import plotly.graph_objects as go
import pandas as pd
from typing import Optional, List
from config import CHART_COLORS, ERROR_MESSAGES
import logging

logger = logging.getLogger(__name__)

def create_pump_curve_chart(
    curve_data: pd.DataFrame,
    model_no: str,
    user_flow: Optional[float] = None,
    user_head: Optional[float] = None
) -> Optional[go.Figure]:
    """
    Create an interactive pump curve chart using Plotly.
    
    Args:
        curve_data (pd.DataFrame): Pump curve data
        model_no (str): Model number of the pump
        user_flow (Optional[float]): User's flow rate
        user_head (Optional[float]): User's head value
    
    Returns:
        Optional[go.Figure]: Plotly figure object or None if error
    """
    try:
        # Extract head columns (columns ending with 'M')
        head_columns = [col for col in curve_data.columns if col.endswith('M') and col not in ['Max Head(M)']]
        
        # Extract pressure columns (columns with 'Kg/cm²')
        pressure_columns = [col for col in curve_data.columns if 'Kg/cm²' in col]
        
        fig = go.Figure()
        
        # Find the pump data
        pump_data = curve_data[curve_data['Model No.'] == model_no]
        
        if pump_data.empty:
            logger.warning(f"No data found for model {model_no}")
            return None
        
        pump_row = pump_data.iloc[0]
        
        # Create head-flow curve
        if head_columns:
            flows = []
            heads = []
            
            for col in head_columns:
                try:
                    head_value = float(col.replace('M', ''))
                    flow_value = pd.to_numeric(pump_row[col], errors='coerce')
                    if not pd.isna(flow_value) and flow_value > 0:
                        flows.append(flow_value)
                        heads.append(head_value)
                except Exception as e:
                    logger.warning(f"Error processing column {col}: {str(e)}")
                    continue
            
            if flows and heads:
                # Sort by flow for proper curve
                sorted_data = sorted(zip(flows, heads))
                flows, heads = zip(*sorted_data)
                
                fig.add_trace(go.Scatter(
                    x=flows,
                    y=heads,
                    mode='lines+markers',
                    name=f'{model_no} - Head Curve',
                    line=dict(color='blue', width=3),
                    marker=dict(size=8)
                ))
        
        # Add pressure curves if available
        if pressure_columns:
            for i, col in enumerate(pressure_columns[:3]):  # Limit to 3 pressure curves
                try:
                    pressure_value = float(col.split('Kg/cm²')[0])
                    flow_value = pd.to_numeric(pump_row[col], errors='coerce')
                    if not pd.isna(flow_value) and flow_value > 0:
                        fig.add_trace(go.Scatter(
                            x=[flow_value],
                            y=[pressure_value * 10],  # Convert kg/cm² to approximate meters
                            mode='markers',
                            name=f'{pressure_value} Kg/cm²',
                            marker=dict(size=10, symbol='diamond')
                        ))
                except Exception as e:
                    logger.warning(f"Error processing pressure column {col}: {str(e)}")
                    continue
        
        # Add user operating point if provided
        if user_flow and user_head and user_flow > 0 and user_head > 0:
            fig.add_trace(go.Scatter(
                x=[user_flow],
                y=[user_head],
                mode='markers',
                name='Operating Point',
                marker=dict(size=15, color='red', symbol='star'),
                hovertemplate=f'Flow: {user_flow} LPM<br>Head: {user_head} M<extra></extra>'
            ))
        
        # Update layout
        fig.update_layout(
            title=f'Performance Curve - {model_no}',
            xaxis_title='Flow Rate (LPM)',
            yaxis_title='Head (M)',
            hovermode='closest',
            showlegend=True,
            height=500,
            template='plotly_white'
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Error creating pump curve chart: {str(e)}")
        return None

def create_comparison_chart(
    curve_data: pd.DataFrame,
    model_nos: List[str],
    user_flow: Optional[float] = None,
    user_head: Optional[float] = None
) -> Optional[go.Figure]:
    """
    Create a comparison chart for multiple pumps.
    
    Args:
        curve_data (pd.DataFrame): Pump curve data
        model_nos (List[str]): List of model numbers to compare
        user_flow (Optional[float]): User's flow rate
        user_head (Optional[float]): User's head value
    
    Returns:
        Optional[go.Figure]: Plotly figure object or None if error
    """
    try:
        fig = go.Figure()
        
        for i, model_no in enumerate(model_nos):
            pump_data = curve_data[curve_data['Model No.'] == model_no]
            
            if pump_data.empty:
                logger.warning(f"No data found for model {model_no}")
                continue
                
            pump_row = pump_data.iloc[0]
            color = CHART_COLORS[i % len(CHART_COLORS)]
            
            # Extract head columns
            head_columns = [col for col in curve_data.columns if col.endswith('M') and col not in ['Max Head(M)']]
            
            flows = []
            heads = []
            
            for col in head_columns:
                try:
                    head_value = float(col.replace('M', ''))
                    flow_value = pd.to_numeric(pump_row[col], errors='coerce')
                    if not pd.isna(flow_value) and flow_value > 0:
                        flows.append(flow_value)
                        heads.append(head_value)
                except Exception as e:
                    logger.warning(f"Error processing column {col}: {str(e)}")
                    continue
            
            if flows and heads:
                # Sort by flow for proper curve
                sorted_data = sorted(zip(flows, heads))
                flows, heads = zip(*sorted_data)
                
                fig.add_trace(go.Scatter(
                    x=flows,
                    y=heads,
                    mode='lines+markers',
                    name=model_no,
                    line=dict(color=color, width=3),
                    marker=dict(size=6)
                ))
        
        # Add user operating point if provided
        if user_flow and user_head and user_flow > 0 and user_head > 0:
            fig.add_trace(go.Scatter(
                x=[user_flow],
                y=[user_head],
                mode='markers',
                name='Operating Point',
                marker=dict(size=15, color='red', symbol='star'),
                hovertemplate=f'Flow: {user_flow} LPM<br>Head: {user_head} M<extra></extra>'
            ))
        
        # Update layout
        fig.update_layout(
            title='Performance Comparison',
            xaxis_title='Flow Rate (LPM)',
            yaxis_title='Head (M)',
            hovermode='closest',
            showlegend=True,
            height=500,
            template='plotly_white'
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Error creating comparison chart: {str(e)}")
        return None 