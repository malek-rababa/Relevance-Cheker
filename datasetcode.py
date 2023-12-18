import openai
import json
import time

# Step 1: Read the JSON file from the D partition
file_path = 'D://tweet_reply.json'

# Initialize an empty string to store the concatenated JSON array
concatenated_json = "["

# Explicitly specify the encoding as UTF-8
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        try:
            # Concatenate each line with a comma
            concatenated_json += line.rstrip('\n') + ","
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}. Skipping line.")

# Close the JSON array
concatenated_json = concatenated_json.rstrip(',') + "]"

# Load the concatenated JSON as a list of dictionaries
data = json.loads(concatenated_json)

# Step 2: Extract Tweets and Replies
tweets = [entry['main_tweet'] for entry in data]
replies = [entry['reply'] for entry in data]

# Step 3: Use the OpenAI GPT API to Generate Relevance Scores
openai.api_key = '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'

for i in range(len(tweets)):
    tweet = tweets[i]
    reply = replies[i]

    # Use the OpenAI GPT API to generate relevance scores
    prompt = f"Tweet: {tweet}\nReply: {reply}\nIs the reply relevant to the tweet? Yes/No: "
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=100,
            n=1,
            stop=None
        )

        # Check the relevance based on the generated response
        generated_reply = response['choices'][0]['text'].strip().lower()
        print(f"Reply: {reply} - Relevant: {generated_reply == 'yes'}")
    except openai.error.RateLimitError as e:
        print(f"Rate limit exceeded. Waiting for {e.retry_after} seconds.")
        time.sleep(e.retry_after)
