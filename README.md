# fide-google-efficiency-chess-ai-challenge

1. Set up Kaggle locally

- Get your API key, put it in `~/.kaggle/kaggle.json`
- `uv venv`
- `uv pip install kaggle pandas numpy matplotlib seaborn scikit-learn`

2. Run

```bash
$ docker build -t chess-agent .
$ docker run --rm --cpus=1 chess_agent
```

