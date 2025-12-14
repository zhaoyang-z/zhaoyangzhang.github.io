Instructions:

```bash
# first ensure you have ruby 3.2.2
brew install ruby # can also be done through rbenv
# setup conda env
conda create -n website python=3.11
conda activate website
gem install bundler jekyll
pip install pyyaml requests
jekyll new . --force
bundle install
```

```bash
# to launch
conad activate website
bundle exec jekyll serve --port 4001
```

```bash
# to check if all files paths and websites work
conad activate website
python check_links.py
```