
from src.smartmovierecommender.main import main
import gradio as gr
import io
import sys

def respond(prompt):
    """
    Generates the recommendation based on the title running through HuggingFace
    Args: the prompt of movie title inputted by the user
    Returns: a dictionary containing the movie titles and similarity of the 5 recommendations
    """
    if not prompt:
        return {"error": "This is not a valid movie title."}
    app_stdout = sys.stdout
    final_app_stdout = io.StringIO()
    sys.stdout = final_app_stdout

    try:
        main(movie_title=prompt)
        output = final_app_stdout.getvalue()  
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    finally:
        sys.stdout = app_stdout 

    if "No recommendations found." in output:
        return {"error": f"No recommendations found for the movie: {prompt}"}
    

    recommendations = []
    for line in output.split("\n"):
        if line.startswith("Top Recommendations:") or not line.strip():
            continue
        try:
            title, similarity = line.rsplit(" (Similarity: ", 1)
            similarity = similarity.rstrip(")")
            recommendations.append({"Title": title.strip(), "Similarity": float(similarity)})
        except ValueError:
            continue

    if not recommendations:
        return {"error": "NO VALID RECOMMENDATIONS"}
    
    return {"recommendations": recommendations}
demo = gr.Interface(
    fn=respond,
    inputs=gr.Textbox(label="Enter the movie title here...", placeholder="Type a movie title..."),
    outputs=gr.JSON(label="Movie Recommendations"),
    title="Smart Movie Recommender",
    description="This app provides movie recommendations based on the input provided."
)

if __name__ == "__main__":
    demo.launch(share=True)

