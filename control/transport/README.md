# ChatGPT Request Transport

ChatGPT creates one JSON file at `control/transport/inbox/<request_id>.json` on the controlled transport branch through the GitHub repository API. The file must validate against `../schemas/episode_request.schema.json`; a resume request sets `resume_run_id` to the prior `WAITING_FOR_FLOW_ASSET` run.

The installed Windows Local Watcher performs `git pull --ff-only`, atomically claims each inbox file, invokes the Bridge, and writes `control/transport/results/<request_id>.json`. That result contains state, log, manifest paths and the terminal/current state for ChatGPT to read via GitHub. The watcher never accepts shell commands or runner paths from a request.

One-time installation uses `control/windows/install_local_watcher.ps1`. After installation, no person runs Python for an individual request: Task Scheduler starts the watcher at logon and it polls continuously. The Git credential used by that Windows account must have push permission to the transport branch for result publication.
