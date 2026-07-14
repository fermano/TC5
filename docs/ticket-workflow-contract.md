# Delivery workflow contract

Delivery owner keys are lowercased after trimming and collapsing each run of whitespace to one ASCII space. Blank owners use `engineering-ops`.

Owner filters preserve input record order and use the same normalized keys as delivery routing. A missing owner selection means no filtering; an explicitly empty selection returns no records.

Delivery summaries expose owner and status. Source metadata may be added as an opt-in field; behavior for blank or missing source values is not yet recorded here.
