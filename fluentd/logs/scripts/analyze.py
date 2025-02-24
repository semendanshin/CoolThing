import re
from collections import defaultdict
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# Replace with the path to your log file
log_file_path = "./2024-11-29.log"  # Update this to your actual log file path

# Load the log file
with open(log_file_path, 'r', encoding='utf-8') as file:
    logs = file.readlines()

# Refine parsing logic to handle all variations in log formats
chat_stats_refined = defaultdict(lambda: {
    "Messages Sent": 0,
    "Skipped": False,
    "Skip Reason": None,
    "Timestamps": []
})

for idx, line in enumerate(logs):
    # Match sent messages, allowing for "to chat" and optional replies
    sent_message_match = re.search(r"sending message .*? from bot .*? to chat (https?://t\.me/[\w\d_]+)", line, re.IGNORECASE)
    if sent_message_match:
        chat_link = sent_message_match.group(1).strip()
        timestamp_match = re.search(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}", line)
        if timestamp_match:
            timestamp = datetime.strptime(timestamp_match.group(), "%Y-%m-%d %H:%M:%S,%f")
            chat_stats_refined[chat_link]["Messages Sent"] += 1
            chat_stats_refined[chat_link]["Timestamps"].append(timestamp)

    # Match skipped messages, allowing for variations in format
    skipped_match = re.search(r"from bot .*? to chat (https?://t\.me/[\w\d_]+|Unknown): (.+Error): (.+)", line, re.IGNORECASE)
    if skipped_match:
        chat_link = skipped_match.group(1).strip() if skipped_match.group(1).strip() != "Unknown" else "Unknown"
        error_type = skipped_match.group(2).strip()
        error_message = skipped_match.group(3).strip()
        chat_stats_refined[chat_link]["Skipped"] = True
        chat_stats_refined[chat_link]["Skip Reason"] = f"{error_type}: {error_message}"

# Recreate the final summary including all chats
chat_stats_summary_refined = []
for chat, stats in chat_stats_refined.items():
    avg_interval = None
    if len(stats["Timestamps"]) > 1:
        intervals = [(stats["Timestamps"][i + 1] - stats["Timestamps"][i]).total_seconds()
                     for i in range(len(stats["Timestamps"]) - 1)]
        avg_interval = sum(intervals) / len(intervals)
    chat_stats_summary_refined.append({
        "Chat Link": chat,
        "Messages Sent": stats["Messages Sent"],
        "Skipped": stats["Skipped"],
        "Skip Reason": stats["Skip Reason"],
        "Average Interval (s)": avg_interval
    })

# Convert the refined data into a DataFrame
chat_stats_df_refined = pd.DataFrame(chat_stats_summary_refined)

# Save refined results to a new CSV
csv_file_path_refined = "chat_statistics_refined.csv"  # Update with your desired output file name
chat_stats_df_refined.to_csv(csv_file_path_refined, index=False)
print(f"Chat statistics saved to: {csv_file_path_refined}")

# Create a visualization for all chats with updated parsing logic
plt.figure(figsize=(12, 8))
top_chats_refined = chat_stats_df_refined.nlargest(10, 'Messages Sent')
plt.bar(top_chats_refined['Chat Link'], top_chats_refined['Messages Sent'])
plt.title("Top 10 Active Chats by Messages Sent (Refined)", fontsize=16)
plt.xlabel("Chat Link", fontsize=12)
plt.ylabel("Messages Sent", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# Save the updated visualization
visualization_path_refined = "chat_activity_visualization_refined.png"  # Update with your desired output file name
plt.savefig(visualization_path_refined)
plt.show()
print(f"Visualization saved to: {visualization_path_refined}")
