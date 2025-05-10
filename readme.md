## Documentation
Documentation can be found in documentation.pdf (in polish).

# Cytatownik — AI Quote Generator 

**Cytatownik** is a web application that allows users to read, add, edit, and generate motivational quotes — including ones created using artificial intelligence (AI).

The project combines Django (backend), Bootstrap (frontend), and the Hugging Face API (AI text generation) to deliver a functional and visually friendly quote management platform.

---

## 🧩 Features

- 📚 Browse quotes from all users
- ➕ Add / edit / delete your own quotes
- 🔐 Register and log in to manage quotes
- 💬 Comment on quotes
- 🔍 Search by keyword, author, or category
- 🤖 Generate original quotes using AI (via Hugging Face)
- ⭐ Custom styling using Bootstrap (Minty theme)

---

## Technologies Used

  - Python 3.10

  - Django 5.x

  - SQLite

  - Bootstrap 5 (Minty theme)

  - Hugging Face Transformers API

--- 

## Authors

  Aleksandra Grabowska — @AleksandraGrabowska04
  Jakub Malinowski - @at-eee
  Jakub Markowski - @kuba913
  Krystian Dzikiewicz - @LionDoge

---

## 🤖 AI Quote Generator

To use the AI quote generator, you’ll need your own user access token from Hugging Face:  
🔗 https://huggingface.co/settings/tokens

When you get your personal token, create a file named `.env` in the root folder of the project and add:

```bash
export HUGGINGFACE_API_KEY='your_token_here'


## AI quote generator

In order to be able to use the AI quote generator, you need to get your own user access API token from the huggingface website: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).

When you get your own personal token, then in the main directory of the project you need to create the *.env* file, and store it there in the following format:

```python
export HUGGINGFACE_API_KEY='insert your personal API token here'
```

The fastest way to do it, is to open the terminal in the directory where the cytatownik project is stored on your machine and run this command:

```bash
echo "export HUGGINGFACE_API_KEY='[!insert your personal API token here!]'" > .env
```
