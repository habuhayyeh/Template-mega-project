# Channel

A file channel so neither agent's output has to be pasted into the other's chat.

## Files

| File | Writer | Reader |
|---|---|---|
| `to-chatgpt.md` | DeepSeek only | ChatGPT |
| `to-deepseek.md` | ChatGPT only | DeepSeek |

One writer per file, so they never conflict.

## Rules

1. Append only. Never edit or delete an entry you did not write.
2. One entry per message. Header line: `## <ISO-8601> · <sender> · <kind>`, where kind is `request`, `review`, `answer`, `decision`, or `note`.
3. Pull with `--rebase` before appending, push after.
4. No patient data, ever.
5. **The channel is conversation, not state.** A decision is not agreed because it appears here; it is agreed when it is in `DECISIONS.md`. Status changes only in `STATUS.md`.

## The trigger problem

GitHub cannot wake a chat model. There is no webhook that reaches into a ChatGPT conversation; ChatGPT reads and writes only when it is asked to. So the loop needs one short prompt instead of a paste:

```
Read channel/to-chatgpt.md and answer in channel/to-deepseek.md.
```

That is the whole improvement: one sentence, and the full text lives in the repository.

Raw URL, if the reader prefers it:

```text
https://raw.githubusercontent.com/habuhayyeh/Template-mega-project/main/channel/to-chatgpt.md
```
