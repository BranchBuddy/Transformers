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

@app.route('/summarize/<code>', methods=['GET'])
def summarize(code):
  """
    ---
    parameters:
      - name: code
        in: path
        schema:
          type: object
          properties:
            code:
              type: string
        example:
          code: "your_code_here"
        required: true
        description: yes
    responses:
      200:
        description: A code summarizer.
  """
  summarizer = CodeSummarizer()
  summary = summarizer.summarizeCode(code)
  print(type(summary))
  return jsonify({'similarity': summary})
if __name__ == '__main__':
    app.run()
