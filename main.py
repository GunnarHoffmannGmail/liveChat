import streamlit as st
from bs4 import BeautifulSoup

# Streamlit app title
st.title("HTML Code Input App")

# HTML input from the user
html_code = st.text_area("Enter HTML Code:", height=300)

# Display the HTML code if the user has entered it
if html_code:
    # Analyze the HTML code for tables
    soup = BeautifulSoup(html_code, "html.parser")
    tables = soup.find_all("table")

    # Add JavaScript to make tables sortable
    script = """
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        var tables = document.querySelectorAll('table');
        tables.forEach(function(table) {
            table.querySelectorAll('th').forEach(function(header, index) {
                header.style.cursor = 'pointer';
                header.innerHTML += ' \u21D5';  // Add sort icon
                
                // Check if the header starts with 'relevance score' (case insensitive)
                if (header.innerText.trim().toLowerCase().startsWith('relevance score')) {
                    header.dataset.sortOrder = 'asc';  // Default sorting order for relevance score is ascending
                    // Trigger sorting by default
                    var rows = Array.from(table.querySelectorAll('tr')).slice(1); // Exclude header row
                    rows.sort(function(rowA, rowB) {
                        var cellA = rowA.children[index].innerText.toLowerCase();
                        var cellB = rowB.children[index].innerText.toLowerCase();
                        return cellA.localeCompare(cellB);
                    });
                    rows.forEach(function(row) {
                        table.appendChild(row);
                    });
                }
                
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
