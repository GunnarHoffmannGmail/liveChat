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
            rows.append([cell.get_text(strip=True) for cell in cells])

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
            table.replace_with(new_table)

    # Add JavaScript to make tables sortable
    script = """
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        var tables = document.querySelectorAll('table');
        tables.forEach(function(table) {
            table.querySelectorAll('th').forEach(function(header, index) {
                header.style.cursor = 'pointer';
                header.innerHTML += ' \u21D5';  // Add sort icon
                
                header.addEventListener('click', function() {
                    var rows = Array.from(table.querySelectorAll('tr')).slice(1); // Exclude header row
                    var isAscending = header.dataset.sortOrder !== 'asc';
                    header.dataset.sortOrder = isAscending ? 'asc' : 'desc';
                    rows.sort(function(rowA, rowB) {
                        var cellA = rowA.children[index].innerText.toLowerCase();
                        var cellB = rowB.children[index].innerText.toLowerCase();
                        return isAscending ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA);
                    });
                    rows.forEach(function(row) {
                        table.appendChild(row);
                    });
                });
            });
        });
    });
    </script>
    """

    # Inject the JavaScript into the HTML
    soup.body.append(BeautifulSoup(script, "html.parser"))

    # Display the HTML code with sortable tables in a text area
    st.subheader("HTML Code with Sortable Tables:")
    st.text_area("Generated HTML Code:", value=str(soup), height=300)

# Add some instructions or examples
st.markdown("""
    ### Instructions:
    - Enter your HTML code in the text area above.
    - If there are tables in the HTML code, they will be made sortable by clicking the table headers.
    - A sort icon (⇕) will be added to indicate that the table headers are sortable.
    - The generated HTML code with sortable tables will also be available for copying.
    
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
