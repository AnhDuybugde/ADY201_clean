import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import streamlit as st
from dython.nominal import associations
import os

def plot_chart(df, x_col=None, y_col=None, chart_type="Histogram", save_path=None):
    """
    Hàm vẽ biểu đồ cho dataframe df.
    chart_type: "Histogram", "Boxplot", "Scatter", "Bar", "Heatmap (corr)", 
                 "Violin", "Countplot", "Line", "Pairplot"
    Nếu save_path != None thì lưu ảnh vào đó.
    """
    plt.figure(figsize=(10, 6))
    sns.set(font_scale=0.9, style="whitegrid")
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)

    # Histogram / Countplot
    if chart_type == "Histogram":
        data = df[x_col].copy()
        if pd.api.types.is_numeric_dtype(data):
            sns.histplot(data.dropna(), bins=30, kde=True)
        else:
            sns.countplot(x=data.fillna("Missing"))
        plt.xlabel(x_col)
        plt.ylabel("Frequency / Count")

    # Boxplot
    elif chart_type == "Boxplot":
        sns.boxplot(data=df, x=x_col, y=y_col)
        plt.xlabel(x_col)
        plt.ylabel(y_col)

    # Violin Plot (phân phối)
    elif chart_type == "Violin":
        sns.violinplot(data=df, x=x_col, y=y_col, inner="quartile")
        plt.xlabel(x_col)
        plt.ylabel(y_col)

    # Scatter (phân tán)
    elif chart_type == "Scatter":
        sns.regplot(x=x_col, y=y_col, data=df, scatter_kws={'alpha':0.6})
        plt.title("Scatter Plot với đường hồi quy")
        plt.show()

    # Pie (tròn)
    elif chart_type == "Pie":
        counts = df[x_col].value_counts()
        plt.pie(counts, labels=counts.index, autopct='%1.1f%%')
        plt.title(f"Biểu đồ tròn của {x_col}")

    # Bar (thanh)
    elif chart_type == "Bar":
        sns.barplot(data=df, x=x_col, y=y_col, estimator=np.mean)
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        
    # Line (đường)
    elif chart_type == "Line":
        sns.lineplot(data=df, x=x_col, y=y_col, marker="o")
        plt.xlabel(x_col)
        plt.ylabel(y_col)

    # Countplot (đếm danh mục)
    elif chart_type == "Countplot":
        sns.countplot(data=df, x=x_col)
        plt.xlabel(x_col)
        plt.ylabel("Count")

    # Pairplot (tương quan nhiều biến)
    elif chart_type == "Pairplot":
        numeric_df = df.select_dtypes(include=["int", "float"]).dropna()
        if numeric_df.shape[1] < 2:
            st.warning("Không đủ cột số để vẽ Pairplot.")
        else:
            sns.pairplot(numeric_df)
            plt.close()  # tránh trùng figure
            if save_path:
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                plt.savefig(save_path, bbox_inches='tight')
            st.pyplot()

            return  # dừng ở đây (vì pairplot đã render xong)

    # Heatmap (ma trận tương quan)
    elif chart_type == "Heatmap (corr)":
        data = df.copy()
        assoc = associations(df, nominal_columns='auto', mark_columns=True, figsize=(10,8))
        corr = assoc['corr']

        plt.figure(figsize=(10,8))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap='rocket', vmin=-1, vmax=1)
        plt.title("Ma trận tương quan giữa category và numeric", fontsize=14)
        # Hoàn thiện
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

    # Lưu file nếu có
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches='tight')
        st.success(f"Biểu đồ đã được lưu vào: `{os.path.basename(save_path)}`")

    st.pyplot(plt)
