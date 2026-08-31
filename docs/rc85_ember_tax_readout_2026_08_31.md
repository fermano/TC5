# Ember RC85 tax readout note

Finance confirmed the total taxable amount did not change between the last two artifacts. That does not prove `inv-502` is classified correctly because it is a zero-cent exemption row.

There is a stale mainline normalizer that understands `certificateId`/`exemptCents`, but it does not preserve RC85 route output.
