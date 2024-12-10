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
import google.generativeai as genai  # Add this import

class MainApp:
    def __init__(self, rss_url='https://techcrunch.com/feed/'):
        # Replace Cohere setup with Gemini setup
        genai.configure(api_key='AIzaSyA_Wkb7YQgw4vY7ECIW5NhoxIiaKb9WvcY')  # Replace with your actual API key
        self.model = genai.GenerativeModel('gemini-pro')
        
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
            prompt = """You are a seasoned technology journalist with a deep understanding of tech innovations and business strategies.

            Task: Transform the following tech article into a polished, professional blog post that captivates both technical and business audiences.
            
            Original Title: {original_title}

            Required Output Format:
            1. First generate a catchy new title that's SEO-friendly and engaging
            2. Format the article using proper HTML tags as follows:
                - Use <h1> for the main title
                - Use <h2> for major section headings
                - Use <h3> for subsection headings
                - Use <p> for paragraphs
                - Use <ul> and <li> for lists
                - Add proper spacing between sections
                - Wrap key terms in <strong> tags
                - Use <blockquote> for important quotes
            
            Required Sections (use <h2> for these):
            - Introduction
            - Key Developments
            - Technical Analysis
            - Business Impact
            - Market Context
            - Future Implications
            - Key Takeaways

            Original Article Content:
            {article_content}

            Please rewrite this as a professional tech industry analysis piece following all guidelines above. Ensure proper HTML formatting and spacing."""

            response = self.model.generate_content(
                prompt.format(
                    original_title=article['title'],
                    article_content=article['content']
                ),
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.9,
                    top_k=50,
                    max_output_tokens=2048,
                )
            )
            
            rewritten_content = response.text.strip()
            
            # Extract new title if provided (assuming it's the first line)
            content_lines = rewritten_content.split('\n')
            new_title = ''
            if content_lines and (content_lines[0].startswith('# ') or content_lines[0].startswith('<h1>')):
                new_title = content_lines[0].replace('# ', '').replace('<h1>', '').replace('</h1>', '').strip()
                rewritten_content = '\n'.join(content_lines[1:])
            else:
                new_title = article['title']

            # Clean up any code formatting
            rewritten_content = re.sub(r'^(?:html|```html|```)\s*', '', rewritten_content, flags=re.IGNORECASE)
            rewritten_content = re.sub(r'```\s*$', '', rewritten_content)

            # Add default styling classes to HTML elements
            rewritten_content = rewritten_content.replace('<h2>', '<h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4">')
            rewritten_content = rewritten_content.replace('<h3>', '<h3 class="text-xl font-semibold text-gray-800 mt-6 mb-3">')
            rewritten_content = rewritten_content.replace('<p>', '<p class="text-gray-700 mb-4 leading-relaxed">')
            rewritten_content = rewritten_content.replace('<ul>', '<ul class="list-disc pl-6 mb-4 space-y-2">')
            rewritten_content = rewritten_content.replace('<blockquote>', '<blockquote class="border-l-4 border-blue-500 pl-4 italic my-4">')

            return {
                'title': new_title,
                'author': article.get('author'),
                'date': article.get('date'),
                'content': rewritten_content,
                'preview': self.strip_html(rewritten_content)[:200] + '...'
            }
            
        except Exception as e:
            print(f"Error rewriting article: {str(e)}")
            return article
    
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