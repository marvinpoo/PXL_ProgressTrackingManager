# (PXL PTM) Progress Tracking Manager

PXL Progress Tracking Manager (PXL PTM) is a powerful tool designed to manage dynamic progress trackers for your live streams. The script supports real-time progress updates displayed as an OBS Browser Source, making it ideal for tracking goals, challenges, or milestones.

---

## Features

- **Dynamic Progress Tracking**: Create, update, reset, or delete trackers directly from chat.
- **OBS Integration**: Display progress bars with real-time updates in your OBS Browser Source.
- **Localization Support**: Available in multiple languages (default: English).
- **User-Friendly Commands**: Simple chat commands for tracker management.
- **Customizable Design**: Fully configurable HTML for progress bar visuals.

---

## Upcoming

- **Spaces or Signs in name:** Finding a solution to be able to allow spaces, `-` or `_` in the tracker name.
- **Streamlabs Chatbot Interface:** Making you able to change settings and manage your progress trackers through the interface.
- **Capabilities:** Adding standard capabilities to the chat commands - Mod + Streamer.
- **Capability Manager:** Making you able to change who can use what command.
- **Rework html system:** I want to rework the html creation, so that you will be able to use the HTML template with variables in the URL instead of selecting single files.
- **Designs:** Adding a batch of sample designs for you to choose from.
- **Command Toggler:** Giving you the ability to toggle if the Bot is allowed to post responses in chat or not.
- **Macro Alternative:** Giving you the ability to use keyboard macros instead of chat commands. (Streamer Only Mode)

---

## Prerequisites

Before you begin, ensure you have the following installed:

- [Streamlabs Chatbot Desktop Client](https://streamlabs.com/chatbot)
- Python 2.7 (Make sure you **use 2.7, not 3.1** or any new version! This is a Streamlabs Chatbot Requirement)
- A streaming setup with OBS or compatible software

---

## Installation

1. **Download the Repository**:

- Clone or download this repository into a folder named `PXL_ProgressTrackingManager`.

2. **Script Folder Setup**:

- Move the `PXL_ProgressTrackingManager` folder into:
  `C:\Users\<YourUsername>\AppData\Roaming\Streamlabs\Streamlabs Chatbot\Services\Scripts`

3. **Enable the Script**:

- Open Streamlabs Chatbot.
- Navigate to `Scripts` > `Settings`.
- Click `Reload Scripts`.
- Ensure `PXL Progress Tracking Manager` appears in the list and is enabled.

Note: If you can not see the `Scripts`-tab in the Chatbot Desktop Client, please make sure your streamer and bot-user are connected in the client.

---

## OBS Setup

1. **Add a Browser Source**:

- Open OBS Studio.
- Click `+` in the `Sources` panel and select `Browser`.
- Name your source (e.g., `Tracker Display`).

2. **Configure the Source**:

- Set the URL to:
  `file:///<PathToScriptFolder>/PXL_ProgressTrackingManager/Trackers/<tracker_name>.html`

Replace `<PathToScriptFolder>` with the absolute path to your script folder and `<tracker_name>` with the name of your tracker.

3. **Adjust Dimensions**:

- Set the width and height to fit your design (e.g., 800x100 for a horizontal progress bar).

4. **Save and Preview**:

- Click `OK` to save.
- The progress bar will update in real-time based on your chat commands.

---

## Commands

### General Format

```
!tracker [name] [command] [value]
```

**IMPORTANT:** Currently this script does **not** support names with spaces. I have not tested seperators like `-` or `_` because they would, at this moment, most likely break the functionality. This will be fixed soon.

### Available Commands

| Command        | Description                                                                 | Example                          |
| -------------- | --------------------------------------------------------------------------- | -------------------------------- |
| `new`          | Create a new tracker with a maximum value.                                  | `!tracker goal new 100`          |
| `reset`        | Reset the tracker progress to `0`.                                          | `!tracker goal reset`            |
| `+value`       | Increment the tracker by the specified value.                               | `!tracker goal +10`              |
| `-value`       | Decrement the tracker by the specified value.                               | `!tracker goal -5`               |
| `=value`       | Set the tracker progress to the specified value.                            | `!tracker goal =50`              |
| `del`          | Delete the tracker and its associated HTML/JSON files.                      | `!tracker goal del`              |

---

## Example Workflow

1. **Create a Tracker**:
   `!tracker ironore neu 100`
   Creates a tracker named `ironore` with a maximum value of 100.

2. **Update the Tracker**:
   **Add progress:**
   `!tracker ironore +10`

**Deduct progress:**
`!tracker ironore -5`

**Set specific progress:**
`!tracker ironore =50`

3. **Reset the Tracker**:
   `!tracker ironore reset`

4. **Delete the Tracker**:
   `!tracker ironore del`

---

## Customization

### Progress Bar Design

To customize the design of the progress bar:

1. Open the `tracker_template.html` file.
2. Modify the CSS to adjust colors, fonts, sizes, and animations.

### Language Support

1. Navigate to the `Languages` folder.
2. Add or edit JSON files (e.g., `lang_de.json` for German).
3. Update the `language` field in `settings.json` to your desired language code.

#### Add Language

Do you want to add your own language support? Simply copy the `lang_en.json` rename it to your language like `lang_de.json` and replace the content like this:

**lang_en.json**

```json
{
  "tracker_created": "Tracker '{tracker}' created with a max value of {value}.",
  "tracker_reset": "Tracker '{tracker}' has been reset to 0.",
  "tracker_updated": "Tracker '{tracker}' updated. Current progress: {value}.",
  "tracker_deleted": "Tracker '{tracker}' has been deleted.",
  "tracker_already_exists": "Tracker '{tracker}' already exists.",
  "tracker_not_found": "Tracker '{tracker}' does not exist.",
  "invalid_value": "Invalid value. Please provide a valid number.",
  "invalid_command": "Invalid command. Available: neu, reset, del, +X, -X, =VALUE."
}
```

**lang_de.json**

```json
{
  "tracker_created": "Tracker '{tracker}' wurde mit einem Maximalwert von {value} erstellt.",
  "tracker_reset": "Tracker '{tracker}' wurde auf 0 zurückgesetzt.",
  "tracker_updated": "Tracker '{tracker}' aktualisiert. Aktueller Fortschritt: {value}.",
  "tracker_deleted": "Tracker '{tracker}' wurde gelöscht.",
  "tracker_already_exists": "Tracker '{tracker}' existiert bereits.",
  "tracker_not_found": "Tracker '{tracker}' existiert nicht.",
  "invalid_value": "Ungültiger Wert. Bitte geben Sie eine gültige Zahl an.",
  "invalid_command": "Ungültiger Befehl. Verfügbar: neu, reset, del, +X, -X, =WERT."
}
```

---

## Known Issues & Debugging

### Script Not Showing in Streamlabs Chatbot

- Ensure the script folder is placed in the correct directory:
  `C:\Users\<YourUsername>\AppData\Roaming\Streamlabs\Streamlabs Chatbot\Services\Scripts`
- Click `Reload Scripts` in the `Scripts` tab.

### Progress Bar Not Updating

- Verify the OBS Browser Source URL points to the correct tracker HTML file.
- Check the logs at `PXL_ProgressTrackingManager_Debug.log` for errors.

### Debugging

You can check the logs and try to fix it yourself or create a issue here in github. This is where you can find the logs:

**PXL Debug Logs**

```
C:\Users\<YourUsername>\AppData\Roaming\Streamlabs\Streamlabs Chatbot\Services\Scripts\PXL_ProgressTrackingManager_Debug.log
```

**Streamlabs Debug Logs**

```
C:\Users\<YourUsername>\AppData\Roaming\Streamlabs\Streamlabs Chatbot\Services\Twitch\Logs\PythonScriptErrorLog.txt
```

---

## Support

**Attention:** I can not offer you support for this. This software is as it is. We have tested it heavily and it works currently exactly as intended. If you need help, feel free to send me a discord message, but I might NOT answer in timely manner. I will try my best to update the FAQ/Debugging/Troubleshooting as much as I can.

### Discord

I do have a Discord for my gaming friends and Gaming Stream. As this tool is made especially for the purpose of gaming or streaming, this tool is covered by my friendly support on Discord. Please note that it can take up to a week to get a response to help requests. Bugs, Suggestions and Contributions have priority but no quick reply guarantee either.

[![Discord Invite Image](https://pxlmon.com/pxlcord.png)](https://discord.gg/pixelempire)

---

## Contributing

Feel free to fork this repository and submit pull requests for improvements or additional features. Suggestions and feedback are always welcome!

---

## License

This project is licensed under the GPL-3.0 license See the `LICENSE` file for details.
