# Agent Torch Protocol

Lightweight coordination layer for all AI agents working in `/home/sin/Projects`.

## File
- `/home/sin/Projects/.agent-coordination/torch.json`

## Commands
Use `/home/sin/.hermes/scripts/agent-torch.sh`:
- `status` — show active torches + pending queue
- `pass <agent> <project> <task-id> <status>` — hand off work
- `claim <agent> <project> <task-id>` — take a task
- `done <agent> <task-id> <result>` — mark complete
- `next <agent>` — assign next pending task to agent

## Rules
1. Read `status` before claiming new work
2. Only one agent per task at a time
3. Update `status` immediately on handoff/completion
4. Never modify another agent's active torch without coordination
5. All timestamps UTC ISO8601
