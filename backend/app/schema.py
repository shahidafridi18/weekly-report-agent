COUNTERPARTY_KEY_COLUMNS = (
    "SIREN",
    "Unique Identifier",
)

COUNTERPARTY_TEXT_COLUMNS = (
    "Counterparty Name",
    *COUNTERPARTY_KEY_COLUMNS,
)

COUNTERPARTY_METRIC_COLUMNS = (
    "Gross CE",
    "Collateral Received",
    "IM Received",
    "VM Received",
    "Net CE",
    "CVA Balance",
    "Derivatives PE",
    "Derivatives SA-CCR EAD",
    "Collateral Received as a Third-Party",
    "Securities Lending/Borrowing PE",
    "Repo/Reverse/Repo PE",
    "Credit hedge notional",
    "Credit hedge Market Value",
    "Total STMP",
    "STMP: Open or Overnight",
    "Equity MTM",
    "Equity Derivatives",
    "Fixed Income MTM",
    "Fixed Income Derivatives",
    "Notional of CDS Bought",
    "Notional of CDS Sold",
    "Net Notional CDS",
    "Net MTM CDS",
    "Net JTD CDS (structured products)",
)

NON_METRIC_COLUMNS = frozenset(
    {
        "Rank",
        "Counterparty Name",
        *COUNTERPARTY_KEY_COLUMNS,
    }
)