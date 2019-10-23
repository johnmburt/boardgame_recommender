#!/usr/bin/env python
# coding: utf-8

# ## Advanced recommend tab
# 
# 
# Next steps:
# 
# - style and formatting
# - format recommendations: icon, link to BGG page, link to buy
# - plot games
# - plot games 3D interactive
# 

# In[3]:


# pandas and numpy for data manipulation
import pandas as pd
import numpy as np

from bokeh.plotting import figure
from bokeh.models import (CategoricalColorMapper, HoverTool, 
    ColumnDataSource, Panel, 
    FuncTickFormatter, SingleIntervalTicker, LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, AutocompleteInput, 
      Tabs, CheckboxButtonGroup, Div, Button, MultiSelect, 
      TableColumn, DataTable, Select, RangeSlider, Slider)
from bokeh.layouts import column, row, WidgetBox, Spacer
from bokeh.palettes import Category20_16

def recommender_tab_advanced(recommender, allgames, categories, mechanics):

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
        global category_includes, category_excludes
        global category_selections, mechanics_selections
#         print('update_filters')
#         print(ctl_game_weight.value)
#         print(ctl_game_min_rating.value)
#         if ctl_category_select_include.value:
#             category_includes = list(set(category_includes + ctl_category_select_include.value))
#             ctl_category_select_include.value = ''
#             print(category_includes)
        category_selections = [
            ctl_category_selection1.labels[i] for i in ctl_category_selection1.active]
        category_selections += [
            ctl_category_selection2.labels[i] for i in ctl_category_selection2.active]
#         print(category_selections)

        mechanics_selections = [
            ctl_mechanics_selection1.labels[i] for i in ctl_mechanics_selection1.active]
        mechanics_selections += [
            ctl_mechanics_selection2.labels[i] for i in ctl_mechanics_selection2.active]
#         print(mechanics_selections)

        # note: I need to also set games_all
        
        # filter data to get new data source
#         new_src = make_dataset(weight_range, categories, mechanics)
#         # update the plot/draw data
#         src.data.update(new_src.data)
        
    # called when a control widget is changed
    def update_preflist(attr, old, new):
        global liked_games
        liked_games.append(ctl_game_entry.value)
        liked_games = list(filter(None, set(liked_games)))
        # get control values
        update_liked_list(liked_games)
        ctl_game_entry.value = ''

    def reset_preferred_games():
        global liked_games
        liked_games = []
        update_liked_list(liked_games)        
        
    def recommend_games():
        global liked_games, recommended_games
        global games_all, n_recommendations, title_list
        global category_selections, mechanics_selections
        
        # select games to search from based on filters:
        # NOTE: put filtering inside recommender class
        recommended_games = recommender.recommend_games_by_pref_list(
            liked_games, games_all, num2rec=n_recommendations,
             weightrange=ctl_game_weight.value,
             minrating=ctl_game_min_rating.value,
             categories_include=category_selections,
             categories_exclude=[],
             mechanics_include=mechanics_selections,
             mechanics_exclude=[]
            )
        
        # NOTE: there's going to be a problem here if I filter games searched:
        #  the index won't match up. I should return the list of titles in 
        #  the recommender.
        # I also should consider passing the filter params to recommender and letting 
        #   it handle the filtering, then if I need filtered data, call a method for that.
#         recommended_games = list(title_list[rec_idx])
        update_recommended_list(recommended_games)
    
    def make_div_list(textlist, max_lines, fmt_str="""%s""", **attribs):
#     def make_div_list(textlist, max_lines, fmt_str="""%s""", render_as_text=False):
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
    global category_selections, mechanics_selections
    
    # layout params
    n_recommendations = 10
    max_liked = 10
    num_check_options = 20
    liked_list_fmt = """<div style="font-size : 12pt; line-height:1pt;">%s</div>"""
    recommended_list_fmt = """<div style="font-size : 14pt; line-height:12pt;">%s</div>"""
    
    # variables used by the tab
    games_all = allgames # use all games for search     
    liked_games = []
    recommended_games = []
    weight_range = [1,5]
    category_selections = []
    mechanics_selections = []

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
    ctl_liked_list_title = Div(text="""<h2>Games you like:</h2>""")
    
    # liked game entries
    ctl_liked_games = WidgetBox(children=make_div_list(liked_games, max_liked, 
        fmt_str=liked_list_fmt))
    
    # recommended list title
    ctl_recommended_list_title = Div(text="""<h2>Games we recommend:</h2>""")
    
    # recommended games
    ctl_recommended_games = WidgetBox(children=make_div_list(recommended_games, 
        n_recommendations, fmt_str=recommended_list_fmt))
    
    # Recommend games button
    ctl_recommend = Button(label = 'Recommend some games!',
                           width_policy='min', align='center')
    ctl_recommend.on_click(recommend_games)
    
    # create the dataset
    # NOTE: not used currently (but will for plotting)
    src = make_dataset(weight_range, categories, mechanics)
    
    # game weight slider
    ctl_game_weight = RangeSlider(start = 1, end = 5, value = (1, 5),
        step = .1, title = 'Game weight range',width_policy='min',)
    ctl_game_weight.on_change('value', update_filters)
    
    # min game rating slider
    ctl_game_min_rating = Slider(start = 1, end = 10, value = 1,
        step = .1, title = 'Minimum average rating', 
                                 width_policy='min')
    ctl_game_min_rating.on_change('value', update_filters)
    
    # game category selection
    category_list = ['Any category'] + list(categories['tag'].values)    
#     ctl_category_select_include = MultiSelect(options=category_list)
#     ctl_category_select_include = Select(options=category_list)
    ctl_category_selection1 = CheckboxGroup(
        labels=category_list[:int(num_check_options/2)], 
        width_policy='min', active = [0])
    ctl_category_selection1.on_change('active', update_filters)
    ctl_category_selection2 = CheckboxGroup(
        labels=category_list[int(num_check_options/2):num_check_options], 
        width_policy='min')
    ctl_category_selection2.on_change('active', update_filters)

    # game mechanism checkbox group
    mechanics_list = ['Any mechanism'] + list(mechanics['tag'].values)
    ctl_mechanics_selection1 = CheckboxGroup(
        labels=mechanics_list[:int(num_check_options/2)], 
        width_policy='min', active = [0])
    ctl_mechanics_selection1.on_change('active', update_filters)
    ctl_mechanics_selection2 = CheckboxGroup(
        labels=mechanics_list[int(num_check_options/2):num_check_options], 
        width_policy='min')
    ctl_mechanics_selection2.on_change('active', update_filters)
        
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
        Spacer(min_height=5),
        )
    
    filter_controls = WidgetBox(
        row(ctl_game_weight, Spacer(min_width=50), ctl_game_min_rating),
#         ctl_category_select_include,
        row(
            column(Div(text="""<h3>Game Categories:</h3>"""),
                row(ctl_category_selection1, ctl_category_selection2)),
            Spacer(min_width=50),
            column(Div(text="""<h3>Game Mechanics:</h3>"""),
                row(ctl_mechanics_selection1, ctl_mechanics_selection2)),
            )
        )
    
    # recommendation results
    results_controls = WidgetBox(
        ctl_recommended_list_title,
        ctl_recommended_games,
        Spacer(min_height=40),
        ctl_recommend)
    
    # Create a row layout
    layout = column(row(pref_controls, Spacer(min_width=50), results_controls), 
                    filter_controls)
    
    # Make a tab with the layout   
    tab = Panel(child=layout, title = 'Advanced Game Recommender')
    
    return tab


# In[ ]:




