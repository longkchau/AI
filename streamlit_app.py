import os
import pandas as pd
import streamlit as st
from pdf2image import convert_from_path

GUIDE_FILE_EXTENSION = (".csv", ".pdf")
UPLOAD_DIRECTORY = "uploads"
GUIDE_DIRECTORY = "guides"


def save_guide_page(guide_name, page_content):
    guide_directory = os.path.join(GUIDE_DIRECTORY, guide_name)
    os.makedirs(guide_directory, exist_ok=True)

    guide_page_count = len(os.listdir(guide_directory))
    file_path = os.path.join(guide_directory, f"page{guide_page_count + 1}{GUIDE_FILE_EXTENSION[0]}")

    df = pd.DataFrame({"Page Content": [page_content]})
    df.to_csv(file_path, index=False)


def display_guide(guide_name, page_number):
    guide_directory = os.path.join(GUIDE_DIRECTORY, guide_name)
    if not os.path.exists(guide_directory):
        st.error(f"No guide found for '{guide_name}'")
        return

    guide_pages = sorted([file for file in os.listdir(guide_directory) if file.endswith(GUIDE_FILE_EXTENSION[0])])
    if not guide_pages:
        st.warning(f"No pages found for '{guide_name}'")
        return

    if not page_number or page_number > len(guide_pages):
        st.warning("Invalid page number selected.")
        return

    selected_page = guide_pages[page_number - 1]
    selected_page_path = os.path.join(guide_directory, selected_page)

    if selected_page.endswith(".csv"):
        df = pd.read_csv(selected_page_path)
        st.dataframe(df)
    elif selected_page.endswith(".pdf"):
        images = convert_from_path(selected_page_path)
        for image in images:
            st.image(image)


def save_uploaded_file(file):
    os.makedirs(GUIDE_DIRECTORY, exist_ok=True)
    file_path = os.path.join(GUIDE_DIRECTORY, file.name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    return file_path


def scan_files(directory, search_query=""):
    guide_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(GUIDE_FILE_EXTENSION):
                guide_files.append(os.path.join(root, file))

    if search_query:
        guide_files = [
            file for file in guide_files
            if search_query.lower() in os.path.basename(file).lower()
        ]

    return guide_files


def display_file_content(file_path):
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
        st.dataframe(df)
    elif file_path.endswith(".pdf"):
        images = convert_from_path(file_path)
        for image in images:
            st.image(image)


def main():
    st.set_page_config(
        page_title="Guide Storage App",
        page_icon=":book:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("Guide Storage App")

    guide_directories = sorted(os.listdir(GUIDE_DIRECTORY))
    if not guide_directories:
        st.warning("No guides found in the directory.")
    else:
        with st.sidebar:
            selected_guide = st.selectbox("Select a guide:", [""] + guide_directories, key="selected_guide")
            guide_directory = os.path.join(GUIDE_DIRECTORY, selected_guide)
            guide_pages = sorted(
                [file for file in os.listdir(guide_directory) if file.endswith(GUIDE_FILE_EXTENSION[0])])

            if not guide_pages:
                st.warning(f"No pages found for '{selected_guide}'")
            else:
                selected_page_number = st.selectbox("Select a page:", range(1, len(guide_pages) + 1),
                                                    key="selected_page_number")
                display_guide(selected_guide, selected_page_number)

    uploaded_file = st.file_uploader("Upload a guide file (CSV/PDF):", type=GUIDE_FILE_EXTENSION)
    if uploaded_file is not None:
        file_path = save_uploaded_file(uploaded_file)
        st.success("Guide file uploaded successfully!")
        st.info("Please refresh the page to view the uploaded guide.")

    search_query = st.sidebar.text_input("Search for a guide:")
    if search_query:
        guide_files = scan_files(GUIDE_DIRECTORY, search_query)
        if guide_files:
            selected_file = st.sidebar.selectbox("Select a guide file:", guide_files)
            display_file_content(selected_file)
        else:
            st.warning("No matching guide files found.")

    st.sidebar.title("Scan for Guide Files")
    if st.sidebar.button("Scan"):
        guide_files = scan_files(GUIDE_DIRECTORY)
        if guide_files:
            selected_file = st.sidebar.selectbox("Select a guide file:", guide_files)
            display_file_content(selected_file)
        else:
            st.warning("No guide files found.")

if __name__ == "__main__":
    main()