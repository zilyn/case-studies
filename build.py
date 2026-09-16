"""Builds the portfolio pages from the content below.

    python build.py

Writes index.html, one page per project, and 404.html next to this file.
Styles live in assets/site.css and the small script in assets/site.js.
"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "https://zilyn.github.io/case-studies/"
CALENDLY = "https://calendly.com/bayoadegokeiyanu/meeting-with-jonathan"
EMAIL = "bayoadegokeiyanu@gmail.com"
GITHUB = "https://github.com/zilyn"

CATS = {
    "outreach": "Outreach",
    "intelligence": "Intelligence",
    "ai": "AI systems",
    "ops": "Operations",
    "product": "Product",
}
STATUS = {
    "live": ("Live", "running for my own business right now"),
    "client": ("Client", "built for a client and handed over"),
    "built": ("Built", "a working system that proves the pattern, not deployed for a client yet"),
}

# node types: trigger, fetch, transform, ai, store, send
PROJECTS = [
    dict(
        slug="linkedin-outreach",
        title="LinkedIn cold outreach system",
        cat="outreach",
        status="live",
        featured=True,
        one="Finds people on LinkedIn, reads their recent posts, writes each of them a short email with Claude and sends it. Running for my own business.",
        lede="Two n8n workflows. The first finds leads on LinkedIn and writes each one an email that refers to something they actually posted. The second sends those emails one at a time and keeps the sheet honest.",
        index_facts=[("91", "emails sent, first run"), ("2", "replies in 24 hours"), ("$3", "per 100 leads")],
        facts=[("Trigger", "manual search, then a daily send job"), ("Cap", "100 emails a day"), ("Spacing", "30 s between sends"), ("Cost", "about $3 per 100 leads")],
        why=[
            "I wanted outreach that reads like I wrote it, without spending a day writing a hundred emails. Most tools send the same template to everyone and people can tell.",
        ],
        canvases=[
            dict(title="Workflow 1. Lead scout", nodes=[
                ("fetch", "Apify search", "LinkedIn profiles, up to 300"),
                ("transform", "Filter", "dupes, excluded companies, no email"),
                ("fetch", "Scrape posts", "last 5 posts per person"),
                ("ai", "Claude", "subject and body from real posts"),
                ("store", "Google Sheets", "full lead record"),
            ]),
            dict(title="Workflow 2. Outreach engine", nodes=[
                ("trigger", "Daily run", "reads the sheet"),
                ("transform", "Filter new", "cap at 100 a day"),
                ("send", "Gmail", "30 s between sends"),
                ("store", "Mark sent", "never emails twice"),
            ]),
        ],
        steps=[
            ("Search", "Apify searches LinkedIn for a keyword like \"founder fintech\" and returns up to 300 profiles with names, titles, companies and emails."),
            ("Filter", "Duplicates, companies I don't want to contact and anyone without an email are dropped."),
            ("Read their posts", "For each lead the workflow pulls their last five LinkedIn posts. This is what makes the email specific to the person."),
            ("Write the email", "Claude gets the bio, title, company and posts and writes a short email that refers to something the person said. The prompt bans buzzwords, asks for contractions and keeps it under a few lines."),
            ("Save", "Everything lands in a Google Sheet: name, email, subject, body, a connection note, a lead score and a status of \"new\"."),
            ("Send", "The second workflow reads the sheet, takes the \"new\" rows, stops at 100 for the day and sends each one through Gmail with 30 seconds between sends."),
            ("Mark sent", "After each send the row flips to \"sent\", so nobody gets the same email twice."),
        ],
        outcome=[
            "The first run sent 91 emails. Two people replied within 24 hours, one of them booked a call.",
        ],
        outcome_facts=[("91", "emails sent"), ("2", "replies in 24 h"), ("1", "call booked"), ("$3", "per 100 leads")],
        quotes=[
            ("Shane Martin", "Fund manager and accelerator founder, B Ventures", "Could you share more use cases and examples? I'm super curious about this."),
            ("Teddy White", "Operations lead, Syntharos", "Asked for a resume and a WhatsApp number. Call booked within 24 hours."),
        ],
        notes=[
            "Two replies from 91 sends is a small sample, so I'm not calling it a reply rate yet. The 30 second spacing and the daily cap are what keep the Gmail account safe. The search step is the part that needs the most care, because LinkedIn limits how much you can pull.",
        ],
        stack=["n8n", "Apify (LinkedIn search, post scraper)", "Claude API", "Gmail", "Google Sheets", "Python"],
    ),
    dict(
        slug="buyer-intent-pipeline",
        featured=True,
        title="Buyer intent research pipeline",
        cat="intelligence",
        status="client",
        one="A nightly system of 28 n8n workflows that finds buying signals across the web, turns them into scored, tiered companies with verified contacts, and feeds a sales CRM. Built over a year for a B2B sales intelligence company.",
        lede="This started as the weekly company monitor and grew into the whole back end of a sales intelligence business. Collectors find signals, an orchestrator turns them into companies and scores them, enrichers add people and firmographics, verifiers check every email and phone, and a weekly loop re-researches the companies that went quiet. It all runs overnight.",
        index_facts=[("28", "workflows, nightly"), ("3,300", "companies tracked"), ("2,800+", "emails verified")],
        facts=[("Runs", "nightly, 28 n8n workflows"), ("Companies", "about 3,300, 900 in the top two tiers"), ("Contacts", "4,000+, every email checked"), ("Client", "B2B sales intelligence company")],
        why=[
            "The client sells to companies that are about to spend on AI and consulting. The signal that they're about to spend shows up in the news, in hiring, in filings and on company sites, but nobody can read all of that for thousands of companies. The first version watched 200 companies once a week. The client wanted every company they might ever sell to, scored every night, with someone to call.",
        ],
        canvases=[
            dict(title="Every night", nodes=[
                ("trigger", "Collectors", "Tavily, filings, news, hiring"),
                ("transform", "Orchestrator", "signal to company, dedupe"),
                ("transform", "Score", "deterministic tiers"),
                ("ai", "Claude", "description, fit, problem"),
                ("fetch", "Enrich", "domain, firmographics, people"),
                ("fetch", "Verify", "email and phone"),
                ("store", "Supabase", "CRM reads it"),
            ]),
            dict(title="Every week", nodes=[
                ("trigger", "Monday", "stuck companies"),
                ("fetch", "Re-research", "biggest first"),
                ("transform", "Classify", "new signals"),
                ("store", "Re-score", "next night"),
            ]),
        ],
        steps=[
            ("Collect", "Several collectors search for signals: funding, layoffs, leadership changes, AI initiatives, regulatory pressure, new hires. Each signal is stored with its source and date."),
            ("Match", "The orchestrator matches every signal to a company, creates the company if it's new and drops duplicates. A name quality gate stops headline fragments from becoming companies, which was the biggest source of junk early on."),
            ("Score", "Scoring is plain JavaScript, not a model, so the same evidence always scores the same way. Companies land in four tiers from Tier 1 to Discard, and the tier drives everything downstream."),
            ("Describe", "Claude writes the description, the fit against the client's offerings and a short problem statement for each company in the top tiers."),
            ("Enrich", "A resolver finds the company domain, then Apollo adds decision makers for 75 companies a night, highest tier first. Domain coverage for the top tiers went from 75% to 97%."),
            ("Verify", "Every new contact goes through NeverBounce for the email and Twilio for the phone line type, plus checks against LinkedIn, the company site, GitHub and the domain's mail records. 350 contacts a night."),
            ("Re-research", "Companies that scored well but went quiet get re-searched every Monday, biggest first, because the small ones return nothing but generic headlines."),
            ("Draft", "For companies that clear the bar, Claude drafts an outreach sequence and a QA gate checks every claim in it before a person sees it."),
        ],
        outcome=[
            "The client's team opens the CRM in the morning and the night's work is there: new companies, tiers, people with checked emails and a reason to call. About 3,300 companies are tracked, 900 or so sit in the top two tiers, and 2,800 plus emails have been validated. A cleanup in August took 64 workflows down to 28 without losing a function.",
        ],
        outcome_facts=[("3,300", "companies tracked"), ("900", "in the top two tiers"), ("4,000+", "contacts"), ("97%", "domain coverage, top tiers")],
        notes=[
            "The expensive lesson: Supabase's REST layer silently caps a response at 1,000 rows. One background worker read its done list unpaged, the list crossed 1,000, and it regenerated the same work every two minutes for five weeks. That was about half of one month's API bill. Every worker that calls a paid API now pages its reads, caps its attempts per day and logs its usage.",
            "The other lesson is that signal discovery is not the same as per company research. A company nobody writes about never improves its score on its own, which is why the weekly re-research loop exists.",
        ],
        stack=["n8n", "Supabase (Postgres)", "Claude API", "Tavily", "Apollo", "NeverBounce", "Twilio Lookup", "Prospeo", "JavaScript", "Python"],
    ),
    dict(
        slug="signals-saas",
        featured=True,
        title="Multi-tenant buyer intent product",
        cat="product",
        status="client",
        one="Took the client's demo screens and built them into a real multi-tenant SaaS in three weeks: own auth, invites and roles, one data lake with row level isolation, a release gate, fail-soft behaviour and an in-app assistant.",
        lede="The sales intelligence client wanted to sell the signals as a product, not a service. In three weeks the demo screens became a tenant app with accounts, workspaces, invites, roles, trials, an isolation harness that runs before every release, and an assistant that answers questions about the workspace's own data.",
        index_facts=[("3 wks", "demo to MVP"), ("29/29", "isolation checks"), ("0.5.0", "releases shipped")],
        facts=[("Built", "three weeks, demo to MVP"), ("Tenancy", "one lake, org id on every row, RLS backstop"), ("Isolation", "29 checks, run before every release"), ("Client", "B2B sales intelligence company")],
        why=[
            "The pipeline above produced the data. The client needed other companies to be able to log in and see only their own slice of it, invite their team, rate signals and get a brief, without any of it leaking across workspaces. And it had to be demoable to partners in under two weeks.",
        ],
        canvases=[dict(title="Request path", nodes=[
            ("trigger", "Browser", "session cookie"),
            ("transform", "App", "Python, own container"),
            ("transform", "Policy", "org membership, role"),
            ("fetch", "Supabase", "per request JWT, RLS"),
            ("ai", "Ask", "Sonnet, ten scoped tools"),
            ("store", "Audit", "every write logged"),
        ])],
        steps=[
            ("Auth", "Extended the client's existing password auth rather than adding a vendor: invites and resets by email, sessions with a version number so a revoke logs everyone out, a 90 day hard cap, roles per workspace."),
            ("Tenancy", "Every row carries the workspace id. The app injects it server side on every query, and as a second line the database enforces row level security with a token minted per request. Both were proven at the database: the right workspace reads its rows, a bogus one gets nothing, a forged token gets a 401."),
            ("Isolation harness", "29 HTTP checks that try to read across workspaces as a stranger, a member, an admin and a former member. It runs before every release and has to be green."),
            ("Release gate", "A scripted browser walk through the product, a dependency scan and the harness. A release that fails any of them doesn't ship. Five releases went through it in the first three weeks."),
            ("Fail soft", "Built during a live database incident. Store errors show a one moment page instead of a broken product, the dataset is served stale while a refresh runs in the background, and a disk copy survives a restart. Two uptime monitors watch it, one inside the box and one on GitHub."),
            ("Ask", "An assistant inside the app on Claude Sonnet with ten read only tools that only see the workspace's own data. Twenty questions an hour per person, sixty a day per workspace, thirteen out of thirteen on the eval."),
        ],
        outcome=[
            "The product went from a set of demo boards to release 0.5.0 on production in three weeks, with the partner demo made and testers on a staging copy. A stress run of 300 concurrent requests came back with no errors and isolation held.",
        ],
        outcome_facts=[("3 wks", "demo to MVP"), ("0.5.0", "on production"), ("29/29", "isolation checks"), ("300", "requests, 0 errors")],
        notes=[
            "The whole app is Python standard library, no framework, which the client's ops setup made the right call. One thing that bit: with strict tool schemas where every field is required, Sonnet fills the fields it doesn't need with fragments of its own tool markup. Optional fields are nullable now and inputs are scrubbed.",
        ],
        stack=["Python", "Supabase (Postgres, RLS)", "Docker", "Traefik", "Claude API (Sonnet)", "Playwright", "GitHub Actions", "n8n"],
    ),
    dict(
        slug="crm-assistant",
        featured=True,
        title="In-CRM AI assistant",
        cat="ai",
        status="client",
        one="A chat assistant inside the client's CRM that answers questions about the pipeline from live data across 23 tables, logs issues and runs a few safe actions. Rebuilt for accuracy from 4 of 9 right to 13 of 13.",
        lede="The client's sales team wanted to ask the CRM questions in plain English: what's in the pipeline, who at this company have we spoken to, which deals are stuck. The first version answered confidently and was wrong almost half the time. The rebuild is what this case study is about.",
        index_facts=[("13/13", "eval, was 4/9"), ("23", "tables it can read"), ("~$1", "a month to run")],
        facts=[("Model", "Claude Opus in a tool loop"), ("Data", "23 CRM tables, read only"), ("Eval", "13 of 13, including traps"), ("Cost", "about a dollar a month")],
        why=[
            "The first version ran on a small model with one read tool that returned 100 rows. Asked for the pipeline total it summed one page and invented the rest, off by $600k. Asked about a live Tier 1 account it said the company wasn't in the system. Asked about a field that shipped the week before it said the field didn't exist. All three answers sounded certain.",
        ],
        canvases=[dict(title="One question", nodes=[
            ("trigger", "Question", "in the CRM widget"),
            ("ai", "Claude", "plans the lookups"),
            ("fetch", "search_crm", "name, domain, ticker"),
            ("transform", "aggregate_rows", "totals in Python"),
            ("fetch", "list_columns", "live schema"),
            ("send", "Answer", "plain language, no dashes"),
        ])],
        steps=[
            ("Stronger model, own setting", "The assistant runs on Claude Opus with its own model constant. Reply classification and social drafts stay on the cheap model. The two are deliberately separate."),
            ("Search that finds things", "A search tool that tries the full phrase, the phrase with spaces removed and the longest words, across name, domain and ticker. That's what finds a company whose row is named differently from how people say it."),
            ("Totals in Python", "Sums, counts and breakdowns page through every row in Python and hand the model a number. The model never adds rows itself."),
            ("Facts from the data", "The prompt used to hardcode thresholds and a column list, both stale. Now it reads the config table and asks the database for the live schema."),
            ("Prompt caching", "Everything per request, the user, the date, the open record, rides on the user turn instead of the system prompt, so about 20,000 tokens a turn come from cache."),
            ("Eval", "Thirteen real questions with answers checked against paged database queries, including a fake company that must come back as not found."),
        ],
        outcome=[
            "Thirteen of thirteen on the eval, including the adversarial cases. The pipeline total matches the database to the dollar. The whole thing costs about a dollar a month to run because of the caching.",
        ],
        outcome_facts=[("13/13", "correct, was 4/9"), ("23", "tables, was 12"), ("20k", "tokens a turn from cache"), ("~$1", "a month")],
        notes=[
            "My own first set of ground truth answers was wrong for the same reason the bot was: Supabase's REST layer caps a response at 1,000 rows and says nothing. The fix is the same in both places, page it or read the count off the header. Two tables that hold credentials are excluded from the assistant on purpose.",
        ],
        stack=["Python", "Claude API (Opus)", "Supabase (Postgres)", "Docker", "Prompt caching"],
    ),
    dict(
        slug="workflow-sentinel",
        title="Workflow watchdog and uptime monitor",
        cat="ops",
        status="client",
        one="A daily n8n job that checks every other workflow, tells a stall from a weekly schedule, re-fires what it can, flags what needs money, and only emails a person when it can't fix the problem itself.",
        lede="Built the day I found a nightly workflow had been failing for two weeks and nobody knew. The client's rule was simple: everything must run all the time, check daily, heal what you can, email me only when you can't.",
        index_facts=[("Daily", "checks 28 workflows"), ("5 min", "uptime probe")],
        facts=[("Runs", "daily at 06:30 UTC"), ("Watches", "every active workflow"), ("Heals", "re-fires once, never twice"), ("Emails", "only when a person is needed")],
        why=[
            "Two dozen scheduled workflows and no one watching them. A failure only surfaced when someone noticed the data had stopped moving, which on a nightly pipeline can take weeks.",
        ],
        canvases=[dict(title="Every morning", nodes=[
            ("trigger", "06:30", "daily"),
            ("fetch", "n8n API", "all active workflows"),
            ("fetch", "Executions", "last 20 each"),
            ("transform", "Classify", "error, stall, credits"),
            ("send", "Re-fire", "the workflow's own webhook"),
            ("store", "Heartbeat", "alerts table"),
            ("send", "Email", "only if action needed"),
        ])],
        steps=[
            ("List", "Pulls every active workflow through the n8n API and the last twenty executions of each."),
            ("Errors", "Anything that errored in the last 24 hours and hasn't since recovered is flagged."),
            ("Stalls", "A stall threshold per workflow: at least 36 hours, or 1.8 times that workflow's usual gap between runs, so a Monday job isn't reported missing on Wednesday."),
            ("Credits", "Failures that match a credit or quota message, from the AI API, the enrichment provider, the email checker or the search API, are marked action needed and never re-fired. Re-firing those only burns more."),
            ("Heal", "Everything else gets its own production webhook fired once. If it recovers, the next morning's report says so."),
            ("Report", "A heartbeat row goes into an alerts table every day with the findings, and an email goes out only when a person has to do something."),
            ("Uptime", "A second job probes the public apps every five minutes and emails on down and on recovery. A GitHub Actions check does the same from outside the box every fifteen minutes and opens an issue, so an outage of the box itself still gets seen."),
        ],
        outcome=[
            "The first live run caught a verifier that had been timing out every night and a nightly job running out of memory, and re-fired the first one. Since then the morning email is the only way anyone hears about a broken workflow, and most days there isn't one.",
        ],
        outcome_facts=[("2", "real failures caught on run one"), ("1", "email a day at most"), ("0", "silent failures since")],
        notes=[
            "The adaptive stall threshold is the part worth copying. A fixed number either misses a stalled nightly job or cries wolf on every weekly one. Two things I learned the hard way: the n8n container resolves its own public hostname to itself, so the box has to be probed from outside, and workflow static data only persists on production runs, not editor test runs.",
        ],
        stack=["n8n", "n8n public API", "Supabase", "Microsoft Graph mail", "GitHub Actions"],
    ),
    dict(
        slug="video-generator",
        title="Personalized video generator",
        cat="ai",
        status="client",
        one="Picks the highest priority leads from Supabase, has Claude write a 45 second script, sends it to Visla to render and saves the video link back on the lead.",
        lede="A workflow that runs every five minutes, takes the leads with the highest pain score, writes each one a short video script with Claude and has Visla render a presenter video. The sales team opens the lead and the video is already there.",
        index_facts=[("5 min", "cycle time"), ("0", "manual steps")],
        facts=[("Trigger", "every 5 minutes"), ("Script", "45 seconds"), ("Render check", "every 30 s"), ("Manual steps", "none")],
        why=[
            "Video gets replies, but recording one per prospect takes hours. So teams either skip it or send one generic video to everyone, which defeats the point.",
        ],
        canvases=[dict(title="Pipeline", nodes=[
            ("trigger", "Schedule", "every 5 minutes"),
            ("fetch", "Supabase", "high priority leads, no video yet"),
            ("ai", "Claude", "45 second script"),
            ("fetch", "Visla", "HMAC signed request"),
            ("transform", "Poll", "until rendered"),
            ("store", "Save URL", "back on the lead"),
        ])],
        steps=[
            ("Pick the leads", "Every five minutes the workflow pulls leads from Supabase that are marked high priority and don't have a video yet. Each one carries company context, pain signals and contact details."),
            ("Write the script", "Claude writes a 45 second script that refers to the lead's specific pain point and keeps the tone conversational."),
            ("Sign the request", "Visla wants HMAC signed requests, so the workflow builds the signature fresh before every call."),
            ("Render", "Visla generates the presenter video from the script."),
            ("Wait", "The workflow polls Visla every 30 seconds until the render is done, so slow renders don't break anything."),
            ("Save", "The video URL goes back on the lead record in Supabase for the sales team."),
        ],
        outcome=[
            "From lead to video link is about five minutes plus render time, with nobody touching it.",
        ],
        outcome_facts=[("5 min", "cycle time"), ("45 s", "per video"), ("0", "manual steps")],
        notes=[
            "Render time varies a lot, so the polling loop is what makes this reliable. The HMAC step was the fiddly part. The signature has to be rebuilt for every request or Visla rejects it.",
        ],
        stack=["n8n", "Claude API", "Visla API", "Supabase", "HMAC auth"],
    ),
    dict(
        slug="company-monitor",
        title="Company intelligence monitor",
        cat="intelligence",
        status="client",
        one="Every Monday it reads a list of target companies, searches for fresh signals like funding, hiring and leadership changes, scores them and pushes the hot ones into the CRM.",
        lede="A weekly system that watches a list of 200 or so target companies for things worth a call. It searches, drops what it has already seen, scores what's new and pushes anything above the line into GoHighLevel with the evidence attached.",
        index_facts=[("Mon 06:00", "weekly run"), ("200+", "companies watched")],
        facts=[("Trigger", "Mondays, 06:00"), ("Companies", "200+"), ("Sources", "Tavily and Jina search"), ("Output", "GoHighLevel CRM")],
        why=[
            "Sales teams have long target lists but no way of knowing when a company is actually ready to talk. Nobody has time to check the news on 200 companies every week, so the signals get missed.",
        ],
        canvases=[dict(title="Weekly run", nodes=[
            ("trigger", "Monday 06:00", "schedule"),
            ("fetch", "Airtable", "target companies"),
            ("fetch", "Tavily + Jina", "recent news per company"),
            ("transform", "Dedupe", "drop known signals"),
            ("transform", "Score", "urgency and fit"),
            ("send", "GoHighLevel", "hot leads with evidence"),
        ])],
        steps=[
            ("Read the list", "Pulls the Tier 1 and Tier 2 companies from Airtable, each with its domain, industry and fit score."),
            ("Search", "For each company it searches Tavily and Jina for recent news: funding rounds, executive hires, launches, expansion."),
            ("Dedupe", "New results are compared against the signals already stored. Only new information moves on, so the same story never gets scored twice."),
            ("Score", "A separate sub-workflow scores each signal on urgency and fit. Funding raised this week beats a blog post from three months ago."),
            ("Push", "Anything above the threshold goes to GoHighLevel with the company, the signal type, the evidence, the urgency and a suggested next step."),
        ],
        outcome=[
            "The team starts every week with a short list of companies that just did something worth a call, with the evidence attached. Nobody reads the news by hand any more.",
        ],
        outcome_facts=[("Weekly", "runs on its own"), ("200+", "companies tracked"), ("0", "manual review")],
        notes=[
            "The search APIs are the budget line, so the dedupe step matters more than it looks. It keeps the weekly run from re-searching and re-scoring the same story. Scoring lives in its own sub-workflow so the rules can change without touching the collector.",
        ],
        also=("buyer-intent-pipeline", "This was the first version. It grew into the buyer intent research pipeline."),
        stack=["n8n", "Airtable", "Tavily search", "Jina search", "GoHighLevel"],
    ),
    dict(
        slug="crm-pipeline",
        title="CRM lead enrichment pipeline",
        cat="intelligence",
        status="client",
        one="Takes a scored lead from the monitor, has Claude write a two sentence problem statement for the company, builds the full CRM record and pushes it to GoHighLevel. About three seconds a lead.",
        lede="A sub-workflow any collector can call. It maps the incoming lead to the CRM's shape, asks Claude for a short executive problem statement, assembles the record and fires it at GoHighLevel. Reps open the CRM and the research is already done.",
        index_facts=[("~3 s", "per lead"), ("0", "manual entry")],
        facts=[("Trigger", "called by the monitor"), ("Time per lead", "about 3 s"), ("Manual entry", "none"), ("Output", "contact and opportunity in GoHighLevel")],
        why=[
            "Reps spend hours researching a company before a call and then write inconsistent notes. Everyone captures something different and leadership can't see a clean pipeline.",
        ],
        canvases=[dict(title="Per lead", nodes=[
            ("trigger", "Upstream call", "from the monitor"),
            ("transform", "Map fields", "to the CRM schema"),
            ("ai", "Claude", "problem statement"),
            ("transform", "Build payload", "full record"),
            ("send", "GoHighLevel", "webhook"),
        ])],
        steps=[
            ("Receive", "The intelligence monitor calls this workflow after a company is scored, with the full lead package."),
            ("Map", "A code node reshapes the data into GoHighLevel's format: contact fields, company fields, custom attributes."),
            ("Write the problem", "Claude gets the company context and the signal and writes a two or three sentence problem statement. Specific, no filler."),
            ("Assemble", "The record is built up: company, decision maker, the problem, urgency score, the evidence and a suggested next step."),
            ("Push", "The payload goes to GoHighLevel by webhook. Contact and opportunity are created or updated."),
        ],
        outcome=[
            "Reps open a lead and the research is there in plain words. Every record has the same fields, so the pipeline view finally means something.",
        ],
        outcome_facts=[("~3 s", "per lead"), ("100%", "of leads qualified the same way"), ("0", "manual data entry")],
        notes=[
            "Keeping this as its own sub-workflow means any collector can feed it, not just the monitor. If the CRM changes, only this one workflow changes.",
        ],
        also=("buyer-intent-pipeline", "This pattern is now part of the buyer intent research pipeline."),
        stack=["n8n", "Claude API", "GoHighLevel", "Webhooks", "JavaScript code nodes"],
    ),
    dict(
        slug="google-maps-leads",
        title="Google Maps lead discovery",
        cat="outreach",
        status="built",
        one="Searches Google Maps for a business type in a city, scrapes each website for contact details, has Claude pull out what the business does and writes a clean lead list to Google Sheets.",
        lede="Give it a category and a city, like \"digital agency in Austin\", and about twenty minutes later there's a sheet of several hundred businesses with emails, a one line description and a lead score.",
        index_facts=[("500+", "leads a run"), ("~80%", "email find rate")],
        facts=[("Input", "a category and a city"), ("Leads per run", "500+"), ("Run time", "about 20 minutes"), ("Email found", "around 80% of businesses")],
        why=[
            "Building a local lead list by hand means searching, clicking through sites and copying emails into a sheet. Most people give up after 20.",
        ],
        canvases=[dict(title="Pipeline", nodes=[
            ("fetch", "Google Places", "via Apify"),
            ("transform", "Filter", "no website, dupes by domain"),
            ("fetch", "Scrape site", "home and contact pages"),
            ("ai", "Claude", "what they do, likely pains"),
            ("store", "Google Sheets", "lead list"),
        ])],
        steps=[
            ("Search", "Apify's Google Places actor returns businesses for the category and location, with names, addresses, phones, websites and ratings."),
            ("Filter", "Businesses with no website are dropped, excluded names are removed and the rest are deduplicated by domain."),
            ("Scrape", "A Python node reads each homepage and contact page looking for email addresses, team names and a description."),
            ("Extract", "Claude reads the scraped text and writes down the business type, likely pain points and a contact name where there is one."),
            ("Save", "Each business goes into the sheet with its email, website, description, signal and score."),
        ],
        outcome=[
            "A run brings back 500 or more businesses in about twenty minutes, roughly 80% of them with an email found.",
        ],
        outcome_facts=[("500+", "leads a run"), ("~20 min", "full run"), ("~80%", "with an email")],
        notes=[
            "This is a working build that proves the pattern. I haven't run it for a client yet. Contact pages are inconsistent, so the scraper checks the homepage and the contact page and gives up quickly on anything else rather than crawling the whole site.",
        ],
        stack=["n8n", "Apify (Google Places)", "Python", "Claude API", "Google Sheets"],
    ),
    dict(
        slug="rag-assistant",
        title="Internal knowledge assistant",
        cat="ai",
        status="client",
        one="Staff ask a plain question about company documents, policies and contracts and get an answer with the source cited. Runs on the company's own servers.",
        lede="A retrieval assistant over the company's own documents. Files are chunked and embedded into Weaviate, a question pulls the closest passages, and Claude answers from those passages only, naming the document and section each fact came from.",
        index_facts=[("~2 s", "per answer"), ("40%", "fewer tickets, reported")],
        facts=[("Answer time", "about 2 s"), ("Data", "stays on internal servers"), ("Interface", "chat and Slack"), ("Reindex", "automatic on change")],
        why=[
            "Companies have hundreds of internal documents and people still email HR or spend twenty minutes digging through PDFs. New staff can't find anything, so onboarding drags.",
        ],
        canvases=[
            dict(title="Ingest", nodes=[
                ("fetch", "Documents", "PDF, Word, text"),
                ("transform", "Chunk + embed", "passages to vectors"),
                ("store", "Weaviate", "semantic index"),
            ]),
            dict(title="Answer", nodes=[
                ("trigger", "Question", "chat or Slack"),
                ("fetch", "Retrieve", "closest passages"),
                ("ai", "Claude", "answer with citations"),
            ]),
        ],
        steps=[
            ("Ingest", "PDFs, Word files and text are split into passages, embedded and stored in Weaviate."),
            ("Stay current", "When a document changes or a new one is added, the pipeline reindexes it. No manual upkeep."),
            ("Ask", "Someone asks a plain question in the chat interface or the Slack bot."),
            ("Retrieve", "The question is embedded and matched against the stored passages. The closest ones are pulled."),
            ("Answer", "Claude gets the question and those passages and writes a short answer grounded in them only. If nothing relevant was found it says so."),
            ("Cite", "Every answer names the document and section it came from, so people can check it."),
        ],
        outcome=[
            "The client reported about 40% fewer internal support tickets after rollout. Answers come back in about two seconds and every one points at its source.",
        ],
        outcome_facts=[("40%", "fewer tickets, client reported"), ("~2 s", "per answer"), ("100%", "answered from internal data")],
        notes=[
            "The \"I couldn't find that\" path is what makes people trust it. An assistant that guesses when the documents don't say gets ignored within a week. Everything runs on the company's own infrastructure, so no document leaves the building.",
        ],
        stack=["Python (FastAPI)", "Weaviate", "LangChain", "Claude API", "Docker", "AWS EC2"],
    ),
    dict(
        slug="recruitment-engine",
        title="Recruitment enrichment engine",
        cat="intelligence",
        status="client",
        one="Scrapes candidate profiles for a role, enriches them with public data, scores fit against the job with AI and pushes only the qualified ones into Airtable with a summary for the recruiter.",
        lede="Set the role, skills, location and experience once. The pipeline finds matching profiles, adds whatever public signal exists, scores each one against the job and hands the recruiter the top 40% with the reasoning.",
        index_facts=[("500+", "candidates a day"), ("40%", "reach a human")],
        facts=[("Candidates a day", "500+"), ("Reviewed by a person", "the top 40%"), ("Screening time", "down about 90%, client reported"), ("Platform", "Make.com")],
        why=[
            "Recruiters spend most of the day on search, copy paste and first pass screening. Almost none of that needs judgment. It's repetitive data work.",
        ],
        canvases=[dict(title="Per opening", nodes=[
            ("trigger", "Job criteria", "role, skills, location"),
            ("fetch", "Apify", "LinkedIn, GitHub, job boards"),
            ("fetch", "Enrich", "public signals"),
            ("ai", "Score", "fit against the job"),
            ("store", "Airtable", "qualified only"),
            ("send", "Notify", "Slack or email"),
        ])],
        steps=[
            ("Define", "Role title, required skills, location and experience level, set once per opening."),
            ("Scrape", "Apify searches LinkedIn, GitHub and job boards for matching candidates and returns structured profiles."),
            ("Enrich", "GitHub activity, portfolio links, publications and any other public signal get added."),
            ("Score", "An AI model rates each profile against the job requirements and writes down its reasoning. The bottom 60% are dropped."),
            ("Store", "Candidates above the line go into Airtable with their score, key strengths and suggested interview questions."),
            ("Notify", "The recruiter gets a Slack message or email: how many found, how many qualified, the top three."),
        ],
        outcome=[
            "Recruiters only look at the top 40%, each with a score, strengths and questions to ask. The client reported screening time down about 90% and a 32% lift in candidates converting to interview.",
        ],
        outcome_facts=[("90%", "less screening time, reported"), ("32%", "conversion lift, reported"), ("500+", "candidates a day")],
        notes=[
            "This one runs on Make.com and OpenAI rather than n8n and Claude because that's what the client already had. The pattern is the same. Scraping profiles has terms of service limits, so volume is kept under what the sources tolerate.",
        ],
        stack=["Make.com", "Apify", "OpenAI API", "Airtable", "Slack"],
    ),
    dict(
        slug="client-onboarding",
        title="Zero touch client onboarding",
        cat="ops",
        status="client",
        one="A signed form kicks off the contract, the e-signature, the project folder, the Slack channel, the CRM deal and the welcome email. About 60 seconds, no hand offs.",
        lede="When a new client fills in the onboarding form, everything that used to take an afternoon happens on its own: the contract is generated and sent for signature, and once it's signed the folder, the Slack channel, the HubSpot deal and the welcome email follow.",
        index_facts=[("~60 s", "end to end"), ("~8 h", "saved per client")],
        facts=[("Trigger", "onboarding form"), ("End to end", "about 60 s after signing"), ("Saved per client", "about 8 hours"), ("Signature", "DocuSign")],
        why=[
            "Onboarding is the same steps every time: draft the contract, send it, chase the signature, make the folder, add people to Slack, update the CRM. Done by hand it takes hours and something always gets missed.",
        ],
        canvases=[dict(title="Pipeline", nodes=[
            ("trigger", "Form", "client details"),
            ("transform", "Contract", "from template"),
            ("send", "DocuSign", "waits for signature"),
            ("store", "Drive folder", "shared with client"),
            ("send", "Slack", "channel and invite"),
            ("store", "HubSpot", "deal created"),
            ("send", "Welcome email", "links and next steps"),
        ])],
        steps=[
            ("Form", "The client fills in name, company, scope and start date. Two minutes."),
            ("Contract", "The template is filled with the client's details and scope of work."),
            ("Signature", "DocuSign sends it to the client. The workflow waits on the signed event before doing anything else."),
            ("Folder", "A Google Drive project folder is created with the standard structure and shared with the client and the team."),
            ("Slack", "A client channel is created, the team is added and the client gets an invite."),
            ("CRM", "The client appears in HubSpot as a won deal with the fields filled."),
            ("Welcome", "The client gets one email with the contract copy, the folder link, the Slack invite and what happens next."),
        ],
        outcome=[
            "About a minute after the signature lands, the client has everything and the team has nothing to set up. Every client goes through exactly the same steps.",
        ],
        outcome_facts=[("~60 s", "after signing"), ("~8 h", "saved per client"), ("0", "manual steps")],
        notes=[
            "Nothing downstream fires until DocuSign reports the signature, so an unsigned contract never creates a channel or a deal. That one gate is what makes the rest safe to automate.",
        ],
        stack=["n8n", "Google Forms", "DocuSign", "Google Drive", "Slack", "HubSpot", "Gmail"],
    ),
    dict(
        slug="investor-reports",
        title="Investor report automation",
        cat="ops",
        status="built",
        one="On the first of the month it pulls portfolio numbers from Sheets, has Claude write the month's narrative, builds each investor's report with their own allocation and sends it.",
        lede="A monthly job for a fund that reports to its LPs. It reads the portfolio sheet and each investor's allocation, drafts the month's narrative, assembles a personal report per investor and sends it from Gmail, logging every send.",
        index_facts=[("1st", "of every month"), ("~20 h", "saved a month")],
        facts=[("Trigger", "1st of the month"), ("Saved", "about 20 hours a month"), ("Source", "Google Sheets"), ("Send", "Gmail, one per investor")],
        why=[
            "Monthly LP updates take 10 to 20 hours by hand: pulling numbers from several sheets, formatting, personalising each one by allocation and sending them one at a time. Tedious, and easy to get a number wrong.",
        ],
        canvases=[dict(title="Monthly run", nodes=[
            ("trigger", "1st of month", "schedule"),
            ("fetch", "Portfolio sheet", "performance, events"),
            ("fetch", "Allocations", "per investor"),
            ("ai", "Claude", "month's narrative"),
            ("transform", "Assemble", "one report each"),
            ("send", "Gmail", "personal email"),
            ("store", "Log", "who got what"),
        ])],
        steps=[
            ("Trigger", "Runs on the first of the month. Nobody has to remember."),
            ("Portfolio", "Reads performance, company updates, valuations and notable events from the master sheet."),
            ("Allocations", "Reads each investor's ownership and holdings from a separate tab."),
            ("Narrative", "Claude turns the numbers and events into a short plain summary: what happened, what it means, what's next."),
            ("Assemble", "Each investor gets a report with their own allocation and figures plus the narrative."),
            ("Send", "Emails go out from Gmail with a personal greeting and subject."),
            ("Log", "Every send is recorded: who, when, which version."),
        ],
        outcome=[
            "The report goes out on the first, every month, with each investor's own numbers and no copy paste in between.",
        ],
        outcome_facts=[("~20 h", "saved a month"), ("1st", "delivered every month"), ("0", "copy paste")],
        notes=[
            "Built to prove the pattern, not running for a fund yet. For a real fund I'd put a review step in front of the send so a person reads the narrative before investors do. It's one node.",
        ],
        stack=["n8n", "Google Sheets", "Claude API", "Gmail"],
    ),
    dict(
        slug="event-followup",
        title="Event follow up engine",
        cat="outreach",
        status="built",
        one="After an event, every attendee gets a follow up within 24 hours that refers to the sessions they actually attended. The most engaged ones get flagged for a personal call.",
        lede="Attendee data comes in from the event platform, each person is grouped by what they attended, Claude writes a follow up that refers to it, and the batch goes out within a day while people still remember the event.",
        index_facts=[("24 h", "follow up window"), ("300+", "attendees an event")],
        facts=[("Trigger", "event export or webhook"), ("Window", "within 24 hours"), ("Attendees", "300+ per event"), ("Spacing", "30 s between sends")],
        why=[
            "Events produce warm leads and then the follow up is slow, generic or doesn't happen. Writing 300 personal emails by hand isn't going to happen, so teams send a blast or nothing.",
        ],
        canvases=[dict(title="Per event", nodes=[
            ("trigger", "Attendee data", "export or webhook"),
            ("transform", "Segment", "by session"),
            ("ai", "Claude", "personal follow up"),
            ("send", "Gmail", "within 24 h"),
            ("store", "Log", "CRM or sheet"),
            ("transform", "Flag", "hot leads"),
        ])],
        steps=[
            ("Import", "Attendee data arrives from the platform's export or a webhook: name, email, sessions, notes."),
            ("Segment", "People are grouped by the sessions they attended and the topics they engaged with."),
            ("Write", "Claude writes each follow up from the person's sessions and notes, so it refers to what they actually saw."),
            ("Send", "The batch goes out within 24 hours with 30 seconds between sends."),
            ("Log", "Each contact is recorded with engagement level, sessions and the follow up sent, ready for sales."),
            ("Flag", "The people who engaged most are flagged for a personal follow up by the team."),
        ],
        outcome=[
            "Everyone hears back within a day with something that refers to their event, and the team gets a short list of who to call personally.",
        ],
        outcome_facts=[("24 h", "follow up window"), ("300+", "attendees handled"), ("0", "attendees missed")],
        notes=[
            "Built to prove the pattern. The segmenting is only as good as the attendance data the event platform exports, so the first thing to check on a new client is what their platform actually records.",
        ],
        stack=["n8n", "Claude API", "Gmail", "Airtable", "Webhooks"],
    ),
]

NODE_TYPE_LABEL = {
    "trigger": "Trigger",
    "fetch": "Fetch",
    "transform": "Transform",
    "ai": "AI",
    "store": "Store",
    "send": "Send",
}


def e(s):
    return escape(s, quote=True)


def head(title, description, path, extra=""):
    url = SITE + path
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{url}">
<meta name="theme-color" content="#F4F5F7" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0E1116" media="(prefers-color-scheme: dark)">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600;12..96,700&family=IBM+Plex+Mono:wght@400;500&family=Instrument+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap">
<link rel="stylesheet" href="assets/site.css">
<script>try{{var t=localStorage.getItem('theme');if(t)document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}</script>
{extra}</head>
<body>
"""


def header(index=False):
    home = "index.html"
    return f"""<header class="top">
  <div class="wrap top-row">
    <a class="brand" href="{home}"><span class="mark" aria-hidden="true"></span>Jonathan Bayo</a>
    <nav class="top-nav" aria-label="Site">
      <a href="{home}#work">Work</a>
      <a href="{home}#about">About</a>
      <a href="{home}#contact">Contact</a>
      <button class="theme" type="button" id="theme-toggle" aria-label="Switch colour theme">Theme</button>
      <a class="btn" href="{CALENDLY}">Book a call</a>
    </nav>
  </div>
</header>
"""


def footer():
    return f"""<footer class="foot">
  <div class="wrap foot-row">
    <span>Jonathan Bayo</span>
    <span><a href="mailto:{EMAIL}">{EMAIL}</a></span>
    <span><a href="{GITHUB}">github.com/zilyn</a></span>
  </div>
</footer>
<script src="assets/site.js"></script>
</body>
</html>
"""


def canvas(c, pulse=False):
    parts = []
    for i, (typ, name, sub) in enumerate(c["nodes"]):
        if i:
            parts.append('<span class="edge" aria-hidden="true"></span>')
        parts.append(
            f'<div class="node node-{typ}"><div class="node-type">{NODE_TYPE_LABEL[typ]}</div>'
            f'<div class="node-name">{e(name)}</div><div class="node-sub">{e(sub)}</div></div>'
        )
    cls = "canvas pulse" if pulse else "canvas"
    return (
        f'<figure class="{cls}"><figcaption class="canvas-title">{e(c["title"])}</figcaption>'
        f'<div class="track">{"".join(parts)}</div></figure>'
    )


def mini(c):
    parts = []
    for i, (typ, name, sub) in enumerate(c["nodes"]):
        if i:
            parts.append('<span class="mini-edge" aria-hidden="true"></span>')
        parts.append(f'<span class="mini-node node-{typ}">{e(name)}</span>')
    return f'<div class="mini" aria-label="Pipeline: {e(", ".join(n for _, n, _ in c["nodes"]))}">{"".join(parts)}</div>'


def status_pill(p):
    label = STATUS[p["status"]][0]
    return f'<span class="status status-{p["status"]}">{label}</span>'


def words(p):
    text = " ".join([p["lede"]] + p["why"] + [t + " " + d for t, d in p["steps"]] + p["outcome"] + p["notes"])
    return len(text.split())


def read_time(p):
    return max(1, round(words(p) / 200))


def fcard(p):
    v, l = p["index_facts"][0]
    stack = " · ".join(e(s) for s in p["stack"][:5])
    quote = ""
    if p.get("quotes"):
        n, r, t = p["quotes"][0]
        quote = f'<blockquote class="fcard-quote"><p>{e(t)}</p><footer>{e(n)}, {e(r)}</footer></blockquote>'
    return f"""<article class="fcard" data-cat="{p["cat"]}" data-href="{p["slug"]}.html">
  <div class="entry-eyebrow"><span class="cat">{CATS[p["cat"]]}</span>{status_pill(p)}</div>
  <h3 class="fcard-title"><a href="{p["slug"]}.html">{e(p["title"])}</a></h3>
  <p class="fcard-one">{e(p["one"])}</p>
  {mini(p["canvases"][0])}
  <div class="fcard-foot">
    <div class="fact fact-big"><span class="fact-val">{e(v)}</span><span class="fact-lab">{e(l)}</span></div>
    <p class="entry-stack">{stack}</p>
  </div>
  {quote}
  <span class="entry-more">Read the case study</span>
</article>"""


def entry(p):
    facts = "".join(
        f'<div class="fact"><span class="fact-val">{e(v)}</span><span class="fact-lab">{e(l)}</span></div>'
        for v, l in p["index_facts"][:2]
    )
    stack = " · ".join(e(s) for s in p["stack"][:5])
    return f"""<article class="entry" data-cat="{p["cat"]}" data-href="{p["slug"]}.html">
  <div class="entry-main">
    <div class="entry-eyebrow"><span class="cat">{CATS[p["cat"]]}</span>{status_pill(p)}</div>
    <h3 class="entry-title"><a href="{p["slug"]}.html">{e(p["title"])}</a></h3>
    <p class="entry-one">{e(p["one"])}</p>
    <p class="entry-stack">{stack}</p>
  </div>
  <div class="entry-side">{facts}<span class="entry-more">Read the case study</span></div>
</article>"""


def build_index():
    legend = " ".join(
        f'<span class="legend-item"><span class="status status-{k}">{v[0]}</span> {e(v[1])}</span>'
        for k, v in STATUS.items()
    )
    filters = '<button type="button" class="filter is-active" data-filter="all" aria-pressed="true">All</button>' + "".join(
        f'<button type="button" class="filter" data-filter="{k}" aria-pressed="false">{v}</button>' for k, v in CATS.items()
    )
    featured = [p for p in PROJECTS if p.get("featured")]
    rest = [p for p in PROJECTS if not p.get("featured")]
    fcards = "\n".join(fcard(p) for p in featured)
    entries = "\n".join(entry(p) for p in rest)
    n = len(PROJECTS)
    description = f"{n} automation systems built by Jonathan Bayo in n8n, Python and Claude: lead research, outreach, CRM plumbing, a multi-tenant product and reporting, with how each one runs and what came out of it."
    html = head("Jonathan Bayo, automation case studies", description, "", "") + header(index=True) + f"""
<main>
  <section class="hero wrap">
    <div class="hero-text">
      <p class="eyebrow">Case studies</p>
      <h1>I build automations that run on their own.</h1>
      <p class="hero-lede">I'm Jonathan Bayo. I build lead research, outreach, CRM and reporting systems in n8n, Python and Claude for founders and small teams. {n} of them are below, with how each one runs and what came out of it.</p>
      <div class="hero-actions"><a class="btn" href="#work">See the work</a><a class="btn btn-quiet" href="{CALENDLY}">Book a 15 minute call</a></div>
    </div>
    <dl class="hero-facts">
      <div><dt>Usual stack</dt><dd>n8n, Python, Claude, Supabase, Apify</dd></div>
      <div><dt>Typical build</dt><dd>one to two weeks</dd></div>
      <div><dt>Where things run</dt><dd>your own accounts and servers</dd></div>
      <div><dt>Right now</dt><dd>taking new builds</dd></div>
    </dl>
  </section>

  <section class="wrap work" id="work">
    <div class="work-head">
      <h2>Featured</h2>
      <p class="work-sub">The four systems that best show what I do.</p>
    </div>
    <div class="fgrid">
{fcards}
    </div>
  </section>

  <section class="wrap work work-all" id="all">
    <div class="work-head">
      <h2>All the work</h2>
      <div class="filters" role="group" aria-label="Filter by category">{filters}</div>
    </div>
    <p class="legend">{legend}</p>
    <div class="entries">
{entries}
    </div>
    <p class="empty" id="empty" hidden>Nothing else in this category. The featured ones above may have it.</p>
  </section>

  <section class="wrap about" id="about">
    <div class="about-grid">
      <div>
        <h2>About</h2>
        <p>I've spent the past year as the automation and back end engineer for a B2B sales intelligence company, building the research pipeline, the CRM tooling and the multi-tenant product you see above. Alongside that I take on builds for founders and small teams: outreach, lead research, onboarding, reporting.</p>
        <p>I work in n8n and Python, use Claude where a step needs judgment, and keep everything in your own accounts so nothing depends on me being around.</p>
      </div>
      <div>
        <h2>How I work</h2>
        <p>We start with what's taking too long. I map the steps, pick the smallest system that removes them and build it, with Claude where a step needs judgment.</p>
        <p>Everything logs its own runs, never sends the same thing twice and fails loudly instead of quietly. You get the workflows, the credentials in your accounts and a short doc on how it runs and what to do when it stops. Most builds take a week or two. If it's going to take longer I'll say so before we start.</p>
      </div>
    </div>
  </section>

  <section class="wrap cta" id="contact">
    <h2>Want something like this built?</h2>
    <p>Tell me what's taking too long. Most things can be built in a week or two.</p>
    <div class="cta-row">
      <a class="btn" href="{CALENDLY}">Book a 15 minute call</a>
      <a class="btn btn-quiet" href="mailto:{EMAIL}">Email me</a>
    </div>
  </section>
</main>
""" + footer()
    (ROOT / "index.html").write_text(html, encoding="utf-8")


def neighbour_card(label, p):
    if not p:
        return ""
    return f"""<a class="nb" href="{p["slug"]}.html"><span class="nb-label">{label}</span><span class="nb-title">{e(p["title"])}</span><span class="nb-one">{e(p["one"])}</span></a>"""


def build_project(p, prev_p, next_p):
    facts = "".join(f"<div><dt>{e(l)}</dt><dd>{e(v)}</dd></div>" for l, v in p["facts"])
    why = "".join(f"<p>{e(t)}</p>" for t in p["why"])
    steps = "".join(f"<li><h3>{e(t)}</h3><p>{e(d)}</p></li>" for t, d in p["steps"])
    outcome = "".join(f"<p>{e(t)}</p>" for t in p["outcome"])
    ofacts = "".join(
        f'<div class="fact"><span class="fact-val">{e(v)}</span><span class="fact-lab">{e(l)}</span></div>'
        for v, l in p["outcome_facts"]
    )
    quotes = ""
    if p.get("quotes"):
        quotes = '<div class="replies">' + "".join(
            f'<blockquote class="reply"><p>{e(t)}</p><footer>{e(n)}, {e(r)}</footer></blockquote>'
            for n, r, t in p["quotes"]
        ) + "</div>"
    notes = "".join(f"<p>{e(t)}</p>" for t in p["notes"])
    if p.get("also"):
        slug, text = p["also"]
        notes += f'<p><a href="{slug}.html">{e(text)}</a></p>'
    stack = "".join(f"<li>{e(s)}</li>" for s in p["stack"])
    title = f'{p["title"]}, Jonathan Bayo'
    canvases = "".join(canvas(c, pulse=(i == 0)) for i, c in enumerate(p["canvases"]))
    html = head(title, p["one"], f'{p["slug"]}.html') + header() + f"""
<main class="article wrap">
  <a class="back" href="index.html#work">All case studies</a>
  <div class="entry-eyebrow"><span class="cat">{CATS[p["cat"]]}</span>{status_pill(p)}<span class="cat cat-time">{read_time(p)} min read</span></div>
  <h1>{e(p["title"])}</h1>
  <p class="lede">{e(p["lede"])}</p>

  <section class="results" aria-label="Results">
    <div class="fact-row">{ofacts}</div>
  </section>

  <dl class="facts">{facts}</dl>

  <nav class="subnav" aria-label="On this page">
    <a href="#why">Why</a><a href="#how">How it runs</a><a href="#outcome">Outcome</a><a href="#notes">Notes</a><a href="#stack">Stack</a>
  </nav>

  <section class="sec" id="why">
    <h2>Why it exists</h2>
    {why}
  </section>

  <section class="sec sec-wide" id="how">
    <h2>How it runs</h2>
    {canvases}
    <ol class="steps">{steps}</ol>
  </section>

  <section class="sec" id="outcome">
    <h2>What came out of it</h2>
    {outcome}
    {quotes}
  </section>

  <section class="sec" id="notes">
    <h2>Notes</h2>
    {notes}
  </section>

  <section class="sec" id="stack">
    <h2>Stack</h2>
    <ul class="stack">{stack}</ul>
  </section>

  <section class="cta cta-article" id="contact">
    <h2>Want something like this built?</h2>
    <p>Tell me what you're trying to automate. Most things can be built in a week or two.</p>
    <div class="cta-row">
      <a class="btn" href="{CALENDLY}">Book a 15 minute call</a>
      <a class="btn btn-quiet" href="mailto:{EMAIL}">Email me</a>
    </div>
  </section>

  <nav class="next-nav" aria-label="More case studies">
    {neighbour_card("Previous", prev_p)}
    {neighbour_card("Next", next_p)}
  </nav>
</main>
""" + footer()
    (ROOT / f'{p["slug"]}.html').write_text(html, encoding="utf-8")


def build_404():
    html = head("Page not found, Jonathan Bayo", "That page isn't here.", "404.html") + header() + """
<main class="article wrap">
  <p class="eyebrow">404</p>
  <h1>That page isn't here.</h1>
  <p class="lede">The case study may have moved. Everything I've published is on the front page.</p>
  <p><a class="btn" href="index.html">Back to the case studies</a></p>
</main>
""" + footer()
    (ROOT / "404.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    build_index()
    for i, p in enumerate(PROJECTS):
        build_project(p, PROJECTS[i - 1] if i else None, PROJECTS[i + 1] if i + 1 < len(PROJECTS) else None)
    build_404()
    print(f"built index, {len(PROJECTS)} case studies, 404")
