# Automated next step processing
This folder illustrates how I will implement the next step processing for the three intents that we have high accuracy- `voice_wants_email_follow_up`, `voice_wants_whatsapp_sms_follow_up`, `voice_wrong_number`.

Key implementation details lie in using email or whatsapp client to do a follow up. I have also picked these two intents as they are asynchronous, so more quickly deployable (as opposed to live calls, where we need to get the timing right).

Lastly, this implementation is standalone and not technically difficult.  I have also intentionally picked the low hanging fruit as there is a lot of uncertainty as to what causes the errors that we have investigated in Part 2.

## Folder structure
project/
│
├── clients/                 # Communication client implementations
│   ├── __init__.py
│   ├── whatsapp_client.py   # Real and mock WhatsApp clients
│   └── email_client.py      # Real and mock Email clients
│
├── interfaces/              # Abstract interfaces for dependency injection
│   ├── __init__.py
│   └── client_interfaces.py
│
├── models/                  # Data models
│   ├── __init__.py
│   └── message_models.py    # WhatsApp message model
│
├── automation_logic.py      # Core processor class and helper functions
├── automation_runner.py     #  Orchestration: process threads and trigger actions
├── factory.py               # Factory functions to create real or mock clients
└── main.py                  # Entry point
