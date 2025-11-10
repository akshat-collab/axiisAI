#!/usr/bin/env python3
"""
AXIS AI - Advanced AI Assistant
Main Startup File with All Functions
"""

import os
import sys
import json
import threading
import subprocess
from time import sleep
from asyncio import run
from dotenv import dotenv_values
import signal

# Import Frontend Components
from Frontend.GUI import (
    GraphicalUserInterface,
    SetAssistantStatus,
    ShowTextToScreen,
    TempDirectoryPath,
    SetMicrophoneStatus,
    AnswerModifier,
    QueryModifier,
    GetMicrophoneStatus,
    GetAssistantStatus
)

# Import Backend Components
from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech

# ==================== CONFIGURATION ====================

class Config:
    """Configuration Manager"""
    def __init__(self):
        self.env_vars = dotenv_values(".env")
        self.username = self.env_vars.get("Username", "User")
        self.assistantname = self.env_vars.get("Assistantname", "Assistant")
        self.default_message = f'''{self.username} : Hello {self.assistantname}, How are you?
{self.assistantname} : Welcome {self.username}. I am doing well. How may i help you?'''
        self.functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]
        self.subprocesses = []
        
        # Paths
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.base_dir, "Data")
        self.chatlog_path = os.path.join(self.data_dir, "ChatLog.json")
        
    def validate(self):
        """Validate configuration and required files"""
        print("🔍 Validating configuration...")
        
        # Check .env file
        if not self.env_vars:
            print("⚠️  Warning: .env file not found or empty")
            return False
            
        # Check required directories
        if not os.path.exists(self.data_dir):
            print(f"📁 Creating Data directory: {self.data_dir}")
            os.makedirs(self.data_dir)
            
        # Check ChatLog.json
        if not os.path.exists(self.chatlog_path):
            print("📝 Creating ChatLog.json...")
            with open(self.chatlog_path, 'w', encoding='utf-8') as f:
                json.dump([], f)
        
        # Check API keys
        required_keys = ["GeminiAPIKey", "CohereAPIKey"]
        missing_keys = [key for key in required_keys if not self.env_vars.get(key)]
        if missing_keys:
            print(f"⚠️  Warning: Missing API keys: {', '.join(missing_keys)}")
            
        print("✅ Configuration validated successfully!")
        return True

# Global configuration instance
config = Config()

# ==================== INITIALIZATION FUNCTIONS ====================

def ShowDefaultChatIfNoChats():
    """Display default chat message if no chat history exists"""
    try:
        with open(config.chatlog_path, "r", encoding='utf-8') as file:
            content = file.read()
            if len(content) < 5:
                with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as f:
                    f.write("")
                with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as f:
                    f.write(config.default_message)
                print("📋 Default chat message loaded")
    except Exception as e:
        print(f"❌ Error in ShowDefaultChatIfNoChats: {e}")

def ReadChatLogJson():
    """Read chat log from JSON file"""
    try:
        with open(config.chatlog_path, 'r', encoding='utf-8') as file:
            chatlog_data = json.load(file)
        return chatlog_data
    except json.JSONDecodeError:
        print("⚠️  ChatLog.json is corrupted. Creating new one...")
        with open(config.chatlog_path, 'w', encoding='utf-8') as file:
            json.dump([], file)
        return []
    except Exception as e:
        print(f"❌ Error reading ChatLog: {e}")
        return []

def ChatLogIntegration():
    """Integrate chat log into GUI display"""
    try:
        json_data = ReadChatLogJson()
        formatted_chatlog = ""
        
        for entry in json_data:
            if entry.get("role") == "user":
                formatted_chatlog += f"User: {entry.get('content', '')}\n"
            elif entry.get("role") == "assistant":
                formatted_chatlog += f"Assistant: {entry.get('content', '')}\n"
        
        formatted_chatlog = formatted_chatlog.replace("User", config.username)
        formatted_chatlog = formatted_chatlog.replace("Assistant", config.assistantname)
        
        with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
            file.write(AnswerModifier(formatted_chatlog))
        
        print("💬 Chat log integrated")
    except Exception as e:
        print(f"❌ Error in ChatLogIntegration: {e}")

def ShowChatsOnGUI():
    """Display chat history on GUI"""
    try:
        with open(TempDirectoryPath('Database.data'), "r", encoding='utf-8') as file:
            data = file.read()
        
        if len(str(data)) > 0:
            lines = data.split('\n')
            result = '\n'.join(lines)
            
            with open(TempDirectoryPath('Responses.data'), "w", encoding='utf-8') as file:
                file.write(result)
        
        print("🖥️  Chat display updated")
    except Exception as e:
        print(f"❌ Error in ShowChatsOnGUI: {e}")

def InitialExecution():
    """Initialize the application"""
    print("\n" + "="*60)
    print("🚀 AXIS AI - Advanced AI Assistant")
    print("="*60 + "\n")
    
    # Validate configuration
    if not config.validate():
        print("⚠️  Configuration validation failed. Continuing with warnings...")
    
    print("\n🔧 Initializing components...")
    
    try:
        # Set initial microphone status
        SetMicrophoneStatus("False")
        print("🎤 Microphone: OFF")
        
        # Clear any existing screen text
        ShowTextToScreen("")
        
        # Setup default chat
        ShowDefaultChatIfNoChats()
        
        # Integrate chat log
        ChatLogIntegration()
        
        # Display chats on GUI
        ShowChatsOnGUI()
        
        print("✅ Initialization complete!")
        print("\n" + "="*60)
        print("💡 Click the microphone button to start speaking")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ Error during initialization: {e}")
        print("⚠️  Some features may not work properly")

# ==================== MAIN EXECUTION FUNCTIONS ====================

def MainExecution():
    """Main execution loop for processing user queries"""
    try:
        TaskExecution = False
        ImageExecution = False
        ImageGenerationQuery = ""
        
        # Listen for user input
        SetAssistantStatus("Listening...")
        Query = SpeechRecognition()
        
        if not Query or Query.strip() == "":
            return False
            
        ShowTextToScreen(f"{config.username} : {Query}")
        
        # Process query through AI decision model
        SetAssistantStatus("Thinking...")
        Decision = FirstLayerDMM(Query)
        
        print(f"\n💭 Decision: {Decision}\n")
        
        # Analyze decision types
        G = any([i for i in Decision if i.startswith("general")])
        R = any([i for i in Decision if i.startswith("realtime")])
        
        Merged_query = " and ".join(
            [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
        )
        
        print(f"🎯 Query: {Merged_query}\n")
        
        # Check for image generation
        for query in Decision:
            if "generate " in query:
                ImageGenerationQuery = str(query)
                ImageExecution = True
        
        # Check for automation tasks
        for query in Decision:
            if not TaskExecution:
                if any(query.startswith(func) for func in config.functions):
                    run(Automation(list(Decision)))
                    TaskExecution = True
        
        # Handle image generation
        if ImageExecution:
            try:
                image_data_path = os.path.join("Frontend", "Files", "ImageGeneration.data")
                with open(image_data_path, "w") as file:
                    file.write(f"{ImageGenerationQuery},True")
                
                image_gen_path = os.path.join(config.base_dir, 'Backend', 'ImageGenration.py')
                p1 = subprocess.Popen(['python3', image_gen_path],
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE,
                                     stdin=subprocess.PIPE, 
                                     shell=False)
                config.subprocesses.append(p1)
                print("🎨 Image generation started")
            except Exception as e:
                print(f"❌ Error starting ImageGeneration: {e}")
        
        # Handle realtime search
        if (G and R) or R:
            SetAssistantStatus("Searching...")
            Answer = RealtimeSearchEngine(QueryModifier(Merged_query))
            ShowTextToScreen(f"{config.assistantname} : {Answer}")
            SetAssistantStatus("Answering...")
            TextToSpeech(Answer)
            return True
        
        # Handle general queries
        else:
            for query in Decision:
                if "general" in query:
                    SetAssistantStatus("Thinking...")
                    QueryFinal = query.replace("general ", "")
                    Answer = ChatBot(QueryModifier(QueryFinal))
                    ShowTextToScreen(f"{config.assistantname} : {Answer}")
                    SetAssistantStatus("Answering...")
                    TextToSpeech(Answer)
                    return True
                    
                elif "realtime" in query:
                    SetAssistantStatus("Searching...")
                    QueryFinal = query.replace("realtime ", "")
                    Answer = RealtimeSearchEngine(QueryModifier(QueryFinal))
                    ShowTextToScreen(f"{config.assistantname} : {Answer}")
                    SetAssistantStatus("Answering...")
                    TextToSpeech(Answer)
                    return True
                    
                elif "exit" in query:
                    QueryFinal = "Okay, Bye!"
                    Answer = ChatBot(QueryModifier(QueryFinal))
                    ShowTextToScreen(f"{config.assistantname} : {Answer}")
                    SetAssistantStatus("Answering...")
                    TextToSpeech(Answer)
                    cleanup_and_exit()
                    
    except Exception as e:
        print(f"❌ Error in MainExecution: {e}")
        SetAssistantStatus("Error occurred")
        return False

# ==================== THREADING FUNCTIONS ====================

def FirstThread():
    """Backend thread - handles AI processing"""
    print("🧵 Backend thread started")
    while True:
        try:
            CurrentStatus = GetMicrophoneStatus()
            if CurrentStatus == "True":
                MainExecution()
            else:
                AIStatus = GetAssistantStatus()
                if "Available ..." not in AIStatus:
                    SetAssistantStatus("Available ...")
                sleep(0.1)
        except Exception as e:
            print(f"❌ Error in backend thread: {e}")
            sleep(1)

def SecondThread():
    """Frontend thread - runs the GUI"""
    print("🧵 Frontend thread started")
    try:
        GraphicalUserInterface()
    except Exception as e:
        print(f"❌ Error in GUI thread: {e}")
        cleanup_and_exit()

# ==================== CLEANUP FUNCTIONS ====================

def cleanup_and_exit(signum=None, frame=None):
    """Clean up resources and exit"""
    print("\n\n🛑 Shutting down AXIS AI...")
    
    # Terminate subprocesses
    for process in config.subprocesses:
        try:
            process.terminate()
            process.wait(timeout=2)
        except:
            process.kill()
    
    print("✅ Cleanup complete. Goodbye!")
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, cleanup_and_exit)
signal.signal(signal.SIGTERM, cleanup_and_exit)

# ==================== MAIN ENTRY POINT ====================

if __name__ == "__main__":
    try:
        # Initialize the application
        InitialExecution()
        
        # Start backend thread
        backend_thread = threading.Thread(target=FirstThread, daemon=True)
        backend_thread.start()
        
        # Start frontend thread (blocks until GUI closes)
        SecondThread()
        
    except KeyboardInterrupt:
        cleanup_and_exit()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        cleanup_and_exit()

