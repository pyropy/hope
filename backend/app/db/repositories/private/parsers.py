
def parse_youtube_link(link) -> str:
    '''
    Parse youtube link and return only 
    '''

    link = link.split('?v=')[1]
    link = link.split("&")[0]
    return link