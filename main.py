import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd

# Streamlit app title
st.title("HTML Code Input App")

# HTML input from the user
html_code = st.text_area("Enter HTML Code:", height=300)

# Display the HTML code if the user has entered it
if html_code:
    # Analyze the HTML code for tables
    soup = BeautifulSoup(html_code, "html.parser")
    tables = soup.find_all("table")

    for table in tables:
        headers = [th.get_text(strip=True) for th in table.find_all("th")]
        rows = []
        for row in table.find_all("tr")[1:]:  # Skip the header row
            cells = row.find_all("td")
            row_data = []
            for cell in cells:
                # Preserve HTML content such as links and images
                row_data.append(cell.decode_contents())
            rows.append(row_data)

        # Create a DataFrame from the table data
        if headers and rows:
            df = pd.DataFrame(rows, columns=headers)

            # Check if there's a 'relevance score' column and sort it by default
            for header in headers:
                if header.lower().startswith('relevance score'):
                    df = df.sort_values(by=header, ascending=False)
                    break

            # Replace the original table with the sorted one
            new_html = df.to_html(index=False, escape=False)
            new_table = BeautifulSoup(new_html, "html.parser")
            for original, new in zip(table.find_all("td"), new_table.find_all("td")):
                original.replace_with(BeautifulSoup(new.encode_contents(), "html.parser"))

    # Display the HTML code with sorted tables in a text area
    st.subheader("HTML Code with Sorted Tables:")
    st.text_area("Generated HTML Code:", value=str(soup), height=300)

# Add some instructions or examples
st.markdown("""
    ### Instructions:
    - Enter your HTML code in the text area above.
    - If there are tables in the HTML code, they will be sorted by default if a 'relevance score' column is present.
    - The generated HTML code with sorted tables will also be available for copying.
    
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
