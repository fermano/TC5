# RC105 Ember certificate readout

Artifact `rc105-ember-retail-h` was sampled against `release/rc-105`.

Aggregate tax smoke: totals match to the cent against the previous packet.

Line sample: `ember/retail/inv-502` still shows `taxable=true` although the partner payload carries `certificate_id=cert-78` and `waivedCents: "0"`.

Interpretation: aggregate totals are green, but row classification remains disputed.
