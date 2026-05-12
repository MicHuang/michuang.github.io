学习 Bootstap and for fun!

## Local preview

This is a static GitHub Pages blog. You can open `index.html` directly in a browser, or run the simple local server:

```bash
node server.js
```

Then visit:

```text
http://localhost:8080/index.html
```

## Create a new article

Use the bundled blog generator:

```bash
python3 tools/blog_generator/generator.py "My New Post" --tag Bootstrap
```

The tool creates a new file in `article/`. After that, update `index.html`, `archive.html`, and the previous/next article links by hand.
