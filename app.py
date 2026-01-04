import streamlit as st
import requests
import json

# --- CONFIGURATION ---
API_URL = "https://smmglobe.com/api/v2"
# Ideally, keep API keys in st.secrets for security, but hardcoding here as requested
API_KEY = "3bbf81f2e050956e7aa37abed188ff42" 

# 28 Pre-filled positive comments
COMMENTS_LIST = [
    "The website actually works omg", "Amazing type shi", "Can't believe but it works", "Wow 😍", 
    "Great video", "i wasn't expecting it to actually work wow", "Thanks man", "This is def my brick",
    "Used it twice and worked as shown wow", "i hope this stays alive thanks", "Valid", "JAJAJJAJAJAJA", 
    "This is it", "Underrated", "Best video I've seen today", 
    "Lol how is this website actually working", "Fire 🔥", "Great stuff", "gonna check my fine shyt snap", 
    "I love this website lol", "i liked this video", "keep spreading this", "Awesome", 
    "lol", "Interesting", "Shared it with my bff", "Saved for later", 
    "Make more vids like this please"
]

# --- HELPER FUNCTIONS ---
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

# --- STREAMLIT APP LAYOUT ---
st.set_page_config(page_title="TikTok Auto-Order", page_icon="🚀")

st.title("🚀 TikTok Bulk Order Tool")
st.markdown("Enter a TikTok link below to automatically place all 7 service orders.")

# Input Field
video_link = st.text_input("TikTok Video Link", placeholder="https://www.tiktok.com/@user/video/...")

# The "Recipe" of orders to place
orders_config = [
    {"id": 2630, "name": "Custom Comments", "qty": 28, "type": "comments"},
    {"id": 3639, "name": "Shares (S. Fast)", "qty": 100, "type": "default"},
    {"id": 3000, "name": "Shares (Real)", "qty": 20, "type": "default"},
    {"id": 557,  "name": "Saves (Never Stuck)", "qty": 100, "type": "default"},
    {"id": 3154, "name": "Saves/Favorites", "qty": 100, "type": "default"},
    {"id": 3050, "name": "Likes + Views", "qty": 50, "type": "default"},
    {"id": 3151, "name": "Likes (Female)", "qty": 20, "type": "default"},
]

# Button Logic
if st.button("Place Orders", type="primary"):
    if not video_link:
        st.error("Please enter a valid link first.")
    else:
        st.write("---")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        results = []
        
        for index, order in enumerate(orders_config):
            # Update status
            status_text.text(f"Processing: {order['name']} (ID: {order['id']})...")
            
            # Prepare data
            if order['type'] == 'comments':
                comments_string = "\n".join(COMMENTS_LIST)
                resp = place_order(service_id=order['id'], link=video_link, comments=comments_string)
            else:
                resp = place_order(service_id=order['id'], link=video_link, quantity=order['qty'])
            
            # Check result
            is_success = 'order' in resp
            results.append({
                "Service": order['name'],
                "ID": order['id'],
                "Status": "✅ Success" if is_success else "❌ Failed",
                "Order ID / Error": resp.get('order', resp)
            })
            
            # Update Progress
            progress_bar.progress((index + 1) / len(orders_config))

        status_text.text("Done!")
        
        # Display Results Table
        st.success("All requests processed.")
        st.table(results)
