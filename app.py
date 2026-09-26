# ============================================================
# APP.PY — COMPLETE DEVELOPER INDEX
# ============================================================
#
# [01] IMPORTS
#      [01-A] Core Libraries
#      [01-B] Settings / Theme Colors
#      [01-C] Service Imports
#      [01-D] View Imports
#
# [02] PAGE CONFIGURATION
#
# [03] GLOBAL PLOTLY THEME
#
# [04] THEME STATE
#      [04-A] Theme Labels
#      [04-B] Session State Initialization
#
# [05] NATIVE STREAMLIT THEME
#      [05-A] Dark Theme Configuration
#      [05-B] Light Theme Configuration
#      [05-C] Native Theme Function
#      [05-D] Initial Theme Synchronization
#
# [06] GLOBAL UI CSS
#      [06-A] CSS Top / Global Styling
#          [06-A-01] Google Fonts
#          [06-A-02] Root Colors
#          [06-A-03] Global Application
#          [06-A-04] Main Text
#          [06-A-05] Headings
#          [06-A-06] Main Container
#          [06-A-07] Home Hero
#          [06-A-08] Hero Statistics
#          [06-A-09] Section Title
#          [06-A-10] Standard Card
#          [06-A-11] Agriculture Card
#          [06-A-12] Result Card
#
#      [06-B] Light Mode Widget CSS
#          [06-B-01] Input Labels
#          [06-B-02] General Input
#          [06-B-03] BaseWeb Input
#          [06-B-04] Number Input
#          [06-B-05] Text Area
#          [06-B-06] Selectbox
#          [06-B-07] Dropdown Menu
#          [06-B-08] Date Input
#          [06-B-09] Radio
#          [06-B-10] Slider
#          [06-B-11] Normal Button
#          [06-B-12] Primary Button
#          [06-B-13] Form Submit Button
#          [06-B-14] Metrics
#          [06-B-15] DataFrame
#          [06-B-16] Expander
#          [06-B-17] Alerts
#          [06-B-18] Divider
#
#      [06-C] Bottom / Common CSS
#          [06-C-01] Sidebar
#          [06-C-02] Footer
#          [06-C-03] Plotly
#          [06-C-04] Hide Streamlit Default UI
#          [06-C-05] Mobile Base Styling
#          [06-C-06] Plotly Touch Stability
#
#      [06-D] Apply Light/Dark Global CSS
#
# [07] LOAD MODEL AND DATASET
#      [07-A] Load Model
#      [07-B] Load Dataset
#      [07-C] Validate Dataset
#      [07-D] Prepare Dataset
#      [07-E] Extract Model Components
#      [07-F] Calculate Model History Requirement
#      [07-G] Loading Error Handling
#
# [08] APPLICATION PAGE LIST
#
# [09] PAGE SESSION STATE
#
# [10] SIDEBAR NAVIGATION CSS
#      [10-A] Sidebar Container
#      [10-B] Sidebar Brand
#      [10-C] Sidebar Section Labels
#      [10-D] Sidebar Navigation Items
#      [10-E] Active Navigation Item
#      [10-F] Theme Switch Styling
#      [10-G] Sidebar Footer Note
#
# [11] SIDEBAR BRAND
#
# [12] SIDEBAR NAVIGATION
#
# [13] THEME SWITCH
#      [13-A] Theme Selection
#      [13-B] Theme Conversion
#      [13-C] Theme State Update
#
# [14] DARK THEME CUSTOM CSS
#      [14-A] Dark Plotly Theme
#      [14-B] Dark Root Variables
#      [14-C] Dark Headings
#      [14-D] Dark Hero
#      [14-E] Dark Cards
#      [14-F] Dark Agriculture Cards
#      [14-G] Dark Result Cards
#      [14-H] Dark Widget Text
#      [14-I] Dark Buttons
#      [14-J] Dark Footer
#      [14-K] Dark Sidebar
#
# [15] RADIO OPTION BOX CSS
#      [15-A] Radio Background Configuration
#      [15-B] Radio CSS Template
#      [15-C] Replace Theme Variables
#      [15-D] Apply Radio CSS
#
# [16] MOBILE / PHONE OPTIMISATION
#      [16-A] Mobile Layout
#      [16-B] Mobile Headings
#      [16-C] Mobile Cards
#      [16-D] Mobile Hero
#      [16-E] Mobile Inputs
#      [16-F] Mobile Buttons
#      [16-G] Mobile Radio
#      [16-H] Mobile Metrics
#      [16-I] Mobile Quick Navigation
#      [16-J] Mobile Charts
#      [16-K] Mobile Tables
#      [16-L] Mobile Sidebar
#      [16-M] Mobile Footer
#      [16-N] Small Phone Optimization
#
# [17] PAGE UPDATE
#
# [18] MAIN PAGE ROUTING
#      [18-A] Home
#      [18-B] Rain Prediction
#      [18-C] Agriculture & Irrigation
#      [18-D] Historical Data
#      [18-E] Analytics
#      [18-F] About
#
# [19] QUICK NAVIGATION
#      [19-A] Quick Navigation Columns
#      [19-B] Quick Page List
#      [19-C] Quick Navigation Buttons
#
# [20] APPLICATION FOOTER
#
# ============================================================
#
# IMPORTANT FILE RESPONSIBILITY
#
# app.py
# → Main application controller
# → Global theme
# → Global CSS
# → Model/data initialization
# → Sidebar navigation
# → Page routing
# → Quick navigation
# → Footer
#
# views/
# → Individual page UI and page-level logic
#
# services/
# → Reusable application/business logic
#
# ============================================================


# ============================================================
# [01] IMPORTS
# ============================================================

# ------------------------------------------------------------
# [01-A] CORE LIBRARIES
# ------------------------------------------------------------

import streamlit as st
import plotly.io as pio


# ------------------------------------------------------------
# [01-B] SETTINGS / THEME COLORS
# ------------------------------------------------------------

from config.settings import (
    INDIGO,
    SLATE,
    TEAL,
    AMBER,
    GREEN,
    INK,
    LINE
)


# ------------------------------------------------------------
# [01-C] SERVICE IMPORTS
# ------------------------------------------------------------

from services.data_loader import (
    load_model,
    load_dataset,
    validate_dataset,
    prepare_dataset,
    get_model_history_days
)


# ------------------------------------------------------------
# [01-D] VIEW IMPORTS
# ------------------------------------------------------------

from views.home import show_home
from views.prediction import show_prediction
from views.agriculture import show_agriculture
from views.data_page import show_data_page
from views.analytics import show_analytics
from views.about import show_about


# ============================================================
# [02] PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Bangladesh Rainfall & Agriculture System",
    page_icon="🌧️",
    layout="wide",
    initial_sidebar_state="auto"
)


# ============================================================
# [03] GLOBAL PLOTLY THEME
# ============================================================

pio.templates["monsoon"] = pio.templates["plotly_white"]

pio.templates["monsoon"].layout.colorway = [
    TEAL,
    INDIGO,
    AMBER,
    SLATE,
    GREEN,
    "#6FA8C4"
]

pio.templates["monsoon"].layout.font = dict(
    family="Inter, sans-serif",
    color=INK,
    size=13
)

pio.templates["monsoon"].layout.title.font = dict(
    family="Space Grotesk, sans-serif",
    size=16,
    color=INDIGO
)

pio.templates["monsoon"].layout.paper_bgcolor = "rgba(0,0,0,0)"
pio.templates["monsoon"].layout.plot_bgcolor = "rgba(0,0,0,0)"

pio.templates["monsoon"].layout.xaxis.gridcolor = LINE
pio.templates["monsoon"].layout.yaxis.gridcolor = LINE

pio.templates.default = "monsoon"


# ============================================================
# [04] THEME STATE
# ============================================================

# ------------------------------------------------------------
# [04-A] THEME LABELS
# ------------------------------------------------------------

THEME_LABELS = {
    "light": "☀️ Light",
    "dark": "🌙 Dark"
}


# ------------------------------------------------------------
# [04-B] SESSION STATE INITIALIZATION
# ------------------------------------------------------------

if "theme" not in st.session_state:
    saved_theme = st.query_params.get("theme", "light")
    st.session_state.theme = "dark" if saved_theme == "dark" else "light"


# ============================================================
# [05] NATIVE STREAMLIT THEME
# ============================================================

# ------------------------------------------------------------
# [05-A] DARK THEME CONFIGURATION
# ------------------------------------------------------------

DARK_NATIVE = {
    "theme.base": "dark",
    "theme.primaryColor": "#168F87",
    "theme.backgroundColor": "#0E1621",
    "theme.secondaryBackgroundColor": "#16212E",
    "theme.textColor": "#E6EDF3",
}


# ------------------------------------------------------------
# [05-B] LIGHT THEME CONFIGURATION
# ------------------------------------------------------------

LIGHT_NATIVE = {
    "theme.base": "light",
    "theme.primaryColor": None,
    "theme.backgroundColor": None,
    "theme.secondaryBackgroundColor": None,
    "theme.textColor": None,
}


# ------------------------------------------------------------
# [05-C] NATIVE THEME FUNCTION
# ------------------------------------------------------------

def apply_native_theme(theme_name):
    """Set Streamlit's native theme. Returns True if it changed."""

    wanted = DARK_NATIVE if theme_name == "dark" else LIGHT_NATIVE

    current_base = st._config.get_option("theme.base")

    if current_base == wanted["theme.base"]:
        return False

    for key, value in wanted.items():
        st._config.set_option(key, value)

    return True


# ------------------------------------------------------------
# [05-D] INITIAL THEME SYNCHRONIZATION
# ------------------------------------------------------------

if apply_native_theme(st.session_state.theme):
    st.rerun()


# ============================================================
# [06] GLOBAL UI CSS
# ============================================================

# ============================================================
# [06-A] CSS TOP / GLOBAL STYLING
# ============================================================

CSS_TOP = """
<style>

/* =========================================================
   [06-A-01] GOOGLE FONTS
========================================================= */

@import url(
'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+Bengali:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap'
);


/* =========================================================
   [06-A-02] ROOT COLORS
========================================================= */

:root {
    --bg: #F4F7FA;
    --card: #FFFFFF;
    --ink: #102A43;
    --text: #102A43;
    --muted: #5C6B78;
    --indigo: #0B1D33;
    --slate: #1B4965;
    --teal: #168F87;
    --teal-light: #E8F7F5;
    --green: #2E8B57;
    --amber: #E8873A;
    --line: #D5DEE7;
}


/* =========================================================
   [06-A-03] GLOBAL APPLICATION
========================================================= */

html,
body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {

    background-color: var(--bg) !important;
    color: var(--text) !important;

    font-family:
        'Inter',
        'Noto Sans Bengali',
        sans-serif !important;
}


.stApp {
    background-color: var(--bg) !important;
    color: var(--text) !important;
}


/* =========================================================
   [06-A-04] MAIN TEXT
========================================================= */

[data-testid="stMain"] p,
[data-testid="stMain"] li {
    color: var(--text) !important;
}

[data-testid="stMain"] .stMarkdown,
[data-testid="stMain"] .stMarkdown p,
[data-testid="stMain"] .stMarkdown li {
    color: var(--text) !important;
}


/* =========================================================
   [06-A-05] HEADINGS
========================================================= */

[data-testid="stMain"] h1,
[data-testid="stMain"] h2,
[data-testid="stMain"] h3,
[data-testid="stMain"] h4 {

    color: var(--indigo) !important;

    font-family:
        'Space Grotesk',
        'Noto Sans Bengali',
        sans-serif !important;

    font-weight: 700 !important;
}


/* =========================================================
   [06-A-06] MAIN CONTAINER
========================================================= */

.block-container {

    max-width: 1380px !important;

    padding-top: 1.6rem !important;
    padding-bottom: 2rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}


/* =========================================================
   [06-A-07] HOME HERO
========================================================= */

.hero {

    position: relative;
    overflow: hidden;

    padding: 2.6rem;

    border-radius: 22px;

    background:
        linear-gradient(
            135deg,
            #0B1D33 0%,
            #123A56 52%,
            #168F87 100%
        ) !important;

    box-shadow:
        0 12px 32px
        rgba(11, 29, 51, 0.16);

    margin-bottom: 1.8rem;
}


.hero h1 {

    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;

    font-size: 2rem !important;
    line-height: 1.35 !important;

    margin-bottom: 0.7rem !important;
}


.hero p {

    color: #E3F1F5 !important;
    -webkit-text-fill-color: #E3F1F5 !important;

    font-size: 1.05rem !important;
    line-height: 1.7 !important;

    margin-bottom: 0 !important;
}


/* =========================================================
   [06-A-08] HERO STATISTICS
========================================================= */

.hero-stats {

    display: flex;
    gap: 2.5rem;
    flex-wrap: wrap;

    margin-top: 1.8rem;
}


.hero-stat {

    border-left:
        4px solid #55D6C2;

    padding-left: 0.9rem;
}


.hero-num {

    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;

    font-size: 1.55rem !important;
    font-weight: 700 !important;

    line-height: 1.3 !important;
}


.hero-label {

    color: #CDE5EC !important;
    -webkit-text-fill-color: #CDE5EC !important;

    font-size: 0.88rem !important;

    margin-top: 0.25rem !important;
}


/* =========================================================
   [06-A-09] SECTION TITLE
========================================================= */

.section-title {

    font-size: 1.25rem;
    font-weight: 700;

    color: var(--indigo) !important;

    margin-top: 1.8rem;
    margin-bottom: 1rem;

    padding-left: 0.8rem;

    border-left:
        4px solid var(--teal);
}


/* =========================================================
   [06-A-10] STANDARD CARD
========================================================= */

.card {

    background: #FFFFFF !important;
    color: var(--text) !important;

    border:
        1px solid var(--line);

    border-radius: 16px;

    padding: 1.3rem;

    margin-bottom: 1rem;

    box-shadow:
        0 4px 15px
        rgba(15, 36, 54, 0.04);
}


.card p,
.card span {
    color: var(--text) !important;
}


/* =========================================================
   [06-A-11] AGRICULTURE CARD
========================================================= */

.agri-card {

    background:
        linear-gradient(
            135deg,
            #F1FAF5,
            #FFFFFF
        ) !important;

    color: var(--text) !important;

    border:
        1px solid #B8DEC7;

    border-left:
        6px solid var(--green);

    border-radius: 16px;

    padding: 1.4rem;

    margin-bottom: 1.2rem;
}


.agri-card h1,
.agri-card h2,
.agri-card h3,
.agri-card h4 {
    color: #176B3A !important;
}


.agri-card p {
    color: var(--text) !important;
    line-height: 1.7;
}


/* =========================================================
   [06-A-12] RESULT CARD
========================================================= */

.result-card {

    background:
        linear-gradient(
            135deg,
            #EAF8F0,
            #FFFFFF
        ) !important;

    color: var(--text) !important;

    border:
        1px solid #A8D9BB;

    border-radius: 18px;

    padding: 1.5rem;

    margin-bottom: 1rem;
}


.result-card h1,
.result-card h2,
.result-card h3 {
    color: #176B3A !important;
}


.result-card p {
    color: #176B3A !important;
}


"""


# ============================================================
# [06-B] LIGHT MODE WIDGET CSS
# ============================================================

CSS_WIDGETS_LIGHT = """/* =========================================================
   [06-B-01] INPUT LABELS
========================================================= */

[data-testid="stMain"] label {

    color: #102A43 !important;

    font-weight: 600 !important;

    font-size: 0.95rem !important;

    opacity: 1 !important;
}


/* =========================================================
   [06-B-02] GENERAL INPUT
========================================================= */

[data-testid="stMain"] input:not([type="date"]) {

    background-color: #FFFFFF !important;

    color: #102A43 !important;

    caret-color: #102A43 !important;

    border-color: #BFCBD5 !important;

    opacity: 1 !important;
}


/* =========================================================
   [06-B-03] GENERAL BASE INPUT
========================================================= */

[data-baseweb="input"] {
    background-color: #FFFFFF !important;
}


/* =========================================================
   [06-B-04] NUMBER INPUT
========================================================= */

[data-testid="stNumberInput"] input {

    color: #102A43 !important;

    background-color: #FFFFFF !important;

    opacity: 1 !important;
}


/* =========================================================
   [06-B-05] TEXT AREA
========================================================= */

[data-testid="stMain"] textarea {

    background-color: #FFFFFF !important;

    color: #102A43 !important;
}


/* =========================================================
   [06-B-06] SELECTBOX
========================================================= */

[data-testid="stSelectbox"] {
    opacity: 1 !important;
}


[data-testid="stSelectbox"] label,
[data-testid="stSelectbox"] label p,
[data-testid="stSelectbox"] label span {

    color: #102A43 !important;

    font-weight: 600 !important;

    opacity: 1 !important;
}


[data-testid="stMain"] [data-baseweb="select"],
[data-testid="stMain"] [data-baseweb="select"] > div {

    background-color: #FFFFFF !important;

    color: #102A43 !important;

    border-color: #BFCBD5 !important;

    opacity: 1 !important;
}


[data-testid="stMain"] [data-baseweb="select"] div,
[data-testid="stMain"] [data-baseweb="select"] span,
[data-testid="stMain"] [data-baseweb="select"] p,
[data-testid="stMain"] [data-baseweb="select"] input {

    color: #102A43 !important;

    opacity: 1 !important;
}


[data-testid="stMain"] [data-baseweb="select"] input {

    background-color: transparent !important;

    caret-color: #102A43 !important;
}


[data-testid="stMain"] [data-baseweb="select"] input::placeholder {

    color: #52616B !important;

    opacity: 1 !important;
}


[data-testid="stMain"] [data-baseweb="select"] svg {

    color: #102A43 !important;

    fill: currentColor !important;

    stroke: currentColor !important;

    opacity: 1 !important;
}


[data-testid="stMain"] [data-baseweb="select"]:focus-within > div {

    background-color: #FFFFFF !important;

    border-color: #168F87 !important;
}


/* =========================================================
   [06-B-07] DROPDOWN MENU
========================================================= */

[data-baseweb="popover"],
[data-baseweb="menu"],
[role="listbox"] {

    background-color: #FFFFFF !important;

    color: #102A43 !important;
}


[role="option"] {

    background-color: #FFFFFF !important;

    color: #102A43 !important;

    opacity: 1 !important;
}


[role="option"]:hover,
[role="option"][aria-selected="true"] {

    background-color: #E8F7F5 !important;

    color: #102A43 !important;
}


/* =========================================================
   [06-B-08] DATE INPUTS
========================================================= */

.st-key-prediction_date,
.st-key-historical_date_range {

    width: 100% !important;
}


/* Date box background only */

.st-key-prediction_date [data-testid="stDateInput"] > div,
.st-key-historical_date_range [data-testid="stDateInput"] > div {

    background-color: #FFFFFF !important;

    border-radius: 8px !important;
}


/* Keep date text visible */

.st-key-prediction_date [data-testid="stDateInput"] input,
.st-key-historical_date_range [data-testid="stDateInput"] input {

    background-color: #FFFFFF !important;

    color: #102A43 !important;

    opacity: 1 !important;
}


/* Calendar button */

.st-key-prediction_date [data-testid="stDateInput"] button,
.st-key-historical_date_range [data-testid="stDateInput"] button {

    background-color: #FFFFFF !important;

    color: #102A43 !important;

    border: none !important;
}


/* Calendar icon */

.st-key-prediction_date [data-testid="stDateInput"] button svg,
.st-key-historical_date_range [data-testid="stDateInput"] button svg {

    color: #102A43 !important;

    opacity: 1 !important;
}


/* =========================================================
   [06-B-09] RADIO
========================================================= */

[data-testid="stRadio"] label {
    color: #102A43 !important;
    font-weight: 500 !important;
}


[data-testid="stRadio"] p {
    color: #102A43 !important;
}


/* =========================================================
   [06-B-10] SLIDER
========================================================= */

[data-testid="stSlider"] {
    color: var(--indigo) !important;
}


/* =========================================================
   [06-B-11] NORMAL BUTTON
========================================================= */

.stButton > button {

    min-height: 44px !important;

    border-radius: 10px !important;

    font-weight: 600 !important;

    border:
        1px solid var(--teal) !important;

    color:
        var(--teal) !important;

    background:
        #FFFFFF !important;

    transition:
        all 0.2s ease !important;
}


.stButton > button:hover {

    background:
        #E8F7F5 !important;

    border-color:
        #168F87 !important;

    transform:
        translateY(-1px);
}


/* =========================================================
   [06-B-12] PRIMARY BUTTON
========================================================= */

.stButton > button[kind="primary"] {

    background:
        linear-gradient(
            135deg,
            #168F87,
            #1F9E92
        ) !important;

    color:
        #FFFFFF !important;

    border-color:
        #168F87 !important;

    box-shadow:
        0 4px 12px
        rgba(22, 143, 135, 0.18);
}


.stButton > button[kind="primary"] p,
.stButton > button[kind="primary"] span {

    color:
        #FFFFFF !important;
}


/* =========================================================
   [06-B-13] FORM SUBMIT BUTTON
========================================================= */

[data-testid="stFormSubmitButton"] button {

    min-height: 46px !important;

    background:
        linear-gradient(
            135deg,
            #168F87,
            #1F9E92
        ) !important;

    color:
        #FFFFFF !important;

    border:
        none !important;

    border-radius:
        10px !important;

    font-weight:
        700 !important;

    box-shadow:
        0 4px 14px
        rgba(22, 143, 135, 0.20) !important;

    transition:
        all 0.2s ease !important;
}


[data-testid="stFormSubmitButton"] button:hover {

    transform:
        translateY(-1px);

    box-shadow:
        0 7px 18px
        rgba(22, 143, 135, 0.28) !important;
}


[data-testid="stFormSubmitButton"] button p,
[data-testid="stFormSubmitButton"] button span {

    color:
        #FFFFFF !important;
}


/* =========================================================
   [06-B-14] METRICS
========================================================= */

div[data-testid="stMetric"] {

    background:
        #FFFFFF !important;

    border:
        1px solid var(--line) !important;

    border-radius:
        14px !important;

    padding:
        1rem !important;

    box-shadow:
        0 3px 12px
        rgba(15, 36, 54, 0.04);
}


[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] * {

    color:
        var(--muted) !important;
}


[data-testid="stMetricValue"],
[data-testid="stMetricValue"] * {

    color:
        var(--indigo) !important;

    font-weight:
        700 !important;
}


/* =========================================================
   [06-B-15] DATAFRAME
========================================================= */

[data-testid="stDataFrame"] {

    background:
        #FFFFFF !important;

    border:
        1px solid var(--line) !important;

    border-radius:
        12px !important;

    overflow:
        hidden !important;
}


/* =========================================================
   [06-B-16] EXPANDER
========================================================= */

[data-testid="stExpander"] {

    background:
        #FFFFFF !important;

    border:
        1px solid var(--line) !important;

    border-radius:
        12px !important;

    overflow:
        hidden !important;
}


[data-testid="stExpander"] p,
[data-testid="stExpander"] span {

    color:
        #102A43 !important;
}


/* =========================================================
   [06-B-17] ALERTS
========================================================= */

[data-testid="stAlert"] {
    border-radius: 12px !important;
}


/* =========================================================
   [06-B-18] DIVIDER
========================================================= */

hr {
    border-color: var(--line) !important;
}


"""


# ============================================================
# [06-C] BOTTOM / COMMON CSS
# ============================================================

CSS_BOTTOM = """/* =========================================================
   [06-C-01] SIDEBAR
========================================================= */

[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #0B1D33 0%,
            #132D42 100%
        ) !important;
}


[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {

    color:
        #F2F7FA !important;
}


[data-testid="stSidebar"]
[data-testid="stRadio"] label {

    color:
        #FFFFFF !important;
}


[data-testid="stSidebar"]
[data-testid="stRadio"] p {

    color:
        #FFFFFF !important;
}


[data-testid="stSidebar"] button {
    color:
        #FFFFFF !important;
}


[data-testid="stSidebar"] input {

    color:
        #102A43 !important;
}


/* =========================================================
   [06-C-02] FOOTER
========================================================= */

.footer {

    text-align:
        center;

    color:
        #52616B !important;

    padding:
        2rem 0 1rem;

    line-height:
        1.8;
}


.footer b {
    color:
        #0B1D33 !important;
}


/* =========================================================
   [06-C-03] PLOTLY
========================================================= */

.js-plotly-plot {
    background:
        transparent !important;
}


/* =========================================================
   [06-C-04] HIDE STREAMLIT DEFAULT UI
========================================================= */

#MainMenu {
    visibility:
        hidden;
}


footer {
    visibility:
        hidden;
}


/* =========================================================
   [06-C-05] MOBILE BASE STYLING
========================================================= */

@media (max-width: 768px) {

    .block-container {

        padding-left:
            1rem !important;

        padding-right:
            1rem !important;

        padding-top:
            1rem !important;
    }


    .hero {

        padding:
            1.5rem !important;

        border-radius:
            18px !important;
    }


    .hero h1 {

        font-size:
            1.45rem !important;
    }


    .hero p {

        font-size:
            0.95rem !important;
    }


    .hero-stats {

        gap:
            1.2rem !important;
    }


    .hero-num {

        font-size:
            1.3rem !important;
    }

}


/* =========================================================
   [06-C-06] PLOTLY TOUCH STABILITY
========================================================= */

.js-plotly-plot .svg-container {
    touch-action: manipulation !important;
}

</style>
"""


# ============================================================
# [06-D] APPLY GLOBAL CSS
# ============================================================

if st.session_state.theme == "dark":
    st.markdown(
        CSS_TOP + CSS_BOTTOM,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        CSS_TOP + CSS_WIDGETS_LIGHT + CSS_BOTTOM,
        unsafe_allow_html=True
    )


# ============================================================
# [07] LOAD MODEL AND DATASET
# ============================================================

try:

    # --------------------------------------------------------
    # [07-A] LOAD MODEL
    # --------------------------------------------------------

    package, MODEL_FILE = load_model()


    # --------------------------------------------------------
    # [07-B] LOAD DATASET
    # --------------------------------------------------------

    df, CSV_FILE = load_dataset()


    # --------------------------------------------------------
    # [07-C] VALIDATE DATASET
    # --------------------------------------------------------

    validate_dataset(df)


    # --------------------------------------------------------
    # [07-D] PREPARE DATASET
    # --------------------------------------------------------

    df = prepare_dataset(df)


    # --------------------------------------------------------
    # [07-E] EXTRACT MODEL COMPONENTS
    # --------------------------------------------------------

    model = package["model"]

    feature_columns = package["feature_columns"]

    train_medians = package["train_medians"]


    # --------------------------------------------------------
    # [07-F] CALCULATE MODEL HISTORY REQUIREMENT
    # --------------------------------------------------------

    HISTORY_DAYS = get_model_history_days(
        feature_columns
    )


# ------------------------------------------------------------
# [07-G] LOADING ERROR HANDLING
# ------------------------------------------------------------

except Exception as e:

    st.error(
        "❌ System file loading failed"
    )

    st.exception(e)

    st.stop()


# ============================================================
# [08] APPLICATION PAGE LIST
# ============================================================

PAGES = [

    "🏠 Home",
    "🔮 Rain Prediction",
    "🌱 Agriculture Irrigation (কৃষি সেচ ব্যবস্থা)",
    "📂 Historical Data",
    "📊 Analytics",
    "ℹ️ About"

]


# ============================================================
# [09] PAGE SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = PAGES[0]


if st.session_state.page not in PAGES:
    st.session_state.page = PAGES[0]


# ============================================================
# [10] SIDEBAR NAVIGATION CSS
# ============================================================

st.markdown(
    """
<style>

/* =========================================================
   [10-A] SIDEBAR CONTAINER
========================================================= */

[data-testid="stSidebar"] > div:first-child {
    padding-top: 0.6rem !important;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.10) !important;
    margin: 0.9rem 0 !important;
}


/* =========================================================
   [10-B] SIDEBAR BRAND
========================================================= */

.sb-brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.4rem 0.4rem 0.2rem 0.4rem;
}

.sb-logo {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    background: linear-gradient(135deg, #168F87, #55D6C2);
    box-shadow: 0 6px 16px rgba(22,143,135,0.35);
}

.sb-title {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.05rem;
    color: #FFFFFF;
    line-height: 1.2;
}

.sb-sub {
    font-size: 0.72rem;
    color: #8FB3C4;
    letter-spacing: 0.02em;
}


/* =========================================================
   [10-C] SIDEBAR SECTION LABELS
========================================================= */

.sb-section {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6F94A6;
    padding: 0.3rem 0.5rem 0.4rem 0.5rem;
}


/* =========================================================
   [10-D] SIDEBAR NAVIGATION ITEMS
========================================================= */

[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] {
    gap: 0.25rem !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    width: 100% !important;
    padding: 0.7rem 0.9rem !important;
    border-radius: 10px !important;
    border-left: 3px solid transparent !important;
    background: transparent !important;
    cursor: pointer !important;
    transition: all 0.18s ease !important;
}


/* =========================================================
   [10-E] ACTIVE NAVIGATION ITEM
========================================================= */

/* hide the radio circle */
[data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child {
    display: none !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label p {
    font-size: 0.93rem !important;
    font-weight: 500 !important;
    margin: 0 !important;
    color: #C9DCE6 !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(255,255,255,0.07) !important;
    transform: translateX(2px);
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover p {
    color: #FFFFFF !important;
}

/* active page */
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: linear-gradient(
        90deg,
        rgba(85,214,194,0.22),
        rgba(85,214,194,0.04)
    ) !important;
    border-left-color: #55D6C2 !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}


/* =========================================================
   [10-F] THEME SWITCH STYLING
========================================================= */

[data-testid="stSidebar"] [data-testid="stButtonGroup"] {
    width: 100% !important;
}

[data-testid="stSidebar"] [data-testid="stButtonGroup"] button {
    flex: 1 !important;
    min-height: 40px !important;
    border-radius: 10px !important;
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: #C9DCE6 !important;
    font-weight: 600 !important;
}

[data-testid="stSidebar"] [data-testid="stButtonGroup"] button p {
    color: inherit !important;
    white-space: nowrap !important;
    overflow: visible !important;
    text-overflow: clip !important;
    font-size: 0.86rem !important;
}

[data-testid="stSidebar"] [data-testid="stButtonGroup"] {
    display: flex !important;
    gap: 0.4rem !important;
}

[data-testid="stSidebar"] [data-testid="stButtonGroup"] button {
    flex: 1 1 0 !important;
    min-width: 0 !important;
    padding-left: 0.4rem !important;
    padding-right: 0.4rem !important;
}

[data-testid="stSidebar"] [data-testid="stButtonGroup"] button [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] [data-testid="stButtonGroup"] button div {
    overflow: visible !important;
    text-overflow: clip !important;
    white-space: nowrap !important;
}

[data-testid="stSidebar"] [data-testid="stButtonGroup"] button[data-testid="stBaseButton-segmented_controlActive"] {
    background: linear-gradient(135deg, #168F87, #1F9E92) !important;
    border-color: #168F87 !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 12px rgba(22,143,135,0.30) !important;
}


/* =========================================================
   [10-G] SIDEBAR FOOTER NOTE
========================================================= */

.sb-note {
    font-size: 0.72rem;
    color: #6F94A6;
    text-align: center;
    padding-top: 0.8rem;
    line-height: 1.6;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# [11] SIDEBAR BRAND
# ============================================================

st.sidebar.markdown(
    """
    <div class="sb-brand">
        <div class="sb-logo">🌧️</div>
        <div>
            <div class="sb-title">Smart Rain & Agriculture</div>
            <div class="sb-sub">Bangladesh Forecast System</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()


# ============================================================
# [12] SIDEBAR NAVIGATION
# ============================================================

st.sidebar.markdown(
    "<div class='sb-section'>Menu</div>",
    unsafe_allow_html=True
)

page_index = PAGES.index(
    st.session_state.page
)

selected_page = st.sidebar.radio(
    "Navigation",
    PAGES,
    index=page_index,
    label_visibility="collapsed"
)


# ============================================================
# [13] THEME SWITCH
# ============================================================

# ------------------------------------------------------------
# [13-A] THEME SELECTION
# ------------------------------------------------------------

st.sidebar.divider()

st.sidebar.markdown(
    "<div class='sb-section'>Appearance</div>",
    unsafe_allow_html=True
)

theme_choice = st.sidebar.segmented_control(
    "Theme",
    options=list(THEME_LABELS.values()),
    default=THEME_LABELS[st.session_state.theme],
    label_visibility="collapsed"
)


# ------------------------------------------------------------
# [13-B] THEME CONVERSION
# ------------------------------------------------------------

# if user clicks the active one (None), keep current theme
if theme_choice is None:
    theme_choice = THEME_LABELS[st.session_state.theme]

new_theme = "dark" if "Dark" in theme_choice else "light"


# ------------------------------------------------------------
# [13-C] THEME STATE UPDATE
# ------------------------------------------------------------

if new_theme != st.session_state.theme:
    st.session_state.theme = new_theme
    st.query_params["theme"] = new_theme
    apply_native_theme(new_theme)
    st.rerun()


# ============================================================
# [14] DARK THEME CUSTOM CSS
# ============================================================

if st.session_state.theme == "dark":

    # --------------------------------------------------------
    # [14-A] DARK PLOTLY THEME
    # --------------------------------------------------------

    pio.templates["monsoon"].layout.font.color = "#E6EDF3"
    pio.templates["monsoon"].layout.title.font.color = "#7FE0D2"
    pio.templates["monsoon"].layout.xaxis.gridcolor = "#263545"
    pio.templates["monsoon"].layout.yaxis.gridcolor = "#263545"


    # --------------------------------------------------------
    # [14-B] DARK ROOT VARIABLES
    # --------------------------------------------------------

    st.markdown(
        """
<style>

:root {
    --bg: #0E1621;
    --card: #16212E;
    --ink: #E6EDF3;
    --text: #E6EDF3;
    --muted: #9FB0BF;
    --indigo: #7FE0D2;
    --line: #263545;
}


/* =========================================================
   [14-C] DARK HEADINGS
========================================================= */

[data-testid="stMain"] h1,
[data-testid="stMain"] h2,
[data-testid="stMain"] h3,
[data-testid="stMain"] h4,
.section-title {
    color: #7FE0D2 !important;
}


/* =========================================================
   [14-D] DARK HERO
========================================================= */

/* keep hero text white */
.hero h1, .hero p, .hero-num, .hero-label {
    color: #FFFFFF !important;
}


/* =========================================================
   [14-E] DARK STANDARD CARDS
========================================================= */

.card {
    background: #16212E !important;
    border-color: #263545 !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.35) !important;
}

.card p, .card span {
    color: #E6EDF3 !important;
}


/* =========================================================
   [14-F] DARK AGRICULTURE CARDS
========================================================= */

.agri-card {
    background: linear-gradient(135deg, #13291F, #16212E) !important;
    border-color: #245A3A !important;
    border-left-color: #2E8B57 !important;
}

.agri-card h1,
.agri-card h2,
.agri-card h3,
.agri-card h4 {
    color: #6FD39A !important;
}

.agri-card p {
    color: #E6EDF3 !important;
}


/* =========================================================
   [14-G] DARK RESULT CARDS
========================================================= */

.result-card {
    background: linear-gradient(135deg, #13291F, #16212E) !important;
    border-color: #245A3A !important;
}

.result-card h1,
.result-card h2,
.result-card h3,
.result-card p {
    color: #6FD39A !important;
}


/* =========================================================
   [14-G-01] AGRICULTURE SUMMARY CARD — DARK MODE FIX
========================================================= */

[data-testid="stMain"] .summary-card {
    background: #FFFFFF !important;
    color: #1F2D3D !important;
    border-color: #DFE8E4 !important;
}

[data-testid="stMain"] .summary-card,
[data-testid="stMain"] .summary-card p,
[data-testid="stMain"] .summary-card ul,
[data-testid="stMain"] .summary-card li,
[data-testid="stMain"] .summary-card li span,
[data-testid="stMain"] .summary-card li strong,
[data-testid="stMain"] .summary-card li b {
    color: #1F2D3D !important;
    -webkit-text-fill-color: #1F2D3D !important;
    opacity: 1 !important;
    filter: none !important;
}

[data-testid="stMain"] .summary-card .summary-title {
    color: #0B7F59 !important;
    -webkit-text-fill-color: #0B7F59 !important;
}

[data-testid="stMain"] .summary-card li strong,
[data-testid="stMain"] .summary-card li b {
    color: #102A43 !important;
    -webkit-text-fill-color: #102A43 !important;
}


/* =========================================================
   [14-H] DARK WIDGET TEXT
========================================================= */

/* ---------------------------------------------------------
   DARK MODE TEXT FIX
   radio / checkbox / toggle / labels / tabs
--------------------------------------------------------- */

[data-testid="stMain"] [data-testid="stRadio"]:not(#x) label:not(#x),
[data-testid="stMain"] [data-testid="stRadio"]:not(#x) label:not(#x) *,
[data-testid="stMain"] [data-testid="stRadio"]:not(#x) p:not(#x),
[data-testid="stMain"] [data-testid="stRadio"]:not(#x) span:not(#x),
[data-testid="stMain"] [data-testid="stRadio"]:not(#x) div:not(#x),
[data-testid="stMain"] [data-testid="stCheckbox"]:not(#x) label:not(#x),
[data-testid="stMain"] [data-testid="stCheckbox"]:not(#x) label:not(#x) *,
[data-testid="stMain"] [data-testid="stToggle"]:not(#x) label:not(#x),
[data-testid="stMain"] [data-testid="stToggle"]:not(#x) label:not(#x) *,
[data-testid="stMain"] [data-testid="stWidgetLabel"]:not(#x),
[data-testid="stMain"] [data-testid="stWidgetLabel"]:not(#x) *,
[data-testid="stMain"] button[role="tab"]:not(#x) p:not(#x),
[data-testid="stMain"] [data-testid="stCaptionContainer"]:not(#x),
[data-testid="stMain"] [data-testid="stCaptionContainer"]:not(#x) * {
    color: #E6EDF3 !important;
    -webkit-text-fill-color: #E6EDF3 !important;
    opacity: 1 !important;
    filter: none !important;
}


/* selected radio */
[data-testid="stMain"] [data-testid="stRadio"]:not(#x) label:not(#x):has(input:checked) p:not(#x) {
    color: #7FE0D2 !important;
    -webkit-text-fill-color: #7FE0D2 !important;
    font-weight: 600 !important;
}

hr {
    border-color: #263545 !important;
}


/* =========================================================
   [14-I] DARK BUTTONS
========================================================= */

/* buttons (quick navigation etc.) */
.stButton > button:not(#x):not([kind="primary"]):not([data-testid="stBaseButton-primary"]) {
    background: #16212E !important;
    border: 1.5px solid #2F4A5E !important;
    color: #E6EDF3 !important;
}

.stButton > button:not(#x):not([kind="primary"]):not([data-testid="stBaseButton-primary"]):hover {
    background: #1F3446 !important;
    border-color: #55D6C2 !important;
    color: #7FE0D2 !important;
}

.stButton > button[kind="primary"]:not(#x),
.stButton > button[data-testid="stBaseButton-primary"]:not(#x) {
    background: linear-gradient(135deg, #168F87, #1F9E92) !important;
    border: 1.5px solid #55D6C2 !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 14px rgba(22,143,135,0.35) !important;
}

.stButton > button[kind="primary"]:not(#x) p,
.stButton > button[data-testid="stBaseButton-primary"]:not(#x) p {
    color: #FFFFFF !important;
}


/* =========================================================
   [14-J] DARK FOOTER
========================================================= */

.footer {
    color: #9FB0BF !important;
}

.footer b {
    color: #E6EDF3 !important;
}


/* =========================================================
   [14-K] DARK SIDEBAR
========================================================= */

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #08121F 0%, #0C1A2A 100%) !important;
    border-right: 1px solid #1B2A3A !important;
}

</style>
""",
        unsafe_allow_html=True
    )


# ============================================================
# [15] RADIO OPTION BOX CSS
# ============================================================

# ------------------------------------------------------------
# [15-A] RADIO BACKGROUND CONFIGURATION
# ------------------------------------------------------------

if st.session_state.theme == "dark":

    RB = {
        "bg": "#16212E",
        "border": "#33475A",
        "hover_bg": "#1F3446",
        "hover_border": "#55D6C2",
        "sel_bg": "rgba(85,214,194,0.14)",
        "sel_border": "#55D6C2",
        "shadow": "rgba(0,0,0,0.35)",
    }

else:

    RB = {
        "bg": "#FFFFFF",
        "border": "#D5DEE7",
        "hover_bg": "#E8F7F5",
        "hover_border": "#168F87",
        "sel_bg": "#E8F7F5",
        "sel_border": "#168F87",
        "shadow": "rgba(22,143,135,0.18)",
    }


# ------------------------------------------------------------
# [15-B] RADIO CSS TEMPLATE
# ------------------------------------------------------------

RADIO_BOX_CSS = """
<style>

[data-testid="stMain"] [data-testid="stRadio"]:not(#x) div[role="radiogroup"]:not(#x) {
    gap: 0.55rem !important;
}


/* each option = a box */
[data-testid="stMain"] [data-testid="stRadio"]:not(#x) label:not(#x) {
    background: __BG__ !important;
    border: 1.5px solid __BORDER__ !important;
    border-radius: 12px !important;
    padding: 0.75rem 1rem !important;
    margin: 0 !important;
    width: 100% !important;
    box-sizing: border-box !important;
    display: flex !important;
    align-items: center !important;
    cursor: pointer !important;
    transition: background 0.18s ease, border-color 0.18s ease,
                box-shadow 0.18s ease, transform 0.18s ease !important;
}


/* mouse over -> highlight */
[data-testid="stMain"] [data-testid="stRadio"]:not(#x) label:not(#x):hover {
    background: __HOVER_BG__ !important;
    border-color: __HOVER_BORDER__ !important;
    box-shadow: 0 4px 14px __SHADOW__ !important;
    transform: translateY(-1px) !important;
}


/* selected option */
[data-testid="stMain"] [data-testid="stRadio"]:not(#x) label:not(#x):has(input:checked) {
    background: __SEL_BG__ !important;
    border-color: __SEL_BORDER__ !important;
    box-shadow: 0 0 0 1px __SEL_BORDER__ !important;
}


/* keyboard focus */
[data-testid="stMain"] [data-testid="stRadio"]:not(#x) label:not(#x):focus-within {
    border-color: __HOVER_BORDER__ !important;
}

</style>
"""


# ------------------------------------------------------------
# [15-C] REPLACE RADIO THEME VARIABLES
# ------------------------------------------------------------

for _k, _v in {
    "__BG__": RB["bg"],
    "__BORDER__": RB["border"],
    "__HOVER_BG__": RB["hover_bg"],
    "__HOVER_BORDER__": RB["hover_border"],
    "__SEL_BG__": RB["sel_bg"],
    "__SEL_BORDER__": RB["sel_border"],
    "__SHADOW__": RB["shadow"],
}.items():

    RADIO_BOX_CSS = RADIO_BOX_CSS.replace(_k, _v)


# ------------------------------------------------------------
# [15-D] APPLY RADIO CSS
# ------------------------------------------------------------

st.markdown(
    RADIO_BOX_CSS,
    unsafe_allow_html=True
)


# ============================================================
# [16] MOBILE / PHONE OPTIMISATION
# ============================================================

st.markdown(
    """
<style>

@media (max-width: 768px) {

    /* =====================================================
       [16-A] MOBILE LAYOUT
    ===================================================== */

    /* stop sideways scrolling */
    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        overflow-x: hidden !important;
    }

    .block-container {
        padding: 1rem 0.9rem 4rem 0.9rem !important;
    }


    /* =====================================================
       [16-B] MOBILE HEADINGS
    ===================================================== */

    [data-testid="stMain"] h1 {
        font-size: 1.55rem !important;
        line-height: 1.3 !important;
    }

    [data-testid="stMain"] h2 {
        font-size: 1.3rem !important;
    }

    [data-testid="stMain"] h3 {
        font-size: 1.15rem !important;
    }

    .section-title {
        font-size: 1.05rem !important;
        margin-top: 1.2rem !important;
        margin-bottom: 0.8rem !important;
    }


    /* =====================================================
       [16-C] MOBILE CARDS
    ===================================================== */

    .card,
    .agri-card,
    .result-card {
        padding: 1rem !important;
        border-radius: 14px !important;
    }


    /* =====================================================
       [16-D] MOBILE HERO
    ===================================================== */

    /* hero stats: two per row */
    .hero-stats {
        gap: 1rem !important;
    }

    .hero-stat {
        flex: 1 1 40% !important;
    }


    /* =====================================================
       [16-E] MOBILE INPUTS
    ===================================================== */

    /* inputs: 16px stops iPhone auto-zoom, bigger touch area */
    [data-testid="stMain"] input,
    [data-testid="stMain"] textarea {
        font-size: 16px !important;
    }

    [data-testid="stMain"] [data-baseweb="select"] > div {
        min-height: 46px !important;
    }


    /* =====================================================
       [16-F] MOBILE BUTTONS
    ===================================================== */

    /* buttons: full width, finger friendly */
    .stButton > button,
    [data-testid="stFormSubmitButton"] button {
        min-height: 48px !important;
        width: 100% !important;
    }


    /* =====================================================
       [16-G] MOBILE RADIO
    ===================================================== */

    /* radio boxes: bigger touch target */
    [data-testid="stMain"] [data-testid="stRadio"]:not(#x) label:not(#x) {
        min-height: 48px !important;
        padding: 0.8rem 0.9rem !important;
    }


    /* =====================================================
       [16-H] MOBILE METRICS
    ===================================================== */

    div[data-testid="stMetric"] {
        padding: 0.8rem !important;
    }

    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] * {
        font-size: 1.4rem !important;
    }


    /* =====================================================
       [16-I] MOBILE QUICK NAVIGATION
    ===================================================== */

    /* bottom quick navigation: 2 x 2 grid */
    [data-testid="stHorizontalBlock"]:has([class*="st-key-quick_nav_"]) {
        flex-wrap: wrap !important;
        gap: 0.6rem !important;
    }

    [data-testid="stHorizontalBlock"]:has([class*="st-key-quick_nav_"]) > [data-testid="stColumn"],
    [data-testid="stHorizontalBlock"]:has([class*="st-key-quick_nav_"]) > [data-testid="column"] {
        flex: 1 1 calc(50% - 0.6rem) !important;
        min-width: calc(50% - 0.6rem) !important;
    }


    /* =====================================================
       [16-J] MOBILE CHARTS
    ===================================================== */

    /* charts: hide hover toolbar (it covers the chart on touch) */
    .js-plotly-plot .modebar-container {
        display: none !important;
    }


    /* =====================================================
       [16-K] MOBILE TABLES
    ===================================================== */

    /* tables scroll inside their own box */
    [data-testid="stDataFrame"] {
        max-width: 100% !important;
    }


    /* =====================================================
       [16-L] MOBILE SIDEBAR
    ===================================================== */

    /* sidebar menu: bigger touch rows */
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        padding: 0.85rem 0.9rem !important;
    }


    /* =====================================================
       [16-M] MOBILE FOOTER
    ===================================================== */

    .footer {
        font-size: 0.85rem !important;
        padding: 1.5rem 0 1rem !important;
    }
}


/* =========================================================
   [16-N] SMALL PHONE OPTIMISATION
========================================================= */

@media (max-width: 420px) {

    .hero {
        padding: 1.2rem !important;
    }

    .hero h1 {
        font-size: 1.3rem !important;
    }

    .hero p {
        font-size: 0.9rem !important;
    }

    .hero-num {
        font-size: 1.15rem !important;
    }
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# [17] PAGE UPDATE
# ============================================================

if selected_page != st.session_state.page:

    st.session_state.page = selected_page

    st.rerun()


# ============================================================
# [18] MAIN PAGE ROUTING
# ============================================================

page = st.session_state.page


# ------------------------------------------------------------
# [18-A] HOME
# ------------------------------------------------------------

if page == "🏠 Home":

    show_home(df)


# ------------------------------------------------------------
# [18-B] RAIN PREDICTION
# ------------------------------------------------------------

elif page == "🔮 Rain Prediction":

    show_prediction(
        df=df,
        model=model,
        feature_columns=feature_columns,
        train_medians=train_medians,
        history_days=HISTORY_DAYS
    )


# ------------------------------------------------------------
# [18-C] AGRICULTURE & IRRIGATION
# ------------------------------------------------------------

elif page == "🌱 Agriculture Irrigation (কৃষি সেচ ব্যবস্থা)":

    show_agriculture(
        df=df,
        model=model,
        feature_columns=feature_columns,
        train_medians=train_medians,
        history_days=HISTORY_DAYS
    )


# ------------------------------------------------------------
# [18-D] HISTORICAL DATA
# ------------------------------------------------------------

elif page == "📂 Historical Data":

    show_data_page(df)


# ------------------------------------------------------------
# [18-E] ANALYTICS
# ------------------------------------------------------------

elif page == "📊 Analytics":

    show_analytics(df)


# ------------------------------------------------------------
# [18-F] ABOUT
# ------------------------------------------------------------

elif page == "ℹ️ About":

    show_about()


# ============================================================
# [19] QUICK NAVIGATION
# ============================================================

# ------------------------------------------------------------
# [19-A] QUICK NAVIGATION COLUMNS
# ------------------------------------------------------------

st.divider()

cols = st.columns(4)


# ------------------------------------------------------------
# [19-B] QUICK PAGE LIST
# ------------------------------------------------------------

quick_pages = [

    (
        "🏠 Home",
        "🏠 Home"
    ),

    (
        "🔮 Prediction",
        "🔮 Rain Prediction"
    ),

    (
        "🌱 Agriculture",
        "🌱 Agriculture Irrigation (কৃষি সেচ ব্যবস্থা)"
    ),

    (
        "📊 Analytics",
        "📊 Analytics"
    )

]


# ------------------------------------------------------------
# [19-C] QUICK NAVIGATION BUTTONS
# ------------------------------------------------------------

for col, (button_text, target_page) in zip(
    cols,
    quick_pages
):

    if col.button(
        button_text,
        width="stretch",
        key=f"quick_nav_{target_page}",
        type=(
            "primary"
            if st.session_state.page == target_page
            else "secondary"
        )
    ):

        st.session_state.page = target_page

        st.rerun()


# ============================================================
# [20] APPLICATION FOOTER
# ============================================================

st.markdown(
    """
    <div class='footer'>

    <b>
    🌧️ Bangladesh Smart Rainfall & Agriculture System
    </b>

    <br>

    🌱 Rain Prediction • Smart Irrigation • Agriculture

    <br>

    Made by

    <b>
    Shams, Tasrif & Jishan
    </b>

    </div>
    """,
    unsafe_allow_html=True
)