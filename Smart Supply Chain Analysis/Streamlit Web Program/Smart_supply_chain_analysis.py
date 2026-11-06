import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Page settings
st.set_page_config(
    page_title="Smart Supply Chain Analytics",
    page_icon="📦",
    layout="wide"
)

# Dashboard title
st.title("📦 Smart Supply Chain Analytics")
st.write(
    "Analyze shipments, suppliers, warehouses, transportation, "
    "delivery costs, and shipment delays."
)

# Project Image
st.image("Smart_Supply_Chain_Analysis_Image.png")


# Sidebar: upload dataset
st.sidebar.header("📂 Upload Dataset")

file = st.sidebar.file_uploader(
    "Upload a Supply Chain CSV or Excel file",
    type=["csv", "xlsx"]
)

# Dataset analysis
if file is not None:

    try:
        if file.name.lower().endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        st.sidebar.success("File uploaded successfully!")

        menu = st.sidebar.radio(
            "Navigate",
            [
                "Data Overview",
                "Statistics",
                "Visualization",
                "Filter Data"
            ]
        )

        # 1. Data Overview
        if menu == "Data Overview":
            st.subheader("📁 Dataset Overview")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Rows", f"{df.shape[0]:,}")

            with col2:
                st.metric("Total Columns", df.shape[1])

            with col3:
                st.metric(
                    "Missing Values",
                    f"{df.isnull().sum().sum():,}"
                )

            st.subheader("Dataset Preview")
            st.dataframe(df, use_container_width=True)

            st.subheader("Column Information")
            info_df = pd.DataFrame({
                "Column Name": df.columns,
                "Data Type": df.dtypes.astype(str).values,
                "Missing Values": df.isnull().sum().values
            })

            st.dataframe(info_df, use_container_width=True)

        # 2. Statistics
        elif menu == "Statistics":
            st.subheader("📈 Statistical Summary")

            numeric_df = df.select_dtypes(include="number")

            if not numeric_df.empty:
                st.dataframe(
                    numeric_df.describe().round(2),
                    use_container_width=True
                )
            else:
                st.info("No numeric columns are available.")

            st.subheader("Dataset Information")
            st.write("Dataset shape:", df.shape)
            st.write("Duplicate rows:", int(df.duplicated().sum()))

        # 3. Visualization
        elif menu == "Visualization":
            st.subheader("📊 Data Visualization")

            numeric_cols = df.select_dtypes(
                include="number"
            ).columns.tolist()

            categorical_cols = df.select_dtypes(
                include=["object", "category", "bool"]
            ).columns.tolist()

            plot_type = st.selectbox(
                "Select Plot Type",
                [
                    "Histogram",
                    "Bar Chart",
                    "Scatter Plot",
                    "Correlation Heatmap",
                    "Box Plot",
                    "Count Plot"
                ]
            )

            if plot_type == "Histogram":
                if numeric_cols:
                    num_col = st.selectbox(
                        "Select numeric column",
                        numeric_cols
                    )

                    bins = st.slider(
                        "Number of bins",
                        min_value=5,
                        max_value=50,
                        value=20
                    )

                    fig, ax = plt.subplots()
                    sns.histplot(
                        data=df,
                        x=num_col,
                        bins=bins,
                        ax=ax
                    )
                    ax.set_title(f"Distribution of {num_col}")
                    st.pyplot(fig)
                    plt.close(fig)
                else:
                    st.info("No numeric columns are available.")

            elif plot_type == "Bar Chart":
                if categorical_cols:
                    col = st.selectbox(
                        "Select category",
                        categorical_cols
                    )

                    top_n = st.slider(
                        "Number of categories to display",
                        5, 30, 10
                    )

                    counts = df[col].value_counts().head(top_n)

                    fig, ax = plt.subplots()
                    counts.plot(kind="bar", ax=ax)
                    ax.set_title(f"Count by {col}")
                    ax.set_xlabel(col)
                    ax.set_ylabel("Count")
                    plt.xticks(rotation=45, ha="right")
                    fig.tight_layout()
                    st.pyplot(fig)
                    plt.close(fig)
                else:
                    st.info("No categorical columns are available.")

            elif plot_type == "Scatter Plot":
                if len(numeric_cols) >= 2:
                    x_col = st.selectbox(
                        "X-axis",
                        numeric_cols,
                        key="scatter_x"
                    )

                    y_options = [
                        col for col in numeric_cols if col != x_col
                    ]

                    y_col = st.selectbox(
                        "Y-axis",
                        y_options,
                        key="scatter_y"
                    )

                    fig, ax = plt.subplots()
                    sns.scatterplot(
                        data=df,
                        x=x_col,
                        y=y_col,
                        ax=ax
                    )
                    ax.set_title(f"{y_col} vs {x_col}")
                    st.pyplot(fig)
                    plt.close(fig)
                else:
                    st.info(
                        "At least two numeric columns are required."
                    )

            elif plot_type == "Correlation Heatmap":
                if len(numeric_cols) >= 2:
                    corr = df[numeric_cols].corr()

                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.heatmap(
                        corr,
                        annot=True,
                        cmap="coolwarm",
                        fmt=".2f",
                        ax=ax
                    )
                    ax.set_title("Correlation Heatmap")
                    fig.tight_layout()
                    st.pyplot(fig)
                    plt.close(fig)
                else:
                    st.info(
                        "At least two numeric columns are required."
                    )

            elif plot_type == "Box Plot":
                if numeric_cols:
                    num_col = st.selectbox(
                        "Select numeric column",
                        numeric_cols,
                        key="box_col"
                    )

                    fig, ax = plt.subplots()
                    sns.boxplot(data=df, y=num_col, ax=ax)
                    ax.set_title(f"Box Plot of {num_col}")
                    st.pyplot(fig)
                    plt.close(fig)
                else:
                    st.info("No numeric columns are available.")

            elif plot_type == "Count Plot":
                if categorical_cols:
                    cat_col = st.selectbox(
                        "Select categorical column",
                        categorical_cols,
                        key="count_col"
                    )

                    counts = df[cat_col].value_counts().head(20)

                    fig, ax = plt.subplots()
                    counts.sort_values().plot(
                        kind="barh",
                        ax=ax
                    )
                    ax.set_title(f"Count Plot of {cat_col}")
                    ax.set_xlabel("Count")
                    st.pyplot(fig)
                    plt.close(fig)
                else:
                    st.info("No categorical columns are available.")

        # 4. Filter Data
        elif menu == "Filter Data":
            st.subheader("🔎 Filter Dataset")

            numeric_cols = df.select_dtypes(
                include="number"
            ).columns.tolist()

            if numeric_cols:
                selected_col = st.selectbox(
                    "Select numeric column",
                    numeric_cols
                )

                min_val = float(df[selected_col].min())
                max_val = float(df[selected_col].max())

                if pd.isna(min_val) or pd.isna(max_val):
                    st.warning("This column has no usable numeric values.")
                elif min_val == max_val:
                    filtered_df = df[df[selected_col] == min_val]
                    st.write("Filtered rows:", len(filtered_df))
                    st.dataframe(
                        filtered_df,
                        use_container_width=True
                    )
                else:
                    user_range = st.slider(
                        "Select value range",
                        min_value=min_val,
                        max_value=max_val,
                        value=(min_val, max_val)
                    )

                    filtered_df = df[
                        df[selected_col].between(
                            user_range[0],
                            user_range[1]
                        )
                    ]

                    st.write("Filtered dataset shape:", filtered_df.shape)
                    st.dataframe(
                        filtered_df,
                        use_container_width=True
                    )

                    csv = filtered_df.to_csv(
                        index=False
                    ).encode("utf-8")

                    st.download_button(
                        "⬇️ Download Filtered Data",
                        data=csv,
                        file_name="filtered_supply_chain.csv",
                        mime="text/csv"
                    )
            else:
                st.info("No numeric columns are available for filtering.")

    except Exception as e:
        st.error(f"Unable to read or analyze this file: {e}")

else:
    st.info(
        "Please upload a supply chain CSV or Excel dataset "
        "from the sidebar to begin."
    )

st.sidebar.caption("Built with Python, Pandas & Streamlit")
