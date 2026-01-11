import streamlit as st
import requests

# --- PAGE CONFIG ---
st.set_page_config(page_title="TikTok Auto-Order", page_icon="🚀")

try:
    SECRET_CODE = st.secrets["ACCESS_PASSWORD"]
    API_KEY = st.secrets["SMM_API_KEY"]
except FileNotFoundError:
    st.error("Secrets not found. Please set ACCESS_PASSWORD and SMM_API_KEY in your .streamlit/secrets.toml or Streamlit Cloud settings.")
    st.stop()

# Check query parameters (The "Special Link" logic)
query_params = st.query_params
url_code = query_params.get("secret", None)

# Initialize session state for login
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Logic: If URL has correct code OR user previously logged in
if url_code == SECRET_CODE:
    st.session_state.authenticated = True

# --- LOGIN SCREEN ---
if not st.session_state.authenticated:
    st.title("🔒 Restricted Access")
    user_input = st.text_input("Enter Access Code:", type="password")
    
    if st.button("Enter"):
        if user_input == SECRET_CODE:
            st.session_state.authenticated = True
            st.rerun() # Refresh to show the tool
        else:
            st.error("Wrong Code.")
    
    # Stop the script here if not authenticated
    st.stop()



API_URL = "https://smmglobe.com/api/v2"

# 28 Pre-filled positive comments
COMMENTS_LIST = [
    "The website actually works omg", "Amazing type shi", "Can't believe but it works", "Wow 😍", 
    "Great video", "i wasn't expecting it to actually work wow", "Thanks man", "This is def my brick",
    "Used it twice and worked as shown wow", "i hope this stays alive thanks", "Valid", "JAJAJJAJAJAJA", 
    "This is it", "Underrated", "Best video I've seen today", 
    "Lol how is this website actually working", "Fire 🔥", "Great stuff", "gonna check my fine shyt snap", 
    "I love this website lol", "WHO NEEDS HELP?", "keep spreading this", "Awesome", 
    "Can someone help me please?", "Interesting", "Shared it with my bff", "Saved for later", 
    "Make more vids like this please"
]

def place_order(service_id, link, quantity=None, comments=None):
    payload = {
        'key': API_KEY,
        'action': 'add',
        'service': service_id,
        'link': link
    }
    if comments:
        payload['comments'] = comments
    elif quantity:
        payload['quantity'] = quantity

    try:
        response = requests.post(API_URL, data=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

st.title("🚀 TikTok Bulk Order Tool")
st.markdown("Enter a TikTok link below to automatically place all 7 service orders.")

video_link = st.text_input("TikTok Video Link", placeholder="https://www.tiktok.com/@user/video/...")

orders_config = [
    {"id": 2630, "name": "Custom Comments", "qty": 28, "type": "comments"},
    {"id": 1299, "name": "Shares (S. Fast)", "qty": 100, "type": "default"},
    {"id": 3000, "name": "Shares (Real)", "qty": 20, "type": "default"},
    {"id": 557,  "name": "Saves (Never Stuck)", "qty": 100, "type": "default"},
    {"id": 3154, "name": "Saves/Favorites", "qty": 100, "type": "default"},
    {"id": 3050, "name": "Likes + Views", "qty": 50, "type": "default"},
    {"id": 3151, "name": "Likes (Female)", "qty": 20, "type": "default"},
]

if st.button("Place Orders", type="primary"):
    if not video_link:
        st.error("Please enter a valid link first.")
    else:
        st.write("---")
        progress_bar = st.progress(0)
        status_text = st.empty()
        results = []
        
        for index, order in enumerate(orders_config):
            status_text.text(f"Processing: {order['name']} (ID: {order['id']})...")
            
            if order['type'] == 'comments':
                comments_string = "\n".join(COMMENTS_LIST)
                resp = place_order(service_id=order['id'], link=video_link, comments=comments_string)
            else:
                resp = place_order(service_id=order['id'], link=video_link, quantity=order['qty'])
            
            is_success = 'order' in resp
            results.append({
                "Service": order['name'],
                "ID": order['id'],
                "Status": "✅ Success" if is_success else "❌ Failed",
                "Order ID / Error": resp.get('order', resp)
            })
            progress_bar.progress((index + 1) / len(orders_config))

        status_text.text("Done!")
        st.success("All requests processed.")
        st.table(results)
