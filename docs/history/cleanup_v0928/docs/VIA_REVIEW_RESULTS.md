# Current via findings

This summary replaces the chronological investigation as the current view. [The viewer](VIA_REVIEW.html) and `evidence/via_audit.json` retain all per-site reports, corrections and rejected recognition artifacts. [Historical text](history/README.md) remains available.

- 123 IDs reviewed; 120 active sites after recognition-artifact rejection. Four unmentioned IDs were already photo-matched ground candidates. These are inventory counts, not a remaining-wire count.
- All PIC pads have modeled local nets. The residual search pool has nine sites in eight local groups; these are not eight proven missing nets.
- No broad via-pair measurement sweep is pending. Seven capacitor-pair OL results and the rejected V053/VREF/V071 joins remain recorded.

| Confirmed report | Current interpretation |
|---|---|
| V022-V016 | PIC15/RC4 to U5.2/INA |
| V023-V019 | PIC16/RC5 to U5.3/INB |
| V036-V108 | PIC5/RA3 to R14 |
| V037-V102 | PIC6/RA4 to R15 |
| V039-V097 | PIC7/RA5 to R16 |
| V047-V091 | PIC11/RC0 to R11 |
| V049-TP3 | PIC13/RC2; R10 local branch photo-derived |
| V053-V070 | PIC12/RC1 to R18.1; not VREF |
| V026, V035, V071 to VREF | PIC21, PIC4/C39, R21.2 respectively |
| V042 to VDD | PIC20/C32.1 logic supply |
| V064-V063 | VDD feed to R37/R39 |
| V064-V075 | Q7 supply node; exact terminal selection remains photo-derived |
| V067-J3.1 | Red PIR supply; U6A option association retained, still DNP |
| V015-TP14 | R43.2 on raw BATTERY+; separate from Q1.L |
| V017-TP4 | R42.1/R44.1 and PIC25/RB4; local pad selections photo-derived |
| V082-VDD TP | VDD confirmed; D3 terminal still unknown |
| V011-V014-Q1.L-U5.4 | VSYS, separate from BATTERY+ and board VDD |
| L1/L2 same VSYS | Supply sides share VSYS; opposite filter ends remain separate |
| V114 | U2.T2/native2 GND, not Q8 |
| V113/V115 | Q8 centre B2/native5 GND |
| V077 | C19/R29 junction GND |
| V072 / V079-V080 | TP6 / U3.5 respectively; separated across C18 |
| V125/V126 / V127 | C5 negative / photo-selected LED common ground |

The remaining candidate groups are V031 (PIC2/C25), V072 (TP6/C18.2), V079/V080 (U3.5), and V090/V095/V100/V103/V107 (five capacitor midpoints). The [completion checklist](FINISHING_CHECKLIST.html) also covers gaps with no unresolved via ID: D2/D3/D6, C6, button/antenna endpoints, identities, values and geometry.

A user report that a via reaches a component does not establish which pad unless specified. Do not promote all attached hypothetical branches to measured status. Surface clearance does not identify an inner-layer net or prove a four-layer stack.
