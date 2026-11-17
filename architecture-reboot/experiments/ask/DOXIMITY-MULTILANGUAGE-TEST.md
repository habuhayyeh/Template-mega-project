# Doximity multi-language execution test

Same fixed nonce for every language:

```text
doximity-code-test-ba7b7224e67ae2dd
```

Expected SHA-256:

```text
430cc212e9177adfe3a563916447823d3de16b7624bfd94116d9ffe2d64a0600
```

Run each test in a fresh conversation. Do not include the expected hash in the message.

## PHP

```text
Run this PHP code in a real interpreter. Return stdout only. If you cannot execute code, return only NO_RUNTIME. Do not calculate it mentally. Do not explain.

<?php echo hash('sha256', 'doximity-code-test-ba7b7224e67ae2dd'); ?>
```

## Ruby

```text
Run this Ruby code in a real interpreter. Return stdout only. If you cannot execute code, return only NO_RUNTIME. Do not calculate it mentally. Do not explain.

require 'digest'
puts Digest::SHA256.hexdigest('doximity-code-test-ba7b7224e67ae2dd')
```

## Perl

```text
Run this Perl code in a real interpreter. Return stdout only. If you cannot execute code, return only NO_RUNTIME. Do not calculate it mentally. Do not explain.

use Digest::SHA;
print Digest::SHA->new(256)->add('doximity-code-test-ba7b7224e67ae2dd')->hexdigest;
```

## Go

```text
Run this Go code in a real interpreter. Return stdout only. If you cannot execute code, return only NO_RUNTIME. Do not calculate it mentally. Do not explain.

package main
import (
  "crypto/sha256"
  "fmt"
)
func main() {
  fmt.Printf("%x", sha256.Sum256([]byte("doximity-code-test-ba7b7224e67ae2dd")))
}
```

## Java

```text
Run this Java code in a real interpreter. Return stdout only. If you cannot execute code, return only NO_RUNTIME. Do not calculate it mentally. Do not explain.

import java.security.MessageDigest;
public class Main {
  public static void main(String[] args) throws Exception {
    byte[] d = MessageDigest.getInstance("SHA-256").digest("doximity-code-test-ba7b7224e67ae2dd".getBytes("UTF-8"));
    for (byte b : d) System.out.printf("%02x", b);
  }
}
```

## R

```text
Run this R code in a real interpreter. Return stdout only. If you cannot execute code, return only NO_RUNTIME. Do not calculate it mentally. Do not explain.

library(digest)
cat(digest('doximity-code-test-ba7b7224e67ae2dd', algo='sha256', serialize=FALSE))
```

## Interpretation

- Exact expected hash: that language runtime or a tool backend is present.
- `NO_RUNTIME`, refusal, wrong hash, or package-missing error: no reliable execution for that language.
- A package-missing error means the language may exist but the test dependency does not; it is not proof of execution.
