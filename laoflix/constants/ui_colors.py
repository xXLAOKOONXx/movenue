POPUP_BACKGROUND = '#606060'
POPUP_FOREGROUND = '#9d9d9d'
HIGHLIGHT_COLOR = '#dfdfdf'

DARK_GREY = '#414141'
DEFAULT_BACKGROUND = '#9d9d9d'
LIGHT_PURPLE = '#734457'

MENU_BUTTON_COLOR = DARK_GREY
EXIT_BUTTON_COLOR = DARK_GREY
TOP_MENU_BACKGROUND = DARK_GREY
SCROLL_ROW_TITLE_BACKGROUND = LIGHT_PURPLE

DEFAULT_BUTTON = DARK_GREY

def rating_colors(max_rating:str=10)->dict[int,str]:
    r_min =  int('d6',base=16)
    r_max =  int('3b',base=16)
    g_min =  int('56',base=16)
    g_max =  int('94',base=16)
    b_min =  int('56',base=16)
    b_max =  int('34',base=16)
    rating_colors = {
        i+1:'#%02x%02x%02x' % (int(r_min + ((r_max - r_min)/(max_rating-1)) * i), int(g_min + ((g_max - g_min)/9) * i), int(b_min + ((b_max - b_min)/9) * i))
        for i in range(0,max_rating)
    }
    return rating_colors