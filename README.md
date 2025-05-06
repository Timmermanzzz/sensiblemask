# Sensible Mask

![Sensible Mask Logo](https://raw.githubusercontent.com/yourusername/sensiblemask/main/images/logo.png)

A powerful tool for redacting sensitive information in PDF documents. Built with Streamlit and powered by advanced AI.

## Features

- **Automatic Detection**: Identifies sensitive data like names, addresses, emails, and more
- **Fast Processing**: Get your redacted documents in seconds
- **Easy to Use**: Simple drag-and-drop interface
- **Privacy First**: Your data remains secure and private

## Installation

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sensiblemask.git
cd sensiblemask
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables in a `.env` file:
```
PRIVATEAI_KEY=your_api_key
PRIVATEAI_URL=https://api.private-ai.com/community/v4
```

4. Run the application:
```bash
streamlit run streamlit_app.py
```

## Usage

1. Open the application in your browser
2. Upload a PDF document (10MB max)
3. Click "Redact Document"
4. View and download the redacted PDF

## Deployment

This application is deployed on [Streamlit Cloud](https://yourusername-sensiblemask.streamlit.app).

## License

[MIT](LICENSE) 