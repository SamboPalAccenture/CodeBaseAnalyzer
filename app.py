import streamlit as st
import tempfile
import shutil
import os
import subprocess
from analyzer import analyze_code, analyze_folder
from git import Repo

st.set_page_config(page_title="Function Flow Analyzer", layout="wide")
st.title("📊Code Base Analyzer")

option = st.radio("Choose input source:", ("📁 Upload Folder of Code Files", "🔗 GitHub Repository"))

# Option 1 Folder upload
if option == "📁 Upload Folder of Code Files":
    uploaded_files = st.file_uploader(
        "Upload all code files from a folder (multi-select supported)",
        type=["py", "js", "ts", "java", "cpp", "c", "cs", "rb", "php", "go", "rs", "sh", "swift", "kt"],
        accept_multiple_files=True
    )

    if uploaded_files:
        with tempfile.TemporaryDirectory() as tmp_dir:
            st.info(f"📁 Simulating folder upload into: {tmp_dir}")

            # Save all files to the temp folder
            for uploaded_file in uploaded_files:
                file_path = os.path.join(tmp_dir, uploaded_file.name)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

            with st.spinner("Analyzing uploaded folder..."):
                try:
                    analysis_result = analyze_folder(tmp_dir)
                    st.success("✅ Analysis Complete")
                    
                    # Display analysis
                    st.markdown("### 🧠 Project Summary")
                    st.markdown(analysis_result.split("// From")[0])
                    
                    st.markdown("### 📂 Per-File Analysis")
                    for section in analysis_result.split("// From")[1:]:
                        st.code("// From" + section, language="text")
                except Exception as e:
                    st.error(f"Error during analysis: {e}")
    else:
        st.info("Please upload all files from a folder to simulate folder-level analysis.")


# Option 2: GitHub Repo
elif option == "🔗 GitHub Repository":
    repo_url = st.text_input("Enter the GitHub repository URL:")

    if st.button("Clone and Analyze"):
        if not repo_url.strip():
            st.warning("Please enter a GitHub URL.")
        else:
            with st.spinner("⏳ Cloning repository and analyzing..."):
                try:
                    with tempfile.TemporaryDirectory() as tmp_dir:
                        Repo.clone_from(repo_url, tmp_dir)
                        flows = analyze_folder(tmp_dir)

                        if not flows.strip():
                            st.warning("Analysis completed, but no output was returned.")
                        else:
                            st.success("✅ Analysis complete.")

                            # Debug view (raw output)
                            with st.expander("🪵 Show Raw Output (Debug)"):
                                st.text(flows[:5000] + "\n... [truncated]" if len(flows) > 5000 else flows)

                            # Parse output into summary and file flows
                            parts = flows.split("// From")
                            summary = parts[0]
                            file_flows = parts[1:]

                            # Show summary
                            st.markdown("### 🧠 Project Summary")
                            if summary.strip():
                                st.markdown(summary)
                            else:
                                st.info("No project summary returned.")

                            # Show file-wise flows
                            st.markdown("### 📂 Per-File Flowcharts")
                            if file_flows:
                                for section in file_flows:
                                    st.code("// From" + section.strip(), language="text")
                            else:
                                st.info("No per-file flowcharts found.")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
