import json
from flask import Flask, jsonify
from flasgger import Swagger
from src.SimilarityComparison import SimilarityComparison
from src.CodeSummarizer import CodeSummarizer
app = Flask(__name__)
swagger = Swagger(app)

@app.route('/compare_code/<main_code>/<compare_code>', methods=['GET'])
def compare_code(main_code, compare_code):
    """
    ---
    parameters:
      - name: main_code
        in: path
        type: string
        required: true
        description: yes
      - name: compare_code
        type: string
        in: path
        required: true
        description: The code to be compared with.
    responses:
      200:
        description: A code comparator.
    """
    cmp = SimilarityComparison()
    similarity = cmp.compare(main_code, compare_code)
    return jsonify({'similarity': similarity})

@app.route('/summarize-assistant/<code>', methods=['GET'])
def summarize_assistant(code):
  """
    ---
    parameters:
      - name: code
        in: path
        type: string
        required: true
        description: yes
    responses:
      200:
        description: A code summarizer.
  """
  summarizer = CodeSummarizer()
  summary = summarizer.summarizeCode(code)
  return jsonify(summary)
  

@app.route('/summarize-complettion/<code>', methods=['GET'])
def summarize_completion(code):
  """
    ---
    parameters:
      - name: code
        in: path
        type: string
        required: true
        description: yes
    responses:
      200:
        description: A code summarizer.
  """
  summarizer = CodeSummarizer()
  summary = summarizer.summarize_code(code)
  print(type(summary))

  return jsonify({'similarity': summary})

@app.route('/comapre-functions/<functions>/<threshold>', methods=['GET'])
def compare_functions(functions, threshold):
  """
    ---
    parameters:
      - name: functions
        in: path
        required: true
        schema:
          type: object
          properties:
            focused_functions:
              type: array
              items:
                type: string
            other_functions:
              type: array
              items:
                type: string
        description: yes
      - name: threshold
        in: path
        required: false
        type: float
        description: yes

    responses:
      200:
        description: A code summarizer.
  """
  cmp = SimilarityComparison()
  functions = json.loads(functions)
  if threshold:
     threshold = float(threshold)
  similarity = cmp.get_similar_functions(functions['focused_functions'], functions['other_functions'], threshold)
  return jsonify({'similarity': similarity})


if __name__ == '__main__':
    app.run()
