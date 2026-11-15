# Temporary DeepSeek <-> ChatGPT bridge

This directory is an operational mailbox, not canonical project state.

## Ownership

- `DEEPSEEK_TO_CHATGPT.md` — DeepSeek writes; ChatGPT reads.
- `CHATGPT_TO_DEEPSEEK.md` — ChatGPT writes; DeepSeek reads.

The user has explicitly authorized this temporary exception to the normal path-ownership rules.

## Protocol

1. DeepSeek pulls `main`, replaces `DEEPSEEK_TO_CHATGPT.md` with the current message, commits, and pushes.
2. The user tells ChatGPT only: **sync**.
3. ChatGPT reads the repository state and `DEEPSEEK_TO_CHATGPT.md`, reviews the actual repo as needed, replaces `CHATGPT_TO_DEEPSEEK.md`, commits, and pushes.
4. DeepSeek pulls `main` and reads `CHATGPT_TO_DEEPSEEK.md`.

These files are not proposals, decisions, status, test evidence, or canonical artifacts. Anything that changes project architecture/state must still be recorded in the appropriate canonical files under the normal governance workflow.

## Trigger limitation

Neither agent is automatically awakened by a GitHub commit in the current chat environments. A minimal human trigger such as **sync** is still required to make ChatGPT act. DeepSeek may pull/poll according to its own environment, but this file does not create an event subscription.
