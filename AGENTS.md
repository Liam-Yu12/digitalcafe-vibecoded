# AGENTS.md

## Project
Rebuild "Digital Cafe" — a Django + SQLite web app for ordering food/drinks
from a cafe, with customer and staff roles.

## Required Workflow

For every feature or change, follow this process in order. Do not skip
or combine stages.

1. **study** — Analyze my request and write a Markdown file in `doc/study/`
   discussing feasibility, tradeoffs, and open questions. Do not write code
   in this stage.
2. **plan** — Based on the study doc, write a checklist Markdown file in
   `doc/plan/` with concrete, ordered steps to implement the feature.
3. **execute plan** — Create a new git branch off `main` and implement the
   plan doc step by step. Commit as you go using Conventional Commits
   (`feat:`, `fix:`, `chore:`, `build:`, `docs:`, `refactor:`, etc.).
4. **rendezvous** — Once the plan is complete and the app is in a working
   state, merge the branch back into `main`. Confirm the app still runs
   before merging.
5. **sync docs** — Update the living documentation in `doc/wiki/` so it
   accurately reflects the current state of the codebase (models, routes,
   features, setup instructions).

Wait for my explicit go-ahead between stages (e.g. after a study doc,
wait for me to approve before writing a plan doc). Do not jump straight
from a request to code.

## Folders
- `doc/study/` — study docs (analysis, feasibility, tradeoffs)
- `doc/plan/` — plan docs (checklists)
- `doc/wiki/` — living manual of the current codebase

## Commit style
Use Conventional Commits for every commit: `feat:`, `fix:`, `chore:`,
`build:`, `docs:`, `refactor:`, `test:`, etc.

## Stack
- Backend: Django
- Database: SQLite
- Keep templates server-rendered (Django templates), no separate frontend
  framework unless I ask for one.