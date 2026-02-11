import streamlit as st
import requests
from typing import Dict, Optional

# Configuration
API_URL = "http://127.0.0.1:8000/predict"
PREDICTION_COLORS = {
    "Low": "🔴",
    "Medium": "🟡",
    "High": "🟢",
    "Viral": "⭐"
}

# Page configuration
st.set_page_config(
    page_title="YouTube Success Predictor",
    page_icon="▶️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom styling
st.markdown("""
    <style>
    .stContainer {
        max-width: 700px;
    }
    .prediction-box {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 24px;
    }
    </style>
    """, unsafe_allow_html=True)


def collect_user_inputs() -> Dict:
    """
    Collect user inputs from Streamlit UI and return as dictionary.
    
    Returns:
        Dict: User inputs organized by section
    """
    inputs = {}
    
    # Video Information Section
    st.header("📹 Video Information")
    inputs["title"] = st.text_input(
        "Video Title",
        placeholder="e.g., How to Learn Python in 30 Days",
        help="Enter your video title"
    )
    
    inputs["description"] = st.text_area(
        "Description",
        placeholder="Enter your video description here...",
        height=100,
        help="Provide a detailed description of your video"
    )
    
    inputs["tags"] = st.text_input(
        "Tags",
        placeholder="tag1|tag2|tag3",
        help="Enter tags separated by pipe (|) character"
    )
    
    st.divider()
    
    # Engagement Metrics Section
    st.header("📊 Engagement Metrics")
    col1, col2 = st.columns(2)
    
    with col1:
        inputs["likes"] = st.number_input(
            "Likes",
            min_value=0,
            value=0,
            step=100,
            help="Number of likes on the video"
        )
    
    with col2:
        inputs["views"] = st.number_input(
            "Views",
            min_value=0,
            value=0,
            step=1000,
            help="Total number of views"
        )
    
    inputs["comment_count"] = st.number_input(
        "Comments",
        min_value=0,
        value=0,
        step=50,
        help="Number of comments on the video"
    )
    
    st.divider()
    
    # Publishing Details Section
    st.header("⏰ Publishing Details")
    inputs["publish_hour"] = st.slider(
        "Publish Hour",
        min_value=0,
        max_value=23,
        value=12,
        step=1,
        help="Hour of day when video was published (0-23, 24-hour format)"
    )
    
    # Display selected hour in readable format
    hour_12 = inputs["publish_hour"] % 12 or 12
    am_pm = "AM" if inputs["publish_hour"] < 12 else "PM"
    st.caption(f"📍 Publishing time: {hour_12}:00 {am_pm}")
    
    return inputs


def call_prediction_api(data: Dict) -> Optional[Dict]:
    """
    Send prediction request to FastAPI backend.
    
    Args:
        data: User inputs dictionary
        
    Returns:
        Optional[Dict]: API response with prediction, or None if request failed
    """
    try:
        response = requests.post(
            API_URL,
            json=data,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error(
            "❌ **Backend Connection Error**\n\n"
            f"Cannot connect to {API_URL}\n\n"
            "Please ensure the FastAPI backend is running:\n"
            "```\npython app/main.py\n```"
        )
        return None
    except requests.exceptions.Timeout:
        st.error("⏱️ **Request Timeout** - Backend took too long to respond")
        return None
    except requests.exceptions.HTTPError as e:
        st.error(f"❌ **API Error**: {e.response.status_code} - {e.response.text}")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ **Error**: {str(e)}")
        return None


def validate_inputs(inputs: Dict) -> tuple[bool, str]:
    """
    Validate user inputs before sending to API.
    
    Args:
        inputs: User inputs dictionary
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not inputs["title"].strip():
        return False, "⚠️ Title is required"
    
    if not inputs["description"].strip():
        return False, "⚠️ Description is required"
    
    if not inputs["tags"].strip():
        return False, "⚠️ Tags are required (use format: tag1|tag2|tag3)"
    
    if inputs["views"] < 0:
        return False, "⚠️ Views cannot be negative"
    
    if inputs["likes"] < 0:
        return False, "⚠️ Likes cannot be negative"
    
    if inputs["comment_count"] < 0:
        return False, "⚠️ Comments cannot be negative"
    
    if inputs["likes"] > inputs["views"]:
        return False, "⚠️ Likes cannot exceed views"
    
    return True, ""


def display_prediction(result: Dict) -> None:
    """
    Display prediction result with styling.
    
    Args:
        result: API response with prediction
    """
    prediction = result.get("prediction", "Unknown")
    emoji = PREDICTION_COLORS.get(prediction, "❓")
    
    # Success message with prediction
    st.success("✅ Prediction Complete!")
    
    # Highlighted prediction box
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            color: white;
            font-size: 28px;
            font-weight: bold;
            margin: 20px 0;
        ">
            {emoji} Your Video is Predicted to be: <br>
            <span style="font-size: 36px; margin-top: 10px; display: block;">
                {prediction}
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    # Category explanation
    explanations = {
        "Low": "Your video is predicted to have low engagement (< 50k views)",
        "Medium": "Your video is predicted to have moderate engagement (50k - 1M views)",
        "High": "Your video is predicted to have high engagement (200k - 1M views)",
        "Viral": "Your video has the potential to go viral (> 1M views)! 🚀"
    }
    
    st.info(f"📌 {explanations.get(prediction, 'Check your video metrics!')}")


def main():
    """Main Streamlit application."""
    
    # Page title
    st.markdown("""
        <h1 style='text-align: center; color: #667eea;'>
            ▶️ YouTube Video Success Predictor
        </h1>
        """, unsafe_allow_html=True)
    
    st.markdown(
        "<p style='text-align: center; color: gray;'>"
        "Predict your video's success category based on metadata"
        "</p>",
        unsafe_allow_html=True
    )
    
    st.divider()
    
    # Collect user inputs
    user_inputs = collect_user_inputs()
    
    st.divider()
    
    # Predict button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        predict_button = st.button(
            "🚀 Predict Success",
            use_container_width=True,
            type="primary"
        )
    
    # Handle prediction flow
    if predict_button:
        # Validate inputs
        is_valid, error_message = validate_inputs(user_inputs)
        
        if not is_valid:
            st.error(error_message)
        else:
            # Show loading spinner
            with st.spinner("🔄 Making prediction..."):
                result = call_prediction_api(user_inputs)
            
            # Display results
            if result:
                display_prediction(result)
                
                # Show input summary
                st.markdown("---")
                st.subheader("📋 Input Summary")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Title", user_inputs["title"][:30] + "..." if len(user_inputs["title"]) > 30 else user_inputs["title"])
                    st.metric("Views", f"{user_inputs['views']:,}")
                    st.metric("Comments", f"{user_inputs['comment_count']:,}")
                
                with col2:
                    st.metric("Likes", f"{user_inputs['likes']:,}")
                    if user_inputs["views"] > 0:
                        like_ratio = (user_inputs["likes"] / user_inputs["views"] * 100)
                        st.metric("Like Ratio", f"{like_ratio:.2f}%")
                    else:
                        st.metric("Like Ratio", "N/A")
                    st.metric("Publish Hour", f"{user_inputs['publish_hour']:02d}:00")


if __name__ == "__main__":
    main()
