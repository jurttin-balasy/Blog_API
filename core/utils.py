from django.core.cache import cache
from .models import Post

def get_statistics():
    # 1. Keshten maǵlıwmattı izleymiz
    stats = cache.get('my_stats_key')

    # 2. Eger keshte joq bolsa (None), esaplaymız
    if not stats:
        print("Qıyın esaplaw islep atır...")
        count = Post.objects.count()
        # ... basqa quramalı esaplawlar ...
        stats = {'total_posts': count, 'status': 'active'}

        # 3. Nátiyjeni keshke saqlaymız (mısalı, 1 saatqa)
        cache.set('my_stats_key', stats, 60 * 60)

    return stats
