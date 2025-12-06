## agentops build

Awesome — here’s the minimum viable, repeatable setup that works on a clean machine and avoids all the auth & networking rabbit holes.

I’ll keep it tight and give you copy-paste blocks.

⸻

0) Prereqs
	•	Docker + Docker Compose
	•	A Supabase project (cloud or local CLI) with keys handy
	•	No need to run anything natively; we’ll use app/compose.yaml (the project’s recommended path).  ￼

⸻

1) Configure env (once)

From repo root:

cd app
cp .env.example .env

Edit app/.env minimally:

# URLs
APP_URL=http://localhost:3000
NEXT_PUBLIC_SITE_URL=http://localhost:3000

# Supabase (get from your project)
NEXT_PUBLIC_SUPABASE_URL=https://<YOUR_PROJECT>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<anon>
SUPABASE_SERVICE_ROLE_KEY=<service_role>
SUPABASE_PROJECT_ID=<proj_id>

# API auth
JWT_SECRET_KEY=change-me-to-long-random-string

# ClickHouse (local CH service from compose)
CLICKHOUSE_HOST=clickhouse
CLICKHOUSE_PORT=8123
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=password
CLICKHOUSE_DATABASE=otel_2
CLICKHOUSE_SECURE=false

(Those CH defaults match the repo’s Docker guide.)  ￼

⸻

2) Bring up the stack

cd app
docker compose --profile dashboard -f compose.yaml up -d

Check health:

docker compose --profile dashboard -f compose.yaml logs --since=60s api
docker compose --profile dashboard -f compose.yaml logs --since=60s dashboard

API docs: http://localhost:8000/redoc
Dashboard: http://localhost:3000
(Those endpoints are what the “Backend Setup” docs describe.)  ￼

⸻

3) Initialize ClickHouse schema (one-liner, ordered)

You’ve got these files:
0000_init.sql, 0001_udfs_and_pricing.sql, 0002_span_counts_mv.sql, 0003_seed_model_costs.sql.

Apply them in order:

# ensure CH is up
until curl -sf http://localhost:8123/ping >/dev/null; do sleep 1; done

# create DB (idempotent)
docker compose --profile dashboard -f app/compose.yaml exec clickhouse \
  clickhouse-client -u default --password password \
  -q "CREATE DATABASE IF NOT EXISTS otel_2;"

# run 0000 → 0003
cat app/clickhouse/migrations/0000_init.sql \
    app/clickhouse/migrations/0001_udfs_and_pricing.sql \
    app/clickhouse/migrations/0002_span_counts_mv.sql \
    app/clickhouse/migrations/0003_seed_model_costs.sql \
	0004_seed_model_costs_full.sql \ 
| docker compose -f app/compose.yaml --profile dashboard exec -T clickhouse \
  clickhouse-client -u default --password password -nm --database otel_2

# quick verify: UDFs + tables
docker compose -f app/compose.yaml --profile dashboard exec clickhouse \
  clickhouse-client -u default --password password \
  -q "SHOW FUNCTIONS LIKE 'calculate_%'"

curl -s -u default:password \
  'http://localhost:8123/?query=SHOW%20TABLES%20FROM%20otel_2'

If the functions don’t show up, re-run that block — 0001 is the file that defines them.

⸻

4) (If you’re using local Supabase) push PG migrations

If you ran supabase start locally, from repo root:

cd supabase
npx supabase db push

If you use Supabase Cloud, you don’t run the CLI; just ensure your service role key is in app/.env. (The self-hosting overview calls out Supabase as the primary DB/auth.)  ￼

⸻

5) Generate traces locally (no auth drama)

You can ignore “API key → JWT” for local dev. Just send OTLP to the local collector — that’s enough for traces to appear in the dashboard.

Option A — run from your devcontainer that’s on the app_default network:

export AGENTOPS_EXPORTER_ENDPOINT=http://otelcollector:4318/v1/traces
export AGENTOPS_API_ENDPOINT=http://api:8000
# optional: quiet nonessential log uploads in some SDK versions
export AGENTOPS_DISABLE_LOG_UPLOAD=1

python examples/openai/openai_example_sync.py

Option B — run from host:

export AGENTOPS_EXPORTER_ENDPOINT=http://localhost:4318/v1/traces
python examples/openai/openai_example_sync.py

(OTLP ingestion does not require a JWT; the docs’ Docker guide emphasizes collector → ClickHouse as the data path.)  ￼

Verify in ClickHouse (authoritative):

curl -s -u default:password \
  "http://localhost:8123/?query=SELECT%20count()%20FROM%20otel_2.otel_traces"

You should see > 0. Then open the dashboard Traces view and/or the Sessions link the example prints.

⸻

6) (Optional) If you want a project token like cloud

Your API exposes a public exchange:

PROJECT_TOKEN=$(curl -s http://localhost:8000/public/v1/auth/access_token \
  -H 'Content-Type: application/json' \
  -d '{"api_key":"'"$AGENTOPS_API_KEY"'"}' \
  | python - <<'PY'
import sys,json; print(json.load(sys.stdin)["access_token"])
PY
)

Use Authorization: Bearer $PROJECT_TOKEN only on /public/v1/* endpoints (it won’t auth /opsboard/*, which is for the dashboard’s user session). That exact route and semantics are in the backend docs.  ￼

⸻

Quick Troubleshooting (copy-paste)
	•	Dashboard 500 with “unknown function calculate_prompt_cost”
You skipped 0001/0003. Re-run Step 3.
	•	SDK prints “Failed to get JWT token: 404” / “0 spans recorded”
That’s the example’s cloud check. Ignore it locally; rely on the ClickHouse count in Step 5. (OTLP path is independent.)  ￼
	•	Devcontainer can’t reach api:8000
Attach it to the compose network:

docker network connect app_default $(cat /etc/hostname)

Or use http://host.docker.internal:8000 from the devcontainer.

⸻

Make it one command next time

Add this to your Makefile:

COMPOSE := cd app && docker compose --profile dashboard -f compose.yaml
CLICKHOUSE_USER ?= default
CLICKHOUSE_PASSWORD ?= password
CLICKHOUSE_DB ?= otel_2

.PHONY: up migrate-clickhouse supabase-migrate ch-verify

up:
	$(COMPOSE) up -d

migrate-clickhouse:
	@until curl -sf http://localhost:8123/ping >/dev/null; do sleep 1; done
	$(COMPOSE) exec clickhouse \
	  clickhouse-client -u $(CLICKHOUSE_USER) --password $(CLICKHOUSE_PASSWORD) \
	  -q "CREATE DATABASE IF NOT EXISTS $(CLICKHOUSE_DB);"
	cat app/clickhouse/migrations/0000_init.sql \
	    app/clickhouse/migrations/0001_udfs_and_pricing.sql \
	    app/clickhouse/migrations/0002_span_counts_mv.sql \
	    app/clickhouse/migrations/0003_seed_model_costs.sql \
	| $(COMPOSE) exec -T clickhouse \
	  clickhouse-client -u $(CLICKHOUSE_USER) --password $(CLICKHOUSE_PASSWORD) -nm --database $(CLICKHOUSE_DB)

ch-verify:
	@$(COMPOSE) exec clickhouse \
	  clickhouse-client -u $(CLICKHOUSE_USER) --password $(CLICKHOUSE_PASSWORD) \
	  -q "SHOW FUNCTIONS LIKE 'calculate_%'"
	@curl -s -u $(CLICKHOUSE_USER):$(CLICKHOUSE_PASSWORD) \
	  "http://localhost:8123/?query=SHOW%20TABLES%20FROM%20$(CLICKHOUSE_DB)" | sed 's/^/ - /'

supabase-migrate:
	cd supabase && npx supabase db push

Daily flow:

make up
make migrate-clickhouse
# (if local Supabase) make supabase-migrate
make ch-verify

That’s the leanest, least fragile path that aligns with the project’s self-hosting + Docker docs.  ￼

If anything still feels sticky, paste the first failing command + output and I’ll zero in on it.


#### Further notes:
1. To get project id, in your supabase run:
 ```select id, name from public.projects;```