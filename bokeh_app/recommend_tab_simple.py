#!/usr/bin/env python
# coding: utf-8

# ## Simple recommend tab
# 
# Next steps:
# 
# - style and formatting
# - format recommendations: icon, link to BGG page, link to buy
# - plot games
# - plot games 3D interactive
# 

# In[86]:


# pandas and numpy for data manipulation
import pandas as pd
import numpy as np

from bokeh.plotting import figure
from bokeh.models import (CategoricalColorMapper, HoverTool, 
    ColumnDataSource, Panel, 
    FuncTickFormatter, SingleIntervalTicker, LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, AutocompleteInput, 
      Tabs, CheckboxButtonGroup, Div, Button,
      TableColumn, DataTable, Select)
from bokeh.layouts import column, row, WidgetBox, Spacer
from bokeh.palettes import Category20_16


# In[2]:


def recommender_tab_simple(recommender, allgames, categories, mechanics):

    # Dataset for widgets
    def make_dataset(weight_range, categories, mechanisms):
        
        # create ColumnDataSource with fields:
        # id,name,nrate,pic_url,nrating_pages,minplayers,maxplayers,
        #  minage,mean_rating,weight,categories,mechanics
        #  f_0,f_1,f_2,f_3,f_4
        
        # filter games based on weight
        
        # filter games based on categories
        
        games_all = allgames # use all games for now
        
        # create the data source for bokeh
        return ColumnDataSource(data={
            'game_id':games_all['id'],
            'title':games_all['name'],
            'weight':games_all['weight'],
            'categories':games_all['categories'],
            'mechanics':games_all['mechanics'],
            'image_url':games_all['pic_url'],
            'f0':games_all['f_0'],
            'f1':games_all['f_1'],
            'f2':games_all['f_2'],
            'f3':games_all['f_3'],
            'f4':games_all['f_4']
            })
    
#     # create the figure plot
#     def make_plot(src):
#         pass
#     # set plot style
#     def style(p):
#         # Title 
#         p.title.align = 'center'
#         p.title.text_font_size = '20pt'
#         p.title.text_font = 'serif'        

    def update_liked_list(titlelist):
        global max_liked
        ctl_liked_games.children = make_div_list(titlelist, 
                                                 max_liked, 
                                                 fmt_str=liked_list_fmt, 
                                                 render_as_text=False)
        
    def update_recommended_list(titlelist):
        global n_recommendations
        ctl_recommended_games.children = make_div_list(titlelist, 
                                                 n_recommendations, 
                                                 fmt_str=recommended_list_fmt, 
                                                 render_as_text=False)

    # called when a control widget is changed
    def update_filters(attr, old, new):
#         print('update_filters')
        # get control values
        
        # note: I need to also set games_all
        
        # filter data to get new data source
        new_src = make_dataset(weight_range, categories, mechanics)
        # update the plot/draw data
        src.data.update(new_src.data)
        
    # called when a control widget is changed
    def update_preflist(attr, old, new):
        global liked_games
#         print('\nupdate_preflist')
#         print('ctl_game_entry.value:', ctl_game_entry.value)
#         print('new: ',new)
        liked_games.append(ctl_game_entry.value)
        liked_games = list(filter(None, set(liked_games)))
#         print('liked_games: ',liked_games)
        # get control values
        update_liked_list(liked_games)
        ctl_game_entry.value = ''

    def reset_preferred_games():
        global liked_games
#         print('\nreset preferred')
#         print('ctl_game_entry.value:', ctl_game_entry.value)
#         print('liked_games: ',liked_games)
        liked_games = []
#         update_liked_list(list(games_all['name'].sample(max_liked)))
        update_liked_list(liked_games)        
        
    def recommend_games():
        global liked_games, recommended_games
        global games_all, n_recommendations, title_list
        global title_list_lower
        
        # get some filter parameters:
        weight = []
        minrating = 7
        categories = ['Any category']
        mechanics = ['Any mechanism']
        for title in liked_games:
            idx = (np.array(title_list_lower) 
                   == title.lower()).nonzero()[0][0]
            info = games_all.iloc[idx,:]
            weight.append(info['weight'])
            categories += info['categories'].split(',')
            mechanics += info['mechanics'].split(',')
            
        weightrange = [max(1,np.min(weight)-0.25),
                       min(5,np.max(weight)+0.25)]
#         if len(categories) > 3:
#            categories = ['Any category']
#         if len(mechanics) > 3:
#            mechanics = ['Any mechanism']  
#         print('recommend_games, filters:')
#         print('  weightrange =',weightrange)
#         print('  categories =',categories)
#         print('  mechanics =',mechanics)
        
        # select games to search from based on filters:
        # NOTE: put filtering inside recommender class
        recommended_games = recommender.recommend_games_by_pref_list(
            liked_games, games_all, num2rec=n_recommendations,
             weightrange=weightrange,
             minrating=minrating,
             categories_include=categories,
             categories_exclude=['Expansion for Base-game'],
             mechanics_include=mechanics,
             mechanics_exclude=[]
            )
        
#         recommended_games = recommender.recommend_games_by_pref_list(
#             liked_games, games_all, num2rec=n_recommendations)

        update_recommended_list(recommended_games)
    
    def make_div_list(textlist, max_lines, fmt_str="""%s""", **attribs):
        # see also: width=200, height=100 + other html formatting
        divs = []
        for i in range(max_lines):
            if len(textlist) > i:
                divs.append(Div(text=fmt_str%(textlist[i]), **attribs)) 
            else:
                divs.append(Div(text=fmt_str%(' '), **attribs))
        return divs

    global liked_games, recommended_games, games_all 
    global n_recommendations, max_liked, title_list, title_list_lower
    
    # layout params
    n_recommendations = 10
    max_liked = 8
    liked_list_fmt = """<div style="font-size : 14pt; line-height:14pt;">%s</div>"""
    recommended_list_fmt = """<div style="font-size : 14pt; line-height:14pt;">%s</div>"""

    # variables used by the tab
    liked_games = []
    recommended_games = []
    weight_range = [1,5]
    games_all = allgames # use all games for search    
        
    # list of all game titles
    title_list = games_all['name']
    title_list_lower = [s.lower() for s in title_list]
    
    # preferred game entry text control
    ctl_game_entry = AutocompleteInput(completions=title_list_lower,
        min_characters = 1,                               
        title = 'Enter some game names you like:')
    ctl_game_entry.on_change('value', update_preflist)
    
    # reset button
    ctl_reset_prefs = Button(label = 'Reset game list',
                             width_policy='min', align='end')
    ctl_reset_prefs.on_click(reset_preferred_games)
    
    # liked list title
    ctl_liked_list_title = Div(text=
        """<div style="font-size : 18pt; line-height:16pt;">Games you like:</div>""")
   
    # liked game entries
    ctl_liked_games = WidgetBox(children=make_div_list(liked_games, max_liked, 
        fmt_str=liked_list_fmt))
    
    # recommended list title
    ctl_recommended_list_title = Div(text=
        """<div style="font-size : 18pt; line-height:16pt;">Games we recommend:</div>""")
    
    # recommended games
    ctl_recommended_games = WidgetBox(children=make_div_list(recommended_games, 
        n_recommendations, fmt_str=recommended_list_fmt))
    
#     update_liked_list(list(games_all['name'].sample(max_liked)))
    
    # Recommend games button
    ctl_recommend = Button(label = 'Recommend some games!',width_policy='min')
    ctl_recommend.on_click(recommend_games)
    
    # game weight slider
#     game_weight = RangeSlider(start = 1, end = 5, value = (1, 5),
#         step = .1, title = 'Game weight range')
#     game_weight.on_change('active', update_filters)

#     num_checks = 20
    
    # game category checkbox group
#     category_selection = CheckboxGroup(labels=categories[:num_checks], active = [0, 1])
#     category_selection.on_change('active', update_filters)

    # game mechanism checkbox group
#     mechanism_selection = CheckboxGroup(labels=mechanisms[:num_checks], active = [0, 1])
#     mechanism_selection.on_change('active', update_filters)
    
    
    # create the dataset
    src = make_dataset(weight_range, categories, mechanics)
    
    # make the plot
#     p = make_plot(src)

    # Add style to the plot
#     p = style(p)
    
    # controls to select preferred games
    pref_controls = WidgetBox(
        ctl_liked_list_title,
        ctl_liked_games, 
        Spacer(min_height=20),
        ctl_game_entry, 
        ctl_reset_prefs,
        Spacer(min_height=40),
        ctl_recommend)
        
    # recommendation results
    results_controls = WidgetBox(
        ctl_recommended_list_title,
        ctl_recommended_games)
    
    # Create a row layout
    layout = row(pref_controls, results_controls)
    
    # Make a tab with the layout   
    tab = Panel(child=layout, title = 'Simple Game Recommender')
    
    return tab


# In[ ]:



