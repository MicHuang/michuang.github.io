# Blog Generator

This tool creates a new static article page for this GitHub Pages blog.

## Create an Article

Run it from the repository root:

```bash
python3 tools/blog_generator/generator.py "My New Post" --tag Bootstrap --tag Notes
```

That creates:

```text
article/my-new-post.html
```

You can choose the filename and starter content:

```bash
python3 tools/blog_generator/generator.py "My New Post" \
  --filename my_post.html \
  --tag Bootstrap,Notes \
  --content "First paragraph.\n\nSecond paragraph."
```

The generated page is only the article file. After creating it, update `index.html`, `archive.html`, and neighboring article pager links by hand.

## Why This Lives Here

The old `BlogGenerator` project was a separate Python 2 helper with hard-coded local paths. This version lives inside the blog repository so it can use the repository layout directly and stay in sync with the article template.
