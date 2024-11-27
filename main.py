import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd
import io

# Streamlit app title
st.title("HTML Code Input App")

# HTML input from the user
html_code = st.text_area("Enter HTML Code:", height=300)

# Display the HTML code if the user has entered it
if html_code:
    # Analyze the HTML code for tables
    soup = BeautifulSoup(html_code, "html.parser")
    tables = soup.find_all("table")

    if tables:
        sorted_tables_html = ""
        for idx, table in enumerate(tables):
            # Convert HTML table to DataFrame
            df = pd.read_html(str(table))[0]

            # Convert DataFrame back to HTML
            table_html = df.to_html(index=False)
            sorted_tables_html += table_html + "\n"

        # Display the HTML code with sortable tables in a text area
        st.subheader("HTML Code with Sortable Tables:")
        st.text_area("Generated HTML Code:", value=sorted_tables_html, height=300)

# Add some instructions or examples
st.markdown("""
    ### Instructions:
    - Enter your HTML code in the text area above.
    - If there are tables in the HTML code, they will be extracted and displayed as sortable tables.
    - The generated HTML code for the tables will also be available for copying.
    
    Example:
    ```html
    <h1>Hello, Streamlit!</h1>
    <p>This is a paragraph of HTML code.</p>
    <table>
        <tr><th>Header 1</th><th>Header 2</th></tr>
        <tr><td>Data 1</td><td>Data 2</td></tr>
    </table>
    ```
""")
