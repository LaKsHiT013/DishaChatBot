import pandas as pd

def fun(input_csv, output_csv, percentage=0.3):
    try:
        df = pd.read_csv(input_csv)
        sampled_data = df.sample(frac=percentage, random_state=42)
        sampled_data.to_csv(output_csv, index=False)
        print(f"Randomly selected {percentage*100:.0f}% rows saved to {output_csv}.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

fun('iiitn.csv', 'test.csv')