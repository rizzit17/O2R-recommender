import pandas as pd

print("HYBRID ENGINE LOADED")

retailer_features = pd.read_parquet(
    "data/processed/retailer_features.parquet"
)

print(
    "Retailers loaded:",
    retailer_features.shape
)

product_features = pd.read_parquet(
    "data/processed/product_features.parquet"
)

region_trends = pd.read_parquet(
    "data/processed/region_trends.parquet"
)

interaction = pd.read_parquet(
    "data/processed/interaction_matrix.parquet"
)

sku_lookup = pd.read_parquet(
    "data/processed/sku_lookup.parquet"
)

similarity_df = pd.read_parquet(
    "data/processed/similarity_matrix.parquet"
)

sku_dict = dict(
    zip(
        sku_lookup["skuNumber"],
        sku_lookup["itemName"]
    )
)

popularity_dict = dict(
    zip(
        product_features["skuNumber"],
        product_features["popularity_score"]
    )
)
def recommend_products(
    customer_id,
    top_n=20
):

    similar_users = (
        similarity_df[customer_id]
        .sort_values(
            ascending=False
        )[1:11]
    )

    customer_products = set(
        interaction.loc[
            customer_id
        ][
            interaction.loc[
                customer_id
            ] > 0
        ].index
    )

    recommendations = {}

    for user in similar_users.index:

        similarity_score = (
            similar_users[user]
        )

        purchased = (
            interaction.loc[user]
        )

        for sku in purchased[
            purchased > 0
        ].index:

            if sku not in customer_products:

                recommendations[
                    sku
                ] = (
                    recommendations.get(
                        sku,
                        0
                    )
                    +
                    similarity_score
                )

    recommendations = sorted(
        recommendations.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return recommendations[:top_n]

def hybrid_recommend(
    customer_id,
    top_n=10,
    weight_cf=0.60,
    weight_region=0.25,
    weight_pop=0.15
):

    cf_recs = recommend_products(
        customer_id,
        top_n=20
    )

    cf_scores = {
        sku: score
        for sku, score in cf_recs
    }

    if len(cf_scores) > 0:

        max_cf = max(
            cf_scores.values()
        )

        cf_scores = {
            sku: score / max_cf
            for sku, score in cf_scores.items()
        }

    customer_profile = retailer_features[
    retailer_features["customerId"] == customer_id
]

    hub = customer_profile[
        "hub_name"
    ].iloc[0]

    shop_type = customer_profile[
        "shop_type"
    ].iloc[0]

    region_recs = region_trends[
        (
            region_trends["hubName"]
            == hub
        )
        &
        (
            region_trends["shopType"]
            == shop_type
        )
    ]

    region_scores = {}

    max_rank = (
        region_recs[
            "region_rank"
        ].max()
    )

    for _, row in region_recs.iterrows():

        region_scores[
            row["skuNumber"]
        ] = (
            max_rank -
            row["region_rank"]
        ) / max_rank

    all_skus = set()

    all_skus.update(
        cf_scores.keys()
    )

    all_skus.update(
        region_scores.keys()
    )

    all_skus.update(
        popularity_dict.keys()
    )

    customer_products = set(
        interaction.loc[
            customer_id
        ][
            interaction.loc[
                customer_id
            ] > 0
        ].index
    )

    hybrid_scores = {}

    for sku in all_skus:

        if sku in customer_products:
            continue

        cf = cf_scores.get(
            sku,
            0
        )

        region = region_scores.get(
            sku,
            0
        )

        popularity = popularity_dict.get(
            sku,
            0
        )

        score = (
            weight_cf * cf
            +
            weight_region * region
            +
            weight_pop * popularity
        )

        hybrid_scores[
            sku
        ] = score

    recommendations = sorted(
        hybrid_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return recommendations[:top_n]

    