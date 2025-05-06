## Documentation
Documentation can be found in documentation.pdf (in polish).

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