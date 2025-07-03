
**MLB Hunch** is a Python CLI app to:

View MLB team info (location, last game, schedule, roster)  
Predict winners for a team’s next 5 games using Gemini AI  
Identify the most exciting upcoming matchup  
Store and view past predictions in a local database

---

## Features

- **Information Mode**: View team details, last game, upcoming schedule, and roster.
- **Winning Games Predictor**: Predict winners, identify the most exciting game, and save predictions.
- **Persistent Storage**: Predictions are stored in `preds_df.db` for later review.

---

## Requirements

- Python 3.8+
- `statsapi`
- `google-generativeai`
- `sqlalchemy`
- `pandas`

Install dependencies:

```bash
pip install statsapi google-generativeai sqlalchemy pandas
```

Set your Gemini API key:

```bash
export MLB_PRED="your_api_key_here"
```

---

## Usage

Run:

```bash
python mlbinfo.py
```

Choose:
- `1` for Information Mode
- `2` for Winning Games Predictor
- `9` to exit

---

## Database

Predictions are stored in `preds_df.db` (SQLite). You can view or clear saved predictions from the CLI.

---

## Contributing

Pull requests welcome for CLI flags, player analytics, historical accuracy tracking, or enhancements.

---

## License

MIT License.
