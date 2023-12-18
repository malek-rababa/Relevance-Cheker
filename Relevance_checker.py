from flask import Flask, render_template, request, jsonify
from flask_profiler import Profiler
import openai

app = Flask(__name__)

# Load OpenAI API key
openai.api_key = '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'

# Initialize the profiler
app.config['flask_profiler'] = {
    'enabled': app.config['DEBUG'],
    'storage': {
        'engine': 'sqlite'
    },
    'basicAuth': {
        'enabled': False
    },
    'ignore': [
        '^/static/.*'
    ]
}
profiler = Profiler()

# Attach the profiler to the app
profiler.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_relevance', methods=['POST'])
def check_relevance():
    try:
        tweet = request.form['tweet']
        reply = request.form['reply']

        # Use the OpenAI GPT API to generate relevance scores
        prompt = f"Tweet: {tweet}\nReply: {reply}\nIs the reply relevant to the tweet? Yes/No: "
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

        return jsonify({'tweet': tweet, 'reply': reply, 'relevant': (generated_reply == 'yes')})
    except openai.error.RateLimitError as e:
        return jsonify({'error': f"Rate limit exceeded. Please try again later. Error: {e}"}), 500
    except Exception as e:
        return jsonify({'error': f"An error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
