def cart_context(request):
    return {'cart_count': request.session.get('cart_count', 0)}
