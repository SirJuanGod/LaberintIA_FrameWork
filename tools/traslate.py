from tbparse import SummaryReader

log_dir = "D:\\USC\\Proyectos\\LaberintIA\\LaberintIA_FrameWork\\logs\\laberintia_ppo_final\\tb\\PPO_3\\events.out.tfevents.1780867694.SJG.10300.0" 
reader = SummaryReader(log_dir)

# Extract scalars (loss, accuracy, etc.) into a Pandas DataFrame
df = reader.scalars

# Save to text/CSV
df.to_csv("tensorboard_data.csv", index=False)
