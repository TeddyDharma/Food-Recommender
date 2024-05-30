import streamlit as st

st.header("Best Indonesian Foods For You !", divider = "gray")
# st.header('_Streamlit_ is :blue[cool] :sunglasses:')



products = [
    {"name": "Product 1", "price": "$10", "description": "This is product 1", "image": "https://via.placeholder.com/150"},
    {"name": "Product 2", "price": "$20", "description": "This is product 2", "image": "https://via.placeholder.com/150"},
    {"name": "Product 3", "price": "$30", "description": "This is product 3", "image": "https://via.placeholder.com/150"},
    {"name": "Product 4", "price": "$40", "description": "This is product 4", "image": "https://via.placeholder.com/150"},
    {"name": "Product 5", "price": "$50", "description": "This is product 5", "image": "https://via.placeholder.com/150"},
    {"name": "Product 6", "price": "$60", "description": "This is product 6", "image": "https://via.placeholder.com/150"},
    {"name": "Product 7", "price": "$70", "description": "This is product 7", "image": "https://via.placeholder.com/150"},
    {"name": "Product 8", "price": "$80", "description": "This is product 8", "image": "https://via.placeholder.com/150"},
    {"name": "Product 9", "price": "$90", "description": "This is product 9", "image": "https://via.placeholder.com/150"},
    {"name": "Product 10", "price": "$100", "description": "This is product 10", "image": "https://via.placeholder.com/150"}
]

# Define the number of columns per row
columns_per_row = 5

# Loop through products and display them in rows of 5 columns
for i in range(0, len(products), columns_per_row):
    cols = st.columns(columns_per_row)
    for col, product in zip(cols, products[i:i + columns_per_row]):
        with col:
            st.image(
             'https://tse1.mm.bing.net/th/id/OIP.gFlPKt3BvMQlEpAwmwXC9wHaFj?pid=ImgDet', use_column_width=True)
            st.text(product["name"])
            st.text(product["price"])
            st.text(product["description"])

# To run this, save it in a file (e.g., `