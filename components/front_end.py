import streamlit as st
import pandas as pd

# Title
st.title("Interactive Data Preprocessing App")

# File upload
uploaded_file = st.file_uploader("Upload your dataset (CSV format)", type="csv")
if uploaded_file:
    # Load the dataset
    df = pd.read_csv(uploaded_file)
    st.write("Dataset Preview:")
    st.dataframe(df)

    # Save the dataset for processing
    st.session_state['df'] = df


if 'df' in st.session_state:
    df = st.session_state['df']

    # Select a column
    column = st.selectbox("Select a column to preprocess", df.columns)

    # Choose an operation
    operation = st.selectbox(
        "Choose an operation",
        ["Fill Missing Values", "Normalize", "Scale", "Encode Categorical Variables", "Drop Duplicates"]
    )

    # Display relevant options for the chosen operation
    if operation == "Fill Missing Values":
        fill_method = st.radio("Select a method to fill missing values", ["Mean", "Median", "Mode"])
    elif operation == "Normalize":
        st.write("This will normalize the column to a [0, 1] range.")
    elif operation == "Scale":
        st.write("This will standardize the column (mean=0, std=1).")
    elif operation == "Encode Categorical Variables":
        st.write("This will encode categories into numerical values.")
    elif operation == "Drop Duplicates":
        st.write("This will remove duplicate rows based on the selected column.")

    # Apply the selected operation
    if st.button("Apply"):
        # Placeholder for processed data and code generation
        processed_df = df.copy()
        generated_code = ""

        if operation == "Fill Missing Values":
            if fill_method == "Mean":
                processed_df[column] = processed_df[column].fillna(processed_df[column].mean())
                generated_code = f"df['{column}'] = df['{column}'].fillna(df['{column}'].mean())"
            elif fill_method == "Median":
                processed_df[column] = processed_df[column].fillna(processed_df[column].median())
                generated_code = f"df['{column}'] = df['{column}'].fillna(df['{column}'].median())"
            elif fill_method == "Mode":
                processed_df[column] = processed_df[column].fillna(processed_df[column].mode()[0])
                generated_code = f"df['{column}'] = df['{column}'].fillna(df['{column}'].mode()[0])"

        elif operation == "Normalize":
            min_val = processed_df[column].min()
            max_val = processed_df[column].max()
            processed_df[column] = (processed_df[column] - min_val) / (max_val - min_val)
            generated_code = (
                f"df['{column}'] = (df['{column}'] - df['{column}'].min()) / "
                f"(df['{column}'].max() - df['{column}'].min())"
            )

        elif operation == "Scale":
            mean_val = processed_df[column].mean()
            std_val = processed_df[column].std()
            processed_df[column] = (processed_df[column] - mean_val) / std_val
            generated_code = (
                f"df['{column}'] = (df['{column}'] - df['{column}'].mean()) / df['{column}'].std()"
            )

        elif operation == "Encode Categorical Variables":
            processed_df[column] = processed_df[column].astype("category").cat.codes
            generated_code = f"df['{column}'] = df['{column}'].astype('category').cat.codes"

        elif operation == "Drop Duplicates":
            processed_df = processed_df.drop_duplicates(subset=[column])
            generated_code = f"df = df.drop_duplicates(subset=['{column}'])"

        # Display processed data and generated code
        st.write("Processed Data:")
        st.dataframe(processed_df)

        st.write("Generated Code:")
        st.code(generated_code)

        # Save processed data for download
        st.session_state['processed_df'] = processed_df
        st.session_state['generated_code'] = generated_code


if 'processed_df' in st.session_state:
    processed_df = st.session_state['processed_df']
    generated_code = st.session_state['generated_code']

    # Download processed data
    csv = processed_df.to_csv(index=False)
    st.download_button(
        "Download Processed Dataset",
        data=csv,
        file_name="processed_dataset.csv",
        mime="text/csv",
    )

    # Download generated code
    st.download_button(
        "Download Generated Code",
        data=generated_code,
        file_name="processing_script.py",
        mime="text/plain",
    )
