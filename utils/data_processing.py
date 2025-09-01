from typing import List, Dict, Any



def extract_sellers(data: List[Dict[str, Any]]) -> List[str]:
    sellers = {item.get('Продавец', 'Unknown Seller') for item in data}
    return list(sellers)

def extract_brands(data: List[Dict[str, Any]]) -> List[str]:
    brands = {item.get('Бренд', 'Unknown Brand') for item in data}
    return list(brands)

def extract_skus(data: List[Dict[str, Any]]) -> List[str]:
    skus = {item.get('SKU', 'Unknown SKU') for item in data}
    return list(skus)

def get_sku_statistics(data: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    sku_stats = {}
    for item in data:
        sku = item.get('SKU', 'Unknown SKU')
        revenue = item.get('Оборот FBO', 0) + item.get('Оборот FBS', 0)
        orders = item.get('Кол-во заказов', 0)

        if sku not in sku_stats:
            sku_stats[sku] = {
                'total_revenue': 0,
                'total_orders': 0
            }

        sku_stats[sku]['total_revenue'] += revenue
        sku_stats[sku]['total_orders'] += orders

    return sku_stats


