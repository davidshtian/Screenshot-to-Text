import io
import sys
import boto3
from PIL import ImageGrab
import markdown2
import webbrowser
import os
import glob
import time

class ScreenshotToText:
    def __init__(self):
        self.bedrock_client = boto3.client(service_name="bedrock-runtime")
        self.model_id = "amazon.nova-lite-v1:0"

        # Create fixed output directory in user's home directory
        self.output_dir = os.path.join(os.path.expanduser("~"), "screenshot_analysis")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.cleanup_old_files()
        self.process_screenshot()

    def cleanup_old_files(self):
        """Clean up old HTML files in the output directory"""
        try:
            # Get all HTML files in the output directory
            pattern = os.path.join(self.output_dir, '*.html')
            old_files = glob.glob(pattern)

            for file_path in old_files:
                try:
                    os.unlink(file_path)
                    print(f"Deleted old file: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
        except Exception as e:
            print(f"Error cleaning directory: {e}")

    def create_html(self, markdown_text):
        """Create HTML with CSS styling"""
        css = """
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .content {
                background-color: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            h1, h2, h3, h4, h5, h6 {
                color: #2c3e50;
                margin-top: 24px;
                margin-bottom: 16px;
            }
            h1 { font-size: 2em; border-bottom: 2px solid #eee; }
            h2 { font-size: 1.5em; border-bottom: 1px solid #eee; }
            pre {
                background-color: #f6f8fa;
                padding: 16px;
                border-radius: 6px;
                overflow-x: auto;
                line-height: 1.45;
            }
            code {
                background-color: #f6f8fa;
                padding: 2px 4px;
                border-radius: 3px;
                font-family: Consolas, monospace;
                font-size: 0.9em;
            }
            blockquote {
                border-left: 4px solid #0078D4;
                margin: 0;
                padding: 10px 20px;
                color: #666;
                background-color: #f8f9fa;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                margin: 16px 0;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }
            th {
                background-color: #f8f9fa;
            }
            tr:nth-child(even) {
                background-color: #f8f9fa;
            }
            img {
                max-width: 100%;
                height: auto;
                border-radius: 4px;
            }
            p {
                margin: 16px 0;
                line-height: 1.8;
            }
            ul, ol {
                padding-left: 20px;
            }
            li {
                margin: 8px 0;
            }
            a {
                color: #0366d6;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
        """

        # Convert markdown to HTML
        html_content = markdown2.markdown(markdown_text, extras=[
            'fenced-code-blocks',
            'tables',
            'break-on-newline',
            'header-ids',
            'task_list'
        ])

        # Combine CSS and HTML content
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Screenshot Analysis</title>
            {css}
        </head>
        <body>
            <div class="content">
                {html_content}
            </div>
        </body>
        </html>
        """
        return full_html

    def open_in_browser(self, markdown_content):
        """Open the markdown content in Chrome browser"""
        # Create HTML content
        html_content = self.create_html(markdown_content)

        # Create file with timestamp in fixed directory
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.output_dir, f'analysis_{timestamp}.html')

        # Write content with UTF-8 encoding
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"Created new file: {output_file}")

        # Convert to file URL
        file_url = f'file:///{output_file.replace(os.sep, "/")}'

        # Open in Chrome browser
        chrome_path = ""
        if sys.platform.startswith('win'):
            chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
        elif sys.platform.startswith('darwin'):  # macOS
            chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
        elif sys.platform.startswith('linux'):
            chrome_path = '/usr/bin/google-chrome'

        try:
            if sys.platform.startswith('darwin'):
                webbrowser.get(chrome_path).open(file_url)
            elif chrome_path and os.path.exists(chrome_path):
                webbrowser.register('chrome', None,
                                  webbrowser.BackgroundBrowser(chrome_path))
                webbrowser.get('chrome').open(file_url)
            else:
                webbrowser.open(file_url)

        except Exception as e:
            print(f"Error opening browser: {e}")
            # Fallback to default browser
            webbrowser.open(file_url)

    def generate_conversation(self, input_text, input_image):
        """Sends a message to the model"""
        try:
            img_byte_arr = io.BytesIO()
            input_image.save(img_byte_arr, format="PNG")
            image = img_byte_arr.getvalue()

            message = {
                "role": "user",
                "content": [
                    {"image": {"format": "png", "source": {"bytes": image}}},
                    {"text": input_text},
                ],
            }

            response = self.bedrock_client.converse(
                modelId=self.model_id, messages=[message]
            )

            return response
        except Exception as error:
            return f"Error processing image: {str(error)}"

    def process_screenshot(self):
        """Process screenshot from clipboard"""
        img = ImageGrab.grabclipboard()

        if img:
            input_text = """Analyze this image and provide a detailed response in markdown format including:
            1. Description of visual elements
            2. Analysis of content
            3. Key insights or findings

            Use appropriate markdown formatting (headers, lists, code blocks, etc.)"""

            response = self.generate_conversation(input_text, img)

            if isinstance(response, dict):
                try:
                    markdown_content = response["output"]["message"]["content"][0]["text"]
                    self.open_in_browser(markdown_content)
                except (KeyError, IndexError) as e:
                    print(f"Error parsing response: {str(e)}")
            else:
                print(str(response))
        else:
            print("No screenshot found in clipboard. Please copy an image first.")

def main():
    ScreenshotToText()

if __name__ == "__main__":
    main()
