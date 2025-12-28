import pandas as pd
import streamlit as st
from io import BytesIO
import openpyxl

def export_csv(df: pd.DataFrame):
    """Export to CSV"""
    st.markdown("### 📥 Export as CSV")
    
    if st.button("Prepare CSV Download"):
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name="data_export.csv",
            mime="text/csv"
        )
        st.success("✅ CSV ready for download")

def export_excel(df: pd.DataFrame):
    """Export to Excel"""
    st.markdown("### 📥 Export as Excel")
    
    if st.button("Prepare Excel Download"):
        try:
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Data', index=False)
                
                workbook = writer.book
                worksheet = writer.sheets['Data']
                
                for idx, col in enumerate(df.columns, 1):
                    worksheet.column_dimensions[openpyxl.utils.get_column_letter(idx)].width = 15
            
            output.seek(0)
            
            st.download_button(
                label="📥 Download Excel",
                data=output.getvalue(),
                file_name="data_export.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            st.success("✅ Excel file ready for download")
        except Exception as e:
            st.error(f"Error: {str(e)}")

def export_json(df: pd.DataFrame):
    """Export to JSON"""
    st.markdown("### 📥 Export as JSON")
    
    if st.button("Prepare JSON Download"):
        json_data = df.to_json(orient='records', indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=json_data,
            file_name="data_export.json",
            mime="application/json"
        )
        st.success("✅ JSON ready for download")

def export_parquet(df: pd.DataFrame):
    """Export to Parquet"""
    st.markdown("### 📥 Export as Parquet")
    
    if st.button("Prepare Parquet Download"):
        try:
            output = BytesIO()
            df.to_parquet(output, index=False)
            output.seek(0)
            
            st.download_button(
                label="📥 Download Parquet",
                data=output.getvalue(),
                file_name="data_export.parquet",
                mime="application/octet-stream"
            )
            st.success("✅ Parquet file ready for download")
        except Exception as e:
            st.error(f"Error: {str(e)}")

def export_sql_insert(df: pd.DataFrame):
    """Generate SQL INSERT statements"""
    st.markdown("### 📥 Export as SQL")
    
    table_name = st.text_input("Table name", "data_table")
    
    if st.button("Generate SQL"):
        sql_statements = []
        for _, row in df.iterrows():
            cols = ', '.join(df.columns)
            vals = ', '.join([f"'{val}'" if not pd.isna(val) else 'NULL' 
                            for val in row.values])
            sql = f"INSERT INTO {table_name} ({cols}) VALUES ({vals});"
            sql_statements.append(sql)
        
        sql_text = '\n'.join(sql_statements)
        st.text_area("SQL Statements", sql_text, height=200)
        
        st.download_button(
            label="📥 Download SQL",
            data=sql_text,
            file_name="insert_statements.sql",
            mime="text/plain"
        )
        st.success("✅ SQL statements ready")

def export_functionality_ui(df: pd.DataFrame):
    """Main export UI"""
    st.markdown("## 📥 Export Data")
    
    export_format = st.radio(
        "Select export format",
        ["CSV", "Excel", "JSON", "Parquet", "SQL"],
        horizontal=True
    )
    
    if export_format == "CSV":
        export_csv(df)
    elif export_format == "Excel":
        export_excel(df)
    elif export_format == "JSON":
        export_json(df)
    elif export_format == "Parquet":
        export_parquet(df)
    elif export_format == "SQL":
        export_sql_insert(df)
    
    st.divider()
    st.info(f"📊 Exporting {len(df)} rows × {len(df.columns)} columns")
