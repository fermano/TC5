# Delivery workflow contract

Delivery owner keys are trimmed and lowercased. Blank owners use `engineering-ops`.

Future record filters must preserve the input record order. A missing owner selection means no filtering. The product meaning of an explicitly empty selection is not yet recorded here.

Delivery summaries expose only owner and status by default. With `include_source=True`, summaries also expose a trimmed `source`; blank or missing sources are represented as `unknown`.
