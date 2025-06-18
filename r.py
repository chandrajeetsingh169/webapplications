import streamlit as st
import os
from datetime import datetime
import dropbox

# Dropbox Setup
DROPBOX_ACCESS_TOKEN = "sl.u.AFyByHevo4A6KmRfuG8VeWYUWrLqF4X1CHS1UP7BVHP4sgpPyuh_AfgEc5O9-bwQjVMqSOloURtZwcF747xBDnCdnhbT4VJPc-r6g6ufmMfxAZ7KYHIuGlYsU0ZSQrDv55uxRNlaXql-c3sv1fmw_OjrSF1gPv7go0wgUi1wOBWZi30ZF52cvvHQxckVhivyke513La0B33fa44mxqOUvrABXDCaXj7_R1IDERXVMjtNuX1lJJzEEon3HLHygbisGLIgvgwaS26GI4QCGkPVmC_-4WKMFlkd5N8RFRPJaPwQ5YUlt4tHFKcdGP3FL3xMOx8rr5xd34tbLM-ADojYnWTEBHyw9wD25Ela8vIefaJjUmADjGlVXtePrkKO39S6yERv_1dj6dCik-8xlXcaOlGcCTnhkqZd06AGQ6qYy_KJb1Qic1otOBOteDizWXb_KHvhoJjTuJcHy8BruQ-yWhjSY-V-n2fHID1uTOnLh4BG7jwsi9TEE9YeGX5_wbjuwd9sK8qIpliCCAae4zYptMbFpFXfc2-wHk7Fu0VKZQEjYO8BKA0JBQDmL5DDuuPcELbXqhXBRdGZqwl7qfXjUv4WF9vB1ajlDoevodqwAKdd-HZZQHRU0ln-kwNlCwBPpvJteObyxPoY_kqjN57rvFMOKSfdoI6sFZSIVQZ-01HU5p-ox-6NCOuZTQiWOuL11PkkLRez8ykSf8_mjT7bH2X6_k3U3DQ43jqAiwM6cYjTCBxKzWjyfQkUWMChfthb95Yv9nf4FvvfemfVspTPEhR_s4b8FQI3RLKeispIUR_pGT6jhpLaGZQzq7gSXL4Xa_Zsw35QpsyAuMtTzxjmT8P4DSmtb8r1jM9t3YL4ehcEz5rm3EFWTRcUzhFionTCY-l9vX9u0sVDyBU4r0ZF3HsYzsol5m058lvViM-ib5TDoDh-vnQMByGyqWYOoH6ysAFkCZCTcxnfRzSGAya4lGdD7OKea-OCBEe2MJOK7dtNFFzQgbLHM6VYDJAJMDPSe7RnHblpBjPOhecAFt7cZ8b4ZApHW4vzux7rvL5noX2Q25el9WB9hxqcgmcQKOjgm64nPiTSSeVz1NJ8SwaSEz75sRFV54ugXa31I_riE_RzfxDT6OYXzGjlbD1gxHLXWm8k-jYPD9qXbv0Qy5p0caFDK4CwPSHRuh0gwspRvLrHToU-wQt8UIcKxXBS7fJl3FhkUyhKpDu05TmLZu6OlfNuPrWi0fbyxFGA26FLOftD-r5aycOIbAP5T0fv7XuPUcdcKih4rDstYMpo7lMeCKm9pS2zAGwXqZYJeH8aWc7MdVumpOa4Q78X8JO2gA7G3hDMfH7_0jIuQanyR01KUbj-CkMpS947-_UeIbAJfVOQ28HkOl1Sm8l6orSnkZfANiGGKbApVxnI_mpFlZYV02_k"
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

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

        if st.button("💾 Save Locally & to Dropbox"):
            try:
                # Save Locally
                local_user_dir = os.path.join(LOCAL_BACKUP_DIR, st.session_state.user)
                os.makedirs(local_user_dir, exist_ok=True)
                local_file_path = os.path.join(local_user_dir, file_name)

                with open(local_file_path, "wb") as f:
                    f.write(file_content)

                st.success(f"✅ File saved locally at: {local_file_path}")

                # Save to Dropbox
                dropbox_path = f"/{st.session_state.user}/{file_name}"
                dbx.files_upload(file_content, dropbox_path, mode=dropbox.files.WriteMode("overwrite"))
                st.success("☁️ File also uploaded to Dropbox!")

                # Preview for Java files
                if file_name.endswith(".java"):
                    st.subheader("📄 Java File Preview")
                    st.code(file_content.decode("utf-8"), language="java")

                # Download locally
                st.download_button("⬇️ Download File", file_content, file_name)

            except Exception as e:
                st.error(f"🚨 Save failed: {e}")

    # List local files
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
