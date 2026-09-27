
# ABOUT.PY — QUICK DEVELOPER INDEX

#
# [01] IMPORTS
#      → Streamlit
#
# [02] HELPER FUNCTIONS
#      → Month cells HTML
#      → Crop chart HTML
#      → Crop season chart renderer
#
# [03] SHOW ABOUT FUNCTION
#      → Main About page controller
#
# [04] ABOUT PAGE TITLE
#      → "About System"
#
# [05] ABOUT PAGE CONTENT
#      → Rainfall Prediction System
#      → Smart Agriculture System
#      → Crop Sowing & Harvesting Season Chart
#      → Machine Learning
#      → Developed By
#
#      [05-A] RAINFALL PREDICTION SYSTEM
#             → Model
#             → Prediction target
#             → Features
#
#      [05-B] SMART AGRICULTURE SYSTEM
#             → Crop water requirement
#             → Land area
#             → Predicted rainfall
#             → Existing water
#             → Soil type
#             → Growth stage
#             → ET0
#             → Irrigation efficiency
#
#      [05-C] CROP SOWING & HARVESTING SEASON CHART
#             → Bangladesh crop calendar
#             → Sowing months
#             → Harvesting months
#             → Crop season
#
#      [05-D] MACHINE LEARNING
#             → CatBoost Regression explanation
#
#      [05-E] DEVELOPED BY
#             → Developer/team names
#
# ------------------------------------------------------------
# QUICK CHANGE GUIDE
# ------------------------------------------------------------
#
# About page title
#      → [04]
#
# Rainfall model information
#      → [05-A]
#
# Agriculture information
#      → [05-B]
#
# Crop season chart
#      → [05-C]
#
# Machine Learning information
#      → [05-D]
#
# Developer names
#      → [05-E]
#
# IMPORTANT:
# Developer comments MUST stay outside the st.markdown()
# content string.
#
# Never put [05-A], [05-B], [05-C], [05-D], [05-E] or other
# developer comments inside the Markdown content.
#




# [01] IMPORTS


import streamlit as st



# [02] HELPER FUNCTIONS



# ফসল বপন ও কাটার মৌসুম চার্ট (বাংলাদেশ)
# Crop Sowing & Harvesting Season Chart — Bangladesh
# Data source: crop-season-calendar-bangladesh.pdf


_MONTHS = [
    "জানু", "ফেব্রু", "মার্চ", "এপ্রিল", "মে", "জুন",
    "জুলাই", "আগস্ট", "সেপ্টে", "অক্টো", "নভে", "ডিসে",
]

_CROP_CHART = [
    {
        "crop": "ধান - আউশ (Aus Rice)",
        "detail": "বপন: চৈত্র - জ্যৈষ্ঠ &nbsp;|&nbsp; কাটা: শ্রাবণ - ভাদ্র",
        "season": "বর্ষাকালীন<br>(উপকারী)",
        "sow": ["মার্চ", "এপ্রিল", "মে"],
        "harvest": ["জুলাই", "আগস্ট", "সেপ্টে"],
    },
    {
        "crop": "ধান - আমন (Aman Rice)",
        "detail": "বপন: আষাঢ় - শ্রাবণ &nbsp;|&nbsp; কাটা: অগ্রহায়ণ - পৌষ",
        "season": "বর্ষাকালীন<br>(প্রধান)",
        "sow": ["জুন", "জুলাই"],
        "harvest": ["নভে", "ডিসে"],
    },
    {
        "crop": "ধান - বোরো (Boro Rice)",
        "detail": "বপন: অগ্রহায়ণ - পৌষ &nbsp;|&nbsp; কাটা: বৈশাখ - জ্যৈষ্ঠ",
        "season": "রবি<br>(শীতকাল)",
        "sow": ["নভে", "ডিসে"],
        "harvest": ["এপ্রিল", "মে"],
    },
    {
        "crop": "গম (Wheat)",
        "detail": "বপন: অগ্রহায়ণ - পৌষ &nbsp;|&nbsp; কাটা: চৈত্র - বৈশাখ",
        "season": "রবি<br>(শীতকাল)",
        "sow": ["নভে", "ডিসে"],
        "harvest": ["মার্চ", "এপ্রিল"],
    },
    {
        "crop": "ভুট্টা (Maize)",
        "detail": "বপন: কার্তিক - অগ্রহায়ণ &nbsp;|&nbsp; কাটা: চৈত্র - বৈশাখ",
        "season": "রবি<br>(শীতকাল)",
        "sow": ["অক্টো", "নভে"],
        "harvest": ["মার্চ", "এপ্রিল"],
    },
    {
        "crop": "আলু (Potato)",
        "detail": "বপন: কার্তিক - অগ্রহায়ণ &nbsp;|&nbsp; কাটা: মাঘ - ফাল্গুন",
        "season": "রবি<br>(শীতকাল)",
        "sow": ["নভে", "ডিসে"],
        "harvest": ["ফেব্রু", "মার্চ"],
    },
    {
        "crop": "সরিষা (Mustard)",
        "detail": "বপন: কার্তিক - অগ্রহায়ণ &nbsp;|&nbsp; কাটা: মাঘ - ফাল্গুন",
        "season": "রবি<br>(শীতকাল)",
        "sow": ["নভে", "ডিসে"],
        "harvest": ["ফেব্রু", "মার্চ"],
    },
    {
        "crop": "টমেটো (Tomato)",
        "detail": "বপন: কার্তিক - অগ্রহায়ণ &nbsp;|&nbsp; কাটা: মাঘ - চৈত্র",
        "season": "রবি<br>(শীতকাল)",
        "sow": ["নভে", "ডিসে"],
        "harvest": ["ফেব্রু", "মার্চ", "এপ্রিল"],
    },
    {
        "crop": "পেঁয়াজ (Onion)",
        "detail": "বপন: কার্তিক - অগ্রহায়ণ &nbsp;|&nbsp; কাটা: চৈত্র - বৈশাখ",
        "season": "রবি<br>(শীতকাল)",
        "sow": ["নভে", "ডিসে"],
        "harvest": ["মার্চ", "এপ্রিল"],
    },
]



# Crop Chart CSS


_CHART_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Bengali:wght@400;500;600;700&display=swap');

.bd-chart-block {
    font-family: 'Noto Sans Bengali', 'Nirmala UI', 'Vrinda',
                 'SolaimanLipi', 'Kalpurush', sans-serif;
    margin: 6px 0 4px 0;
}

.bd-chart-title {
    font-size: 20px;
    font-weight: 700;
    color: #0b3d3d;
    margin: 0 0 3px 0;
    line-height: 1.35;
}

.bd-chart-subtitle {
    font-size: 12.5px;
    color: #4a5c5c;
    margin: 0 0 14px 0;
    line-height: 1.5;
}

.bd-chart-scroll {
    width: 100%;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    border-radius: 4px;
}

table.bd-crop-chart {
    border-collapse: collapse;
    width: 100%;
    min-width: 1080px;
    table-layout: fixed;
    background: #ffffff;
    font-size: 12px;
}

table.bd-crop-chart th,
table.bd-crop-chart td {
    border: 1px solid #a9bcbc;
    padding: 6px 4px;
    vertical-align: middle;
}

table.bd-crop-chart thead th {
    background: #16595a;
    color: #ffffff;
    font-weight: 700;
    font-size: 12px;
    text-align: center;
    padding: 9px 3px;
    letter-spacing: .2px;
    white-space: nowrap;
}

table.bd-crop-chart thead th.col-crop,
table.bd-crop-chart thead th.col-season {
    text-align: left;
    padding-left: 9px;
}

table.bd-crop-chart td.cell-crop {
    background: #eaf2f1;
    text-align: left;
    padding: 8px 9px;
}

.bd-crop-name {
    display: block;
    font-weight: 700;
    font-size: 12.5px;
    color: #0b3d3d;
    line-height: 1.35;
}

.bd-crop-detail {
    display: block;
    font-size: 10.5px;
    color: #55696a;
    line-height: 1.45;
    margin-top: 3px;
}

table.bd-crop-chart td.cell-season {
    background: #eaf2f1;
    text-align: left;
    padding: 8px 9px;
    font-size: 11.5px;
    color: #0b3d3d;
    line-height: 1.45;
    font-weight: 500;
}

table.bd-crop-chart td.month-cell {
    background: #ffffff;
    text-align: center;
    padding: 7px 5px;
}

span.month-box {
    display: block;
    background: #d9d9d9;
    border: 1px solid #b6b6b6;
    border-radius: 5px;
    color: #1c1c1c;
    font-size: 11.5px;
    font-weight: 600;
    padding: 5px 4px;
    line-height: 1.2;
    white-space: nowrap;
}

.bd-chart-legend {
    margin-top: 10px;
    font-size: 11.5px;
    color: #3d4f4f;
    line-height: 1.6;
}

.bd-chart-note {
    margin-top: 8px;
    padding: 9px 12px;
    background: #f4f8f8;
    border-left: 4px solid #16595a;
    border-radius: 3px;
    font-size: 11.5px;
    color: #3d4f4f;
    line-height: 1.6;
}
</style>
"""



# Build Month Cells


def _month_cells_html(sow, harvest):
    """Build the 12 month <td> cells, merging consecutive equal labels."""

    labels = []

    for m in _MONTHS:

        if m in sow:
            labels.append("বপন")

        elif m in harvest:
            labels.append("কাটা")

        else:
            labels.append("")

    cells = []
    i = 0

    while i < len(labels):

        j = i

        while j + 1 < len(labels) and labels[j + 1] == labels[i]:
            j += 1

        span = j - i + 1
        label = labels[i]

        if label:

            cells.append(
                f'<td class="month-cell" colspan="{span}">'
                f'<span class="month-box">{label}</span>'
                f'</td>'
            )

        else:

            cells.append(
                f'<td class="month-cell" colspan="{span}"></td>'
            )

        i = j + 1

    return "".join(cells)



# Build Complete Crop Chart HTML


def _build_chart_html():

    colgroup = (
        '<colgroup>'
        '<col style="width:15%">'
        '<col style="width:10%">'
        + '<col style="width:6.25%">' * 12 +
        '</colgroup>'
    )

    thead = (
        '<thead><tr>'
        '<th class="col-crop">ফসল (Crop)</th>'
        '<th class="col-season">মৌসুম (Season)</th>'
        + "".join(f'<th>{m}</th>' for m in _MONTHS) +
        '</tr></thead>'
    )

    rows = []

    for item in _CROP_CHART:

        rows.append(
            "<tr>"
            f'<td class="cell-crop">'
            f'<span class="bd-crop-name">{item["crop"]}</span>'
            f'<span class="bd-crop-detail">{item["detail"]}</span>'
            f'</td>'
            f'<td class="cell-season">{item["season"]}</td>'
            + _month_cells_html(item["sow"], item["harvest"]) +
            "</tr>"
        )

    return (
        '<div class="bd-chart-block">'

        '<div class="bd-chart-title">'
        'ফসল বপন ও কাটার মৌসুম চার্ট (বাংলাদেশ)'
        '</div>'

        '<div class="bd-chart-subtitle">'
        'Crop Sowing &amp; Harvesting Season Chart — '
        'কোন ফসল কখন মৌসুম শুরু থেকে কখন শেষ, তার সাধারণ নির্দেশিকা'
        '</div>'

        '<div class="bd-chart-scroll">'

        f'<table class="bd-crop-chart">'
        f'{colgroup}'
        f'{thead}'
        f'<tbody>{"".join(rows)}</tbody>'
        f'</table>'

        '</div>'

        '<div class="bd-chart-legend">'
        '<strong>বর্ণনা:</strong> &nbsp;'
        'বপন = বীজ বপন মাস &nbsp;|&nbsp; '
        'কাটা = ফসল সংগ্রহ মাস'
        '</div>'

        '<div class="bd-chart-note">'
        '<strong>দ্রষ্টব্য:</strong> এই তথ্য বাংলাদেশ কৃষি সম্প্রসারণ '
        'অধিদপ্তর (DAE)-এর কৃষি তথ্য অনুসারে তৈরি করা হয়েছে। '
        'এলাকা ও জাতভেদে তারিখ কিছুটা ভিন্ন হতে পারে — সঠিক তথ্যের জন্য '
        'স্থানীয় কৃষি অফিসের পরামর্শ নিন।'
        '</div>'

        '</div>'
    )



# Render Crop Season Chart


def render_crop_season_chart():
    """Render the crop sowing / harvesting season chart."""

    st.markdown(
        _CHART_CSS,
        unsafe_allow_html=True
    )

    st.markdown(
        _build_chart_html(),
        unsafe_allow_html=True
    )



# [03] MAIN ABOUT PAGE FUNCTION

#
# Function:
#     show_about()
#
# This function displays the complete About page.
#


def show_about():


    
    # [04] ABOUT PAGE TITLE
    

    st.title(
        "ℹ️ About System"
    )


    
    # [05] ABOUT PAGE CONTENT
    
    #
    # IMPORTANT:
    # Keep this Markdown content clean.
    #
    # DO NOT put developer index comments inside this string.
    #
    

    st.markdown(

        """

        ### 🌧️ Bangladesh Rainfall Prediction System

        **Model:** CatBoost Regression

        **Prediction Target:** Daily Rainfall (mm)

        **Features:**
        Weather, Calendar, Lag, Rolling & Station Features


        ---


        ### 🌱 Smart Agriculture System

        এই অংশে ব্যবহারকারী জানতে পারবেন:

        - 🌾 কোন ফসল কত পানি চায়

        - 📐 জমির পরিমাণ অনুযায়ী মোট পানি

        - 🌧️ predicted rainfall অনুযায়ী সেচ কমবে কিনা

        - 💧 আগে থেকে থাকা পানি বিবেচনা

        - 🟫 মাটির ধরন অনুযায়ী পানি

        - 🌱 crop growth stage অনুযায়ী পানি

        - 💨 ET0 অনুযায়ী পানির চাহিদা

        - 🚿 irrigation efficiency অনুযায়ী সেচ

        """

    )


    
    # [05-C] CROP SOWING & HARVESTING SEASON CHART
    
    #
    # Bangladesh crop calendar
    # Shows sowing and harvesting months for major crops.
    #
    

    st.markdown("---")

    st.markdown(
        "### 📅 ফসল বপন ও কাটার মৌসুম চার্ট (বাংলাদেশ)"
    )

    render_crop_season_chart()


    
    # [05-D] MACHINE LEARNING
    

    st.markdown("---")

    st.markdown(

        """

        ### 🤖 Machine Learning

        এই system CatBoost Regression model ব্যবহার করে
        daily rainfall prediction করে.


        ---


        ### 👨‍💻 Developed By

        **Shams, Tasrif & Jishan**

        """

    )



# END OF FILE

#
# FINAL DEVELOPER MAP

#
# [01] Imports
#
# [02] Helper Functions
#       │
#       ├── _month_cells_html()
#       ├── _build_chart_html()
#       └── render_crop_season_chart()
#
# [03] show_about()
#       │
#       ├── [04] About Page Title
#       │
#       └── [05] About Page Content
#             │
#             ├── [05-A] Rainfall Prediction System
#             ├── [05-B] Smart Agriculture System
#             ├── [05-C] Crop Sowing & Harvesting Season Chart
#             ├── [05-D] Machine Learning
#             └── [05-E] Developed By
#

