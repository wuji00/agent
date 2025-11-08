## Updating this README

This README uses [cogapp](https://nedbatchelder.com/code/cog/) to automatically generate project descriptions.

### Automatic updates

A GitHub Action automatically runs `cog -r -P README.md` on every push to main and commits any changes to the README or new `_summary.md` files.

### Manual updates

To update locally:

```bash
# Run cogapp to regenerate the project list
cog -r -P README.md
```

The script automatically:
- Discovers all subdirectories in this folder
- Gets the first commit date for each folder and sorts by most recent first
- For each folder, checks if a `_summary.md` file exists
- If the summary exists, it uses the cached version
- If not, it generates a new summary using `llm -m <!--[[[cog
print(MODEL, end='')
]]]-->
github/gpt-4.1
<!--[[[end]]]-->` with a prompt that creates engaging descriptions with bullets and links
- Creates markdown links to each project folder on GitHub
- New summaries are saved to `_summary.md` to avoid regenerating them on every run

To regenerate a specific project's description, delete its `_summary.md` file and run `cog -r -P README.md` again.
