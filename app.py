import json
from flask import Flask, jsonify
from flasgger import Swagger
from src.SimilarityComparison import SimilarityComparison
from src.CodeImprover import CodeImprover
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

@app.route('/compare-functions-between-branches/<focused_diff>/<focused_sources>/<other_diff>/<other_sources>/<threshold>', methods=['GET'])
def compare_functions_between_branches(focused_diff, focused_sources, other_diff, other_sources, threshold):
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
  cmp = SimilarityComparison()
  focused_sources = json.loads(focused_sources)
  other_sources = json.loads(other_sources)
  if threshold:
     threshold = float(threshold)
  similarity = cmp.get_similar_functions_from_diff_and_source(focused_diff, focused_sources, other_diff, other_sources, threshold)
  return jsonify({'similarity': similarity})

@app.route('/improve/<code>', methods=['GET'])
def improve(code):
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
  codeImprover = CodeImprover()
  improvedCode = codeImprover.improveCode(code)
  return improvedCode

@app.route('/comment/<code>', methods=['GET'])
def comment(code):
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
  codeImprover = CodeImprover()
  commentedCode = codeImprover.commentCode(code)

  return jsonify(commentedCode)
if __name__ == '__main__':
    app.run()
