# POST-RESULT CORRECTION (2026-07-22, after external audit round 7)
# Corrects two defects in final2.py's H2 computation:
#  (1) Endpoint: pd.Timestamp('2023-02-17') is MIDNIGHT Feb 17, so the
#      <= filter silently excluded Feb 17's trade. Manifest requires
#      entries through Feb 17 inclusive -> filter is < 2023-02-18.
#      Correct H2: 1,769 trades (1,766 valid), $212,427, not $214,640.
#  (2) Method name: the "valid-only" equity path is an EQUITY-NORMALIZED
#      RECONSTRUCTION: r_i = pnl_i / (25000 + cum pnl of ALL prior
#      trades), compounded over valid trades only. Mathematically
#      identical to recursively rescaling each P&L by clean/TV equity —
#      a continuous-share approximation, not raw row removal (raw
#      removal gives $223,351, a different and less defensible number).
# PF note: PF computed on equity-NORMALIZED per-trade returns is 1.250
# and passes the manifest's >1.2 criterion; PF on raw exported DOLLARS
# is 1.173 and fails it. The manifest did not specify which basis.
# Both are reported; the ambiguity is recorded as a pre-registration
# drafting defect, resolved conservatively: the criterion is scored as
# NOT CLEANLY PASSED.
