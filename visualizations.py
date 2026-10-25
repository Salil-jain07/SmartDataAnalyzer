
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns


def show_visualizations(df):
    st.subheader("Data Visualization")

    if df.empty:
        st.warning("The dataset is empty.")
        return

    sns.set_theme(style="darkgrid")

    plt.rcParams.update({
        "figure.facecolor": "#1B1F29",
        "axes.facecolor": "#1B1F29",
        "axes.edgecolor": "#414653",
        "axes.labelcolor": "#E5E7EB",
        "text.color": "#F3F4F6",
        "xtick.color": "#D1D5DB",
        "ytick.color": "#D1D5DB",
        "grid.color": "#343946",
    })

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category", "string"]
    ).columns.tolist()

    # Dataset Overview
    total_rows, total_columns = df.shape
    missing_values = int(df.isna().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    st.markdown("### Dataset Overview")

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric("Total Rows", f"{total_rows:,}")
    metric2.metric("Total Columns", f"{total_columns:,}")
    metric3.metric("Missing Values", f"{missing_values:,}")
    metric4.metric("Duplicate Rows", f"{duplicate_rows:,}")

    st.markdown("---")
    st.markdown("### Explore Your Data")

    chart_type = st.selectbox(
        "Choose chart type",
        [
            "Histogram",
            "Bar Chart",
            "Scatter Plot",
            "Correlation Heatmap",
        ],
        key="visualization_chart_type",
    )



    # Histogram
    if chart_type == "Histogram":
        left_col, right_col = st.columns(2, gap="large")
        if not numeric_columns:
            st.info("No numerical columns available.")
            return

        with left_col:
            column = st.selectbox(
                "Numerical column",
                numeric_columns,
                key="histogram_column",
            )

        with right_col:
            st.markdown("#### Distribution")

            fig, ax = plt.subplots(figsize=(5, 3))
            sns.histplot(
                data=df,
                x=column,
                kde=True,
                color="#43A6C6",
                ax=ax,
            )
            ax.set_title(f"Distribution of {column}")
            ax.set_ylabel("Frequency")
            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

    # Bar Chart
    elif chart_type == "Bar Chart":
        left_col, right_col = st.columns(2, gap="large")
        if not categorical_columns:
            st.info("No categorical columns available.")
            return

        with left_col:
            column = st.selectbox(
                "Categorical column",
                categorical_columns,
                key="bar_column",
            )

        top_values = (
            df[column]
            .fillna("Missing")
            .astype(str)
            .value_counts()
            .head(10)
            .sort_values()
        )

        with right_col:
            st.markdown("#### Category Counts")

            fig, ax = plt.subplots(figsize=(5, 3))
            top_values.plot(
                kind="barh",
                color="#43A6C6",
                ax=ax,
            )
            ax.set_title(f"Top Categories in {column}")
            ax.set_xlabel("Count")
            ax.set_ylabel("")
            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

    # Scatter Plot
    elif chart_type == "Scatter Plot":
        left_col, right_col = st.columns(2, gap="large")
        if len(numeric_columns) < 2:
            st.info("At least two numerical columns are needed.")
            return

        with left_col:
            x_column = st.selectbox(
                "X-axis column",
                numeric_columns,
                key="scatter_x",
            )

        y_options = [
            c for c in numeric_columns if c != x_column
        ]

        with right_col:
            y_column = st.selectbox(
                "Y-axis column",
                y_options,
                key="scatter_y",
            )

        st.markdown("#### Relationship Between Variables")

        fig, ax = plt.subplots(figsize=(5, 3))

        sns.scatterplot(
            data=df,
            x=x_column,
            y=y_column,
            color="#8B83D8",
            s=45,
            ax=ax,
        )

        ax.set_title(f"{y_column} vs {x_column}")
        fig.tight_layout()

        st.pyplot(fig, use_container_width=False)
        plt.close(fig)


    # Correlation Heatmap

    # Correlation Heatmap
    elif chart_type == "Correlation Heatmap":
        numeric_df = df.select_dtypes(include="number")

        if numeric_df.shape[1] < 2:
            st.warning("At least two numeric columns are required.")
        else:
            corr = numeric_df.corr()

            fig = px.imshow(
                corr,
                text_auto=".2f" if len(corr.columns) <= 12 else False,
                color_continuous_scale="RdBu_r",
                zmin=-1,
                zmax=1,
                aspect="auto",
                labels=dict(
                    x="Columns",
                    y="Columns",
                    color="Correlation"
                ),
                title="Correlation Heatmap"
            )

            fig.update_layout(
                autosize=True,
                height=max(550, len(corr.columns) * 65),
                margin=dict(l=40, r=40, t=70, b=120),
                xaxis=dict(tickangle=-45),
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )
