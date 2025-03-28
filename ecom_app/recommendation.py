import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Product
from .models import UserInteraction


def recommend_products(product_id):
    products = list(Product.objects.all().values(
        'id', 'name', 'description', 'category'))

    # Convert to DataFrame
    df = pd.DataFrame(products)

    # Combine text features for content similarity
    df['features'] = df['name'] + " " + \
        df['description'] + " " + df['category']

    # Convert text data to feature vectors
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['features'])

    # Compute similarity matrix
    similarity_matrix = cosine_similarity(tfidf_matrix)

    # Find index of the selected product
    product_idx = df[df['id'] == product_id].index[0]

    # Get similarity scores and sort
    scores = list(enumerate(similarity_matrix[product_idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:6]

    # Get recommended product IDs
    recommended_product_ids = [df.iloc[i[0]]['id'] for i in scores]

    return Product.objects.filter(id__in=recommended_product_ids)


def recommend_products_based_on_user(user_id):
    # Get the products that the user has interacted with
    # You can filter by other interaction types as needed
    user_interactions = UserInteraction.objects.filter(
        user_id=user_id, interaction_type='view')
    interacted_products = [
        interaction.product for interaction in user_interactions]

    if not interacted_products:
        return []  # No recommendations if the user has not interacted with any product

    # Get the data for these products (name, description, etc.)
    products = Product.objects.filter(
        id__in=[product.id for product in interacted_products])

    # Convert the product data to a DataFrame
    df = pd.DataFrame(list(products.values(
        'id', 'name', 'description', 'category')))

    # Combine text features for content similarity
    df['features'] = df['name'] + " " + \
        df['description'] + " " + df['category']

    # Convert text data to feature vectors
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['features'])

    # Compute similarity matrix
    similarity_matrix = cosine_similarity(tfidf_matrix)

    # Create a list of recommended products
    recommended_products = set()
    for product in interacted_products:
        # Find the index of the product
        product_idx = df[df['id'] == product.id].index[0]

        # Get similarity scores and sort
        scores = list(enumerate(similarity_matrix[product_idx]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)[
            1:6]  # Get top 5 similar products

        # Add recommended products to the set (to avoid duplicates)
        for score in scores:
            recommended_products.add(df.iloc[score[0]]['id'])

    # Return the recommended products
    return Product.objects.filter(id__in=list(recommended_products))
