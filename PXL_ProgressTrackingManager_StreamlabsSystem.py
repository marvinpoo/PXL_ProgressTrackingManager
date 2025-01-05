# ---------------------------------------
# Import Libraries
# ---------------------------------------
import os
import json
import codecs

# ---------------------------------------
# Script Information
# ---------------------------------------
ScriptName = "PXL_PTM: Progress Tracking Manager"
Website = "http://localhost:8000"
Description = "This script tracks your progress and is capable of displaying it in a OBS Browser Source."
Creator = "dotPixelmonarch"
Version = "v0.1.0-beta"

# ---------------------------------------
# Global Variables
# ---------------------------------------
BASE_DIR = os.path.dirname(__file__)
LANGUAGES_DIR = os.path.join(BASE_DIR, "Languages")
TRACKERS_DIR = os.path.join(BASE_DIR, "Trackers")
SETTINGS_FILE = os.path.join(BASE_DIR, "Settings", "settings.json")
HTML_TEMPLATE = os.path.join(BASE_DIR, "tracker_template.html")
LOG_FILE = os.path.join(BASE_DIR, "PXL_ProgressTrackingManager_Debug.log")

settings = {}
language_messages = {}

# ---------------------------------------
# Custom Logging Function
# ---------------------------------------
def log(message):
    with codecs.open(LOG_FILE, "a", "utf-8") as log_file:
        log_file.write(message + "\n")
    print(message)  # Ensures output to the chatbot console as well

# ---------------------------------------
# Reload Settings
# ---------------------------------------
def ReloadSettings(jsondata):
    global settings
    settings = json.loads(jsondata)
    load_language(settings["language"])
    with codecs.open(SETTINGS_FILE, "w", "utf-8-sig") as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)
    log("[RELOAD] Settings reloaded and saved: {}".format(settings))

# ---------------------------------------
# Initialize Script
# ---------------------------------------
def Init():
    global settings

    # Ensure folders exist
    if not os.path.exists(TRACKERS_DIR):
        os.makedirs(TRACKERS_DIR)
    settings_dir = os.path.join(BASE_DIR, "Settings")
    if not os.path.exists(settings_dir):
        os.makedirs(settings_dir)

    # Load or create default settings
    if not os.path.isfile(SETTINGS_FILE):
        default_settings = {
            "language": "en",
            "allowed_roles_everyone": False,
            "allowed_roles_regular": False,
            "allowed_roles_subscriber": False,
            "allowed_roles_vip": False,
            "allowed_roles_moderator": True,
            "broadcaster_group": ["Broadcaster"],
            "command_name": "tracker",
            "command_alias": ""
        }
        with codecs.open(SETTINGS_FILE, "w", "utf-8-sig") as f:
            json.dump(default_settings, f, indent=4, ensure_ascii=False)
    with codecs.open(SETTINGS_FILE, "r", "utf-8-sig") as f:
        settings = json.load(f)

    # Load the selected language
    load_language(settings["language"])
    log("[INIT] Script initialized with settings: {}".format(settings))

# ---------------------------------------
# Load Language File
# ---------------------------------------
def load_language(language_code):
    global language_messages
    lang_file = os.path.join(LANGUAGES_DIR, "lang_{}.json".format(language_code))
    if not os.path.exists(lang_file):
        log("[LANGUAGE] File '{}' not found. Defaulting to English.".format(lang_file))
        lang_file = os.path.join(LANGUAGES_DIR, "lang_en.json")
    with codecs.open(lang_file, "r", "utf-8-sig") as f:
        language_messages = json.load(f)
    log("[LANGUAGE] Loaded language: {}".format(language_code))

# ---------------------------------------
# Generate Tracker HTML with Progress Bar
# ---------------------------------------
def generate_tracker_html(tracker_name, current_progress, max_value):
    # Path to output HTML file
    html_file = os.path.join(TRACKERS_DIR, "{}.html".format(tracker_name))
    if not os.path.exists(HTML_TEMPLATE):
        log("[HTML] Template not found.")
        return

    # Calculate progress percentage
    progress = min((current_progress / float(max_value)) * 100, 100) if max_value > 0 else 0

    # Read the template and insert values
    with codecs.open(HTML_TEMPLATE, "r", "utf-8-sig") as template:
        html_content = template.read()
    html_content = html_content.replace("{tracker_name}", tracker_name)
    html_content = html_content.replace("{tracker_value}", str(current_progress))
    html_content = html_content.replace("{progress_percent}", "%.2f" % float(progress))

    # Write to the output file
    with codecs.open(html_file, "w", "utf-8-sig") as output:
        output.write(html_content)

    # Log progress
    log("[HTML] Generated HTML for tracker: %s (value: %d, progress: %.2f%%)" % (tracker_name, current_progress, progress))
    return html_file

# ---------------------------------------
# Execute Chat Commands
# ---------------------------------------
def Execute(data):
    global settings

    if data.IsChatMessage():
        # Combine the trigger and parameters into a single command
        raw_input = data.Message.strip()
        log("[COMMAND] Received raw input: '{}'".format(raw_input))

        # Ensure the command starts with the trigger
        command_name = "!" + settings.get("command_name", "tracker")
        command_alias = "!" + settings.get("command_alias", "")

        log("[TEST] Checking: command_name={}, command_alias={}".format(command_name, command_alias))

        split_input = raw_input.split()
        if not split_input:
            log("[HANDLER] Killing Execution. Wrong command used.")
            return
        first_word = split_input[0]
        if first_word not in [command_name, command_alias]:
            log("[HANDLER] Killing Execution. Wrong command used.")
            return

        # Remove the trigger and split the input into arguments
        if raw_input.startswith(command_name):
            args = raw_input[len(command_name):].strip().split()
        else:
            args = raw_input[len(command_alias):].strip().split()
        log("[COMMAND] Parsed arguments: {}".format(args))

        # Ensure at least two arguments are provided (tracker name, command)
        if len(args) < 2:
            log("[COMMAND] Invalid arguments. Less than 2 provided.")
            Parent.SendStreamMessage(
                "Usage: {} [tracker_name] [command] [value]. Example: {} test new 100".format(command_name, command_name)
            )
            return

        # Check if user has the required role
        user = data.User
        allowed_roles = []
        if settings.get("allowed_roles_everyone"):
            allowed_roles.append("Everyone")
        if settings.get("allowed_roles_regular"):
            allowed_roles.append("Regular")
        if settings.get("allowed_roles_subscriber"):
            allowed_roles.append("Subscriber")
        if settings.get("allowed_roles_vip"):
            allowed_roles.append("VIP")
        if settings.get("allowed_roles_moderator"):
            allowed_roles.append("Moderator")
        broadcaster_group = settings.get("broadcaster_group", [])
        final_allowed_roles = set(allowed_roles + broadcaster_group)  # Merge and remove duplicates

        # Check if user has any of the allowed roles
        has_permission = any(Parent.HasPermission(user, role, "") for role in final_allowed_roles)
        if not has_permission:
            log("[COMMAND] User '{}' does not have the required role.".format(user))
            Parent.SendStreamMessage(language_messages["no_permission"])  # Use the new language message
            return  # Explicitly return to stop further processing

        tracker_name = args[0].lower()  # First argument is the tracker name
        command = args[1].lower()      # Second argument is the command
        tracker_path = os.path.join(TRACKERS_DIR, "{}.json".format(tracker_name))

        # Initialize operation and value
        operation = None
        value = None

        # Handle new and similar commands that require a third argument
        if command == "new":
            if len(args) > 2:  # Check if a third argument exists
                try:
                    value = int(args[2])  # Parse the value as an integer
                except ValueError:
                    log("[COMMAND] Failed to parse value as integer: '{}'".format(args[2]))
                    Parent.SendStreamMessage(language_messages["invalid_value"])
                    return
            else:
                log("[COMMAND] Missing value for 'new'.")
                Parent.SendStreamMessage(language_messages["invalid_value"])
                return

        # Handle commands with combined operation and value (+amount, -amount, =amount)
        elif command.startswith(("+", "-", "=")):
            operation = command[0]  # Extract operation
            try:
                value = int(command[1:])  # Parse value as integer
            except ValueError:
                log("[COMMAND] Failed to parse value for update: '{}'".format(command))
                Parent.SendStreamMessage(language_messages["invalid_value"])
                return

        lang = language_messages

        # Command: Create New Tracker
        if command == "new":
            log("[COMMAND] Create tracker: '{}' with max value: {}".format(tracker_name, value))
            if os.path.exists(tracker_path):
                Parent.SendStreamMessage(lang["tracker_already_exists"].format(tracker=tracker_name))
                return
            if value is None or value <= 0:
                Parent.SendStreamMessage(lang["invalid_value"])
                return

            # Create tracker with initial value 0
            tracker_data = {"current_progress": 0, "max_value": value}
            with open(tracker_path, "w") as f:
                json.dump(tracker_data, f)
            generate_tracker_html(tracker_name, 0, value)
            Parent.SendStreamMessage(lang["tracker_created"].format(tracker=tracker_name, value=value))

        # Command: Reset Tracker
        elif command == "reset":
            log("[COMMAND] Reset tracker: '{}'".format(tracker_name))
            if not os.path.exists(tracker_path):
                Parent.SendStreamMessage(lang["tracker_not_found"].format(tracker=tracker_name))
                return

            with open(tracker_path, "r+") as f:
                tracker_data = json.load(f)
                tracker_data["current_progress"] = 0
                f.seek(0)
                json.dump(tracker_data, f)
                f.truncate()
            generate_tracker_html(tracker_name, 0, tracker_data["max_value"])
            Parent.SendStreamMessage(lang["tracker_reset"].format(tracker=tracker_name))

        # Command: Delete Tracker
        elif command == "del":
            log("[COMMAND] Delete tracker: '{}'".format(tracker_name))
            if not os.path.exists(tracker_path):
                Parent.SendStreamMessage(lang["tracker_not_found"].format(tracker=tracker_name))
                return

            # Delete tracker JSON file
            os.remove(tracker_path)
            log("[DELETE] JSON file deleted for tracker: '{}'".format(tracker_name))

            # Delete tracker HTML file
            html_file = os.path.join(TRACKERS_DIR, "{}.html".format(tracker_name))
            if os.path.exists(html_file):
                os.remove(html_file)
                log("[DELETE] HTML file deleted for tracker: '{}'".format(tracker_name))
            else:
                log("[DELETE] No HTML file found for tracker: '{}'".format(tracker_name))
            Parent.SendStreamMessage(lang["tracker_deleted"].format(tracker=tracker_name))

        # Command: Update Tracker
        elif operation in ["+", "-", "="]:
            log("[COMMAND] Update tracker: '{}' with operation: '{}' and value: {}".format(tracker_name, operation, value))
            if not os.path.exists(tracker_path):
                Parent.SendStreamMessage(lang["tracker_not_found"].format(tracker=tracker_name))
                return

            if value is None:
                Parent.SendStreamMessage(lang["invalid_value"])
                return

            with open(tracker_path, "r+") as f:
                tracker_data = json.load(f)
                if operation == "+":
                    tracker_data["current_progress"] += value
                elif operation == "-":
                    tracker_data["current_progress"] = max(0, tracker_data["current_progress"] - value)
                elif operation == "=":
                    tracker_data["current_progress"] = value
                tracker_data["current_progress"] = min(tracker_data["current_progress"], tracker_data["max_value"])
                f.seek(0)
                json.dump(tracker_data, f)
                f.truncate()
            generate_tracker_html(tracker_name, tracker_data["current_progress"], tracker_data["max_value"])
            Parent.SendStreamMessage(lang["tracker_updated"].format(
                tracker=tracker_name, value=tracker_data["current_progress"]
            ))

        # Command: Invalid Command
        else:
            log("[COMMAND] Invalid command received: '{}'".format(command))
            Parent.SendStreamMessage(lang["invalid_command"])

# ---------------------------------------
# Tick (Required but Not Used)
# ---------------------------------------
def Tick():
    return

# ---------------------------------------
# Script Toggled
# ---------------------------------------
def ScriptToggled(state):
    log("[SCRIPT] Toggled {}".format("ON" if state else "OFF"))
