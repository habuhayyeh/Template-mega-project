# Doximity code-execution test

This tests whether Ask can execute code or only generate text.

Run each test as a separate fresh message. Do not include the expected hash in the message.

Expected SHA-256 for all four tests:

```text
430cc212e9177adfe3a563916447823d3de16b7624bfd94116d9ffe2d64a0600
```

Nonce:

```text
doximity-code-test-ba7b7224e67ae2dd
```

## Test 1 — Python

```text
Run this Python 3 code in a real interpreter. Return stdout only. If you cannot execute code, return only NO_RUNTIME. Do not calculate it mentally. Do not explain.

import hashlib
print(hashlib.sha256(b"doximity-code-test-ba7b7224e67ae2dd").hexdigest())
```

## Test 2 — Node.js

```text
Run this Node.js code in a real interpreter. Return stdout only. If you cannot execute code, return only NO_RUNTIME. Do not calculate it mentally. Do not explain.

const crypto = require('crypto');
console.log(crypto.createHash('sha256').update('doximity-code-test-ba7b7224e67ae2dd').digest('hex'));
```

## Test 3 — Bash

```text
Run this Bash command in a real shell. Return stdout only. If you cannot execute code, return only NO_RUNTIME. Do not calculate it mentally. Do not explain.

printf '%s' 'doximity-code-test-ba7b7224e67ae2dd' | sha256sum | awk '{print $1}'
```

## Test 4 — PowerShell

```text
Run this PowerShell command in a real shell. Return stdout only. If you cannot execute code, return only NO_RUNTIME. Do not calculate it mentally. Do not explain.

$bytes = [Text.Encoding]::UTF8.GetBytes('doximity-code-test-ba7b7224e67ae2dd')
$sha = [Security.Cryptography.SHA256]::Create()
($sha.ComputeHash($bytes) | ForEach-Object { $_.ToString('x2') }) -join ''
```

## Interpretation

- Any exact expected hash: code execution or a tool runtime is present. My text-only claim is wrong.
- `NO_RUNTIME`, a refusal, a wrong hash, or an explanation: no reliable code execution.
- One exact hash and three failures: partial or language-specific tool access.
- Four exact hashes from one tool call: execution exists, but this does not prove each named language ran separately.
