def no_field_blank(blog_title, blog_body):
    """All fields must have content."""
    try:
        if (blog_title == '') or (blog_body == ''):
            return True
    except ValueError:
        return False

def blogs_have_same_content(prev_blog_title, blog_title, prev_blog_body, blog_body):
    """No repetion of last post."""
    try:
        if (prev_blog_title == blog_title) or (prev_blog_body == blog_body):
            return True
    except ValueError:
        return False

