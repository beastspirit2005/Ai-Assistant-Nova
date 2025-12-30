Nova — A Secure, Emotion-Aware Desktop AI Assistant

Nova is a desktop AI assistant built in Python that combines system automation, conversational AI, emotion awareness, voice interaction, and security into a single, cleanly-architected application.

Unlike basic chatbots, Nova is designed as a real desktop assistant — with authentication, system control, persistent memory, and ethical emotional intelligence.

Key Features
1.Security First

Face authentication (OpenCV, offline)

   PIN authentication fallback
   Authentication required before app access
   Secure reset flows
   No cloud-stored biometric data

2.Conversational AI (OpenAI-powered)

   Natural language conversations
   General knowledge & explanations
   Calculations and reasoning
   Friendly, calm, supportive tone

3.Emotion-Aware Responses

   Detects emotional tone from user input
   Tracks emotional patterns over time (not raw messages)
   Adjusts tone, empathy, and verbosity
   Ethical by design (no diagnosis, no dependency)

4.Voice Interaction

   Voice input (mic toggle)
   Speech-to-text conversion
   Optional text-to-speech output
   User-controlled speaker toggle

5.System & App Control

   Open and close applications
   Volume up/down, mute/unmute
   Lock screen
   Sleep, restart, shutdown (with confirmation)
   Safe execution boundaries

6.Persistent Memory

   Remembers profile information (e.g., name)
   Stores notes across sessions
   SQLite-based local storage
   Emotion memory stored separately and safely

7.Desktop UI (PyQt)

   Responsive chat interface
   Dark & light themes
   Settings panel
   Non-blocking UI using worker threads

8.nova/
├── main.py                 
├── ui                    
│   ├── main_window.py
│   └── settings_window.py
├── workers/                
│   └── ai_worker.py
├── core                  
│   ├── intent.py
│   ├── memory_manager.py
│   ├── emotion.py
│   ├── emotion_memory.py
│   └── settings_manager.py
├── system                
│   ├── app_control.py
│   └── system_control.py
├── voice                
│   ├── speech_input.py
│   └── speech_output.py
├── security               
│   ├── auth_manager.py
│   ├── face_auth.py
│   └── pin_auth.py
└── data                 
