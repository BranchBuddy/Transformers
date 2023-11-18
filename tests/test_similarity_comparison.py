import pytest
from src.SimilarityComparison import SimilarityComparison


@pytest.fixture
def similarity_comparison():
    return SimilarityComparison()

def test_get_similar_functions_from_diff_and_source(similarity_comparison):
    diff_message1 = """
diff --git a/file1.java b/file1.java
index abcdef1..1234567 100644
--- a/file1.java
+++ b/file1.java
@@ -1,5 +1,5 @@
 public class MyClass1 {
-    public void method1() {
+    public void updatedMethod1() {
         // Code here
     }
 }

diff --git a/file2.java b/file2.java
index 1234567..abcdef1 100644
--- a/file2.java
+++ b/file2.java
@@ -1,5 +1,5 @@
 public class MyClass2 {
-    public void method2() {
+    public void updatedMethod2() {
         // Code here
     }
 }
"""
    sources1 ={
        "file1.java": """
        public class MyClass1 {
            public void updatedMethod1() {
                // Code here
            }
        }
        """,
        "file2.java": """
        public class MyClass2 {
            public void updatedMethod2() {
                // Code here
            }
        }
        """}
    diff_message2 = diff_message1
    sources2 = sources1
    function_similarities = similarity_comparison.get_similar_functions_from_diff_and_source(diff_message1, sources1, diff_message2, sources2)

    print(function_similarities)
    for i, j, similarity in function_similarities:
        if i == j:
            assert similarity == 1.0, "Similarity score should be the same for the same function"
