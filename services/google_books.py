def _parse_books(self, items):
    """Parse book data from API response"""
    books = []
    for item in items:
        try:
            volume_info = item.get('volumeInfo', {})
            image_links = volume_info.get('imageLinks', {})
            
            # Try to get the largest available image
            thumbnail = (image_links.get('extraLarge') or  # Best quality
                        image_links.get('large') or
                        image_links.get('medium') or
                        image_links.get('small') or
                        image_links.get('thumbnail'))
            
            # Remove zoom parameter and update to higher quality
            if thumbnail:
                thumbnail = thumbnail.replace('zoom=1', 'zoom=3')  # Higher zoom level
                thumbnail = thumbnail.replace('http://', 'https://')  # Use HTTPS
            
            books.append({
                'id': item.get('id'),
                'title': volume_info.get('title'),
                'authors': volume_info.get('authors', []),
                'thumbnail': thumbnail,  # Using the higher quality image
                'preview_link': volume_info.get('previewLink'),
                'published_date': volume_info.get('publishedDate'),
                'description': volume_info.get('description', '')[:200] + '...'
            })
        except Exception as e:
            logger.error(f"Error parsing book data: {str(e)}")
            continue
    return books

def _parse_book_details(self, data):
    """Parse detailed book information"""
    volume_info = data.get('volumeInfo', {})
    image_links = volume_info.get('imageLinks', {})
    
    # Try to get the largest available image
    thumbnail = (image_links.get('extraLarge') or
                image_links.get('large') or
                image_links.get('medium') or
                image_links.get('small') or
                image_links.get('thumbnail'))
    
    # Remove zoom parameter and update to higher quality
    if thumbnail:
        thumbnail = thumbnail.replace('zoom=1', 'zoom=3')
        thumbnail = thumbnail.replace('http://', 'https://')
    
    return {
        'id': data.get('id'),
        'title': volume_info.get('title'),
        'authors': volume_info.get('authors', []),
        'publisher': volume_info.get('publisher'),
        'published_date': volume_info.get('publishedDate'),
        'description': volume_info.get('description'),
        'page_count': volume_info.get('pageCount'),
        'categories': volume_info.get('categories', []),
        'rating': volume_info.get('averageRating'),
        'ratings_count': volume_info.get('ratingsCount'),
        'thumbnail': thumbnail,  # Using the higher quality image
        'preview_link': volume_info.get('previewLink'),
        'isbn_13': next((id['identifier'] for id in volume_info.get('industryIdentifiers', [])
                       if id['type'] == 'ISBN_13'), None)
    } 