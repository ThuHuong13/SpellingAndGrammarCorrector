from transformers import pipeline
from gramformer import Gramformer

fix_spelling = pipeline(
    "text2text-generation", model="oliverguhr/spelling-correction-english-base"
)


gf = Gramformer(models=1, use_gpu=False)


def correct_grammar(content: str):
    """
    Splits content by periods, applies spell-check to each sentence, and recombines the result.
    """
    # Split content by periods and keep the delimiter
    sentences = [sentence + "." for sentence in content.split(".") if sentence.strip()]
    corrected_sentence = []
    # Apply spell-check to each sentence
    for sentence in sentences:
        correction_result = gf.correct(sentence, max_candidates=1)
        for result in correction_result:
            corrected_sentence.append(result)

    # Rejoin the corrected sentences
    corrected_content = " ".join(corrected_sentence)
    return corrected_content
    # return gf.correct(content, max_candidates=1)


def get_edits(content: str, correction: str):
    return gf.get_edits(content, correction)


def get_highlighted_text(content: str, correction: str):
    return gf.highlight(content, correction)


def correct_spelling(content: str):
    """
    Splits content by periods, applies spell-check to each sentence, and recombines the result.
    """
    # Split content by periods and keep the delimiter
    sentences = [sentence + "." for sentence in content.split(".") if sentence.strip()]

    # Apply spell-check to each sentence
    corrected_sentences = [
        fix_spelling(sentence.strip(), max_length=2048)[0].get("generated_text")
        for sentence in sentences
    ]

    # Rejoin the corrected sentences
    corrected_content = " ".join(corrected_sentences)
    return corrected_content
