def create_features(data):
    """
    Create all 12 engineered features from raw video metadata.
    
    Expected input keys:
    - title, description, tags, views, likes, comment_count, publish_hour
    """
    title = data.get("title", "")
    description = data.get("description", "")
    tags = data.get("tags", "")
    views = max(data.get("views", 1), 1)
    likes = data.get("likes", 0)
    comment_count = data.get("comment_count", 0)
    publish_hour = data.get("publish_hour", 12)

    features = {}

    # Original features
    features["title_length"] = len(title)
    features["description_length"] = len(description)
    features["num_tags"] = len(tags.split("|")) if tags else 0
    features["publish_hour"] = publish_hour
    features["like_view_ratio"] = likes / views if views > 0 else 0

    # Engagement features
    features["comment_view_ratio"] = comment_count / (views + 1)
    features["like_comment_ratio"] = likes / (comment_count + 1)

    # Title-based features
    features["uppercase_words"] = sum(1 for word in title.split() if word.isupper())
    features["title_contains_number"] = 1 if any(char.isdigit() for char in title) else 0
    features["title_word_count"] = len(title.split()) if title else 0

    # Text complexity features
    features["description_word_count"] = len(description.split()) if description else 0
    features["average_word_length_title"] = (
        sum(len(word) for word in title.split()) / len(title.split())
        if len(title.split()) > 0 else 0
    )

    return features
