import sys
from pathlib import Path
import streamlit as st
import pandas as pd

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.lexer import Lexer


def main():
    """Main Streamlit application"""
    
    # Page configuration
    st.set_page_config(
        page_title="Lexical Analyzer",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Title and description
    st.title("Lexical Analyzer - Compiler Project")
    st.markdown("""
    This tool demonstrates the **lexical analysis phase** of compiler construction.
    - **Tokenization**: Break source code into meaningful tokens
    - **Symbol Table**: Track all identifiers
    - **Error Detection**: Find lexical errors
    """)
    
    # Sidebar for configuration
    st.sidebar.header(" Configuration")
    language = st.sidebar.selectbox(
        "Select Language",
        ["C"]
    )
    
    # Main content in columns
    col1, col2 = st.columns(2)
    
    # LEFT COLUMN: Input
    with col1:
        st.header("Input Source Code")
        
        # Input method selection
        input_method = st.radio(
            "Choose input method:",
            ["Paste Code", "Upload File"]
        )
        
        source_code = ""
        
        if input_method == "Paste Code":
            # Text area for manual input
            source_code = st.text_area(
                "Enter C code here:",
                value="int x = 10;\ny = x + 20;",
                height=300,
                placeholder="Enter your source code here..."
            )
        
        else:  # Upload File
            uploaded_file = st.file_uploader(
                "Upload C file (.c, .h)",
                type=['c', 'h', 'txt']
            )
            if uploaded_file is not None:
                source_code = uploaded_file.read().decode('utf-8')
                st.text_area(
                    "File contents:",
                    value=source_code,
                    height=300,
                    disabled=True
                )
    
    # RIGHT COLUMN: Analysis options
    with col2:
        st.header(" Analysis Options")
        
        analyze_button = st.button(
            "Analyze Code",
            use_container_width=True,
            type="primary"
        )
        
        st.markdown("---")
        
        # Display options
        st.subheader("Display Options")
        show_tokens = st.checkbox("Show Tokens", value=True)
        show_symbols = st.checkbox("Show Symbol Table", value=True)
        show_errors = st.checkbox("Show Errors", value=True)
        show_stats = st.checkbox("Show Statistics", value=True)
    
    # MAIN ANALYSIS SECTION
    if analyze_button or source_code:
        st.markdown("---")
        
        # Create lexer and tokenize
        lexer = Lexer()
        tokens, errors, symbol_table = lexer.tokenize(source_code)
        
        # Get statistics
        stats = lexer.get_statistics()
        
        # Display results
        if show_stats:
            st.header("Statistics")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Tokens", stats['Total Tokens'])
            with col2:
                st.metric("Token Types", stats['Unique Token Types'])
            with col3:
                st.metric("Symbols Found", stats['Symbols'])
            with col4:
                st.metric("Errors", stats['Errors'], delta="error" if stats['Errors'] > 0 else "")
            
            # Token breakdown
            st.subheader("Token Type Breakdown")
            if stats['Token Breakdown']:
                breakdown_df = pd.DataFrame(
                    list(stats['Token Breakdown'].items()),
                    columns=['Token Type', 'Count']
                ).sort_values('Count', ascending=False)
                
                st.bar_chart(breakdown_df.set_index('Token Type'))
        
        # Display tokens
        if show_tokens:
            st.header(" Token Stream")
            if tokens:
                tokens_data = [token.to_dict() for token in tokens]
                tokens_df = pd.DataFrame(tokens_data)
                
                st.dataframe(
                    tokens_df,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Download tokens
                csv = tokens_df.to_csv(index=False)
                st.download_button(
                    label="Download Tokens (CSV)",
                    data=csv,
                    file_name="tokens.csv",
                    mime="text/csv"
                )
            else:
                st.info("No tokens generated (empty input or all comments/whitespace)")
        
        # Display symbol table
        if show_symbols:
            st.header("Symbol Table")
            symbols = symbol_table.get_all_symbols()
            
            if symbols:
                symbols_df = pd.DataFrame(symbols)
                st.dataframe(
                    symbols_df,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Download symbols
                csv = symbols_df.to_csv(index=False)
                st.download_button(
                    label=" Download Symbol Table (CSV)",
                    data=csv,
                    file_name="symbol_table.csv",
                    mime="text/csv"
                )
            else:
                st.info("No symbols found")
        
        # Display errors
        if show_errors:
            st.header("Lexical Errors")
            
            if errors:
                st.error(f"Found {len(errors)} error(s)")
                errors_data = [error.to_dict() for error in errors]
                errors_df = pd.DataFrame(errors_data)
                
                st.dataframe(
                    errors_df,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Highlight errors in source code
                st.subheader("Error Highlighting")
                st.code(source_code, language="c")
            else:
                st.success(" No lexical errors found!")


if __name__ == "__main__":
    main()