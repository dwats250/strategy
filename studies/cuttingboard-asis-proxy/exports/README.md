# exports/

Immutable capture outputs from proxy runs (`docs/conventions.md` §e).

**Empty: no run has been executed.** TradingView execution was not available to the agent that
built this study package. See `../README.md` § *What remains for Dustin to run*.

Once a run happens: filenames encode symbol, timeframe, session, date window, and script hash;
files are never edited after writing; a re-capture produces a new file, never an edit.
