import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Set page config
st.set_page_config(
    page_title="QA Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("📊 QA Analysis Dashboard")
st.markdown("Upload your QA analysis CSV file to visualize insights and performance metrics.")

# Sidebar for file upload
st.sidebar.header("Upload Data")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        
        # Clean column names (strip whitespace)
        df.columns = df.columns.str.strip()
        
        # Display basic info
        st.sidebar.success(f"✅ File uploaded successfully!")
        st.sidebar.info(f"Total records: {len(df)}")
        
        # Main dashboard
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            intent_match_rate = (df['Intent Matched? (Y/N)'] == 'Y').mean() * 100
            st.metric("Intent Match Rate", f"{intent_match_rate:.1f}%")
        
        with col2:
            resolution_rate = (df['Resolution Achieved? (Y/N)'] == 'Y').mean() * 100
            st.metric("Resolution Rate", f"{resolution_rate:.1f}%")
        
        with col3:
            avg_tone = df['Tone Natural? (1-5)'].mean()
            st.metric("Avg Tone Score", f"{avg_tone:.1f}/5")
        
        with col4:
            error_rate = (df['Miscommunication / Errors'] != 'None').mean() * 100
            st.metric("Error Rate", f"{error_rate:.1f}%")
        
        # Filters
        st.sidebar.header("Filters")
        
        # Tone filter
        tone_filter = st.sidebar.slider(
            "Minimum Tone Score",
            min_value=1,
            max_value=5,
            value=1,
            help="Filter records by minimum tone score"
        )
        
        # Resolution filter
        resolution_filter = st.sidebar.selectbox(
            "Resolution Status",
            ["All", "Achieved", "Not Achieved"],
            help="Filter by resolution status"
        )
        
        # Intent match filter
        intent_filter = st.sidebar.selectbox(
            "Intent Match Status",
            ["All", "Matched", "Not Matched"],
            help="Filter by intent match status"
        )
        
        # Error filter
        error_filter = st.sidebar.selectbox(
            "Error Status",
            ["All", "No Errors", "Has Errors"],
            help="Filter by error presence"
        )
        
        # Apply filters
        filtered_df = df.copy()
        
        # Apply tone filter
        filtered_df = filtered_df[filtered_df['Tone Natural? (1-5)'] >= tone_filter]
        
        # Apply resolution filter
        if resolution_filter == "Achieved":
            filtered_df = filtered_df[filtered_df['Resolution Achieved? (Y/N)'] == 'Y']
        elif resolution_filter == "Not Achieved":
            filtered_df = filtered_df[filtered_df['Resolution Achieved? (Y/N)'] == 'N']
        
        # Apply intent filter
        if intent_filter == "Matched":
            filtered_df = filtered_df[filtered_df['Intent Matched? (Y/N)'] == 'Y']
        elif intent_filter == "Not Matched":
            filtered_df = filtered_df[filtered_df['Intent Matched? (Y/N)'] == 'N']
        
        # Apply error filter
        if error_filter == "No Errors":
            filtered_df = filtered_df[filtered_df['Miscommunication / Errors'] == 'None']
        elif error_filter == "Has Errors":
            filtered_df = filtered_df[filtered_df['Miscommunication / Errors'] != 'None']
        
        st.sidebar.info(f"Filtered records: {len(filtered_df)}")
        
        # Charts section
        st.header("📈 Analytics")
        
        # Create two columns for charts
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            # Intent Match Rate by Use Case
            st.subheader("Intent Match by Use Case")
            intent_by_usecase = filtered_df.groupby('Use Case')['Intent Matched? (Y/N)'].apply(
                lambda x: (x == 'Y').mean() * 100
            ).sort_values(ascending=False)
            
            fig_intent = px.bar(
                x=intent_by_usecase.values,
                y=intent_by_usecase.index,
                orientation='h',
                title="Intent Match Rate by Use Case (%)",
                labels={'x': 'Match Rate (%)', 'y': 'Use Case'},
                color=intent_by_usecase.values,
                color_continuous_scale='RdYlGn'
            )
            fig_intent.update_layout(height=500)
            st.plotly_chart(fig_intent, use_container_width=True)
        
        with chart_col2:
            # Resolution Rate by Use Case
            st.subheader("Resolution Rate by Use Case")
            resolution_by_usecase = filtered_df.groupby('Use Case')['Resolution Achieved? (Y/N)'].apply(
                lambda x: (x == 'Y').mean() * 100
            ).sort_values(ascending=False)
            
            fig_resolution = px.bar(
                x=resolution_by_usecase.values,
                y=resolution_by_usecase.index,
                orientation='h',
                title="Resolution Rate by Use Case (%)",
                labels={'x': 'Resolution Rate (%)', 'y': 'Use Case'},
                color=resolution_by_usecase.values,
                color_continuous_scale='RdYlGn'
            )
            fig_resolution.update_layout(height=500)
            st.plotly_chart(fig_resolution, use_container_width=True)
        
        # Tone distribution
        st.subheader("Tone Score Distribution")
        tone_counts = filtered_df['Tone Natural? (1-5)'].value_counts().sort_index()
        
        fig_tone = px.bar(
            x=tone_counts.index,
            y=tone_counts.values,
            title="Distribution of Tone Scores",
            labels={'x': 'Tone Score', 'y': 'Count'},
            color=tone_counts.values,
            color_continuous_scale='Viridis'
        )
        fig_tone.update_xaxis(tickmode='linear', dtick=1)
        st.plotly_chart(fig_tone, use_container_width=True)
        
        # Performance overview
        st.subheader("Performance Overview")
        
        # Create metrics summary
        perf_col1, perf_col2 = st.columns(2)
        
        with perf_col1:
            # Success rate by tone score
            st.write("**Success Rate by Tone Score**")
            success_by_tone = filtered_df.groupby('Tone Natural? (1-5)')['Resolution Achieved? (Y/N)'].apply(
                lambda x: (x == 'Y').mean() * 100
            )
            
            fig_success_tone = px.line(
                x=success_by_tone.index,
                y=success_by_tone.values,
                title="Success Rate vs Tone Score",
                labels={'x': 'Tone Score', 'y': 'Success Rate (%)'},
                markers=True
            )
            fig_success_tone.update_xaxis(tickmode='linear', dtick=1)
            st.plotly_chart(fig_success_tone, use_container_width=True)
        
        with perf_col2:
            # Error analysis
            st.write("**Error Analysis**")
            error_summary = filtered_df['Miscommunication / Errors'].value_counts()
            
            fig_errors = px.pie(
                values=error_summary.values,
                names=error_summary.index,
                title="Error Distribution"
            )
            st.plotly_chart(fig_errors, use_container_width=True)
        
        # Data table
        st.header("📋 Detailed Data")
        
        # Display options
        show_all = st.checkbox("Show all columns", value=False)
        
        if show_all:
            st.dataframe(filtered_df, use_container_width=True)
        else:
            # Show key columns
            key_columns = ['Transcript ID', 'Use Case', 'Intent Matched? (Y/N)', 
                          'Tone Natural? (1-5)', 'Resolution Achieved? (Y/N)', 
                          'Miscommunication / Errors']
            st.dataframe(filtered_df[key_columns], use_container_width=True)
        
        # Export filtered data
        st.subheader("Export Data")
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download filtered data as CSV",
            data=csv,
            file_name="filtered_qa_analysis.csv",
            mime="text/csv"
        )
        
        # Summary insights
        st.header("🔍 Key Insights")
        
        insights_col1, insights_col2 = st.columns(2)
        
        with insights_col1:
            st.write("**Top Performing Use Cases:**")
            top_performers = resolution_by_usecase.head(5)
            for use_case, rate in top_performers.items():
                st.write(f"• {use_case}: {rate:.1f}%")
        
        with insights_col2:
            st.write("**Areas for Improvement:**")
            bottom_performers = resolution_by_usecase.tail(5)
            for use_case, rate in bottom_performers.items():
                st.write(f"• {use_case}: {rate:.1f}%")
        
        # Correlation analysis
        st.subheader("Correlation Analysis")
        
        # Create correlation matrix
        df_numeric = filtered_df.copy()
        df_numeric['Intent_Match_Numeric'] = (df_numeric['Intent Matched? (Y/N)'] == 'Y').astype(int)
        df_numeric['Resolution_Numeric'] = (df_numeric['Resolution Achieved? (Y/N)'] == 'Y').astype(int)
        df_numeric['Has_Error'] = (df_numeric['Miscommunication / Errors'] != 'None').astype(int)
        
        corr_cols = ['Tone Natural? (1-5)', 'Intent_Match_Numeric', 'Resolution_Numeric', 'Has_Error']
        corr_matrix = df_numeric[corr_cols].corr()
        
        fig_corr = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="Correlation Matrix",
            labels=dict(color="Correlation"),
            color_continuous_scale='RdBu'
        )
        st.plotly_chart(fig_corr, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        st.info("Please make sure your CSV file has the correct format and column names.")

else:
    st.info("👆 Please upload a CSV file to begin analysis.")
    
    # Show expected format
    st.subheader("Expected CSV Format")
    st.code("""
    Transcript ID,Use Case,Intent Matched? (Y/N),Tone Natural? (1-5),Resolution Achieved? (Y/N),Miscommunication / Errors,Comments / Notes
    1,Bill Reminder,Y,4,Y,None,Good pacing covered all points.
    2,Order Tracking,Y,3,Y,Slight delay in response,Rephrase last line for clarity.
    ...
    """)