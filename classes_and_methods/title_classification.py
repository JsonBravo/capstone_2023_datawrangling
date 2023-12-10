def subject_type_classifications(new_text, top_n, cleaning_method, imported_model, values_only = False):

    cleaned_text = [cleaning_method(text) for text in new_text]

    predicted_scores = imported_model.decision_function(cleaned_text)

    top_categories = []
    for scores in predicted_scores:
        temp_dict = dict(zip(scores,imported_model.classes_))
        # Get the top N largest scores
        n = top_n
        top_scores = sorted(temp_dict.keys(), reverse=True)[:n]
        # Retrieve the categorys corresponding to the top scores
        top_values = [temp_dict[key] for key in top_scores]
        top_categories.append(top_values)

    if values_only:
        return top_categories
    else:
        return dict(zip(new_text,top_categories))