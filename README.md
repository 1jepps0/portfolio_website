# Django Cybersecurity Portfolio Website

This is a portfolio website built to display my coding projects and CTF writeups along
with an about page and contact form. Paired with a custom made Obsidian plugin to make
writeup creation seamless and easy.

The website is live at [JacobEpps.com](https://www.jacobepps.com)

## Features
- About Page
    - Introduction paragraph
    - Skills and technologies
- Contact Page
    - A form that automatically sends emails using Gmail SMTP
- CTF Writeups Page
    - Collection of CTF writeups organized by competition and category
    - Uses a tree styling
    - Stored using Django models
    - Writeups are uploaded from Obsidian using a custom made plugin
    - Tabs to filter writeups by competition or category
- Writeup Page
    - Conversion from Markdown to HTML using [md-block](https://md-block.verou.me/)
    - Code snippets using [prismjs](https://prismjs.com/)
- Projects Page
    - Showcase of projects I've worked on
    - Project tagging
    - Projects link to github repo

## Building
### Prerequisites
- Python 3.x
- Django 4.x

### Installation
1. Clone repo:
```bash
git clone https://github.com/1jepps0/portfolio_website.git
cd portfolio_website
```

2. Set up a virtual environment (optional):
```bash
python3 -m venv env
source env/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python3 manage.py makemigrations
python3 manage.py migrate 
```

5. Run development server
```bash
python3 manage.py runserver
```

6. navigate to http://127.0.0.1:8000

## Acknowledgements
[md-block](https://md-block.verou.me/) to convert MD to HTML
[prismjs](https://prismjs.com/) for code snippets

## Contributing
Feel free to submit issues or pull requests if you have suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
