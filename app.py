import json
from flask import Flask, jsonify, request
from flasgger import Swagger
from src.SimilarityComparison import SimilarityComparison
from src.CodeImprover import CodeImprover
from src.CodeSummarizer import CodeSummarizer
app = Flask(__name__)
swagger = Swagger(app)

@app.route('/compare_code', methods=['POST'])
def compare_code():
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
    data = request.get_json()
    main_code = data.get('main_code')
    compare_code = data.get('compare_code')
    cmp = SimilarityComparison()
    similarity = cmp.compare(main_code, compare_code)
    return jsonify({'similarity': similarity})

@app.route('/summarize-assistant', methods=['POST'])
def summarize_assistant():
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
  code = request.get_json().get('code')
  summarizer = CodeSummarizer()
  summary = summarizer.summarizeCode(code)
  return jsonify(summary)
  

@app.route('/summarize-completion', methods=['POST'])
def summarize_completion():
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
  code = request.get_json().get('code')
  summarizer = CodeSummarizer()
  summary = summarizer.summarize_code(code)
  print(type(summary))

  return jsonify({'similarity': summary})

@app.route('/compare-functions/', methods=['POST'])
def compare_functions():
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
  data = request.get_json()
  functions = data.get('functions')
  threshold = data.get('threshold')
  cmp = SimilarityComparison()
  functions = json.loads(functions)
  if threshold:
     threshold = float(threshold)
  similarity = cmp.get_similar_functions(functions['focused_functions'], functions['other_functions'], threshold)
  return jsonify({'similarity': similarity})

@app.route('/compare-functions-between-branches', methods=['POST'])
def compare_functions_between_branches():
  """
    ---
    parameters:
      - name: focused_diff
        in: path
        type: string
        required: true
        description: yes
      - name: focused_sources
        in: path
        type: string
        required: true
        description: yes
      - name: other_diff
        in: path
        type: string
        required: true
        description: yes
      - name: other_sources
        in: path
        type: string
        required: true
        description: yes
      - name: threshold
        in: path
        type: float
        required: true
        description: yes
    responses:
      200:
        description: A code summarizer.
  """
  request_data = request.get_json()
  focused_diff = request_data.get('focused_diff')
  focused_sources = request_data.get('focused_sources')
  other_diff = request_data.get('other_diff')
  other_sources = request_data.get('other_sources')
  cmp = SimilarityComparison()
  focused_sources = json.loads(focused_sources)
  other_sources = json.loads(other_sources)
  if threshold:
     threshold = float(threshold)
  similarity = cmp.get_similar_functions_from_diff_and_source(focused_diff, focused_sources, other_diff, other_sources, threshold)
  return jsonify({'similarity': similarity})

@app.route('/improve', methods=['POST'])
def improve():
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
  code = request.get_json().get('code')
  codeImprover = CodeImprover()
  improvedCode = codeImprover.improveCode(code)
  return improvedCode

@app.route('/comment', methods=['POST'])
def comment():
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
  code = request.get_json().get('code')
  codeImprover = CodeImprover()
  commentedCode = codeImprover.commentCode(code)

  return jsonify(commentedCode)
if __name__ == '__main__':
    app.run()
