import requests
from openai import AzureOpenAI
from typing import Dict, List
import feedparser
from bs4 import BeautifulSoup
import random
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import hashlib
import re
import cohere  # Add this import

class MainApp:
    def __init__(self, rss_url='https://techcrunch.com/feed/'):
        # Replace OpenAI setup with Cohere setup
        self.client = cohere.Client('d4FwulVp9JUvELKQYDrqa7hWmwZ1VHW9GjUGhVlW')  # Replace with your actual API key

        # Web Scraping Setup
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
        ]
        self.session = self._create_session()
        self.rss_url = rss_url
    
    def _create_session(self):
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def parse_rss_feed(self) -> List[Dict]:
        print("\nParsing RSS feed...")
        feed = feedparser.parse(self.rss_url)
        print(f"Found {len(feed.entries)} entries in feed")
        articles = []
        
        for entry in feed.entries:
            article = {
                'title': entry.title,
                'link': entry.link,
                'published_date': entry.get('published', ''),
                'description': entry.get('description', ''),
                'author': entry.get('author', '')
            }
            articles.append(article)
            print(f"Parsed article: {article['title']}")
        return articles

    def scrape_news_from_link(self, link) -> Dict:
        try:
            time.sleep(random.uniform(1, 3))
            response = self.session.get(
                link, 
                headers={'User-Agent': random.choice(self.user_agents)}, 
                timeout=15
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            print(f"\nScraping: {link}")
            
            # Get title
            title = soup.select_one('h1.wp-block-post-title')
            title = title.text.strip() if title else None
            
            # Get author
            author = soup.select_one('div.wp-block-tc23-author-card-name > a')
            author = author.text.strip() if author else None
            
            # Get date
            date = soup.select_one('div.wp-block-post-date > time')
            date = date['datetime'] if date else None
            
            # Get content
            article_content = soup.select_one('div.wp-block-post-content')
            if article_content:
                # Remove ads and unwanted elements
                for unwanted in article_content.select('.ad-unit, .wp-block-tc-ads-ad-slot, .marfeel-experience-inline-cta'):
                    unwanted.decompose()
                
                # Get paragraphs with wp-block-paragraph class
                paragraphs = article_content.select('p.wp-block-paragraph')
                
                if paragraphs:
                    # Filter out short paragraphs and clean text
                    valid_paragraphs = []
                    for p in paragraphs:
                        text = p.get_text(strip=True)
                        if len(text) > 50 and not text.startswith('Image Credits:'):
                            valid_paragraphs.append(text)
                    
                    if valid_paragraphs:
                        content = ' '.join(valid_paragraphs)
                        print(f"Found article content: {len(content)} chars")
                        print(f"Preview: {content[:150]}...")
                        
                        return {
                            'title': title,
                            'author': author,
                            'date': date,
                            'content': content
                        }
                        
            print("No valid content found")
            return None
            
        except Exception as e:
            print(f"Error scraping {link}: {str(e)}")
            return None

    def rewrite_article(self, article: Dict) -> Dict:
        try:
            response = self.client.generate(
                model='command',
                prompt=(
                    "You are an expert tech journalist and analyst with deep knowledge of technology, business, and innovation. "
                    "Your writing style is clear, engaging, and insightful, aimed at both technical and non-technical readers.\n\n"
                    
                    "Writing Style Requirements:\n"
                    "1) Use specific numbers, metrics, and data points to support arguments\n"
                    "2) Focus on practical implications and actionable insights\n"
                    "3) Include expert citations and references with links\n"
                    "4) Break down complex technical concepts into understandable terms\n"
                    "5) Add relevant market context and industry trends\n"
                    "6) Include a 'Why It Matters' section\n"
                    "7) End with key takeaways or a 'Bottom Line' section\n"
                    "8) Add a P.S. with an interesting related fact or future prediction\n\n"
                    
                    "Article Structure:\n"
                    "- Strong opening hook\n"
                    "- Clear context and background\n"
                    "- Main analysis with supporting evidence\n"
                    "- Industry implications\n"
                    "- Future outlook\n"
                    "- Practical takeaways\n\n"
                    
                    "Additional Guidelines:\n"
                    "- Use bullet points for key information\n"
                    "- Include relevant statistics and market data\n"
                    "- Add subheadings for better readability\n"
                    "- Highlight expert quotes or insights\n"
                    "- Reference similar technologies or competing solutions\n"
                    "- Address potential challenges or limitations\n"
                    "- Include real-world examples or use cases\n\n"
                    
                    f"Please rewrite this tech article following the above guidelines:\n\n{article['content']}\n\n"
                    "Format the article in clean HTML with appropriate tags for headings, paragraphs, and lists."
                ),
                max_tokens=2048,
                temperature=0.7,
                k=0,
                p=1,
                frequency_penalty=0.2,
                presence_penalty=0.1,
                stop_sequences=[],
                return_likelihoods='NONE'
            )
            
            rewritten_content = response.generations[0].text.strip()
            # Remove 'html' prefix if present
            rewritten_content = re.sub(r'^(?:html|```html|```)\s*', '', rewritten_content, flags=re.IGNORECASE)

            return {
                'title': article['title'],
                'author': article.get('author'),
                'date': article.get('date'),
                'content': rewritten_content,
                'preview': self.strip_html(rewritten_content)
            }
            
        except Exception as e:
            print(f"Error rewriting article: {str(e)}")
            return article  # Return original article if rewriting fails
    
    def strip_html(self, html_content: str) -> str:
        # Remove HTML tags
        clean_text = re.sub(r'<[^>]+>', '', html_content)
        # Remove extra whitespace
        clean_text = ' '.join(clean_text.split())
        # Limit preview length to first 200 characters
        return clean_text[:200] + '...' if len(clean_text) > 200 else clean_text
    def hash_md5(self, data):
        unique_data = f"{data['title']}-{data['link']}"
        return hashlib.md5(unique_data.encode()).hexdigest()

    def load_hashes(self):
        try:
            with open("hash-logs.txt", 'r') as f:
                return set(f.read().splitlines())
        except FileNotFoundError:
            return set()

    def save_hash(self,hash_str):
        with open("hash-logs.txt", 'a') as f:
            f.write(str(hash_str) + '\n')

    def does_hash_exist(self, hash_str, existing_hashes):
        return hash_str in existing_hashes

    def process_articles(self, filter_keywords=None):

        existing_hashes = self.load_hashes()
        processed_articles = []

        articles = self.parse_rss_feed()

        for article in articles:
            article_hash = self.hash_md5(article)

            if self.does_hash_exist(article_hash, existing_hashes):
                print(f"Skipping duplicate article: {article['title']}")
                continue

            
            print(f"Processing article: {article['title']}")

            content = self.scrape_news_from_link(article['link']) 
            if content:
                article['content'] = content
                rewritten_article = self.rewrite_article(article) 

                if self.upload_article(rewritten_article): 
                    processed_articles.append(rewritten_article)
                    self.save_hash(article_hash)
                    existing_hashes.add(article_hash)  # Update in-memory set

        print(f"\nProcessed {len(processed_articles)} articles.")
        return processed_articles

    def upload_article(self, article, upload_url="http://localhost:8000/upload"):
        article_data = {
            'title': article['title'],
            'content': article['content']['content'].replace('```', '') if isinstance(article['content'], dict) else article['content'].replace('```', ''),
            'author': article.get('author', 'No author'),
            'preview': article.get('preview'),
            'date': article.get('date') or article.get('published_date', 'No date'),
            'link': article.get('link', '')
        }

        try:
            response = requests.post(
                upload_url, 
                json=article_data,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                print(f"Successfully uploaded article: {article['title']}")
                return True
            else:
                print(f"Failed to upload article: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"Error uploading article: {str(e)}")
            return False


def main():
    processor = MainApp()
    processor.process_articles()

if __name__ == "__main__":
    main()