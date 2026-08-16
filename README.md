# Torch & Key Freelancer Scout

![Torch & Key Freelancer Scout emblem](assets/TK_Freelancer_Scout.png)

> Bounded opportunity intelligence for human-reviewed freelance project intake.

Torch & Key Freelancer Scout is an internal business-development aid for Torch & Key's freelance services work. It helps a human operator discover and review potentially suitable Freelancer projects. The Scout is not a marketplace, bidding bot, or autonomous contracting agent.

## Initial capability boundary

The initial Scout is read-only. It may:

- search active project listings;
- retrieve project details needed for qualification;
- organize opportunities for human review; and
- prepare non-binding bid/no-bid recommendations.

It may not:

- place or withdraw bids;
- send or read messages;
- accept awards or projects;
- create, release, dispute, or otherwise manage milestones;
- modify account, profile, project, contest, or financial data; or
- take any contractual or financial action.

Any future capability beyond read-only retrieval requires explicit authorization from CJ before each action surface is enabled. A recommendation is not authorization.

## Business model

Torch & Key earns revenue by completing freelance projects for clients. The Scout supports opportunity discovery and project intake; it is not sold as a service, and Freelancer data is not resold, redistributed, or monetized.

## Data and privacy

The public sample requests only the data needed to return matching active projects. Credentials are supplied at runtime and must never be committed. The sample prints API responses to standard output and does not create a local database, analytics stream, or evidence archive. See [PRIVACY.md](PRIVACY.md).

## Public read-only sample

`src/freelancer_scout.py` is deliberately small and exposes one operation: search active projects with an HTTP `GET`. It contains no methods for bids, messages, awards, milestones, or account mutation.

```powershell
$env:FLN_OAUTH_TOKEN = "your-local-token"
python .\src\freelancer_scout.py --query "data extraction" --limit 10
```

Use a Freelancer sandbox credential and `--sandbox` for development. Never paste a token into source code, issues, logs, screenshots, or commits.

Run the offline boundary checks with:

```powershell
python -m unittest discover -s tests -v
```

## Application home

The concise reviewer-facing application description is in [index.md](index.md). This repository is intended to be the application's public informational home once the repository owner makes it public.

## Status

Early read-only integration. Human review is mandatory. No automated marketplace action is authorized.

