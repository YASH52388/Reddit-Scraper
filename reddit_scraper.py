import praw
import pandas as pd
import time
import os
from datetime import datetime
import argparse

class RedditScraper:
    def __init__(self, client_id, client_secret, user_agent):
        """
        Initialize the Reddit API client using PRAW
        
        Args:
            client_id (str): Reddit API client ID
            client_secret (str): Reddit API client secret
            user_agent (str): User agent string for API requests
        """
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        
    def get_top_posts(self, subreddit_name, limit=25, time_filter='week'):
        """
        Fetch top posts from a subreddit
        
        Args:
            subreddit_name (str): Name of the subreddit to scrape
            limit (int): Maximum number of posts to retrieve
            time_filter (str): Time filter to use ('day', 'week', 'month', 'year', 'all')
            
        Returns:
            list: List of post data dictionaries
        """
        subreddit = self.reddit.subreddit(subreddit_name)
        posts = []
        
        try:
            for post in subreddit.top(time_filter=time_filter, limit=limit):
                # Extract post data
                post_data = {
                    'subreddit': subreddit_name,
                    'post_id': post.id,
                    'title': post.title,
                    'score': post.score,
                    'num_comments': post.num_comments,
                    'created_utc': datetime.fromtimestamp(post.created_utc),
                    'url': post.url,
                    'permalink': f"https://www.reddit.com{post.permalink}",
                    'is_self_post': post.is_self,
                }
                
                # Add post content if it's a self post
                if post.is_self:
                    post_data['selftext'] = post.selftext
                else:
                    post_data['selftext'] = ""
                
                # Add author if available (might be deleted)
                if post.author:
                    post_data['author'] = post.author.name
                else:
                    post_data['author'] = "[deleted]"
                
                posts.append(post_data)
                
            print(f"Successfully scraped {len(posts)} posts from r/{subreddit_name}")
            return posts
            
        except Exception as e:
            print(f"Error scraping r/{subreddit_name}: {str(e)}")
            return []
    
    def scrape_multiple_subreddits(self, subreddit_list, limit=25, time_filter='week'):
        """
        Scrape top posts from multiple subreddits
        
        Args:
            subreddit_list (list): List of subreddit names to scrape
            limit (int): Maximum number of posts per subreddit
            time_filter (str): Time filter for posts
            
        Returns:
            DataFrame: Combined dataframe of all posts
        """
        all_posts = []
        
        for subreddit in subreddit_list:
            print(f"Scraping r/{subreddit}...")
            posts = self.get_top_posts(subreddit, limit, time_filter)
            all_posts.extend(posts)
            
            # Sleep to avoid hitting rate limits
            time.sleep(2)
            
        # Convert to DataFrame
        if all_posts:
            df = pd.DataFrame(all_posts)
            return df
        else:
            print("No posts were collected.")
            return pd.DataFrame()
    
    def save_to_excel(self, df, output_file=None):
        """
        Save the collected posts to an Excel file
        
        Args:
            df (DataFrame): DataFrame containing the posts
            output_file (str, optional): Output file path. If not provided,
                                       a timestamp-based name will be used.
        
        Returns:
            str: Path to the saved file
        """
        if df.empty:
            print("No data to save.")
            return None
            
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"reddit_top_posts_{timestamp}.xlsx"
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Write to Excel
        df.to_excel(output_file, index=False)
        print(f"Data saved to {output_file}")
        return output_file
    
    def save_to_csv(self, df, output_file=None):
        """
        Save the collected posts to a CSV file
        
        Args:
            df (DataFrame): DataFrame containing the posts
            output_file (str, optional): Output file path. If not provided,
                                        a timestamp-based name will be used.
        
        Returns:
            str: Path to the saved file
        """
        if df.empty:
            print("No data to save.")
            return None
            
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"reddit_top_posts_{timestamp}.csv"
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Write to CSV
        df.to_csv(output_file, index=False)
        print(f"Data saved to {output_file}")
        return output_file


def main():
    """
    Main function to run the scraper from command line
    """
    parser = argparse.ArgumentParser(description='Scrape top posts from Reddit subreddits')
    parser.add_argument('--subreddits', type=str, nargs='+', required=True,
                        help='List of subreddits to scrape (without r/)')
    parser.add_argument('--limit', type=int, default=25,
                        help='Maximum number of posts per subreddit')
    parser.add_argument('--time-filter', type=str, default='week',
                        choices=['day', 'week', 'month', 'year', 'all'],
                        help='Time filter for top posts')
    parser.add_argument('--output', type=str, default=None,
                        help='Output file path (Excel or CSV depending on extension)')
    parser.add_argument('--client-id', type=str, required=True,
                        help='Reddit API client ID')
    parser.add_argument('--client-secret', type=str, required=True,
                        help='Reddit API client secret')
    parser.add_argument('--user-agent', type=str, default='RedditScraper/1.0',
                        help='User agent for Reddit API')
    
    args = parser.parse_args()
    
    # Initialize the scraper
    scraper = RedditScraper(
        client_id=args.client_id,
        client_secret=args.client_secret,
        user_agent=args.user_agent
    )
    
    # Scrape the subreddits
    df = scraper.scrape_multiple_subreddits(
        args.subreddits,
        limit=args.limit,
        time_filter=args.time_filter
    )
    
    # Save the results
    if args.output:
        if args.output.endswith('.xlsx'):
            scraper.save_to_excel(df, args.output)
        elif args.output.endswith('.csv'):
            scraper.save_to_csv(df, args.output)
        else:
            print("Unsupported output format. Using CSV format.")
            scraper.save_to_csv(df, args.output + '.csv')
    else:
        # Default to Excel if no output specified
        scraper.save_to_excel(df)


if __name__ == "__main__":
    main()
