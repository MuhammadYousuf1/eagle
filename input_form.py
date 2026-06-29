from datetime import date
import io
import os
import pandas as pd
import streamlit as st

# ==============================================================================
# 1. PAGE & STORAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Deposit & Expense Input",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- Custom UI styling (Glassmorphism Transformation) ---
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* Vibrant gradient background to maximize the frosted glass look */
        .stApp {
            background: radial-gradient(at 0% 0%, #e0e7ff 0px, transparent 50%),
                        radial-gradient(at 50% 0%, #eef2ff 0px, transparent 50%),
                        radial-gradient(at 100% 0%, #e0f2fe 0px, transparent 50%),
                        radial-gradient(at 0% 100%, #f1f5f9 0px, transparent 50%),
                        radial-gradient(at 100% 100%, #e0e7ff 0px, transparent 50%);
            background-color: ##fdc3ff;
            font-family: 'Inter', sans-serif;
        }

        [data-testid="stMainBlockContainer"] {
            background: linear-gradient(135deg, rgb(255 255 255 / 10%) 0%, rgb(26 0 255 / 16%) 100%);
            max-width: 920px;
            padding-top: 1.5rem;
            padding-bottom: 2.5rem;
        }

        /* --- Glassmorphism Cards --- */
        .hero-card {
            background: linear-gradient(135deg, rgb(34 65 255) 0%, rgb(77 57 255 / 40%) 100%);
            backdrop-filter: blur(25px) saturate(160%);
            -webkit-backdrop-filter: blur(25px) saturate(160%);
            border: 1px solid rgba(0, 240, 255, 0.45);
            border-radius: 18px;
            padding: 1.75rem 2rem;
            margin-bottom: 1.25rem;
            box-shadow: 0 12px 40px 0 rgba(0, 240, 255, 0.25);
            color: #ffffff;
        }

        .hero-card h1 {
            margin: 0 0 0.45rem 0;
            font-size: 1.85rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            color: #ffffff !important;
        }

        .hero-card p {
            margin: 0;
            font-size: 0.98rem;
            line-height: 1.55;
            color: rgba(255, 255, 255, 0.9);
        }

        .section-card {
            background: rgba(255, 255, 255, 0.45);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.5);
            border-radius: 16px;
            padding: 1.35rem 1.45rem 0.35rem 1.45rem;
            margin-bottom: 1.1rem;
            box-shadow: 0 8px 32px 0 rgba(15, 23, 42, 0.04);
        }

        .section-title {
            display: flex;
            align-items: center;
            gap: 0.55rem;
            margin: 0 0 0.85rem 0;
            font-size: 1.05rem;
            font-weight: 700;
            color: #0f172a;
        }

        .section-title .badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 1.65rem;
            height: 1.65rem;
            border-radius: 999px;
            background: rgba(37, 99, 235, 0.1);
            color: #2563eb;
            font-size: 0.82rem;
            font-weight: 700;
        }

        .section-subtitle {
            margin: -0.35rem 0 1rem 0;
            color: #475569;
            font-size: 16px;
        }

        .stat-row {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.75rem;
            margin-bottom: 1rem;
        }

        .stat-pill {
            background: rgba(255, 255, 255, 0.65);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.6);
            border-radius: 14px;
            padding: 0.85rem 1rem;
            box-shadow: 0 8px 24px 0 rgba(15, 23, 42, 0.03);
            text-align: center;
        }

        .stat-pill .label {
            font-size: 0.76rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #475569;
            font-weight: 600;
            margin-bottom: 0.2rem;
        }

        .stat-pill .value {
            font-size: 1.15rem;
            font-weight: 700;
            color: #0f172a;
        }

        /* ---- Main Glass Form Area ---- */
        div[data-testid="stForm"] {
            background: rgba(255, 255, 255, 0.45);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.6);
            border-radius: 18px;
            padding: 1.5rem 1.55rem 1.25rem 1.55rem;
            margin-bottom: 1.1rem;
            box-shadow: 0 8px 32px 0 rgba(37, 99, 235, 0.05);
        }

        .form-card-header {
            margin-bottom: 1.15rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid rgba(15, 23, 42, 0.08);
        }

        .form-card-header .section-title {
            margin-bottom: 0.35rem;
        }

        .form-card-header .section-subtitle {
            margin: 0;
        }

        .form-group-label {
            display: flex;
            align-items: center;
            gap: 0.45rem;
            margin: 0.5rem 0 0.75rem 0;
            font-size: 0.92rem;
            font-weight: 700;
            color: #0f172a;
            letter-spacing: 0.01em;
        }

        .form-group-label .icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 1.55rem;
            height: 1.55rem;
            border-radius: 8px;
            background: rgba(37, 99, 235, 0.08);
            font-size: 0.82rem;
        }

        div[data-testid="stForm"] [data-testid="stHorizontalBlock"] {
            background: rgba(255, 255, 255, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.4);
            border-radius: 14px;
            padding: 1rem 1rem 0.35rem 1rem;
            margin-bottom: 0.9rem;
            gap: 1.1rem !important;
        }

        div[data-testid="stForm"] [data-testid="stVerticalBlock"] > div[data-testid="stMarkdown"] + div[data-testid="stVerticalBlock"] {
            background: rgba(255, 255, 255, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.4);
            border-radius: 14px;
            padding: 0.15rem 1rem 0.35rem 1rem;
            margin-bottom: 0.35rem;
        }

        div[data-testid="stForm"] label {
            font-weight: 600 !important;
            color: #1e293b !important;
            font-size: 0.84rem !important;
        }

        div[data-testid="stForm"] input,
        div[data-testid="stForm"] textarea {
            border-radius: 10px !important;
            border: 1px solid rgba(15, 23, 42, 0.15) !important;
            background: rgba(255, 255, 255, 0.7) !important;
            color: #0f172a !important;
            transition: border-color 0.15s ease, box-shadow 0.15s ease;
        }

        div[data-testid="stForm"] input:focus,
        div[data-testid="stForm"] textarea:focus {
            border-color: #3b82f6 !important;
            background: #ffffff !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
        }

        div[data-testid="stForm"] [data-testid="stNumberInput"] button {
            border-radius: 8px !important;
        }

        div[data-testid="stForm"] [data-testid="stDateInput"] input {
            font-weight: 500 !important;
        }

        div[data-testid="stForm"] [data-testid="stTextArea"] {
            background: rgba(255, 255, 255, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.4);
            border-radius: 14px;
            padding: 0.75rem 0.85rem 0.35rem 0.85rem;
            margin-bottom: 0.35rem;
        }

        div[data-testid="stForm"] [data-testid="stTextArea"] textarea {
            min-height: 140px !important;
        }

        .notes-panel-hint {
            margin: -0.5rem 0 0.65rem 0;
            font-size: 0.8rem;
            color: #475569;
            line-height: 1.45;
        }

        .form-footer-note {
            margin: 0.85rem 0 0.15rem 0;
            padding: 0.65rem 0.85rem;
            border-radius: 10px;
            background: rgba(239, 246, 255, 0.5);
            border: 1px dashed rgba(59, 130, 246, 0.3);
            color: #1d4ed8;
            font-size: 0.8rem;
            line-height: 1.45;
        }

        div[data-testid="stFormSubmitButton"] button {
            width: 100%;
            border-radius: 12px !important;
            border: none !important;
            background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            padding: 0.72rem 1rem !important;
            box-shadow: 0 10px 22px rgba(37, 99, 235, 0.2) !important;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }

        div[data-testid="stFormSubmitButton"] button:hover {
            transform: translateY(-1px);
            box-shadow: 0 14px 28px rgba(37, 99, 235, 0.28) !important;
            background: linear-gradient(135deg, #589bff 0%, #2563eb 100%) !important
        }

        div[data-testid="stDownloadButton"] button,
        div[data-testid="stFileUploader"] button {
            background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
            color: #ffffff !important;
            border: none !important;
            box-shadow: 0 8px 18px rgba(15, 118, 110, 0.15) !important;
        }

        div[data-testid="stFileUploader"] button:hover, 
        div[data-testid="stDownloadButton"] button:hover{
            transform: translateY(-1px);
            box-shadow: 0 14px 28px rgba(37, 99, 235, 0.28) !important;
            background: linear-gradient(135deg, #589bff 0%, #2563eb 100%) !important
        }

        .table-card {
            background: rgba(255, 255, 255, 0.45);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.6);
            border-radius: 16px;
            padding: 1.15rem 1.15rem 0.35rem 1.15rem;
            box-shadow: 0 8px 32px 0 rgba(15, 23, 42, 0.04);
            display: flex !important;
            justify-content: center !important;
        }

        div[data-testid="stDataFrame"] table,
        div[data-testid="stDataFrame"] th,
        div[data-testid="stDataFrame"] td,
        div[data-testid="stDataFrame"] div[role="columnheader"],
        div[data-testid="stDataFrame"] div[role="rowheader"],
        div[data-testid="stDataFrame"] div[role="gridcell"],
        div[data-testid="stDataFrame"] div[role="cell"] {
            text-align: center !important;
            display: flex !important;
            justify-content: center !important;
        }

        div[data-testid="stDataFrame"] div[role="columnheader"] > div,
        div[data-testid="stDataFrame"] div[role="gridcell"] > div {
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            text-align: center !important;
            width: 100% !important;
            display: flex !important;
            justify-content: center !important;
        }

        .stDataFrameGlideDataEditor,
        .stDataFrameGlideDataEditor * {
            text-align: center !important;
            display: flex !important;
            justify-content: center !important;
        }

        .file-path-chip {
            display: inline-block;
            margin-top: 0.35rem;
            padding: 0.35rem 0.65rem;
            border-radius: 999px;
            background: rgba(248, 250, 252, 0.6);
            border: 1px solid rgba(226, 232, 240, 0.6);
            color: #475569;
            font-size: 0.82rem;
            font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        }

        div[data-testid="stAlert"] {
            border-radius: 12px;
            backdrop-filter: blur(8px);
        }

        div[data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.5);
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-card">
        <h1 style="text-align: center;">🏪 Store Deposit & Expense Form</h1>
        <p style="text-align: center;">
            Fill out the form below. Only one entry is allowed per date.
            Records are permanently saved straight to your Excel sheet.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

FILE_NAME = "deposit_maintenance_data.xlsx"
FULL_PATH = FILE_NAME
UPLOAD_DIR = "uploaded_photos"

# Ensure target folder for image uploads exists locally
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


# ==============================================================================
# 2. HELPER FUNCTIONS
# ==============================================================================
def load_excel_data(file_path):
    """Safely reads from the Excel file and handles database schema initialization."""
    if os.path.exists(file_path):
        try:
            df = pd.read_excel(file_path, engine="openpyxl")
            if "Date" in df.columns:
                df["Date"] = df["Date"].astype(str)
            return df
        except Exception as e:
            st.error(f"Error reading existing Excel file: {e}")
            return pd.DataFrame()
    else:
        return pd.DataFrame(
            columns=[
                "Store Name",
                "Emp Name",
                "Date",
                "Cash in Hand",
                "Expense Amt",
                "Expense Type",
                "Comments/Extra Notes",
                "Photo Path",
            ]
        )


# ==============================================================================
# 3. INPUT FORM SECTION
# ==============================================================================
preview_df = load_excel_data(FULL_PATH)
record_count = len(preview_df) if not preview_df.empty else 0
total_cash = preview_df["Cash in Hand"].sum() if record_count and "Cash in Hand" in preview_df.columns else 0.0
total_expense = preview_df["Expense Amt"].sum() if record_count and "Expense Amt" in preview_df.columns else 0.0

st.markdown(
    f"""
    <div class="stat-row">
        <div class="stat-pill">
            <div class="label">Total Records</div>
            <div class="value">{record_count}</div>
        </div>
        <div class="stat-pill">
            <div class="label">Cash in Hand</div>
            <div class="value">${total_cash:,.2f}</div>
        </div>
        <div class="stat-pill">
            <div class="label">Total Expenses</div>
            <div class="value">${total_expense:,.2f}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form(key="deposit_form", clear_on_submit=True):
    st.markdown(
        """
        <div class="form-card-header">
            <div class="section-title"><span class="badge">1</span> New Entry Form</div>
            <div class="section-subtitle">
                Enter store, employee, and expense details for the selected date.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="form-group-label">
            <span class="icon">🏪</span> Store &amp; Cash Details
        </div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns(2, gap="large")

    with col1:
        store_name = st.text_input("Store Name", placeholder="e.g. Downtown Branch")
        cash_in_hand = st.number_input("Cash in Hand", min_value=0.0, step=100.0, format="%.2f")
        expense_amt = st.number_input("Expense Amt", min_value=0.0, step=50.0, format="%.2f")

    with col2:
        emp_name = st.text_input("Emp Name", placeholder="e.g. John Doe")
        current_date = st.date_input("Date", value=date.today(), format="MM/DD/YYYY")
        expense_type = st.text_input(
            "Expense Type",
            placeholder="e.g. Utilities, Maintenance, Supplies",
        )

    # Photo upload layout fields
    st.markdown(
        """
        <div class="form-group-label">
            <span class="icon">📸</span> Upload Image / Receipt
        </div>
        <p class="notes-panel-hint">Optional — drag and drop or snap a photo of the deposit slip or store bill.</p>
        """,
        unsafe_allow_html=True,
    )
    uploaded_photo = st.file_uploader(
        "Upload Photo",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

    st.markdown(
        """
        <div class="form-group-label">
            <span class="icon">📝</span> Additional Notes
        </div>
        <p class="notes-panel-hint">Optional — add context such as receipt numbers, vendor names, or any adjustments.</p>
        """,
        unsafe_allow_html=True,
    )
    comments_notes = st.text_area(
        "Comments/Extra Notes",
        placeholder="Add any additional information here...",
        height=140,
        label_visibility="collapsed",
    )

    st.markdown('<div class="divider-soft"></div>', unsafe_allow_html=True)
    submit_button = st.form_submit_button(label="💾 Save Entry directly to Excel File")


# ==============================================================================
# 4. DATA PROCESSING & VALIDATION
# ==============================================================================
if submit_button:
    selected_date_str = current_date.strftime("%Y-%m-%d")
    existing_df = load_excel_data(FULL_PATH)

    duplicate_date_found = False
    if not existing_df.empty and "Date" in existing_df.columns:
        duplicate_date_found = selected_date_str in existing_df["Date"].values

    if not store_name.strip():
        st.error("⚠️ Store Name cannot be empty!")

    elif not emp_name.strip():
        st.error("⚠️ Employee Name cannot be empty!")

    elif duplicate_date_found:
        st.error(
            f"🚫 An entry for **{selected_date_str}** already exists inside the file database! "
            f"Changes/overwrites are blocked."
        )

    else:
        photo_path_saved = "N/A"
        
        # Save photo onto local storage safely if it exists
        if uploaded_photo is not None:
            # Handle clean unique string names for standard file systems
            clean_store_basename = "".join(c for c in store_name if c.isalnum()).lower()
            file_extension = os.path.splitext(uploaded_photo.name)[1]
            unique_filename = f"{selected_date_str}_{clean_store_basename}{file_extension}"
            photo_path_saved = os.path.join(UPLOAD_DIR, unique_filename)
            
            # Write stream chunks onto server disk target folder
            with open(photo_path_saved, "wb") as f:
                f.write(uploaded_photo.getbuffer())

        new_entry = {
            "Store Name": store_name,
            "Emp Name": emp_name,
            "Date": selected_date_str,
            "Cash in Hand": cash_in_hand,
            "Expense Amt": expense_amt,
            "Expense Type": expense_type.strip() if expense_type.strip() else "N/A",
            "Comments/Extra Notes": comments_notes.strip() if comments_notes.strip() else "N/A",
            "Photo Path": photo_path_saved,
        }

        new_row_df = pd.DataFrame([new_entry])
        updated_df = pd.concat([existing_df, new_row_df], ignore_index=True)

        try:
            updated_df.to_excel(FULL_PATH, index=False, sheet_name="Deposit_Data")
            st.success(
                f"✅ Successfully written and compiled data entry for '{store_name}' "
                f"by {emp_name} on date {selected_date_str}!"
            )
            st.rerun()
        except Exception as e:
            st.error(
                f"❌ Failed to access or rewrite the file system layout. Please verify "
                f"that the Excel file is not open in another desktop application! "
                f"Error logs: {e}"
            )


# ==============================================================================
# 5. DOWNLOAD BUTTON SECTION
# ==============================================================================
st.markdown('<div class="divider-soft"></div>', unsafe_allow_html=True)

latest_df = load_excel_data(FULL_PATH)

if not latest_df.empty:
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        latest_df.to_excel(writer, index=False, sheet_name="Deposit_Data")

    st.download_button(
        label="📥 Download Excel Table",
        data=buffer.getvalue(),
        file_name=FILE_NAME,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
else:
    st.button(
        "📥 Download Excel",
        disabled=True,
        help="No data available to download yet.",
        use_container_width=True,
    )

st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# 6. FILE REVISION DISPLAY (READ-ONLY)
# ==============================================================================
st.markdown(
    """
    <div class="table-card">
        <div class="section-title"><span class="badge">2</span>  RECORDED DATA</div>
    """,
    unsafe_allow_html=True,
)

if not latest_df.empty:
    styled_df = latest_df.style.set_properties(**{
        'text-align': 'center',
    }).set_table_styles([ # type: ignore
        {
            'selector': 'th',
            'props': [('text-align', 'center')],
        },
    ])

    st.dataframe(styled_df, width="stretch", hide_index=True)
else:
    st.info("No records are inside.")

st.markdown("</div>", unsafe_allow_html=True)