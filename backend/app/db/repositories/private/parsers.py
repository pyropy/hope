from fastapi import HTTPException

def parse_youtube_link(link) -> str:
    '''
    Parse youtube link and return only 
    '''
    try:
        link = link.split('?v=')[1]
        link = link.split("&")[0]
    except:
        raise HTTPException(status_code=400, detail="Error trying to parse youtube link. Please refer to documentation to find out how to get and post valid youtube link.")
    return link