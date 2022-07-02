def clean_email_form(form):
    user_email = form.cleaned_data['user_mail']
    email_text = form.cleaned_data['question']
    user_name = form.cleaned_data['first_name']
    user_last_name = form.cleaned_data['last_name']
    email_contents = {
        'user_email': user_email,
        'email_text': email_text,
        'user_name': user_name,
        'user_last_name': user_last_name
    }
    return email_contents
