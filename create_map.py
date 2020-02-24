import json
from geopy import Nominatim
import folium
import twitter1


def get_location(dct):
    '''
    dict -> dict
    Function for getting name, location, and a photo of twitter user.
    '''
    user_dict = {}
    for user in dct['users']:
        user_dict[user['screen_name']] = [user['location'],
                                          user['profile_image_url']]
    return user_dict


def get_coordinates(dictionary):
    '''
    dict -> dict
    >>> get_coordinates({'realDonaldTrump': ['Washington, DC', 'http://pbs.twimg.com/profile_images/874276197357596672/kUuht00m_normal.jpg'], 
                        'neural_machine': ['Основано на Google Translate', 'http://pbs.twimg.com/profile_images/1042258536775016448/RHlhkkLu_normal.jpg'], 
                        'anya_v_tumane': ['Lviv, Ukraine', 'http://pbs.twimg.com/profile_images/1230441927054700544/Mv9O1Dy8_normal.jpg'], 
                        'strng': ['Ukraine', 'http://pbs.twimg.com/profile_images/1229312910893166593/HWYi8M_D_normal.jpg'], 
                        'grekhov': ['Ukraine', 'http://pbs.twimg.com/profile_images/1144131486523764736/Un_JwqvK_normal.png']})
    {'realDonaldTrump': [(38.8948932, -77.0365529), 'http://pbs.twimg.com/profile_images/874276197357596672/kUuht00m_normal.jpg'], 
    'anya_v_tumane': [(49.841952, 24.0315921), 'http://pbs.twimg.com/profile_images/1230441927054700544/Mv9O1Dy8_normal.jpg'], 
    'strng': [(49.4871968, 31.2718321), 'http://pbs.twimg.com/profile_images/1229312910893166593/HWYi8M_D_normal.jpg'], 
    'grekhov': [(49.4871968, 31.2718321), 'http://pbs.twimg.com/profile_images/1144131486523764736/Un_JwqvK_normal.png']}
    '''
    coordinates_dict = {}
    geolocator = Nominatim(user_agent="Flask_TwitterApp")
    for key in dictionary:
        spot = dictionary[key][0]
        try:
            location = geolocator.geocode(spot)
            coordinates_dict[key] = [(location.latitude, location.longitude), dictionary[key][1]]
        except KeyError:
            continue
        except AttributeError:
            continue
    return coordinates_dict


def get_map(dct, name):
    '''
    dict -> ()
    Function for creating a folium map.
    '''
    friends_map = folium.Map()
    fg = folium.FeatureGroup(name='Friend_location')
    for key in dct:
        spot = dct[key][0]
        icon = folium.features.CustomIcon(dct[key][1], icon_size=(30, 30))
        fg.add_child(folium.Marker(location=[spot[0], spot[1]],
                                   popup=key,
                                   icon=icon))
    friends_map.add_child(fg)
    friends_map.add_child(folium.LayerControl())
    friends_map.save("templates/" + name + "_map.html")


def main(name):
    '''
    str -> ()
    Get all modules together. 
    '''
    dict_json = twitter1.main(name)
    locations = get_coordinates(get_location(dict_json))
    return get_map(locations, name)


