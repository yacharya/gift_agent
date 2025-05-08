import os
import praw
from dotenv import load_dotenv

load_dotenv()

def search_reddit(query: str) -> str:
    """Search Reddit for gift ideas based on the query."""
    try:
        reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent="GiftAgent/1.0"
        )
        
        # Search across relevant subreddits
        subreddits = ["giftideas", "gifts", "perfectgift"]
        results = []
        
        for subreddit in subreddits:
            try:
                sub = reddit.subreddit(subreddit)
                for post in sub.search(query, limit=3):
                    results.append({
                        "title": post.title,
                        "url": f"https://reddit.com{post.permalink}",
                        "score": post.score,
                        "num_comments": post.num_comments
                    })
            except Exception as e:
                print(f"Error searching subreddit {subreddit}: {str(e)}")
                continue
        
        # Sort by score and format results
        results.sort(key=lambda x: x["score"], reverse=True)
        formatted_results = []
        
        for post in results[:5]:  # Top 5 results
            formatted_results.append(
                f"- {post['title']} (Score: {post['score']}, Comments: {post['num_comments']})"
            )
        
        return "\n".join(formatted_results) if formatted_results else "No relevant gift ideas found on Reddit."
    
    except Exception as e:
        return f"Error searching Reddit: {str(e)}"
