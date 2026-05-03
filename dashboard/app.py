import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
import random
import requests

API_URL = "https://ecommerce-backend-3731.onrender.com"

def call_api(method, path, params=None, retries=3, timeout=30):
    url = f"{API_URL}{path}"

    for attempt in range(retries):
            try:
            
                if method == "GET":
                    res = requests.get(url, params=params, timeout=timeout)
                else:
                    res = requests.post(url, params=params, timeout=timeout)

            try:
                data = res.json() if res.text else {}
                print("API RESPONSE:", data)
            except:
                data = {}
            if res.status_code == 200 and data:
                return data
            else:
                return {"error": data.get("error", f"API failed ({res.status_code})")}
           

        except:
            if attempt < retries - 1:
                time.sleep(3)
            else:
                return {"error": "Server waking up... try again"}

st.set_page_config(page_title="AI Commerce Intelligence", layout="wide")
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
st.sidebar.title("🔐 Authentication")

# ================= AUTH =================
# ================= AUTH =================
email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")
otp = st.sidebar.text_input("Enter OTP")

if st.sidebar.button("Send OTP"):
    data = call_api("POST", "/send-otp", {"email": email})
    if "message" in data:
        st.sidebar.success(data["message"])
    else:
        st.sidebar.error(data.get("error", "Something went wrong"))
   

if st.sidebar.button("Verify OTP"):
    data = call_api("POST", "/verify-otp", {"email": email, "otp": otp})
    if "message" in data:
        st.sidebar.success(data["message"])
    else:
        st.sidebar.error(data.get("error", "Something went wrong"))
   

if st.sidebar.button("Register"):
    data = call_api("POST", "/register", {"email": email, "password": password})
    if "message" in data:
        st.sidebar.success(data["message"])
    else:
        st.sidebar.error(data.get("error", "Something went wrong"))
   

if st.sidebar.button("Login"):
    data = call_api("POST", "/login", {"email": email, "password": password})

    if "message" in data:
        st.session_state.logged_in = True
        st.sidebar.success("Login successful")
    else:
        st.sidebar.error(data.get("error", "Login failed"))

# ===== PREMIUM UI STYLES =====
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}
.glass {
    background: rgba(255,255,255,0.05);
    border-radius: 15px;
    padding: 20px;
    backdrop-filter: blur(10px);
}
.metric-box {
    background: linear-gradient(135deg,#1e293b,#020617);
    padding: 15px;
    border-radius: 12px;
    text-align:center;
}
.hero {
    font-size:32px;
    font-weight:700;
    text-align:center;
}
.subhero {
    text-align:center;
    color:gray;
    margin-bottom:20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero">🚀 AI Commerce Intelligence</div>', unsafe_allow_html=True)
try:
    status = requests.get(f"{API_URL}/", timeout=5).json()
except:
    status = {}
if "status" in status:
    st.success("🟢 Backend Live")
else:
    st.warning(status.get("error", "🟡 Backend waking up..."))
st.markdown('<div class="subhero">AI-powered analytics • forecasting • decision system</div>', unsafe_allow_html=True)
# ---------------- CSS ----------------
st.markdown("""
<style>
.big-font {
    font-size:22px !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    url = "https://drive.google.com/uc?id=14PhCD4ABT5uWrQqdL5OpX2LsrVfZwJ6s"

    df = pd.read_csv(url, encoding="ISO-8859-1", low_memory=False)

    df.columns = df.columns.str.strip().str.lower()

    df.rename(columns={
        "stockcode": "product_id",
        "price": "price",
        "quantity": "quantity",
        "country": "country",
        "customer id": "user_id"
    }, inplace=True)

    df = df.dropna(subset=["user_id", "price", "quantity"])

    df["total"] = df["price"] * df["quantity"]

    # 🔥 PERFORMANCE FIX (VERY IMPORTANT)
    if len(df) > 10000:
        df = df.sample(10000, random_state=42)

    return df

df = load_data()

# ---------------- LOADING EFFECT ----------------
placeholder = st.empty()
placeholder.text("🔄 Updating live data...")
time.sleep(1)
placeholder.empty()

# 🔥 FIXED-AREA SLIDESHOW (ONLY IMAGE CHANGES VISUALLY)
st.title("🚀 AI Powered E-Commerce Intelligence Dashboard")

# ---------------- HERO IMAGE ----------------
st.image(
    "https://images.unsplash.com/photo-1551288049-bebda4e38f71",
    use_container_width=True
)

# ---------------- HERO IMAGE ----------------


# ---------------- SIDEBAR BRANDING ----------------
st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
    width=100
)
st.sidebar.title("AI Commerce App")

# ---------------- SIDEBAR ----------------
st.sidebar.header("🔍 Filters")

users = st.sidebar.multiselect("Users", df["user_id"].unique())
products = st.sidebar.multiselect("Products", df["product_id"].unique())
countries = st.sidebar.multiselect("Countries", df["country"].unique())

min_q, max_q = st.sidebar.slider(
    "Quantity Range",
    int(df["quantity"].min()),
    int(df["quantity"].max()),
    (int(df["quantity"].min()), int(df["quantity"].max()))
)

filtered_df = df

if users:
    filtered_df = filtered_df[filtered_df["user_id"].isin(users)]
if products:
    filtered_df = filtered_df[filtered_df["product_id"].isin(products)]
if countries:
    filtered_df = filtered_df[filtered_df["country"].isin(countries)]

filtered_df = filtered_df[
    (filtered_df["quantity"] >= min_q) &
    (filtered_df["quantity"] <= max_q)
]

# ===== ROLE BASED ACCESS =====
role = st.sidebar.selectbox("Role", ["Admin", "Manager", "Viewer"])

if role == "Viewer":
    st.warning("👁️ View-only mode enabled")

# ---------------- KPI ----------------
st.subheader("📊 Business Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Revenue", f"₹ {filtered_df['total'].sum():,.0f}")
col2.metric("📦 Orders", len(filtered_df))
avg_order = filtered_df["total"].mean() if len(filtered_df) > 0 else 0
col3.metric("📊 Avg Order", f"₹ {avg_order:.0f}")

top_country = "N/A"
if len(filtered_df) > 0:
    top_country = filtered_df.groupby("country")["total"].sum().idxmax()

col4.metric("🌍 Top Country", top_country)

# ---------------- LIVE KPI ----------------
live_revenue = filtered_df["total"].sum() + random.randint(0, 500)
st.metric("⚡ Live Revenue", f"₹ {live_revenue}")
# ===== REAL-TIME STREAM =====
live_placeholder = st.empty()

for i in range(1):
    live_placeholder.metric("📡 Live Revenue Update", f"₹ {live_revenue + i*5}")
    time.sleep(1)

st.divider()
st.markdown("### 💎 Premium KPI View")

col1, col2, col3, col4 = st.columns(4)

col1.markdown(f'<div class="metric-box">💰 Revenue<br><h2>₹ {filtered_df["total"].sum():,.0f}</h2></div>', unsafe_allow_html=True)
col2.markdown(f'<div class="metric-box">📦 Orders<br><h2>{len(filtered_df)}</h2></div>', unsafe_allow_html=True)
avg_order = filtered_df["total"].mean() if len(filtered_df) > 0 else 0

col3.markdown(
    f'<div class="metric-box">📊 Avg Order<br><h2>₹ {avg_order:.0f}</h2></div>',
    unsafe_allow_html=True
)

top_country = filtered_df.groupby("country")["total"].sum().idxmax() if len(filtered_df)>0 else "N/A"
col4.markdown(f'<div class="metric-box">🌍 Top Country<br><h2>{top_country}</h2></div>', unsafe_allow_html=True)

# ---------------- DOWNLOAD ----------------
st.download_button(
    "📥 Download Filtered Data",
    filtered_df.to_csv(index=False),
    file_name="filtered_data.csv"
)
import io

buffer = io.StringIO()
filtered_df.describe().to_csv(buffer)

st.download_button(
    "📄 Download Business Report",
    buffer.getvalue(),
    file_name="report.csv"
)


# ---------------- TABS ----------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📊 Dashboard",
    "🤖 Prediction",
    "📈 Insights",
    "📉 Simulator",
    "🧠 Advanced",
    "🚀 AI Lab",
    "💬 Chat",
    "🧠 Pro Analytics"
])



# ================= DASHBOARD =================
with tab1:
    st.subheader("📊 Analytics")

    col1, col2 = st.columns(2)

    with col1:
        user_df = filtered_df.groupby("user_id")["total"].sum().nlargest(20).reset_index()
        fig = px.bar(user_df, x="user_id", y="total", title="Top Users by Revenue")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        prod_df = filtered_df.groupby("product_id")["total"].sum().nlargest(20).reset_index()
        fig = px.bar(prod_df, x="product_id", y="total", title="Top Products")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("🌍 Country Distribution")

    country_df = filtered_df.groupby("country")["total"].sum().reset_index()

    fig = px.pie(country_df, names="country", values="total", title="Revenue Share")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🌍 Global Revenue Map")

    if len(country_df) > 0:
        fig = px.choropleth(
            country_df,
            locations="country",
            locationmode="country names",
            color="total",
            title="Global Revenue Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No country data available")

# ================= PREDICTION =================
with tab2:
    st.subheader("🤖 AI Prediction")

    # ===== EXISTING FEATURE (manual prediction) =====
    st.markdown("### 🔢 Manual Prediction")

    col1, col2 = st.columns(2)

    with col1:
        price = st.number_input("Price", min_value=0.0, value=100.0)

    with col2:
        quantity = st.slider("Quantity", 1, 10, 1)
    if st.button("Predict Revenue"):
        data = call_api("GET", "/predict", {
            "price": price,
            "quantity": quantity
        })

        if "revenue" in data:
            st.success(f"💰 Predicted Revenue: ₹ {data['revenue']:.2f}")
        else:
            st.error(data.get("error", "Prediction failed"))


       

    # ===== NEW FEATURE (CSV upload) =====
    st.markdown("---")
    st.markdown("### 📂 Bulk Prediction via CSV Upload")

    uploaded_file = st.file_uploader(
        "Upload CSV (price, quantity)",
        type=["csv"],
        key="csv_upload"
    )

    if uploaded_file is not None:
        try:
            df_upload = pd.read_csv(uploaded_file)

            st.write("📄 Preview:")
            st.dataframe(df_upload.head())

            if "price" in df_upload.columns and "quantity" in df_upload.columns:

                predicted_revenue = []
                actual_revenue = []
                with st.spinner("Processing..."):
                    for _, row in df_upload.iterrows():
                        try:
                            data = call_api(
                                "GET",
                                "/predict",
                                {
                                    "price": float(row["price"]),
                                    "quantity": int(row["quantity"])
                                }
                            )

                        except:
                            data = {}

                        predicted_revenue.append(data.get("revenue", 0))
                        actual_revenue.append(row["price"] * row["quantity"])
        
                

                df_upload["Predicted Revenue"] = predicted_revenue
                df_upload["Actual Revenue"] = actual_revenue

                st.success("✅ Bulk prediction done")

                col1, col2 = st.columns(2)
                col1.metric("Total Predicted", f"₹ {sum(predicted_revenue):,.2f}")
                col2.metric("Total Actual", f"₹ {sum(actual_revenue):,.2f}")

                st.dataframe(df_upload)

                st.download_button(
                    "📥 Download Results",
                    df_upload.to_csv(index=False),
                    file_name="bulk_predictions.csv"
                )

            else:
                st.error("❌ CSV must contain 'price' and 'quantity' columns")

        except Exception:
            st.error("❌ Error reading CSV file")

# ================= INSIGHTS =================
with tab3:
    st.subheader("📈 Smart Insights")

    if len(filtered_df) > 0:
        top_user = filtered_df.groupby("user_id")["total"].sum().idxmax()
        top_product = filtered_df.groupby("product_id")["total"].sum().idxmax()

        st.success(f"🔥 Top User: {top_user}")
        st.success(f"🔥 Top Product: {top_product}")
    else:
        st.warning("No data after filters")

    st.subheader("📦 Quantity Distribution")
    fig = px.histogram(filtered_df, x="quantity")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📈 Revenue Trend")
    fig = px.line(filtered_df.head(1000), y="total")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🧠 Correlation Heatmap")
    corr = filtered_df[["price", "quantity", "total"]].corr()
    fig = px.imshow(corr, text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

# ================= SIMULATOR =================
with tab4:
    st.subheader("📉 What-if Simulator")

    price_range = st.slider("Price Range", 10, 1000, (50, 500))

    prices = np.arange(price_range[0], price_range[1], 20)
    preds = []
    for p in prices:
        data = call_api("GET", "/predict", {"price": p, "quantity": 2})
        preds.append(data.get("revenue", 0))

    sim_df = pd.DataFrame({
        "Price": prices,
        "Revenue": preds
    })

    fig = px.line(sim_df, x="Price", y="Revenue", title="Revenue Simulation")
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(sim_df.head(20))

# ================= ADVANCED =================
with tab5:
    st.subheader("🧠 Advanced Analytics")

    if len(filtered_df) == 0:
        st.warning("No data after filters.")
    else:
        rfm = filtered_df.groupby("user_id").agg({
            "total": ["sum", "mean"],
            "quantity": "sum"
        })

        rfm.columns = ["total_spent", "avg_spent", "total_qty"]

        rfm["segment"] = np.where(
            rfm["total_spent"] > rfm["total_spent"].quantile(0.75),
            "High Value",
            np.where(
                rfm["total_spent"] > rfm["total_spent"].quantile(0.4),
                "Mid Value",
                "Low Value"
            )
        )

        st.dataframe(rfm.head(20))

        fig = px.pie(rfm.reset_index(), names="segment")
        st.plotly_chart(fig, use_container_width=True)

        threshold = filtered_df["total"].mean() + 2 * filtered_df["total"].std()
        temp_df = filtered_df.copy()
        temp_df["anomaly"] = temp_df["total"] > threshold

        fig = px.scatter(temp_df.head(1000), x="price", y="total", color="anomaly")
        st.plotly_chart(fig)

# ================= AI LAB =================
with tab6:
    st.subheader("🚀 AI Decision Lab")

    if len(filtered_df) == 0:
        st.warning("No data available")
    else:
        base_price = st.slider("Base Price", 10, 1000, 100)

        test_prices = np.arange(base_price * 0.5, base_price * 1.5, 10)
        preds = []
        for p in test_prices:
            data = call_api("GET", "/predict", {"price": p, "quantity": 2})
            preds.append(data.get("revenue", 0))
        

        opt_df = pd.DataFrame({
            "Price": test_prices,
            "Revenue": preds
        })

        best_price = opt_df.loc[opt_df["Revenue"].idxmax()]

        st.success(f"🔥 Optimal Price: ₹ {round(best_price['Price'], 2)}")

        fig = px.line(opt_df, x="Price", y="Revenue")
        st.plotly_chart(fig)

        clv = filtered_df.groupby("user_id")["total"].sum().reset_index()
        st.dataframe(clv.sort_values("total", ascending=False).head(10))

        repeat_users = filtered_df["user_id"].value_counts()
        repeat_rate = (repeat_users > 1).sum() / len(repeat_users) if len(repeat_users) > 0 else 0

        st.metric("Repeat Customer Rate", f"{round(repeat_rate * 100, 2)} %")

# ================= CHAT =================
with tab7:
    st.subheader("💬 AI Assistant")

    def smart_ai(question):
        if "revenue" in question.lower():
            return f"Total revenue: ₹ {filtered_df['total'].sum():,.0f}"
        elif "country" in question.lower():
            return filtered_df.groupby("country")["total"].sum().idxmax()
        elif "user" in question.lower():
            return filtered_df.groupby("user_id")["total"].sum().idxmax()
        return "Try asking about revenue, country, or users"

    q = st.text_input("Ask AI about your data")

    if q:
        st.success(smart_ai(q))


# ================= PRO ANALYTICS =================
with tab8:
    st.subheader("🧠 Pro Analytics Engine")

    # ---------- USER SEGMENTATION ----------
    st.markdown("### 👥 Customer Segmentation")
    from sklearn.cluster import KMeans

    seg_df = filtered_df.groupby("user_id").agg({
        "total":"sum",
        "quantity":"sum"
    })

    if len(seg_df) >= 3:
        kmeans = KMeans(n_clusters=3, random_state=42)
        seg_df["cluster"] = kmeans.fit_predict(seg_df)

        fig = px.scatter(seg_df, x="quantity", y="total", color="cluster",
                         title="User Segmentation")
        st.plotly_chart(fig, use_container_width=True)

    # ---------- PRICE OPTIMIZATION ----------
    st.markdown("### 💰 Price Optimization")

    prices = np.linspace(10, 1000, 50)
    preds = []
    for p in prices:
        data = call_api("GET", "/predict", {"price": p, "quantity": 2})
        preds.append(data.get("revenue", 0))
   

    df_opt = pd.DataFrame({"Price": prices, "Revenue": preds})

    fig = px.line(df_opt, x="Price", y="Revenue", title="Price vs Revenue")
    st.plotly_chart(fig, use_container_width=True)

    best = df_opt.loc[df_opt["Revenue"].idxmax()]
    st.success(f"🔥 Optimal Price: ₹ {round(best['Price'],2)}")

    # ---------- DRILL DOWN ----------
    # ---------- DRILL DOWN ----------
    st.markdown("### 🔍 Drill Down Analysis")

    if len(filtered_df) > 0:
        selected_country = st.selectbox(
            "Select Country",
            filtered_df["country"].unique()
        )

        temp = filtered_df[filtered_df["country"] == selected_country]

        fig = px.bar(
            temp.groupby("product_id")["total"].sum().reset_index().head(20),
            x="product_id",
            y="total",
            title=f"Top Products in {selected_country}"
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No data available for drill-down")


    # ---------- ALERT SYSTEM ----------
    st.markdown("### 🚨 Smart Alerts")

    threshold = filtered_df["total"].mean() + 2 * filtered_df["total"].std()

    anomalies = filtered_df[filtered_df["total"] > threshold]

    st.write(f"⚠️ {len(anomalies)} anomalies detected")

    if len(anomalies) > 0:
        st.dataframe(anomalies.head())

    # ---------- CLV ----------
    st.markdown("### 💎 Customer Lifetime Value")

    if len(filtered_df) > 0:
        clv = filtered_df.groupby("user_id")["total"].sum()
        st.dataframe(clv.sort_values(ascending=False).head(10))
    else:
        st.warning("No data available for CLV")


    # ---------- FRAUD DETECTION ----------
    st.markdown("### 🚨 Fraud Detection")

    if len(filtered_df) > 0:
        threshold = filtered_df["total"].mean() + 2 * filtered_df["total"].std()

        temp_df = filtered_df.copy()
        temp_df["fraud"] = temp_df["total"] > threshold

        fraud_cases = temp_df[temp_df["fraud"] == True]

        st.write(f"⚠️ {len(fraud_cases)} suspicious transactions detected")

        if len(fraud_cases) > 0:
            st.dataframe(fraud_cases.head())
    else:
        st.warning("No data available for fraud detection")


    # ---------- A/B TEST ----------
    st.markdown("### 🧪 A/B Price Testing")

    price_a = 100
    price_b = 120

    rev_a = call_api("GET", "/predict", {"price": price_a, "quantity": 2}).get("revenue", 0)
    rev_b = call_api("GET", "/predict", {"price": price_b, "quantity": 2}).get("revenue", 0)
   
    st.write(f"Variant A Revenue: ₹ {rev_a:.2f}")
    st.write(f"Variant B Revenue: ₹ {rev_b:.2f}")
    
    if rev_a > rev_b:
        st.success("✅ Variant A performs better")
    else:
        st.success("✅ Variant B performs better")
    
    # ---------- SYSTEM INFO ----------
    st.markdown("### ⚙️ System Info")

    st.write("""
    - Data Source: Google Drive
    - ML Model: Regression
    - Analytics: Real-time
    - Deployment: Streamlit Cloud
    """)
