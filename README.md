A comprehensive Streamlit-based dashboard for analyzing Quality Assurance data from customer service interactions. This tool provides interactive visualizations, filtering capabilities, and performance metrics to help teams understand and improve their QA processes.
🚀 Features
✅ Interactive Filters: Filter by tone score, resolution status, intent match, and errors
✅ Real-time Metrics: KPI cards showing key performance indicators
✅ Visual Analytics: Charts for intent match rates, resolution rates, and distributions
✅ Data Export: Download filtered data as CSV
✅ Correlation Analysis: Understand relationships between metrics
✅ Responsive Design: Works on different screen sizes
📋 Requirements

Python 3.8+
Streamlit
Pandas
Plotly
Numpy

🛠️ Installation

Clone the repository

bashgit clone https://github.com/your-username/qa-analysis-dashboard.git
cd qa-analysis-dashboard

Install dependencies

bashpip install -r requirements.txt

Run the application

bashstreamlit run app.py
📁 Project Structure
qa-analysis-dashboard/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml       # Streamlit configuration
└── README.md             # Project documentation
📊 Data Requirements
Your CSV file must contain the following columns with exact names:
Column NameTypeDescriptionTranscript IDIntegerUnique identifier for each transcriptUse CaseStringType of customer service interactionIntent Matched? (Y/N)StringWhether the intent was correctly identifiedTone Natural? (1-5)IntegerNaturalness rating from 1-5Resolution Achieved? (Y/N)StringWhether the issue was resolvedMiscommunication / ErrorsStringDescription of any errors (use "None" for no errors)Comments / NotesStringAdditional observations
Sample Data Format
csvTranscript ID,Use Case,Intent Matched? (Y/N),Tone Natural? (1-5),Resolution Achieved? (Y/N),Miscommunication / Errors,Comments / Notes
1,Bill Reminder,Y,4,Y,None,Good pacing covered all points.
2,Order Tracking,Y,3,Y,Slight delay in response,Rephrase last line for clarity.
3,Account Opening,Y,5,Y,None,Excellent tone and follow-up.
🎯 Usage Instructions

Upload CSV: Use the sidebar to upload your QA analysis file
Apply Filters: Use sidebar filters to focus on specific data subsets
Analyze Charts: View performance metrics across different use cases
Export Data: Download filtered results for further analysis
Monitor KPIs: Track intent match rates, resolution rates, and tone scores

📈 Dashboard Components
Key Metrics

Intent Match Rate: Percentage of correctly identified intents
Resolution Rate: Percentage of successfully resolved issues
Average Tone Score: Mean naturalness rating
Error Rate: Percentage of interactions with errors

Visualizations

Intent Match by Use Case: Horizontal bar chart showing performance by category
Resolution Rate by Use Case: Success rates across different interaction types
Tone Score Distribution: Histogram of naturalness ratings
Success Rate vs Tone Score: Line chart showing correlation
Error Distribution: Pie chart of error types
Correlation Matrix: Heatmap showing relationships between metrics

Interactive Features

Dynamic Filtering: Real-time data filtering based on selected criteria
Data Export: Download filtered datasets as CSV
Responsive Layout: Adapts to different screen sizes
Hover Tooltips: Additional information on chart elements

⚙️ Configuration
The dashboard can be customized using the .streamlit/config.toml file:
toml[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"

[server]
maxUploadSize = 200
🚀 Deployment
Streamlit Community Cloud (Recommended)

Push your code to GitHub
Go to share.streamlit.io
Connect your GitHub account
Deploy directly from your repository

Local Development
bash# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
Other Platforms

Heroku: Add setup.sh and Procfile
AWS/GCP: Use container deployment
Railway: Direct GitHub integration

🔧 Dependencies
txtstreamlit==1.28.0
pandas==2.0.3
plotly==5.15.0
numpy==1.24.3
