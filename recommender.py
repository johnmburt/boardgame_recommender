#!/usr/bin/env python
# coding: utf-8

# ## Recommender models

# In[5]:


import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.decomposition import TruncatedSVD, PCA
from scipy.spatial.distance import cdist
from sklearn.preprocessing import StandardScaler


# Recommender model 1: Game Space Search
class RecommenderGSS():
    """recommender engine as an estimator"""

    # ******************************************************************
    def __init__(self, n_neighbors=10):
        """
        Called when initializing the model
        """
        # model parameters
        self.n_neighbors = n_neighbors  # number of neighbor titles to search for

    # ******************************************************************
    def set_params(self, **params):
        self.__dict__.update(params)

    # ******************************************************************
    def find_nearest_neighbors(self, coords, x, numnearest):
        """Brute force nearest neighbor search"""

        # get euclidean distances of all points to x
        # dists = cdist(np.reshape(x, (1, -1)), coords)
        dists = cdist(x, coords)

        # sort the distances
        ind, = np.argsort(dists)

        # return the numnearest nearest neighbors
        return ind[:numnearest]

    # ******************************************************************
    def recommend_games_by_one_title(self, targettitle, game_data, search_data, num2rec=1):
        """Recommend games based on nearest neighbor to one game title"""

        print('recommend_games_by_one_title:',targettitle)
        print('game_data.shape', game_data.shape)
        print('search_data.shape', search_data.shape)
        
        # NOTE: this needs to be cleaned up!
        
        all_gametitles = game_data['name'].values
        all_coords = game_data[[s for s in game_data.columns if 'f_' in s]].values
        # get coords of target title,
        # use case insensitive search
        targetindex = (np.array([s.lower() for s in all_gametitles]) == targettitle.lower()
                      ).nonzero()[0]
#         print(targetindex, gametitles[targetindex])
        targetcoord = all_coords[targetindex, :]
        print('targetcoord', targetcoord)

        if targetcoord.shape[0] == 0:
            return []

        search_coords = search_data[[s for s in game_data.columns if 'f_' in s]].values
        search_gametitles = search_data['name'].values
        
        # find nearest neighbors
        print(search_coords.shape, targetcoord.shape)
        ind = self.find_nearest_neighbors(search_coords, targetcoord, 
                                          max(self.n_neighbors, num2rec+1))
        # ind = self.find_nearest_neighbors(coords, targetcoord, num2rec + 1)
        print('ind.shape',ind.shape)
        print(ind[1:num2rec+1])
        # Note: first entry will be the target title (distance 0)
#         print('returned: ', list(ind[1:num2rec+1]))

#         return list(ind[1:num2rec+1])
        return list(search_gametitles[ind[1:num2rec+1]])

#     # ******************************************************************
#     def recommend_games_by_prefs_sets(self, pref, game_data, num2rec=10):
#         """Recommend games using multiple liked and disliked games.
#            This method creates a set of recommended games for each title in prefs and
#              then selects the most commonly recommended,
#              excluding any recs based on disliked games"""

#         recs = []
#         for title in pref['like']:
#             recs.extend(self.recommend_games_by_one_title(title, self.n_neighbors))
#         unique, counts = np.unique(recs, return_counts=True)
#         recs = (np.array([unique, counts])[0, np.argsort(-counts)].T)

#         norecs = []
#         for title in pref['dislike']:
#             norecs.extend(self.recommend_games_by_one_title(title, game_data, self.n_neighbors))
#         norecs = list(np.unique(norecs))

#         allrecs = []
#         for r in recs:
#             if ~any(r == norecs):
#                 allrecs.append(r)

#         return allrecs[:num2rec]
    
    # ******************************************************************
    def remove_prefs_from_recs(self, preflist, game_data, recs):
        pass
    
    # ******************************************************************
    def filter_data(self, df, 
                     weightrange=[1,5],
                     minrating=1,
                     categories_include=[],
                     categories_exclude=[],
                     mechanics_include=[],
                     mechanics_exclude=[]):

        # start with all data
        filt_df = df

        print('filter_data, all data:',filt_df.shape)

        # filter by game weight
        # only filter if not defaults: [1,5]
        if weightrange[0] > 1 or weightrange[1] < 5:
            filt_df = filt_df[ (filt_df['weight'] >= weightrange[0]) &
                             (filt_df['weight'] <= weightrange[1])]
#             print('weightrange, filt_df:',filt_df.shape)

        # filter by lowest average game rating
        # only filter if not default: 1
        if minrating > 1:
            filt_df = filt_df[ filt_df['mean_rating'] >= minrating ]
#             print('minrating, filt_df:',filt_df.shape)

        def tags_in_col(col, taglist):
            return col.apply(lambda x: any(tag in x for tag in taglist))

        # filter by categories to include
        # only filter if not default: [], or ['Any category',...]
        if (len(categories_include) and 
            'Any category' not in categories_include):
            filt_df = filt_df[ tags_in_col(filt_df['categories'], categories_include)]
#             print('categories_include, filt_df:',filt_df.shape)

        # filter by mechanics to include
        # only filter if not default: [], or ['Any category',...]
        if (len(mechanics_include) and 
            'Any mechanism' not in mechanics_include):
            filt_df = filt_df[ tags_in_col(filt_df['mechanics'], mechanics_include)]
#             print('mechanics_include, filt_df:',filt_df.shape)

        print('   filt_df:',filt_df.shape)

        return filt_df      

    # ******************************************************************
    def recommend_games_by_pref_list(self, preflist, game_data, num2rec=10, **filtargs): 
        
        """Recommend games using multiple liked games in a list of titles.
           This method creates a set of recommended games for each title in prefs and
             then selects the most commonly recommended"""

        recs = []
        for title in preflist:
            recs.extend(self.recommend_games_by_one_title(title, game_data,
                self.filter_data(game_data, **filtargs), self.n_neighbors))
#         print('recs',recs)
        # NOTE: np.unique sorts the results, which could create a bias for older games 
        unique, counts = np.unique(recs, return_counts=True)
#         print('unique, counts', unique, counts)
        recs = (np.array([unique, counts])[0, np.argsort(-counts)].T)
        print('recommend_games_by_pref_list recs:',recs)
        return recs[:num2rec]
    
 


# In[ ]:




