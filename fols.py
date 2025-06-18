import streamlit as st
import os
from datetime import datetime

LOCAL_BACKUP_DIR = "local_backups"

st.set_page_config(page_title="Local File Saver", page_icon="💾")
st.title("📁 Save Files Locally")

if 'user' not in st.session_state:
    st.session_state.user = None

# Login/logout UI
if st.session_state.user:
    st.sidebar.write(f"Logged in as: {st.session_state.user}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()
else:
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if username and password:
            st.session_state.user = username
            st.success("Logged in!")
            st.rerun()
        else:
            st.error("Please enter credentials")

if st.session_state.user:
    st.subheader("Upload your file")
    uploaded_file = st.file_uploader("Choose a file to upload")
    if uploaded_file:
        file_content = uploaded_file.read()
        file_name = uploaded_file.name

        if st.button("💾 Save Locally"):
            try:
                local_user_dir = os.path.join(LOCAL_BACKUP_DIR, st.session_state.user)
                os.makedirs(local_user_dir, exist_ok=True)
                local_file_path = os.path.join(local_user_dir, file_name)

                with open(local_file_path, "wb") as f:
                    f.write(file_content)

                st.success(f"✅ File saved locally at: {local_file_path}")

                # Show preview for .java files
                if file_name.endswith(".java"):
                    st.subheader("📄 Java File Preview")
                    st.code(file_content.decode("utf-8"), language="java")

                # Download button
                st.download_button("⬇️ Download File", file_content, file_name)

            except Exception as e:
                st.error(f"🚨 Save failed: {e}")

    # List existing local files
    st.subheader("📜 Your Saved Files")
    user_dir = os.path.join(LOCAL_BACKUP_DIR, st.session_state.user)
    if os.path.exists(user_dir):
        for file_name in os.listdir(user_dir):
            file_path = os.path.join(user_dir, file_name)
            st.markdown(f"📄 `{file_name}`")
            with open(file_path, "rb") as f:
                st.download_button(f"⬇️ Download {file_name}", f.read(), file_name)
    else:
        st.info("No files saved yet.")
