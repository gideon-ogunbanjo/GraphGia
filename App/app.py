# Libraires
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import io
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from wordcloud import wordcloud
import streamlit.components.v1 as components
from tempfile import NamedTemporaryFile

# Main Function
def main():
    st.sidebar.title("GraphGia - Data Cleaning & Exploration Tool")
    st.sidebar.write(
        "GraphGia is a tool for Data Cleaning, Visualization, and Exploratory Data Analysis."
    )
    st.sidebar.write("🫶")
    app_mode = st.sidebar.selectbox(
        "Choose the app mode", ["GraphGia", "EDA Dashboard"]
    )

    if app_mode == "GraphGia":
        graphgia()
    elif app_mode == "EDA Dashboard":
        eda_dashboard()



# Data Cleaning Function
def clean_data(data):
    st.subheader("Data Cleaning")

    # Remove Null Values
    data = data.dropna()

    # Remove Duplicate Values
    data = data.drop_duplicates()

    # Label Encoding for Categorical Columns
    categorical_columns = data.select_dtypes(include=["object"]).columns
    label_encoder = LabelEncoder()
    for col in categorical_columns:
        data[col] = label_encoder.fit_transform(data[col])

    st.write("Null and Duplicate Values Removed.")
    st.write("Data Cleaned Successfully!")
    return data

# Data Export Function
def export_data(data, file_format, encoded=False):
    if encoded:
        if file_format == "CSV":
            # Export to CSV
            csv_file = data.to_csv(index=False)
            st.download_button(
                label="Download Clean Encoded CSV",
                data=csv_file,
                file_name="encoded_data.csv",
                mime="text/csv",
            )
        else:
            st.write("An error occurred")
    else:
        if file_format == "CSV":
            # Export to CSV
            csv_file = data.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv_file,
                file_name="exported_data.csv",
                mime="text/csv",
            )
        else:
            st.write("An error occurred")

# Function for Ordinal Encoding of Yes/No Columns
def ordinal_encode_yes_no(data, column_name):
    data[column_name] = data[column_name].map({"No": 0, "Yes": 1})
    return data

# GraphGia
def graphgia():
    st.set_option("deprecation.showPyplotGlobalUse", False)
    st.title("GraphGia - Data Cleaning & Exploration Tool")
    st.write("This is a data cleaning & exploration tool.")

    # File Uploader Widget
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        if uploaded_file.name.endswith("csv"):
            data = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith("xlsx"):
            data = pd.read_excel(uploaded_file, engine="openpyxl")
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")

        st.write("Uploaded Data:", data)

        # Additional Information Button - Data Description
        if st.button("Show Extended Dataset Information"):
            st.subheader("Dataset Description")
            description = data.describe()
            st.write(description)

        # Cleaning Section
        st.subheader("Data Cleaning")
        if st.button("Clean Data"):
            data = clean_data(data)

        # Encoding Section
        st.subheader("Encoding Section")
        selected_column = st.selectbox("Select a column to encode:", data.columns)
        encode_method = st.radio("Select encoding method:", ["Label Encoding", "One-Hot Encoding", "Ordinal Encoding"])

        if st.button("Encode Column"):
            if encode_method == "Label Encoding":
                label_encoder = LabelEncoder()
                data[selected_column] = label_encoder.fit_transform(data[selected_column])
                st.write(f'{selected_column} Encoded Successfully using Label Encoding')
            elif encode_method == "One-Hot Encoding":
                data = pd.get_dummies(data, columns=[selected_column])
                st.write(f'{selected_column} Encoded Successfully using One-Hot Encoding')
            elif encode_method == "Ordinal Encoding":
                data = ordinal_encode_yes_no(data, selected_column)
                st.write(f'{selected_column} Encoded Successfully using Ordinal Encoding (Yes/No to 0/1)')

        # Data Export Section
        if st.button("Export Cleaned & Encoded Data"):
            st.subheader("Data Export")
            export_format = st.radio("Select export format:", ["CSV"])
            export_data(data, export_format, encoded=True)


# EDA Dashboard
def eda_dashboard():
    st.title("EDA Dashboard")
    st.write("This is an exploratory data analysis dashboard. Upload your datasets and visualize your data interactively!")

    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        st.write("Dataset Statistics:")
        st.write(df.describe())

        # Checkbox for user-selected visualizations
        st.sidebar.title("Select Visualizations")
        histogram = st.sidebar.checkbox("Histogram")
        scatter_plot = st.sidebar.checkbox("Scatter Plot")
        correlation_matrix = st.sidebar.checkbox("Correlation Matrix")
        bar_chart = st.sidebar.checkbox("Bar Chart")
        scatter_matrix = st.sidebar.checkbox("Scatter Matrix")
        box_plot = st.sidebar.checkbox("Box Plot")
        pair_plot = st.sidebar.checkbox("Pair Plot")
        count_plot = st.sidebar.checkbox("Count Plot")
        dist_plot = st.sidebar.checkbox("Distribution Plot")
        pie_chart = st.sidebar.checkbox("Pie Chart")
        time_series = st.sidebar.checkbox("Time Series Plot")
        violin_plot = st.sidebar.checkbox("Violin Plot")

        # Histogram
        if histogram:
            st.subheader("Histogram")
            column = st.selectbox("Select a column for the histogram", df.columns)
            plt.hist(df[column], bins=20, edgecolor="k")
            st.pyplot()

            # Generated Histogram Code
            st.write("**Generated Histogram Code:**")
            hist_code = f"""
            import matplotlib.pyplot as plt
            column = '{column}'
            plt.hist(df[column], bins=20, edgecolor='k')
            plt.xlabel('{column}')
            plt.ylabel('Frequency')
            plt.title('Histogram of {column}')
            plt.show()
            """
            st.code(hist_code, language="python")

        # Scatter Plot
        if scatter_plot:
            st.subheader("Scatter Plot")
            x_column = st.selectbox("Select X-axis column", df.columns)
            y_column = st.selectbox("Select Y-axis column", df.columns)
            plt.scatter(df[x_column], df[y_column])
            plt.xlabel(x_column)
            plt.ylabel(y_column)
            st.pyplot()

            # Generated Scatter Plot Code
            st.write("**Generated Scatter Plot Code:**")
            scatter_code = f"""
            import matplotlib.pyplot as plt
            x_column = '{x_column}'
            y_column = '{y_column}'
            plt.scatter(df[x_column], df[y_column])
            plt.xlabel('{x_column}')
            plt.ylabel('{y_column}')
            plt.title('Scatter Plot: {x_column} vs {y_column}')
            plt.show()
            """
            st.code(scatter_code, language="python")

        # Correlation Matrix
        if correlation_matrix:
            st.subheader("Correlation Matrix")
            corr_matrix = df.corr()
            plt.figure(figsize=(10, 8))
            sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", center=0)
            st.pyplot()

            # Generated Correlation Matrix Code
            st.write("**Generated Correlation Matrix Code**")
            corr_code = f"""
            import seaborn as sns
            import matplotlib.pyplot as plt
            corr_matrix = df.corr()
            plt.figure(figsize=(10, 8))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
            plt.title('Correlation Matrix')
            plt.show()
            """
            st.code(corr_code, language="python")

        # Bar Chart
        if bar_chart:
            st.subheader("Bar Chart")
            bar_column = st.selectbox("Select a column for the bar chart", df.columns)
            bar_chart = px.bar(df, x=bar_column)
            st.plotly_chart(bar_chart, use_container_width=True)

            # Generated Bar Chart Code
            st.write("**Generated Bar Chart Code**")
            bar_code = f"""
            import plotly.express as px
            bar_column = '{bar_column}'
            bar_chart = px.bar(df, x=bar_column)
            bar_chart.show()
            """
            st.code(bar_code, language="python")

        # Scatter Matrix
        if scatter_matrix:
            st.subheader("Scatter Matrix Plot")
            scatter_matrix = px.scatter_matrix(
                df, dimensions=df.columns, title="Scatter Matrix"
            )
            st.plotly_chart(scatter_matrix, use_container_width=True)

            # Generated Scatter Matrix Code
            st.write("**Generated Scatter Matrix Code**")
            scatter_matrix_code = f"""
            import plotly.express as px
            scatter_matrix = px.scatter_matrix(df, dimensions=df.columns, title='Scatter Matrix')
            scatter_matrix.show()
            """
            st.code(scatter_matrix_code, language="python")
            
        # Box Plot
        if box_plot:
            box_column = st.selectbox("Select a column for the box plot", df.columns)
            plt.boxplot(df[box_column])
            plt.xlabel(box_column)
            plt.ylabel("Value")
            st.pyplot()
            
            # Generated Box Plot Code
            st.write("**Generated Box Plot Code**")
            box_code = f"""
            box_column = '{box_column}'
            plt.boxplot(df[box_column])
            plt.xlabel('{box_column}')
            plt.ylabel('Value')
            plt.title('Box Plot: {box_column}')
            plt.show()
            """
            st.code(box_code, language="python")
        
        # Pair Plot
        if pair_plot:
            pair_plot = sns.pairplot(df)
            st.pyplot()

            # Generated Pair Plot Code
            st.write("**Generated Pair Plot Code**")
            pair_plot_code = """
            import seaborn as sns
            pair_plot = sns.pairplot(df)
            plt.show()
            """
            st.code(pair_plot_code, language="python")
            
        # Count Plot
        if count_plot:
            # Count Plot
            count_column = st.selectbox("Select a column for the count plot", df.columns)
            count_plot = sns.countplot(data=df, x=count_column)
            st.pyplot()

            # Generated Count Plot Code
            st.write("**Generated Count Plot Code**")
            count_plot_code = f"""
            count_column = '{count_column}'
            count_plot = sns.countplot(data=df, x='{count_column}')
            plt.show()
            """
            st.code(count_plot_code, language="python")
        
        # Distribution Plot
        if dist_plot:
            dist_column = st.selectbox("Select a column for the distribution plot", df.columns)
            sns.histplot(df[dist_column], kde=True)
            plt.xlabel(dist_column)
            plt.ylabel("Density")
            st.pyplot()

            # Generated Distribution Plot Code
            st.write("**Generated Distribution Plot Code**")
            dist_plot_code = f"""
            dist_column = '{dist_column}'
            sns.histplot(df['{dist_column}'], kde=True)
            plt.xlabel('{dist_column}')
            plt.ylabel('Density')
            plt.title('Distribution Plot: {dist_column}')
            plt.show()
            """
            st.code(dist_plot_code, language="python")
            
        # Pie Chart
        if pie_chart:
            pie_column = st.selectbox("Select a categorical column for the pie chart", df.columns)
            pie_data = df[pie_column].value_counts()
            plt.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%", startangle=140)
            plt.axis("equal")
            st.pyplot()

            # Generated Pie Chart Code
            st.write("**Generated Pie Chart Code**")
            pie_chart_code = f"""
            pie_column = '{pie_column}'
            pie_data = df['{pie_column}'].value_counts()
            plt.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%", startangle=140)
            plt.axis("equal")
            plt.title('Pie Chart: {pie_column}')
            plt.show()
            """
            st.code(pie_chart_code, language="python")
            
        # Time Series Plot
        if time_series:
            time_column = st.selectbox("Select the time-based column", df.columns)
            df[time_column] = pd.to_datetime(df[time_column])
            df.set_index(time_column, inplace=True)

            # Select Y-axis column for the time series plot
            y_column = st.selectbox("Select Y-axis column", df.columns)

            plt.plot(df.index, df[y_column])
            plt.xlabel("Time")
            plt.ylabel(y_column)
            st.pyplot()

            # Generated Time Series Plot Code
            st.write("**Generated Time Series Plot Code**")
            time_series_code = f"""
            time_column = '{time_column}'
            df['{time_column}'] = pd.to_datetime(df['{time_column}'])
            df.set_index('{time_column}', inplace=True)
            y_column = '{y_column}'
            plt.plot(df.index, df['{y_column}'])
            plt.xlabel('Time')
            plt.ylabel('{y_column}')
            plt.title('Time Series Plot: {y_column} over Time')
            plt.show()
            """
            st.code(time_series_code, language="python")
        
        # Violin Plot
        if violin_plot:
            violin_x = st.selectbox("Select a categorical column for X-axis", df.columns)
            violin_y = st.selectbox("Select a numerical column for Y-axis", df.columns)
            sns.violinplot(data=df, x=violin_x, y=violin_y)
            st.pyplot()

            # Generated Violin Plot Code
            st.write("**Generated Violin Plot Code**")
            violin_code = f"""
            violin_x = '{violin_x}'
            violin_y = '{violin_y}'
            sns.violinplot(data=df, x='{violin_x}', y='{violin_y}')
            plt.show()
            """
            st.code(violin_code, language="python")

if __name__ == "__main__":
    main()

link = "Created by: [Gideon Ogunbanjo](https://gideonogunbanjo.netlify.app)"
st.markdown(link, unsafe_allow_html=True)
