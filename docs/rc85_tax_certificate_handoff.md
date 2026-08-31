# RC85 tax certificate handoff

RC85 moved certificate rows onto route-scoped invoice output. A count-only smoke passed, but one partner sample disagreed on whether a zero-cent exemption with a certificate should remain exempt.

Resolved on the release route path (GitHub #96): a certificate plus a *supplied* exemption amount is an exemption, including when that amount is zero. Presence is the test, not truthiness. The release helper now resolves snake-case release-fixture keys and camel-case replay keys (`certificateId` / `exemptCents`) onto the same route-shaped row, so `ember/retail/inv-502` exports `status=exempt` while `artifact_schema` and `tax_key` stay intact.

Aggregate taxable totals (GitHub #97) remain supporting context only; an unchanged total does not validate a zero-cent row.

Treat broad tax-policy cleanup as separate unless the code path affects the release artifact sample.
